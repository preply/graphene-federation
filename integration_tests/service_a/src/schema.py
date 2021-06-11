from graphene import ObjectType, String, Int, List, NonNull, Field, Interface
from graphene_federation import build_schema, extend, external


class DecoratedText(Interface):
    color = Int(required=True)


@extend(fields='id')
class FileNode(ObjectType):
    id = external(Int(required=True))


@extend(fields='id')
class FunnyText(ObjectType):
    class Meta:
        interfaces = (DecoratedText,)
    id = external(Int(required=True))

    def resolve_color(self, info, **kwargs):
        return self.id + 2


class FunnyTextAnother(ObjectType):
    """
    To test @extend on types with same prefix
    """
    class Meta:
        interfaces = (DecoratedText,)
    id = Int(required=True)

    def resolve_color(self, info, **kwargs):
        return self.id + 2


@extend(fields='primaryEmail')
class User(ObjectType):
    primaryEmail = external(String())


class Post(ObjectType):
    id = Int(required=True)
    title = String(required=True)
    text = Field(lambda: FunnyText)
    files = List(NonNull(FileNode))
    author = Field(lambda: User)


class Query(ObjectType):
    goodbye = String()
    posts = List(NonNull(Post))

    def resolve_posts(root, info):
        return [
            Post(id=1, title='title1', text=FunnyText(id=1), files=[FileNode(id=1)]),
            Post(id=2, title='title2', text=FunnyText(id=2), files=[FileNode(id=2), FileNode(id=3)]),
            Post(id=3, title='title3', text=FunnyText(id=3)),
            Post(
                id=4, title='title4', text=FunnyText(id=4),
                author=User(primaryEmail="frank@frank.com")
            ),
        ]

    def resolve_goodbye(root, info):
        return 'See ya!'


schema = build_schema(query=Query, types=[FunnyTextAnother], auto_camelcase=False)
