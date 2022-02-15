from typing import Any, Dict, List, Union

from graphene import Schema

from graphene_federation import graphql_compatibility


def get_extended_types(schema: Schema) -> Dict[str, Any]:
    """
    Find all the extended types from the schema.
    They can be easily distinguished from the other type as
    the `@extend` decorator adds a `_extended` attribute to them.
    """
    extended_types = {}
    for type_name, type_ in graphql_compatibility.get_type_map_from_schema(
        schema
    ).items():
        if not hasattr(type_, "graphene_type"):
            continue
        if getattr(type_.graphene_type, "_extended", False):
            extended_types[type_name] = type_.graphene_type
    return extended_types


def extend(fields: str):
    """
    Decorator to use to extend a given type.
    The field to extend must be provided as input as a string.
    """

    def decorator(Type):
        assert not hasattr(
            Type, "_keys"
        ), "Can't extend type which is already extended or has @key"
        # Check the provided fields actually exist on the Type.
        assert (
            fields in Type._meta.fields
        ), f'Field "{fields}" does not exist on type "{Type._meta.name}"'
        if hasattr(Type._meta, "description") and Type._meta.description is not None:
            raise ValueError(
                f"""{Type.__name__} has a non empty description and it is also marked with extend. 
                They are mututally exclusive. 
                See https://github.com/graphql/graphql-js/issues/2385#issuecomment-577997521"""
            )
        # Set a `_keys` attribute so it will be registered as an entity
        setattr(Type, "_keys", [fields])
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


def requires(field, fields: Union[str, List[str]]):
    """
    Mark the required fields for a given field.
    The input `fields` can be either a string or a list.
    When it is a string we split at spaces to get the list of fields.
    """
    # TODO: We should validate the `fields` input to check it is actually existing fields but we
    # don't have access here to the parent graphene type.
    if isinstance(fields, str):
        fields = fields.split()
    assert not hasattr(
        field, "_requires"
    ), "Can't chain `requires()` method calls on one field."
    field._requires = fields
    return field
