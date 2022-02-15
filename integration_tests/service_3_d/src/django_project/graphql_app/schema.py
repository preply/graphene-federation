from graphene import ObjectType, Int, Field
from graphene_federation import build_schema, extend, external

"""
Alphabet order - matters
Y should be just after X in sdl
https://github.com/preply/graphene-federation/issues/26#issuecomment-572127271
"""


@extend(fields='id')
class Article(ObjectType):
    id = external(Int(required=True))


class X(ObjectType):
    x_article = Field(Article)


class Y(ObjectType):
    id = Int(required=True)


class Query(ObjectType):
    x = Field(X)
    y = Field(Y)


schema = build_schema(query=Query)
