from graphene import List, Union

import graphene

from .types import _Any


custom_entities = {}


def register_entity(typename, Type):
    custom_entities[typename] = Type


def get_entity_cls():
    class _Entity(Union):
        class Meta:
            types = tuple(custom_entities.values())
    return _Entity


def get_entity_query():
    if not custom_entities:
        return

    class EntityQuery:
        entities = graphene.List(get_entity_cls(), name="_entities", representations=List(_Any))

        def resolve_entities(parent, info, representations):
            entities = []
            for representation in representations:
                model = custom_entities[representation["__typename"]]
                resolver = getattr(model, "_%s__resolve_reference" % representation["__typename"])
                model_aguments = representation.copy()
                model_aguments.pop("__typename")

                entities.append(
                    resolver(model(**model_aguments), info)
                )
            return entities

    return EntityQuery
