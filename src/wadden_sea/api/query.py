"""Query service for processing RAG queries against entity knowledge bases."""

from typing import Dict
from wadden_sea.api.types import get_entity_config
from wadden_sea.api.engine import get_or_load_index


def process_query(
    query: str,
    entity: str,
) -> Dict[str, any]:
    """Process a RAG query for a specific entity.
    
    Parameters
    ----------
    query: str
        The user's query string
    entity: str
        The entity to query (e.g., 'seal', 'seagrass')
    
    Returns
    -------
    Dict[str, any]
        Dictionary containing:
        - answer: The generated answer
        - sources: List of source file names 
        - query: The original query
        - entity: The queried entity
    
    Raises
    ------
    ValueError
        If entity is unknown or configuration is invalid
    """
    config = get_entity_config(entity)
    original_query = query
    
    if config.grounded_prompt:
        query = f"{config.grounded_prompt} {query}"
    
 
    index = get_or_load_index(entity, config)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    
    sources = [
        node.metadata.get("file_name", "unknown")
        for node in response.source_nodes
    ]
    return {
        "answer": response.response,
        "sources": sources,
        "query": original_query,
        "entity": entity
    }
