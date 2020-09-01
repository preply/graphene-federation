from graphene import List, Union
from graphene.utils.str_converters import to_snake_case

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


def get_entity_query(auto_camelcase):
    if not custom_entities:
        return

    class EntityQuery:
        entities = graphene.List(get_entity_cls(), name="_entities", representations=List(_Any))

        def resolve_entities(parent, info, representations):
            entities = []
            for representation in representations:
                model = custom_entities[representation["__typename"]]
                model_aguments = representation.copy()
                model_aguments.pop("__typename")
                # todo use schema to identify correct mapping for field names
                if auto_camelcase:
                    model_aguments = {to_snake_case(k): v for k, v in model_aguments.items()}
                model_instance = model(**model_aguments)

                try:
                    resolver = getattr(
                        model, "_%s__resolve_reference" % representation["__typename"])
                except AttributeError:
                    pass
                else:
                    model_instance = resolver(model_instance, info)

                entities.append(model_instance)
            return entities

    return EntityQuery


def key(fields: str):
    def decorator(Type):
        register_entity(Type.__name__, Type)

        existing = getattr(Type, "_sdl", "")

        key_sdl = f'@key(fields: "{fields}")'
        updated = f"{key_sdl} {existing}" if existing else key_sdl

        setattr(Type, '_sdl', updated)
        return Type
    return decorator
