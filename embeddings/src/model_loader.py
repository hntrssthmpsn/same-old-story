import os
import tensorflow as tf
import tensorflow_hub as hub

class ModelLoaderError(Exception):
    """
    Custom exception class for errors related to model loading.
    """

def download_and_save_model(model_url, model_path):
    """
    Downloads a TensorFlow model from a given URL and saves it to a specified path.

    Args:
        model_url (str): The URL where the TensorFlow model is hosted.
        model_path (str): The file path where the model should be saved.

    Raises:
        ModelLoaderError: If the model cannot be downloaded or saved.
    """
    try:
        model = hub.load(model_url)
        tf.saved_model.save(model, model_path)
    except Exception as e:
        raise ModelLoaderError(f"Failed to download and save model: {e}")

def load_or_download_model(config):
    """
    Loads a TensorFlow model from a specified path, or downloads it if it doesn't exist and downloading is allowed.

    Args:
        config (dict): Configuration dictionary containing:
            - path (str): Path where the model is saved or should be saved.
            - allow_download (bool): Flag indicating if downloading is allowed if the model is not found.
            - url (str, optional): URL to download the model from if not found and downloading is allowed.

    Returns:
        The loaded TensorFlow model.

    Raises:
        ModelLoaderError: If the model cannot be found and downloading is disabled, 
                          or if an error occurs during model loading.
    """
    model_path = config['path']
    allow_download = config['allow_download']

    if not os.path.exists(model_path):
        if allow_download:
            model_dir = os.path.dirname(model_path)
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            download_and_save_model(config['url'], model_path)
        else:
            raise ModelLoaderError(f"Model not found at path '{model_path}' and model downloading is disabled.")
    
    try:
        return tf.saved_model.load(model_path)
    except Exception as e:
        raise ModelLoaderError(f"Error in loading model: {e}")

