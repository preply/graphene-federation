import re

from graphene import ObjectType, String, Field

from .entity import custom_entities


def get_sdl(schema, custom_entities):
    string_schema = str(schema)
    string_schema = string_schema.replace("\n", " ")

    string_schema = string_schema.replace("type Query", "extend type Query")
    regex = r"schema \{(\w|\!|\s|\:)*\}"
    pattern = re.compile(regex)
    string_schema = pattern.sub(" ", string_schema)

    for entity_name, entity in custom_entities.items():
        type_def = "type " + entity_name
        repl_str = "%s %s" % (type_def, entity._sdl)
        pattern = re.compile(type_def)
        string_schema = pattern.sub(repl_str, string_schema)

    return string_schema


def get_service_query(schema):
    sdl = get_sdl(schema, custom_entities)

    class _Service(ObjectType):
        sdl = String()

        def resolve_sdl(parent, _):
            return sdl

    class ServiceQuery(ObjectType):
        _service = Field(_Service, name="_service")

        def resolve__service(parent, info):
            return _Service()

    return ServiceQuery
