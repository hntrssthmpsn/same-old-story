import pytest
from flask import Flask
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_get(client):
    """Test the GET request to the main route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"input" in response.data  # Checking that the input field is in the rendered HTML

def test_index_post(client, monkeypatch):
    """Test the POST request to the main route."""
    def mock_post(url, json):
        """Mock the requests.post function."""
        class MockResponse:
            def json(self):
                if 'texts' in json:
                    # Mock embedding response
                    return {key: [0.1, 0.2, 0.3] for key in json['texts']}
                else:
                    # Mock comparison response
                    return [(('sample_text', 'text1'), 0.9), (('sample_text', 'text2'), 0.8), (('sample_text', 'text3'), 0.7)]
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    response = client.post("/", data={
        'sample_text': 'sample text',
        'text1': 'comparison text 1',
        'text2': 'comparison text 2',
        'text3': 'comparison text 3'
    })
    assert response.status_code == 200
    assert b"sample text" in response.data  # Checking that the original text is in the rendered HTML
    assert b"comparison text 1" in response.data  # Checking that the compared texts are in the rendered HTML
    assert b"comparison text 2" in response.data
    assert b"comparison text 3" in response.data

