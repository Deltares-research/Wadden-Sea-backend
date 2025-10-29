# Cosmos database

The database used for this project is a [Cosmos database](https://learn.microsoft.com/en-us/azure/cosmos-db/). Different scientific papers are stored as vectors that could be efficiently searched through to provide a response as accurate as possible. This page aims at describing how we structured the database, the process by which documents can be added to this database and how it can be used for queries on specific topics. 

## Overall structure
This structure of the database is kept as simple as possible while allowing for future extension, possibly for other region than the Wadden Sea or more elements that the user can interact with inside that region.

### Design
The voice for nature project connects humans to other elements of nature, in our case ones that belong in the Wadden Sea. Therefore, we have multiple sources of information and we wanted to keep them all under one database related to the Wadden Sea, but we created different containers related to individual elements that a user could talk to in the Wadden Sea (for example seagrass, shellfish etc).

**CosmosDB design with vector search index creation**
![db design](../../figures/CosmosDB.svg)

When the user asks a question to an entity of the Wadden Sea, the backend will make a query using a specialised search index (yellow). The search index is tailored with articles related to the entity and not any others. This is translated in the design by having different containers (grey) inside one database (blue) that isolate the data. So when querying information about seagrass, results will not be polluted with shellfish information.

This design accelerates the search in addition to improving accuracy. 


## Upload of articles
A key aspect of the database design is the ability to upload new articles, either for adding new entities to interact with or to enrich the existing containers. Let us walk through the process of uploading new papers, from preprocessing to the actual connection with the database.

This can be achieved through the `Cosmos` class. Its `create` method takes as argument the name of the database "vectorSearchDB" and the name of the container into which the papers will go. The name of the container should be related to the entity as described above. This method establishes the connection to the database in the cloud. If the container does not already exist it will be created.

### Preprocessing
In order for text files to be digestable for a search index and an LLM (Large Language Model), they need to be stored as vectors. We developed a pipeline to streamline this process. It is explained here and can be set up with the `setup_chunking_pipeline` method of the database.

The pipeline takes as input a directory where it will read every file contained. From then, each file will be processed though the pipeline, more detailed below. The final output will be embedded vectors, enriched with enough information to enable a search later on. Those vectors are stored in the corresponding container in the database.

**Visualisation of pipeline process**

![pipeline design](../../figures/ingestion_pipeline.svg)

#### Splitting
First the text file is split into chunks using a SentenceSplitter. This gives the base of each vector of the file. Multiple splitters exist, but we use a SentenceSplitter to conserve the sentence structures. This helps with preserving coherent chunks of data instead of a TokenSplitter for example. One thing to keep in mind is that there is less fine control over the amount of tokens produced. 

The SentenceSplitter uses two parameters. The first one, chunk size determines the length of the vector, the higher the chunking size, the more sentences will be included, so the less individual vectors it produces. The second parameter is the chunk overlap. This determines the number of chunks from the previous vector is included to retain context information. 

Through trial and error, we have found that a chunk size of 512 and chunk overlap of 10 provide more satisfying results than a bigger size and overlap, without storing too many vectors.

#### Extractors
The vectors obtained after splitting can be enriched with more information using extractors. Extractors perform LLM operation on each chunk to extract information contained in their text to speed up the search later on. The following extractors can be enabled with a `True` value:
- Summary: extracts a quick summary of the vector.
- Title: gives an overall title to the vector.
- Keyword: extracts 5 keywords corresponding to the vector.
- QuestionAnswered: extracts 5 questions that are answered in the vector.

*NB: the extractors use an LLM prompt on each vector to add metadata. Their use can quickly consume a lot of tokens. We enabled the summary and keyword for the papers we uploaded.*

#### Embedding
The final step of the pipeline and the most important one is to embed the vectors. This enables the vectors to be represented in multi-dimensional data that can be interpreted by LLMs. The Azure AI foundry environment makes different models available, but we have used the [text-embedding-3-large](https://ai.azure.com/catalog/models/text-embedding-3-large) model so far.

*NB: it is essential to use the same embedding model for preprocessing vectors and loading a search index from the database.*

### Upload to CosmosDB
The upload is managed by the `Cosmos` class. After the pipeline has been setup through the aforementioned steps, the method `run_pipeline` can simply be called. This method takes care of running the different transformers provided to it and when linked directly to a database as is the case for Cosmos, it uploads directly the created vectors.

### Online visualisation
The Azure online portal provides great visualisation tools for the database, notably [here](https://cosmos.azure.com/). For users who have access, the data explorer is great to see the different containers in the database as well as their vectors. It is also possible to perform SQL operations directly from there. 

## How to use
Once the relevant containers are created and populated, they can be accessed through the `Cosmos.load` method to generate a `VectorSearchIndex`. This index can then be used to make queries and will use the content of the container to answer.

Examples scripts are available in the `/examples/data-base/` from the root directory. 
- [cosmos-upload-chunks.py](../../../examples/data-base/cosmos-upload-chunks.py) which runs a pipeline and uploads to the corresponding container.
- [azure-cosmos-load.py](../../../examples/data-base/azure-cosmos-load.py) which loads a certain container to make a search index and query it.