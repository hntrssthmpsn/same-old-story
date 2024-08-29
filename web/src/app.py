from flask import Flask, render_template, request, jsonify
import requests
import os

# Initialize the Flask application
app = Flask(__name__)

# Retrieve URLs for the embeddings and compare services from environment variables
EMBEDDINGS_SERVICE_URL = os.environ.get('EMBEDDINGS_SERVICE_URL')
COMPARE_SERVICE_URL = os.environ.get('COMPARE_SERVICE_URL')

def process_results(compare_result, texts):
    """
    Process and format the results received from the compare service.

    Args:
        compare_result (dict): A dictionary containing comparison results.
        texts (dict): A dictionary of the original texts sent for comparison.

    Returns:
        list: A sorted list of tuples, each containing a compared text and its similarity score.
    """
    scores = []
    for ((id1, id2), score) in compare_result:
        # Identify the text compared with 'text1' and store its score
        if id1 == 'sample_text':
            compared_text = texts[id2]
        else:
            compared_text = texts[id1]
        scores.append((compared_text, score))

    # Sort the texts based on their scores in descending order for better readability
    compared_texts = sorted(scores, key=lambda x: x[1], reverse=True)
    return compared_texts

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    The main route of the web application, handling both GET and POST requests.

    GET requests render the main index page where users can input texts.
    POST requests process the input texts, interact with the embeddings and compare services, 
    and render the results.
    """
    if request.method == 'POST':
        # Collecting texts from the form data
        sample_text = {"sample_text": request.form['sample_text']}
        compare_texts = {f'text{i}': request.form[f'text{i}'] for i in range(1, 4)}

        # Send texts to the embeddings service and receive embeddings
        embedding_set_1 = requests.post(EMBEDDINGS_SERVICE_URL, json={"texts": sample_text}).json()
        embedding_set_2 = requests.post(EMBEDDINGS_SERVICE_URL, json={"texts": compare_texts}).json()

        # Prepare the payload for the compare service
        compare_payload = {
            "embedding_set_1": embedding_set_1,
            "embedding_set_2": embedding_set_2
        }
        # Get comparison results from the compare service
        compare_result = requests.post(COMPARE_SERVICE_URL, json=compare_payload).json()
        
        # Process the results and prepare them for rendering
        compared_texts = process_results(compare_result, compare_texts)

        # Render the results page with the original and compared texts
        return render_template('results.html', original_text=sample_text['sample_text'], compared_texts=compared_texts)

    # Render the main index page for GET requests
    return render_template('index.html')

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)

