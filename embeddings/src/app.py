from flask import Flask, request, jsonify
import os
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from generator import EmbeddingGenerator
from model_loader import load_or_download_model

app = Flask(__name__)

# Configure Flask settings
app.config['LOG_LEVEL'] = os.getenv('LOG_LEVEL', 'INFO')
app.config['MAX_TEXT_LENGTH'] = int(os.getenv('MAX_TEXT_LENGTH', 1000))
app.config['model'] = {
    'path': os.getenv('MODEL_PATH', '/app_data/models/universal-sentence-encoder-large-5/saved_model'),
    'url': os.getenv('MODEL_DOWNLOAD_URL', 'https://tfhub.dev/google/universal-sentence-encoder-large/5'),
    'allow_download': os.getenv('ALLOW_DOWNLOAD_MODEL', 'False').lower() == 'true'
}

# Set logger level
app.logger.setLevel(app.config['LOG_LEVEL'])

model = load_or_download_model(app.config['model'])

emb_gen = EmbeddingGenerator(model)

@app.route('/embeddings', methods=['POST'])
def generate_embeddings():
    """
    Generate embeddings for provided texts with the universal sentence encoder.

    This endpoint receives a JSON object with a 'texts' key, where the value is a dictionary
    of ID-text pairs. It returns a dictionary of ID-embedding pairs, where each embedding
    is a list of floats.

    Parameters:
    - data: A JSON object received from the request, expected to contain a 'texts' key.

    Returns:
    - A Flask JSON response containing the embeddings or an error message.
    """
    try:
        data = request.get_json()

        # Validate input: check if 'texts' is present and is a dictionary
        if 'texts' not in data or not isinstance(data['texts'], dict):
            app.logger.warning("Invalid input: 'texts' key not found or not a dictionary.")
            return jsonify({"error": "Invalid input, 'texts' must be a dictionary."}), 400

        texts = data['texts']
        embeddings = {}
        
        for id, text in texts.items():

        # Validate text type and length
            if not isinstance(text, str):
                app.logger.error(f"Invalid text type for ID {id}. Expected string.")
                return jsonify({"error": f"Text for ID {id} is not a string."}), 400
        
            if len(text) > app.config['MAX_TEXT_LENGTH']:
                app.logger.warning(f"Text for ID {id} exceeds maximum length.")
                return jsonify({"error": f"Text for ID {id} is too long. Maximum length is {app.config['MAX_TEXT_LENGTH']} characters."}), 400

           
            # Generate embedding for each text 
            try:
                embedding = emb_gen.embedding_from_text(text)
                embeddings[id] = embedding.tolist()
            except Exception as e:
                app.logger.error(f"Error processing text for ID {id}: {str(e)}")
                return jsonify({"error": f"Error processing text for ID {id}: {str(e)}"}), 500

        return jsonify(embeddings)

    except Exception as e:
        app.logger.critical(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred."}), 500
