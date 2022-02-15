import graphene
from typing import Any, Dict, Union
from . import graphql_compatibility
from .types import _Any
from .utils import field_name_to_type_attribute


def get_entities(schema: graphene.Schema) -> Dict[str, Any]:
    """
    Find all the entities from the schema.
    They can be easily distinguished from the other type as
    the `@key` and `@extend` decorators adds a `_sdl` attribute to them.
    """
    entities = {}
    for type_name, type_ in graphql_compatibility.get_type_map_from_schema(
        schema
    ).items():
        if not hasattr(type_, "graphene_type"):
            continue
        if getattr(type_.graphene_type, "_keys", None):
            entities[type_name] = type_.graphene_type
    return entities


def get_entity_cls(entities: Dict[str, Any]):
    """
    Create _Entity type which is a union of all the entities types.
    """

    class _Entity(graphene.Union):
        class Meta:
            types = tuple(entities.values())

    return _Entity


def get_entity_query(schema: graphene.Schema):
    """
    Create Entity query.
    """
    entities_dict = get_entities(schema)
    if not entities_dict:
        return

    entity_type = get_entity_cls(entities_dict)

    class EntityQuery:
        entities = graphene.List(
            entity_type, name="_entities", representations=graphene.List(_Any)
        )

        def resolve_entities(self, info, representations):
            entities = []
            for representation in representations:
                # old type_ = schema.get_type(representation["__typename"])
                type_ = graphql_compatibility.call_schema_get_type(
                    schema, representation["__typename"]
                )
                model = type_.graphene_type
                model_arguments = representation.copy()
                model_arguments.pop("__typename")
                if graphql_compatibility.is_schema_in_auto_camelcase(schema):
                    get_model_attr = field_name_to_type_attribute(schema, model)
                    model_arguments = {
                        get_model_attr(k): v for k, v in model_arguments.items()
                    }
                model_instance = model(**model_arguments)

                resolver = getattr(
                    model, "_%s__resolve_reference" % model.__name__, None
                ) or getattr(model, "_resolve_reference", None)
                if resolver:
                    model_instance = resolver(model_instance, info)

                entities.append(model_instance)
            return entities

    return EntityQuery


def key(fields: str):
    """
    Take as input a field that should be used as key for that entity.
    See specification: https://www.apollographql.com/docs/federation/federation-spec/#key

    If the input contains a space it means it's a [compound primary key](https://www.apollographql.com/docs/federation/entities/#defining-a-compound-primary-key)
    which is not yet supported.
    """
    if " " in fields:
        raise NotImplementedError("Compound primary keys are not supported.")

    def decorator(Type):
        # Check the provided fields actually exist on the Type.
        assert (
            fields in Type._meta.fields
        ), f'Field "{fields}" does not exist on type "{Type._meta.name}"'

        keys = getattr(Type, "_keys", [])
        keys.append(fields)
        setattr(Type, "_keys", keys)

        return Type

    return decorator
