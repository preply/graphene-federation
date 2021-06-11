from graphene import ObjectType, String, Int, List, NonNull, Field
from graphene_federation import build_schema, extend, external, requires, key, provides


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


@key(fields='id')
class Article(ObjectType):
    id = Int(required=True)
    text = String(required=True)
    author = Field(lambda: User)

    def __resolve_reference(self, info, **kwargs):
        return Article(id=self.id, text=f'text_{self.id}')


@provides
class ArticleThatProvideAuthorAge(ObjectType):
    """
    should not contain other graphene-federation decorators to proper test test-case
    """
    id = Int(required=True)
    text = String(required=True)
    author = provides(Field(User), fields='age')

    def __resolve_reference(self, info, **kwargs):
        return Article(id=self.id, text=f'text_{self.id}')


class Query(ObjectType):
    articles = List(NonNull(lambda: Article))
    articles_with_author_age_provide = List(NonNull(lambda: ArticleThatProvideAuthorAge))

    def resolve_articles(self, info):
        return [
            Article(id=1, text='some text', author=User(id=5))
        ]

    def resolve_articles_with_author_age_provide(self, info):
        return [
            ArticleThatProvideAuthorAge(id=1, text='some text', author=User(id=5))
        ]


schema = build_schema(Query)
