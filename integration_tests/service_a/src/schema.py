from graphene import ObjectType, String, Int, List, NonNull, Field
from graphene_federation import build_schema, extend, external


@extend(fields='id')
class FileNode(ObjectType):
    id = external(Int(required=True))


@extend(fields='id')
class FunnyText(ObjectType):
    id = external(Int(required=True))


@extend(fields='email')
class User(ObjectType):
    email = external(String())


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
            Post(id=4, title='title4', text=FunnyText(id=4), author=User(email="frank@frank.com")),
        ]

    def resolve_goodbye(root, info):
        return 'See ya!'


schema = build_schema(query=Query)
