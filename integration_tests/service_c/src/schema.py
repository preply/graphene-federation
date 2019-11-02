from graphene import ObjectType, String, Int, List, NonNull, Field
from graphene_federation import build_schema, extend, external


@extend(fields='id')
class User(ObjectType):
    id = external(Int(required=True))


class Article(ObjectType):
    id = Int(required=True)
    text = String(required=True)
    author = Field(lambda: User)


class Query(ObjectType):
    articles = List(NonNull(lambda: Article))

    def resolve_articles(self, info):
        return [
            Article(id=1, text='some text', author=User(id=5))
        ]


schema = build_schema(Query)
