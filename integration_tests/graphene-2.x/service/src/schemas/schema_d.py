import graphene
from graphene import ObjectType
from graphene_federation import build_schema, extend, external

"""
Alphabet order - matters
Y should be just after X in sdl
https://github.com/preply/graphene-federation/issues/26#issuecomment-572127271
"""


@extend(fields='id')
class Article(ObjectType):
    id = external(graphene.Int(required=True))


class X(ObjectType):
    x_article = graphene.Field(Article)


class Y(ObjectType):
    id = graphene.Int(required=True)


class Query(ObjectType):
    x = graphene.Field(X)
    y = graphene.Field(Y)


schema = build_schema(query=Query)


def get_schema():
    """Return the defined schema."""
    return schema