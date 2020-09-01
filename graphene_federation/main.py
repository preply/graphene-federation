import graphene

from .entity import get_entity_query, register_entity
from .service import get_service_query

class SchemaWithCamelCase(graphene.Schema):
    """
    Schema with `auto_camelcase` available as an attribute.
    """
    def __init__(
        self,
        query=None,
        mutation=None,
        subscription=None,
        types=None,
        directives=None,
        auto_camelcase=True,
    ):
        self.auto_camelcase = auto_camelcase
        super().__init__(
            query,
            mutation,
            subscription,
            types,
            directives,
            auto_camelcase
        )

def _get_query(schema, query_cls=None):
    bases = [get_service_query(schema)]
    entity_cls = get_entity_query(schema.auto_camelcase)
    if entity_cls:
        bases.append(entity_cls)
    if query_cls is not None:
        bases.append(query_cls)
    bases = tuple(bases)
    federated_query_cls = type('Query', bases, {})
    return federated_query_cls


def build_schema(query=None, mutation=None, **kwargs):
    schema = SchemaWithCamelCase(query=query, mutation=mutation, **kwargs)
    return SchemaWithCamelCase(query=_get_query(schema, query), mutation=mutation, **kwargs)
