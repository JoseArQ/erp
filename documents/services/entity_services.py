from django.shortcuts import get_object_or_404
from ..models import Entity

def get_entity(entity_data : dict):
    """
    Retrieve an existing Entity instance by ID.
    Raise 404 if not found.
    """
    entity_id = entity_data.get("id")

    if not entity_id:
        raise ValueError("Entity ID is required to retrieve an entity.")
    
    entity = get_object_or_404(Entity, id=entity_id)
    return entity
