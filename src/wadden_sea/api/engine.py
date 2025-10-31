"""Cosmos DB client management with singleton pattern."""

import os
from typing import Optional
from azure.cosmos import CosmosClient
from llama_index.core import VectorStoreIndex
from vfn_rag.retrieval.cosmos import Cosmos
from llama_index.core.settings import Settings
from wadden_sea.api.types import EntityConfig

_client: Optional[CosmosClient] = None


def get_cosmos_client() -> CosmosClient:
    """Get or create a Cosmos client instance (singleton pattern).

    The client is created lazily on first access and cached for subsequent calls.
    This ensures a single shared client across the application with connection pooling.

    Returns
    -------
    CosmosClient
        The Azure Cosmos client instance

    Raises
    ------
    ValueError
        If Azure Cosmos DB credentials are not configured
    """
    global _client
    if _client is None:
        uri = os.getenv("AZURE_COSMOSDB_URI")
        key = os.getenv("AZURE_COSMOSDB_KEY")

        if not uri or not key:
            raise ValueError("Azure Cosmos DB credentials not configured. Set AZURE_COSMOSDB_URI and AZURE_COSMOSDB_KEY environment variables.")

        _client = CosmosClient(uri, credential=key)

    return _client


def reset_client():
    """Reset the cached client (useful for testing or reconnection).

    The next call to get_cosmos_client() will create a new client instance.
    """
    global _client
    _client = None



def get_or_load_index(entity: str, config: EntityConfig) -> VectorStoreIndex:
    """Load index for an entity from Cosmos DB.

    This function always loads fresh data from Cosmos DB on every call.

    Parameters
    ----------
    entity: str
        The entity name
    config: EntityConfig
        The entity configuration

    Returns
    -------
    VectorStoreIndex
        The loaded vector index

    Raises
    ------
    Exception
        If unable to load the index from Cosmos DB
    """
    storage_context = Cosmos.load(
        database_name=config.database_name,
        container_name=config.container_name,
        client=get_cosmos_client()
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=storage_context.store.vector_store,
        embed_model=Settings.embed_model
    )

    return index