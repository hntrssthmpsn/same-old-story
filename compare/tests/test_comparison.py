import pytest
import numpy as np
import logging
from unittest.mock import patch, MagicMock
from comparison import Comparison, SimilarityCalculationError, ComparisonError

# Mock logger for the Comparison class
@pytest.fixture
def mock_logger():
    with patch('comparison.logger', new=MagicMock(spec=logging.Logger)) as mock_logger:
        yield mock_logger

# Normalize mocked embeddings
def normalize_vector(vec):
    norm = np.linalg.norm(vec)
    return vec / norm if norm != 0 else vec

# Test for successful calculation of similarity score
def test_similarity_score_success():
    embedding1 = normalize_vector(np.array([0.1, 0.2, 0.3]))
    embedding2 = normalize_vector(np.array([0.4, 0.5, 0.6]))
    compare = Comparison({'id1': embedding1}, {'id2': embedding2})
    # Note that we use pytest.approx here to avoid failures due to very small variances introduced by floating point arithmatic
    assert compare.similarity_score(embedding1, embedding2) == pytest.approx(np.dot(embedding1 / np.linalg.norm(embedding1), embedding2 / np.linalg.norm(embedding2)))


# Test for successful comparison of embedding sets
def test_compare_embedding_sets_success():
    set1 = {'id1': normalize_vector(np.array([0.1, 0.2, 0.3]))}
    set2 = {'id2': normalize_vector(np.array([0.4, 0.5, 0.6]))}
    compare = Comparison(set1, set2)
    results = compare.compare_embedding_sets()
    assert isinstance(results, list)
    assert len(results) == 1
    assert isinstance(results[0], tuple)
    assert results[0][0] == ('id1', 'id2')
    assert isinstance(results[0][1], float)

# Test for error during similarity score calculation
def test_similarity_score_error(mock_logger):
    compare = Comparison({}, {})
    with pytest.raises(SimilarityCalculationError):
        compare.similarity_score(None, None)
    error_message = "Error calculating similarity score: unsupported operand type(s) for *: 'NoneType' and 'NoneType'"
    mock_logger.error.assert_called()
    assert error_message in mock_logger.error.call_args_list[0][0][0]

# Test for error during comparison of embedding sets
def test_compare_embedding_sets_error(mock_logger):
    compare = Comparison({'id1': normalize_vector(np.array([0.1, 0.2, 0.3]))}, {'id2': normalize_vector(np.array([0.4, 0.5, 0.6]))})

    # Mock an error during similarity score calculation
    with patch.object(Comparison, 'similarity_score', side_effect=SimilarityCalculationError("Mock error")):
        with pytest.raises(ComparisonError):
            compare.compare_embedding_sets()  # Simulated error during comparison

    error_message = "Raised ComparisonError due to SimilarityCalculationError: Mock error"
    mock_logger.error.assert_called()
    assert error_message in mock_logger.error.call_args_list[0][0][0]
