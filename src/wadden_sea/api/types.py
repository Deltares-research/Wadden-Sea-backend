"""Entity configuration for mapping knowledge bases to database containers."""

from typing import NamedTuple, Optional


class EntityConfig(NamedTuple):
    """Configuration for an entity knowledge base.
    
    Attributes:
        grounded_prompt:
            The prompt to prepend to queries for this entity (optional)
        database_name:
            The Azure Cosmos DB database name
        container_name:
            The container name within the database
        description:
            Human-readable description of the entity
    """
    grounded_prompt: Optional[str]
    database_name: str
    container_name: str
    description: str


ENTITY_MAPPING = {
    "seal": EntityConfig(
        grounded_prompt="Pretend that you are a seal in the wadden sea and give truthful answers based on the report data. Do not hallucinate if no information is available.",
        database_name="vectorSearchDB",
        container_name="seal_vectorSearchContainer",
        description="Seal knowledge base"
    ),
    "seagrass": EntityConfig(
        grounded_prompt="Pretend that you are seagrass in the wadden sea and give truthful answers based on the report data. Do not hallucinate if no information is available.",
        database_name="vectorSearchDB",
        container_name="seagrassContainer",
        description="Seagrass knowledge base"
    ),
}


def get_entity_config(entity: str) -> EntityConfig:
    """Get configuration for an entity.
    
    Parameters
    ----------
    entity: str
        The entity name (e.g., 'seal', 'seagrass')
    
    Returns
    -------
    EntityConfig
        The configuration for the entity
    
    Raises
    ------
    ValueError
        If the entity is not found in the mapping
    """
    if entity not in ENTITY_MAPPING:
        raise ValueError(
            f"Unknown entity: '{entity}'. Available entities: {list(ENTITY_MAPPING.keys())}"
        )
    return ENTITY_MAPPING[entity]

