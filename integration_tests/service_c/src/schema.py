from graphene import ObjectType, String, Int, List, NonNull, Field
from graphene_federation import build_schema, extend, external, requires, provides


@extend(fields='id')
class User(ObjectType):
    id = external(Int(required=True))
    primary_email = external(String())
    uppercase_email = requires(String(), fields='primaryEmail')
    age = external(Int())

    def resolve_uppercase_email(self, info):
        return self.primary_email.upper() if self.primary_email else self.primary_email

    def resolve_age(self, info):
        return 18


class Article(ObjectType):
    id = Int(required=True)
    text = String(required=True)
    author = provides(Field(lambda: User), fields='age')


class Query(ObjectType):
    articles = List(NonNull(lambda: Article))

    def resolve_articles(self, info):
        return [
            Article(id=1, text='some text', author=User(id=5))
        ]


schema = build_schema(Query)
