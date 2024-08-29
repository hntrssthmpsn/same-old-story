import pytest
from model_loader import ModelLoaderError, load_or_download_model

def test_model_loader_invalid_path():
    """
    Test if the ModelLoaderError is raised when no model is found at the given path 
    and model downloading is disabled.
    """
    config = {'path': 'invalid/path', 'allow_download': False}
    with pytest.raises(ModelLoaderError) as excinfo:
        load_or_download_model(config)
    assert "Model not found at path" in str(excinfo.value)
    assert "and model downloading is disabled" in str(excinfo.value)

def test_model_loader_download_failure(mocker):
    """
    Test if the ModelLoaderError is raised during a simulated failure in the model download process.
    """
    config = {'path': '/valid/path/model', 'allow_download': True, 'url': 'http://model.url'}
    mocker.patch('os.path.exists', return_value=False)
    mocker.patch('os.makedirs')
    mocker.patch('tensorflow_hub.load', side_effect=Exception("Download failed"))

    with pytest.raises(ModelLoaderError) as excinfo:
        load_or_download_model(config)
    assert "Failed to download and save model" in str(excinfo.value)

def test_model_loader_load_error(mocker):
    """
    Test if the ModelLoaderError is raised during a simulated error in the model loading process.
    """
    config = {'path': '/valid/path/model', 'allow_download': False}
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('os.makedirs')
    mocker.patch('tensorflow.saved_model.load', side_effect=Exception("Load error"))

    with pytest.raises(ModelLoaderError) as excinfo:
        load_or_download_model(config)
    assert "Error in loading model" in str(excinfo.value)

def test_model_loader_success_existing_model(mocker):
    """
    Test that a mock model is successfully returned when the model path exists 
    and the model is successfully loaded.
    """
    config = {'path': '/valid/path/model', 'allow_download': False}
    
    mocker.patch('os.path.exists', return_value=True)
    mocked_model = mocker.Mock()
    mocker.patch('tensorflow.saved_model.load', return_value=mocked_model)

    model = load_or_download_model(config)
    assert model == mocked_model

