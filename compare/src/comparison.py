import numpy as np
import logging
from app_logs import configure_logger

# Configure the logger
logger = logging.getLogger(__name__)
configure_logger(logger)

class ComparisonError(Exception):
    """Custom exception for errors during comparison of embedding sets."""

class SimilarityCalculationError(Exception):
    """Custom exception for errors related to similarity calculations."""

class Comparison:
    def __init__(self, set1, set2):
        """
        Initialize the Comparison object with two embedding sets. Each embedding
        set is expected to be a dictionary of kv pairs where the key is an id and
        the value is a list representation of a numpy array. 
        
        Args:
            set1 (dict): First embedding set.
            set2 (dict): Second embedding set.

        Raises:
            ValueError: If the embedding sets are not in a valid format.
        """
        self.set1 = self.validate_embedding_set_format(set1)
        self.set2 = self.validate_embedding_set_format(set2)

    def validate_embedding_set_format(self, embedding_set):
        """
        Validates that all embedding values in a single embedding set are in a valid format.
        Specifically, it checks if the embeddings are lists or numpy arrays of floats.

        Args:
            embedding_set (dict): A dictionary representing an embedding set.

        Returns:
            dict: Validated embedding set.

        Raises:
            ValueError: If invalid format is detected in the embedding set.
        """
        for emb in embedding_set.values():
            if not isinstance(emb, (list, np.ndarray)) or not all(isinstance(x, float) for x in emb):
                raise ValueError("Invalid embedding format detected in the embedding set.")
        return embedding_set


    def similarity_score(self, embedding1, embedding2):
        """
        Calculates the cosine similarity score between two embeddings using NumPy.

        Args:
            embedding1 (list or np.ndarray): The first embedding vector.
            embedding2 (list or np.ndarray): The second embedding vector.

        Returns:
            float: The cosine similarity score between the two embeddings.

        Raises:
            SimilarityCalculationError: If an error occurs during the similarity calculation.
        """
        try:
            logger.debug(f"Returning similarity score as {np.dot(embedding1, embedding2)}")
            return np.dot(embedding1, embedding2)
        except Exception as e:
            logger.error(f"Error calculating similarity score: {e}")
            raise SimilarityCalculationError(f"Error calculating similarity score: {e}")

    def compare_embedding_sets(self):
        """
        Compares two sets of embeddings and returns a sorted list of similarity scores.
        Each pair of embeddings from the two sets is compared, and the results are sorted
        by the similarity scores in descending order.

        Returns:
            list: A list of tuples, where each tuple contains a pair of IDs and their
                  similarity score. Sorted by similarity score in descending order.

        Raises:
            ComparisonError: If an error occurs during the comparison process.
        """
        results = []
        try:
            for id1, emb1 in self.set1.items():
                for id2, emb2 in self.set2.items():
                    score = self.similarity_score(emb1, emb2)
                    results.append(((id1, id2), score))
            results.sort(key=lambda x: x[1], reverse=True)
        except SimilarityCalculationError as e:
            logger.error(f"Raised ComparisonError due to SimilarityCalculationError: {e}")
            raise ComparisonError(f"Error comparing embeddings: {e}")
        except Exception as e:
            logger.error(f"Raised ComparisonError for error during comparison: {e}")
            raise ComparisonError(f"Error during comparison: {e}")
        return results


