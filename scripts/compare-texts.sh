#!/bin/bash

# This is a convenience script that can be used to for
# local testing when both embedding and compare services
# are running locally as described in their respective
# Dockerfiles.

# Define the sample texts
f1="The quick brown fox jumps over the lazy dog."
b1="Pack my box with five dozen liquor jugs."
f2="The speedy beige fox leaps over the lazy hound."
b2="Fill my case with a lot of booze."

# Endpoint URLs - modify if running in a different configuration than that described 
# by docker-compose or service's READMEs.

embeddings_url="http://localhost:5005/embeddings"
compare_url="http://localhost:5006/compare"

# Fetch embeddings for the texts
embedding_set_1=$(curl -s -X POST "$embeddings_url" -H "Content-Type: application/json" -d "{\"texts\": {\"f1\": \"$f1\", \"b1\": \"$b1\"}}")

embedding_set_2=$(curl -s -X POST "$embeddings_url" -H "Content-Type: application/json" -d "{\"texts\": {\"f2\": \"$f2\", \"b2\": \"$b2\"}}")

# Prepare the JSON payload for compare
json_payload="{\"embedding_set_1\": $embedding_set_1, \"embedding_set_2\": $embedding_set_2}"
echo "$json_payload"

# Call compare with the embeddings
#compare_response=$(curl -s -X POST "$compare_url" -H "Content-Type: application/json" -d "$json_payload")

#echo "$compare_response" 
