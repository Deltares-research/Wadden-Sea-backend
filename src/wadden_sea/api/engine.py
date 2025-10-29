import os
from llama_index.core import VectorStoreIndex
from vfn_rag.utils.models import azure_open_ai, get_azure_open_ai_embedding
from vfn_rag.utils.config_loader import ConfigLoader
from azure.cosmos import CosmosClient
from vfn_rag.retrieval.cosmos import Cosmos
from dotenv import load_dotenv
#%%
load_dotenv()

def load_configs():
    COSMOS_URI = os.getenv("AZURE_COSMOSDB_URI")
    COSMOS_KEY = os.getenv("AZURE_COSMOSDB_KEY")

    llm = azure_open_ai()
    embed_model = get_azure_open_ai_embedding()
    ConfigLoader(llm, embed_model)

    client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
    database_name = "vectorSearchDB"
    container_name = "vectorSearchContainer"


    storage_context = Cosmos.load(
        database_name, container_name, client
    )
    store = storage_context.store
    # load index
    index = VectorStoreIndex.from_vector_store(vector_store=store.vector_store, embed_model=embed_model)

    query_engine = index.as_query_engine()
    return query_engine