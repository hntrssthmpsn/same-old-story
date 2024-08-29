import pytest
from flask import json
import numpy as np
from unittest.mock import patch
from app import app
from comparison import Comparison, SimilarityCalculationError, ComparisonError

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_comparison():
    with patch('app.Comparison') as MockComparison:
        yield MockComparison

# Test for correct response when comparison succeeds
def test_compare_success(client):
    sample_data = {
        'embedding_set_1': {'id1': [1.0, 2.0, 3.0]},
        'embedding_set_2': {'id2': [4.0, 5.0, 6.0]}
    }

    # Mock the Comparison class to return a dummy response
    with patch('app.Comparison') as mock_comparison:
        mock_comparison.return_value.compare_embedding_sets.return_value = [('id1', 'id2'), 0.99]

        response = client.post('/compare', json=sample_data)
        assert response.status_code == 200
        assert json.loads(response.data) == [['id1', 'id2'], 0.99]

# Test for error handling in the comparison endpoint
def test_compare_error(client, mock_comparison):
    mock_comparison.side_effect = ComparisonError("Mock Comparison Error")
    sample_data = {
        'embedding_set_1': {'id1': [1.0, 2.0, 3.0]},
        'embedding_set_2': {'id2': [4.0, 5.0, 6.0]}
    }
    response = client.post('/compare', json=sample_data)
    assert response.status_code == 500
    assert response.json == {'error': 'Mock Comparison Error'}

