import re

from graphene import ObjectType, String, Field
from graphene.utils.str_converters import to_camel_case

from graphene_federation.extend import extended_types
from graphene_federation.provides import provides_parent_types
from .entity import custom_entities


def _mark_field(
        entity_name, entity, schema: str, mark_attr_name: str,
        decorator_resolver: callable, auto_camelcase: bool
):
    for field_name in dir(entity):
        field = getattr(entity, field_name, None)
        if field is not None and getattr(field, mark_attr_name, None):
            # todo write tests on regexp
            schema_field_name = to_camel_case(field_name) if auto_camelcase else field_name
            pattern = re.compile(
                r"(type\s%s\s[^\{]*\{[^\}]*\s%s[\s]*:[\s]*[^\s]+)(\s)" % (
                    entity_name, schema_field_name))
            schema = pattern.sub(
                rf'\g<1> {decorator_resolver(getattr(field, mark_attr_name))} ', schema)

    return schema


def _mark_external(entity_name, entity, schema, auto_camelcase):
    return _mark_field(
        entity_name, entity, schema, '_external', lambda _: '@external', auto_camelcase)


def _mark_requires(entity_name, entity, schema, auto_camelcase):
    return _mark_field(
        entity_name, entity, schema, '_requires', lambda fields: f'@requires(fields: "{fields}")',
        auto_camelcase
    )


def _mark_provides(entity_name, entity, schema, auto_camelcase):
    return _mark_field(
        entity_name, entity, schema, '_provides', lambda fields: f'@provides(fields: "{fields}")',
        auto_camelcase
    )


def get_sdl(schema, custom_entities):
    string_schema = str(schema)
    string_schema = string_schema.replace("\n", " ")

    regex = r"schema \{(\w|\!|\s|\:)*\}"
    pattern = re.compile(regex)
    string_schema = pattern.sub(" ", string_schema)

    for entity_name, entity in custom_entities.items():
        type_def_re = r"(type %s [^\{]*)" % entity_name
        repl_str = r"\1 %s " % entity._sdl
        pattern = re.compile(type_def_re)
        string_schema = pattern.sub(repl_str, string_schema)

    for entity in provides_parent_types:
        string_schema = _mark_provides(
            entity.__name__, entity, string_schema, schema.auto_camelcase)

    for entity_name, entity in extended_types.items():
        string_schema = _mark_external(entity_name, entity, string_schema, schema.auto_camelcase)
        string_schema = _mark_requires(entity_name, entity, string_schema, schema.auto_camelcase)

        type_def_re = r"type %s ([^\{]*)" % entity_name
        type_def = r"type %s " % entity_name
        repl_str = r"extend %s \1" % type_def
        pattern = re.compile(type_def_re)

        string_schema = pattern.sub(repl_str, string_schema)

    return string_schema


def get_service_query(schema):
    sdl_str = get_sdl(schema, custom_entities)

    class _Service(ObjectType):
        sdl = String()

        def resolve_sdl(parent, _):
            return sdl_str

    class ServiceQuery(ObjectType):
        _service = Field(_Service, name="_service")

        def resolve__service(parent, info):
            return _Service()

    return ServiceQuery
