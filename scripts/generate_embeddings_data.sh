#!/bin/bash

# This is an example of a convenience script that can be used to generate an embeddings_data.json file 
# appropriate for use in the tests in compare/tests/test_integration.py The sample texts configured 
# below are the ones used to produce the current version of that sample data.
# 
# This script can be modified to create other embeddings by replacing the sample texts below with any number
# of sample text configurations in the form of $id=$string, and updating the texts dictionary in the
# json payload of the embeddings_response curl command to reflect any changes to the ids or total count.

# Define the sample texts
f1="The quick brown fox jumps over the lazy dog."
b1="Pack my box with five dozen liquor jugs."
f2="The speedy beige fox leaps over the lazy hound."
b2="Fill my case with a lot of booze."

# Endpoint URL - modify if running in a different configuration than that described 
# by docker-compose or the embeddings service's README.

embeddings_url="http://localhost:5005/embeddings"

# Fetch embeddings for the texts
embeddings_response=$(curl -s -X POST "$embeddings_url" -H "Content-Type: application/json" -d "{\"texts\": {\"f1\": \"$f1\", \"b1\": \"$b1\", \"f2\": \"$f2\", \"b2\": \"$b2\"}}")

echo "$embeddings_response"
