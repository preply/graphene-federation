from typing import Any, Dict

from graphene import List, Union, Schema
from graphene.utils.str_converters import to_camel_case

import graphene

from .types import _Any


def get_entities(schema: Schema) -> Dict[str, Any]:
    """
    Find all the entities from the schema.
    They can be easily distinguished from the other type as
    the `@key` and `@extend` decorators adds a `_sdl` attribute to them.
    """
    entities = {}
    for type_name, type_ in schema._type_map.items():
        if not hasattr(type_, "graphene_type"):
            continue
        if getattr(type_.graphene_type, "_sdl", None):
            entities[type_name] = type_.graphene_type
    return entities


def get_entity_cls(entities: Dict[str, Any]):
    """
    Create _Entity type which is a union of all the entities types.
    """
    class _Entity(Union):
        class Meta:
            types = tuple(entities.values())
    return _Entity


def get_entity_query(schema: Schema):
    """
    Create Entity query.
    """
    entities_dict = get_entities(schema)
    if not entities_dict:
        return

    entity_type = get_entity_cls(entities_dict)

    class EntityQuery:
        entities = graphene.List(entity_type, name="_entities", representations=List(_Any))

        def resolve_entities(self, info, representations):
            entities = []
            for representation in representations:
                type_ = schema.get_type(representation["__typename"])
                model = type_.graphene_type
                model_arguments = representation.copy()
                model_arguments.pop("__typename")
                if schema.auto_camelcase:
                    # Create field name conversion dict (from schema name to actual graphene_type field name)
                    field_names = {to_camel_case(name): name for name in model._meta.fields}
                    model_arguments = {field_names[k]: v for k, v in model_arguments.items()}
                model_instance = model(**model_arguments)

                try:
                    resolver = getattr(
                        model, "_%s__resolve_reference" % model.__name__)
                except AttributeError:
                    pass
                else:
                    model_instance = resolver(model_instance, info)

                entities.append(model_instance)
            return entities

    return EntityQuery


def key(fields: str):
    def decorator(Type):
        existing = getattr(Type, "_sdl", "")

        key_sdl = f'@key(fields: "{fields}")'
        updated = f"{key_sdl} {existing}" if existing else key_sdl

        setattr(Type, '_sdl', updated)
        return Type
    return decorator
