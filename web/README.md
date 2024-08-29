# Web Service

## Introduction
The Web service acts as a simple usage example for the compare and embeddings services. It provides a web-based interface for submitting a single text sample and a set of three texts
to be scored against the sample which are then scored on the basis of semantic similarity, optionally using absolute value.

## Technology Stack
- Flask web framework
- Docker for containerization

## Configuration
The service utilizes two environment variables:
- `EMBEDDINGS_SERVICE_URL`: URL for the `embeddings` service.
- `COMPARE_SERVICE_URL`: URL for the `compare` service.

## Run locally with docker
This service requires the compare and embeddings services to be accessible to run properly. To run them all together
locally you can use the docker-compose file at the root of this directory.
```bash
docker-compose up
```
4. 
## Usage
Access the web interface through the browser by navigating to `http://localhost:5007/`. Here, you can input text into the provided fields and submit it to see the semantic comparison results.

