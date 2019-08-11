from graphene import ObjectType, String, Int, List, NonNull
from graphene_federation import build_schema, extend, external


@extend(fields='id')
class FileNode(ObjectType):
    id = external(Int(required=True))


class Post(ObjectType):
    id = Int(required=True)
    title = String(required=True)
    text = String(required=True)
    files = List(NonNull(FileNode))


class Query(ObjectType):
    goodbye = String()
    posts = List(NonNull(Post))

    def resolve_posts(root, info):
        return [
            Post(id=1, title='title1', text='text1', files=[FileNode(id=1)]),
            Post(id=2, title='title2', text='text2', files=[FileNode(id=2), FileNode(id=3)]),
            Post(id=3, title='title3', text='text3'),
        ]

    def resolve_goodbye(root, info):
        return 'See ya!'


schema = build_schema(query=Query)
