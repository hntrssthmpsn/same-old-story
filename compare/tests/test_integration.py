import pytest
import json
from flask import json as flask_json

# Path to the embeddings data file
EMBEDDINGS_DATA_FILE = 'tests/sample_data/embeddings_data.json'

@pytest.fixture
def client():
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_compare_integration(client):
    # Load embeddings data from the JSON file
    with open(EMBEDDINGS_DATA_FILE) as file:
        embeddings_data = json.load(file)

    # Prepare the JSON payload for compare
    json_payload = {
        "embedding_set_1": {"f1": embeddings_data["f1"], "b1": embeddings_data["b1"]},
        "embedding_set_2": {"f2": embeddings_data["f2"], "b2": embeddings_data["b2"]}
    }

    # Send a POST request to the compare endpoint
    response = client.post("/compare", json=json_payload)

    # Check that the response is as expected
    assert response.status_code == 200
    # response_data = flask_json.loads(response.data)
    # assert len(response_data) == 2  # Or other relevant checks

    # Additional assertions can be added as needed

