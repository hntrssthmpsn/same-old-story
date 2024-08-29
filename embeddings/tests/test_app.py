import pytest
import os
import json
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MAX_TEXT_LENGTH'] = 100  # Set a low value for testing

    with app.test_client() as client:
        yield client

def test_excessively_long_input(client):
    # Test case for input text exceeding MAX_TEXT_LENGTH
    long_text = "a" * (app.config['MAX_TEXT_LENGTH'] + 1) # Exceed the character limit
    response = client.post('/embeddings', json={"texts": {"1": long_text}})
    assert response.status_code == 400
    assert "is too long" in response.json['error']

def test_generate_embeddings(client):
    # Sample payload with texts
    sample_texts = {
        "texts": {
            "1": "Hello, world!",
            "2": "This is a sample text for testing."
        }
    }

    response = client.post('/embeddings', data=json.dumps(sample_texts), content_type='application/json')
    assert response.status_code == 200

    # Parse the response data
    response_data = json.loads(response.data.decode('utf-8'))

    # Assertions to check if the response contains embeddings for each text
    assert "1" in response_data and isinstance(response_data["1"], list)
    assert "2" in response_data and isinstance(response_data["2"], list)

def test_invalid_input_missing_texts(client):
    # Test case for missing 'texts' key
    response = client.post('/embeddings', json={})
    assert response.status_code == 400
    assert "Invalid input" in response.json['error']

def test_invalid_input_non_dict_texts(client):
    # Test case for non-dictionary 'texts' key
    response = client.post('/embeddings', json={"texts": "not a dict"})
    assert response.status_code == 400
    assert "Invalid input" in response.json['error']

def test_invalid_text_type(client):
    # Test case for non-string text
    response = client.post('/embeddings', json={"texts": {"1": 123}})
    assert response.status_code == 400
    assert "Text for ID 1 is not a string" in response.json['error']
