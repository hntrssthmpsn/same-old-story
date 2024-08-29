import tensorflow as tf
import html
import re

class EmbeddingGeneratorError(Exception):
    """
    Custom exception class for errors in the EmbeddingGenerator.

    Attributes:
        message (str): Description of the error.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message

class EmbeddingGenerator:
    """
    A class for generating text embeddings using a TensorFlow model.

    Attributes:
        model (tf.Model): TensorFlow model used for generating embeddings.
        max_length (int, optional): Maximum length of the text to be processed.
    """

    def __init__(self, model, max_length=None):
        """
        Initialize the EmbeddingGenerator.

        Args:
            model (tf.Model): TensorFlow model to be used for generating embeddings.
            max_length (int, optional): Maximum number of characters to consider for the embeddings.
        """
        self.model = model
        self.max_length = max_length

    @staticmethod
    def _load_text(text, max_length):
        """
        Process and clean the input text.

        Args:
            text (str): The text to be processed.
            max_length (int, optional): Maximum length of the text to consider.

        Returns:
            str: Processed text.

        Raises:
            ValueError: If max_length is not a positive integer.
        """
        if max_length is not None and (not isinstance(max_length, int) or max_length < 1):
            raise ValueError("max_length must be a positive integer.")

        if max_length is not None:
            text = text[:max_length]

        text = html.escape(text)
        text = re.sub(r'\s+', ' ', text)
        text = ''.join(filter(lambda x: x.isprintable(), text))

        return text

    def embedding_from_text(self, raw_text, max_length=None):
        """
        Generate an embedding from the input text.

        Args:
            raw_text (str): The raw text to generate an embedding for.
            max_length (int, optional): Maximum length of the text to consider.

        Returns:
            numpy.ndarray: The generated text embedding.

        Raises:
            ValueError: If raw_text is not a non-empty string.
            EmbeddingGeneratorError: If there is an issue generating the embedding.
        """
        if not isinstance(raw_text, str) or not raw_text.strip():
            raise ValueError("Input text must be a non-empty string.")

        text = self._load_text(raw_text, max_length)

        try:
            model = self.model
            signature = model.signatures["serving_default"]
            text_emb = signature(tf.constant([text]))["output_0"].numpy()[0]
            return text_emb
        except tf.errors.InvalidArgumentError as e:
            raise EmbeddingGeneratorError(f"Error processing text with TensorFlow model: {e}")


