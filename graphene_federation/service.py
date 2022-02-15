import re

from typing import Any, Dict, List

import graphene
from graphene import ObjectType, String, Field, Schema

from graphene_federation.extend import get_extended_types
from graphene_federation.provides import get_provides_parent_types
from . import graphql_compatibility

from .entity import get_entities
from .utils import field_name_to_type_attribute, type_attribute_to_field_name


class MonoFieldType:
    """
    In order to be able to reuse the `print_fields` method to get a singular field
    string definition, we need to define an object that has a `.fields` attribute.
    """

    def __init__(self, name, field):
        self.fields = {name: field}


def convert_fields(schema: Schema, fields: List[str]) -> str:
    get_field_name = type_attribute_to_field_name(schema)
    return " ".join([get_field_name(field) for field in fields])


DECORATORS = {
    "_external": lambda _schema, _fields: "@external",
    "_requires": lambda schema, fields: f'@requires(fields: "{convert_fields(schema, fields)}")',
    "_provides": lambda schema, fields: f'@provides(fields: "{convert_fields(schema, fields)}")',
}


def add_entity_fields_decorators(entity, schema: Schema, string_schema: str) -> str:
    """
    For a given entity, go through all its field and see if any directive decorator need to be added.
    The methods (from graphene-federation) marking fields that require some special treatment for federation add
    corresponding attributes to the field itself.
    Those attributes are listed in the `DECORATORS` variable as key and their respective value is the resolver that
    returns what needs to be amended to the field declaration.

    This method simply go through the field that need to be modified and replace them with their annotated version in the
    schema string representation.
    """
    entity_name = entity._meta.name
    # old entity_type = schema.get_type(entity_name)
    entity_type = graphql_compatibility.call_schema_get_type(schema, entity_name)
    str_fields = []
    get_model_attr = field_name_to_type_attribute(schema, entity)
    for field_name, field in entity_type.fields.items():
        str_field = graphql_compatibility.call_schema_print_fields(
            schema, MonoFieldType(field_name, field)
        )
        # Check if we need to annotate the field by checking if it has the decorator attribute set on the field.
        f = getattr(entity, get_model_attr(field_name), None)
        if f is not None:
            for decorator, decorator_resolver in DECORATORS.items():
                decorator_value = getattr(f, decorator, None)
                if decorator_value:
                    str_field += f" {decorator_resolver(schema, decorator_value)}"
        str_fields.append(str_field)
    str_fields_annotated = "\n".join(str_fields)
    # Replace the original field declaration by the annotated one
    str_fields_original = graphql_compatibility.call_schema_print_fields(
        schema, entity_type
    )
    pattern = re.compile(
        r"(type\s%s\s[^\{]*)\{\s*%s\s*\}"
        % (entity_name, re.escape(str_fields_original))
    )
    string_schema_original = string_schema + ""
    string_schema = pattern.sub(r"\g<1> {\n%s\n}" % str_fields_annotated, string_schema)
    return string_schema


def get_sdl(schema: Schema) -> str:
    """
    Add all needed decorators to the string representation of the schema.
    """
    string_schema = str(schema)

    regex = r"schema \{(\w|\!|\s|\:)*\}"
    pattern = re.compile(regex)
    string_schema = pattern.sub(" ", string_schema)

    # Get various objects that need to be amended
    extended_types = get_extended_types(schema)
    provides_parent_types = get_provides_parent_types(schema)
    entities = get_entities(schema)

    # Add fields directives (@external, @provides, @requires)
    for entity in set(provides_parent_types.values()) | set(extended_types.values()):
        string_schema = add_entity_fields_decorators(entity, schema, string_schema)

    # Prepend `extend` keyword to the type definition of extended types
    for entity_name, entity in extended_types.items():
        type_def = re.compile(r"type %s ([^\{]*)" % entity_name)
        repl_str = r"extend type %s \1" % entity_name
        string_schema = type_def.sub(repl_str, string_schema)

    # Add entity keys declarations
    get_field_name = type_attribute_to_field_name(schema)
    for entity_name, entity in entities.items():
        type_def_re = r"(type %s [^\{]*)" % entity_name
        type_annotation = " ".join(
            [f'@key(fields: "{get_field_name(key)}")' for key in entity._keys]
        )
        repl_str = r"\1%s " % type_annotation
        pattern = re.compile(type_def_re)
        string_schema = pattern.sub(repl_str, string_schema)

    return string_schema


def get_service_query(schema: Schema):
    sdl_str = get_sdl(schema)

    class _Service(ObjectType):
        sdl = String()

        def resolve_sdl(parent, _):
            return sdl_str

    class ServiceQuery(ObjectType):
        _service = Field(_Service, name="_service")

        def resolve__service(parent, info):
            return _Service()

    return ServiceQuery
