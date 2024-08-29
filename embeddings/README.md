# embeddings

## Introduction

The `embeddings` service is designed to facilitate the processing of natural language text into machine-readable vector representations, known as embeddings. These embeddings capture the semantic essence of the text, making them valuable in various natural language processing (NLP) applications. This code uses Google's Universal Sentence Encoder Large model to generate embeddings from text and Flask to provide embedding generation as a service.

### Key Features

- **Text Processing:** The service accepts a dictionary where each entry consists of a unique identifier (ID) and an associated arbitrary text string.
- **Embedding Generation:** Utilizing Google's Universal Sentence Encoder, the service transforms these text strings into embeddings. Each embedding is a dense vector of floating-point numbers.
- **Output:** The service returns a dictionary mapping each original ID to its corresponding embedding. This format preserves the association between the input text and its vector representation, facilitating easy integration into downstream NLP tasks.

### Usage

The embeddings service accepts as input a JSON http payload in the form of a dictionary `texts` containing mappings of ids (strings) mapped to short texts (strings) and returns a dictionary mapping the ids to embeddings 
created from the texts using the universal sentence encoder large model.

Example input:
```json
{"texts": {"f1": "The quick brown fox jumped over the lazy dog.", "f2": "The speedy beige fox leaps over the lazy hound.", "b1": "Pack my box with five dozen liquor jugs.", "b2": "Fill my case with a lot of booze."}}
```

Example return:
```json
{"b1": [0.06954514980316162, ..., -0.030764779075980186], "b2": [0.048967715352773666, ..., -0.004508910700678825], "f1": [0.013051041401922703, ..., -0.11492756754159927], "f2": [-0.039564285427331924, ..., -0.08798880130052567]} 
```

For an example of calling the embeddings and compare services in python, see the web service.

## Local Development


### Docker Image and Resource Management

Building the Docker image for this service, especially the testing target, can result in the creation of large images and intermediate layers. This is mainly due to TensorFlow dependencies and the model download functionality used in testing.

#### Reclaiming Disk Space

This is a large image, currently about 1.67GB, and it creates additional large layers during the build process. After building the image, particularly for development or testing purposes, it's advisable to clean up unused Docker resources to reclaim disk space. If you don't have any local images or containers hanging around not running that it'd be problematic to replace, you can use `docker system prune` to remove all stopped containers, unused networks, dangling images, and build cache. If that's too aggressive for your docker situation, `docker builder prune` will simply clean up all the unused build layers.


#### Considerations for Local Development

If you are building the Docker image locally:

- Ensure adequate disk space is available. The image is about 1.67GB, and can utilize over 7GB of disk space when building the test target
- Regularly clean up Docker resources to maintain system performance.
- Be aware of network bandwidth usage:
  - The Universal Sentence Encoder Large model is 600MB, so downloading it every time the service runs can add up
  - Save the model locally and set MODEL_PATH to reduce bandwidth consumption

### Building the embeddings image

This project uses a multistage Docker build process, allowing for separate production and testing builds. To build the Docker container for this service, navigate to the directory containing the `Dockerfile`.

#### Building for Production

To build the production image, run:

```bash
docker build --target production -t embeddings:your-meaningful-tag .
```

To run a production image locally:
```bash
docker run -p 5005:5000 -v /path/to/model_directory:/app/model_path -e MODEL_PATH=/app/model_path embeddings:your-meaningful-tag
```

If you don't have the model downloaded, you can use the ALLOW_DOWNLOAD_MODEL flag to let the embeddings service download it and save it to MODEL_PATH, with a local directory mounted if you want to preserve the copy of the model locally after the docker container exits. Note that you may need to raise the timeout value for gunicorn, which runs the flask app in the production image, when downloading the large model. This can be done by setting the GUNICORN_TIMEOUT environment variable. To customize the source from which the model is downloaded, use the MODEL_URL environment variable. The current default is `https://tfhub.dev/google/universal-sentence-encoder-large/5`

```bash
docker run -p 5005:5000 -v /path/to/model_directory:/app_data/ -e MODEL_PATH=/app_data/saved-model -e ALLOW_DOWNLOAD_MODEL=true -e GUNICORN_TIMEOUT=90 embeddings:your-meaningful-tag
```

Use the locally running container:
```bash
curl -X POST http://localhost:5005/embeddings -H "Content-Type: application/json" -d '{"texts": {"1": "Hello, world!", "2": "Sample text"}}'
```

#### Building for Testing

To build the image for testing:

```bash
docker build --target test -t embeddings:your-test-tag .
```
This command builds the test stage of the Dockerfile. It installs testing dependencies and sets up test code. The `ALLOW_DOWNLOAD_MODEL` environment variable is set to `true` in this stage to facilitate model downloading during testing.

To run pytest with all default settings, downloading the model to the image and discarding it when complete:
```bash
docker run --rm -e MODEL_PATH=/app/model_path -e ALLOW_DOWNLOAD_MODEL=true embeddings:your-test-tag pytest
```

To run pytest and download the model to a local directory for use in further testing or with the production build:
```bash
docker run -v /local/model/path:/app/model_path -e MODEL_PATH=/app/model_path -e ALLOW_DOWNLOAD_MODEL=true embeddings:your-test-tag pytest
```

To run pytest with a previously downloaded model
```bash
docker run -v /local/model/path:/app/model_path -e MODEL_PATH=/app/model_path embeddings:your-test-tag pytest
```

