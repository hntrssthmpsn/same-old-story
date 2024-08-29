# Same Old Story 
# Semantic Similarity as a Service

## Introduction
This project is designed to facilitate the comparison of short texts by converting them into embeddings and assessing their semantic relatedness using cosine similarity. The project is experimental in nature, aiming to explore the potential of semantic text comparison as a microservice.

### Main Functionality:
The project is composed of two main services, each with a specific role in the process of semantic comparison:

- embeddings
    * This service is responsible for generating embeddings from input strings. It provides the option to download a model for generating these embeddings.
- compare
    * The compare service performs the actual semantic comparison between the generated text embeddings.

Additionally, the web microservice provides a minimal web interface.

### Technologies Used:
This project is developed using Flask to create microservices and TensorFlow and Numpy to work with embeddings. Testing is conducted using pytest. The services are containerized with Docker, and the docker-compose file in the root of this repo can run a functional local deployment without any external requirements.

## Components Overview
1. **Embeddings Service**
   - Purpose: Generate embeddings from text using Google's Universal Sentence Encoder.
   - Key Features: Text processing, embedding generation, Flask-based service.
     - Optionally download model if not present.

2. **Compare Service**
   - Purpose: Perform semantic comparisons between sets of text embeddings.
   - Key Features: Semantic analysis, integration with Embeddings service.

3. **Web Service**
   - Purpose: Provide a user-friendly web interface for demonstration of basic functionality
   - Key Features: Text submission, sort and display texts by similarity, integration with Compare and Embeddings services.


## Getting Started

### Running the services

The docker-compose file at the root of this repository defines a fully functional deployment and is the easiest way to run the same old story microservices locally.

> [!WARNING]
> Note that by default, the embeddings service as configured in the dockerfile will download the Universal Sentence Encoder Large model to its local filesystem. This is a nontrivial download at almost 600MB. By default, we store the downloaded model in a docker volume, so that subsequent runs initiated via our docker-compose file will use the previously downloaded model. This behavior can be customized in docker-compose.yml.

- Clone this repository
- cd to this repo's root
- bring it all up with docker-compose
  ```bash
  docker-compose up
  ```
- try out some test strings in the web interface at http://localhost:5007

### Next Steps

For examples of interacting with the embeddings and compare services running locally via docker-compoase, see:

* scripts/generate_embeddings_data.sh
  - Generate embeddings from plain text strings using the embeddings service in a bash shell
* scripts/compare_texts.sh
  - Generate embeddings from plain text using the embeddings service, then compare them via the compare service in a bash shell
* web/src/app.py
  - compare a plain text string to a set of three plain text strings and sort the results by similarity in python

## Testing

Automated testing can be run for each service by way of the `test` stage in each service's Dockerfile. The example below is for the embeddings service, but the process is the same for the compare or web services.

```bash
cd embeddings/
docker build --target=test -t embeddings:test .
docker run --rm embeddings:test pytest
```

See the testing documentation in the embeddings, compare, and web service READMEs for more information on testing for each service.


