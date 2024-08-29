# SOS Helper Scripts

The scripts in this directory are helper utilities for interacting with the compare and embeddings
services when they're running locally.

* generate_test_data.sh can be used to generate a dictionary of the `id: vector` format expected by the compare service.
    - This script is used to generate the test data used for testing the compare service, and can be modified to create arbitrary embeddings
    - This requires that the embeddings service is running and by default assumes it's running as a local docker container 
      as described in the embeddings service's README or via docker-compose.

* compare_texts.sh
    - This is a convenience script for interacting with the running compare and embeddings services via a local bash shell.
    - This requires jq for flingin' dictionaries around
    - This requires that both the embeddings and the comparison service be running, and by default assumes they're running as local docker containers
      as described in the embeddings and compare service's README documentation or via docker-compose. 
