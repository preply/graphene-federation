import graphene
from graphene import ObjectType
from graphene_federation import build_schema, extend, external, requires, key, provides


@extend(fields='id')
class User(ObjectType):
    id = external(graphene.Int(required=True))
    primary_email = external(graphene.String())
    uppercase_email = requires(graphene.String(), fields='primaryEmail')
    age = external(graphene.Int())

    def resolve_uppercase_email(self, info):
        return self.primary_email.upper() if self.primary_email else self.primary_email

    def resolve_age(self, info):
        return 18


@key(fields='id')
class Article(ObjectType):
    id = graphene.Int(required=True)
    text = graphene.String(required=True)
    author = graphene.Field(lambda: User)

    def __resolve_reference(self, info, **kwargs):
        return Article(id=self.id, text=f'text_{self.id}')


@provides
class ArticleThatProvideAuthorAge(ObjectType):
    """
    should not contain other graphene-federation decorators to proper test test-case
    """
    id = graphene.Int(required=True)
    text = graphene.String(required=True)
    author = provides(graphene.Field(User), fields='age')

    def __resolve_reference(self, info, **kwargs):
        return Article(id=self.id, text=f'text_{self.id}')


class Query(ObjectType):
    articles = graphene.List(graphene.NonNull(lambda: Article))
    articles_with_author_age_provide = graphene.List(graphene.NonNull(lambda: ArticleThatProvideAuthorAge))

    def resolve_articles(self, info):
        return [
            Article(id=1, text='some text', author=User(id=5))
        ]

    def resolve_articles_with_author_age_provide(self, info):
        return [
            ArticleThatProvideAuthorAge(id=1, text='some text', author=User(id=5))
        ]


schema = build_schema(Query)


def get_schema():
    """Return the defined schema."""
    return schema