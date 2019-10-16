from graphene import ObjectType, String, Int, Field, Interface, Mutation
from graphene_federation import build_schema, key


class TextInterface(Interface):
    id = Int(required=True)
    body = String(required=True)


@key(fields='id')
class FunnyText(ObjectType):
    class Meta:
        interfaces = (TextInterface,)

    def __resolve_reference(self, info, **kwargs):
        return FunnyText(id=self.id, body=f'funny_text_{self.id}')


@key(fields='id')
class FileNode(ObjectType):
    id = Int(required=True)
    name = String(required=True)

    def __resolve_reference(self, info, **kwargs):
        # todo test raise exception here
        return FileNode(id=self.id, name=f'file_{self.id}')


# to test that @key applied only to FileNode, but not to FileNodeAnother
class FileNodeAnother(ObjectType):
    id = Int(required=True)
    name = String(required=True)


class Query(ObjectType):
    file = Field(lambda: FileNode)


class FunnyMutation(Mutation):
    result = String(required=True)

    @classmethod
    def mutate(cls, root, info, **data):
        return FunnyMutation(result='Funny')


class Mutation(ObjectType):
    funny_mutation = FunnyMutation.Field()


schema = build_schema(Query, Mutation, types=[FileNode, FunnyText, FileNodeAnother])
