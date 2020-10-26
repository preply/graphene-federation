from typing import Any, Dict

from graphene import Schema


def get_extended_types(schema: Schema) -> Dict[str, Any]:
    """
    Find all the extended types from the schema.
    They can be easily distinguished from the other type as
    the `@extend` decorator adds a `_extended` attribute to them.
    """
    extended_types = {}
    for type_name, type_ in schema._type_map.items():
        if not hasattr(type_, "graphene_type"):
            continue
        if getattr(type_.graphene_type, "_extended", False):
            extended_types[type_name] = type_.graphene_type
    return extended_types


def extend(fields: str):
    """
    Decorator to use to extend a given type.
    The fields to extend must be provided as input.
    """
    def decorator(Type):
        if hasattr(Type, "_sdl"):
            raise RuntimeError("Can't extend type which is already extended or has @key")
        # Set a `_sdl` attribute so it will be registered as an entity
        setattr(Type, "_sdl", '@key(fields: "%s")' % fields)
        # Set a `_extended` attribute to be able to distinguish it from the other entities
        setattr(Type, "_extended", True)
        return Type
    return decorator


def external(field):
    """
    Mark a field as external.
    """
    field._external = True
    return field


def requires(field, fields: str):
    field._requires = fields
    return field
