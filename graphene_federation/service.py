import re

from typing import Any, Dict

from packaging import version

import graphene
from graphene import ObjectType, String, Field, Schema, __version__ as graphene_version

if version.parse(graphene_version) < version.parse('3.0.0'):
    from graphql.utils.schema_printer import _print_fields as print_fields
else:
    from graphql.utilities.print_schema import print_fields as print_fields

from graphene_federation.extend import get_extended_types
from graphene_federation.provides import get_provides_parent_types

from .entity import get_entities


class MonoFieldType:
    """
    In order to be able to reuse the `print_fields` method to get a singular field
    string definition, we need to define an object that has a `.fields` attribute.
    """
    def __init__(self, name, field):
        self.fields = {
            name: field
        }

DECORATORS = {
    "_external": lambda _: "@external",
    "_requires": lambda fields: f'@requires(fields: "{fields}")',
    "_provides": lambda fields: f'@provides(fields: "{fields}")',
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
    entity_type = schema.get_type(entity_name)
    str_fields = []
    for name, field in entity_type.fields.items():
        str_field = print_fields(MonoFieldType(name, field))
        f = getattr(entity, name, None)
        if f is not None:
            for decorator, decorator_resolver in DECORATORS.items():
                decorator_value = getattr(f, decorator, None)
                if decorator_value:
                    str_field += f" {decorator_resolver(decorator_value)}"
        str_fields.append(str_field)
    str_fields_annotated = "\n".join(str_fields)
    # Replace the original field declaration by the annotated one
    str_fields_original = print_fields(entity_type)
    pattern = re.compile(
        r"(type\s%s\s[^\{]*)\{\s*%s\s*\}" % (
            entity_name, re.escape(str_fields_original)
        )
    )
    string_schema_original = string_schema + ""
    string_schema = pattern.sub(
        r"\g<1> {\n%s\n}" % str_fields_annotated,
        string_schema
    )
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

    # Add entity sdl
    for entity_name, entity in entities.items():
        type_def_re = r"(type %s [^\{]*)" % entity_name
        repl_str = r"\1 %s " % entity._sdl
        pattern = re.compile(type_def_re)
        string_schema = pattern.sub(repl_str, string_schema)

    # print(string_schema)
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
