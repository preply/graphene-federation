import graphene

from .entity import get_entity_query, register_entity
from .service import get_service_query


def _get_query(schema, query_cls):
    bases = [get_service_query(schema)]
    entity_cls = get_entity_query()
    if entity_cls:
        bases.append(entity_cls)
    bases.append(query_cls)
    bases = tuple(bases)
    federated_query_cls = type('Query', bases, {})
    return federated_query_cls


def build_schema(query, mutation=None, **kwargs):
    schema = graphene.Schema(query=query, mutation=mutation, **kwargs)
    return graphene.Schema(query=_get_query(schema, query), mutation=mutation, **kwargs)


def key(fields: str):
    def decorator(Type):
        register_entity(Type.__name__, Type)

        existing = getattr(Type, "_sdl", "")

        key_sdl = f'@key(fields: "{fields}")'
        updated = f"{key_sdl} {existing}" if existing else key_sdl

        setattr(Type, '_sdl', updated)
        return Type
    return decorator
