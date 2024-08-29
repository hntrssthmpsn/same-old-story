# Compare service sample data

## embeddings_data.json
embeddings_data.json is used for integration testing of the compare service. A new version can be created with arbitrary strings 
using a script like generate_embeddings_data.sh with the embeddings service running locally, or by the method of your choice that
captures the embeddings service's returns as json files. 

See generate_embeddings_data.sh for the strings used to generate the embeddings in embeddings_data.json if you have a
use case for knowing the text origins of this sample data.
