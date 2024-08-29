from flask import Flask, request, jsonify
import os
import sys
import logging
from app_logs import log_route, configure_logger
from comparison import Comparison, SimilarityCalculationError, ComparisonError

app = Flask(__name__)

configure_logger(app.logger)

@app.route('/compare', methods=['POST'])
@log_route
def compare():
    """
    API endpoint to compare two sets of embeddings.

    Accepts a POST request with a JSON payload containing two sets of embeddings and a flag
    indicating whether to use absolute values in similarity calculations. Utilizes the Comparison
    class to perform the comparison and returns the results.

    Returns:
        A JSON response with the comparison results.
    """
    data = request.get_json()
    
    compare = Comparison(data['embedding_set_1'], data['embedding_set_2'])

    results = compare.compare_embedding_sets()


    return jsonify(results)


@app.errorhandler(SimilarityCalculationError)
def handle_similarity_calculation_error(error):
    """
    Error handler for SimilarityCalculationError.

    Logs the error and returns a JSON response with the error message and a 500 HTTP status code.

    Args:
        error (SimilarityCalculationError): The caught similarity calculation error.

    Returns:
        A tuple containing a JSON object with the error message and an HTTP status code (500).
    """
    app.logger.error(f"Handled SimilarityCalculationError: {error}")
    return jsonify({'error': str(error)}), 500

@app.errorhandler(ComparisonError)
def handle_comparison_error(error):
    """
    Error handler for ComparisonError.

    Logs the error and returns a JSON response with the error message and a 500 HTTP status code.

    Args:
        error (ComparisonError): The caught comparison error.

    Returns:
        A tuple containing a JSON object with the error message and an HTTP status code (500).
    """
    app.logger.error(f"Handled ComparisonError: {error}")
    return jsonify({'error': str(error)}), 500

if __name__ == '__main__':
    app.run()

