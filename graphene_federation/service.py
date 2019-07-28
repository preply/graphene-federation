import re

from graphene import ObjectType, String, Field

from graphene_federation.extend import extended_types
from .entity import custom_entities


def _mark_external(entity_name, entity, schema):
    for field_name in dir(entity):
        field = getattr(entity, field_name, None)
        if field is not None and getattr(field, '_external', False):
            # todo write tests on regexp
            pattern = re.compile("(\s%s\s*\{[^\}]*\s%s[\s]*:[\s]*[^\s]+)(\s)" % (entity_name, field_name))
            schema = pattern.sub('\g<1> @external ', schema)

    return schema


def get_sdl(schema, custom_entities):
    string_schema = str(schema)
    string_schema = string_schema.replace("\n", " ")

    regex = r"schema \{(\w|\!|\s|\:)*\}"
    pattern = re.compile(regex)
    string_schema = pattern.sub(" ", string_schema)

    for entity_name, entity in custom_entities.items():
        type_def = "type %s " % entity_name
        repl_str = "%s %s " % (type_def, entity._sdl)
        pattern = re.compile(type_def)
        string_schema = pattern.sub(repl_str, string_schema)

    for entity_name, entity in extended_types.items():
        string_schema = _mark_external(entity_name, entity, string_schema)

        type_def = "type %s " % entity_name
        repl_str = "extend %s %s " % (type_def, entity._sdl)
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
