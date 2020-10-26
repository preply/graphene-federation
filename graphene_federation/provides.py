from typing import Any, Dict

from graphene import Field, Schema


def get_provides_parent_types(schema: Schema) -> Dict[str, Any]:
    """
    Find all the types for which a field is provided from the schema.
    They can be easily distinguished from the other type as
    the `@provides` decorator used on the type itself adds a `_provide_parent_type` attribute to them.
    """
    provides_parent_types = {}
    for type_name, type_ in schema._type_map.items():
        if not hasattr(type_, "graphene_type"):
            continue
        if getattr(type_.graphene_type, "_provide_parent_type", False):
            provides_parent_types[type_name] = type_.graphene_type
    return provides_parent_types


def provides(field, fields: str = None):
    """

    :param field: base type (when used as decorator) or field of base type
    :param fields:
    :return:
    """
    if fields is None:  # used as decorator on base type
        if isinstance(field, Field):
            raise RuntimeError("Please specify fields")
        field._provide_parent_type = True
    else:  # used as wrapper over field
        field._provides = fields
    return field
