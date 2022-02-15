import graphene
from graphene import ObjectType, Interface, Mutation
from graphene_federation import build_schema, key


class TextInterface(Interface):
    id = graphene.Int(required=True)
    body = graphene.String(required=True)


@key(fields='id')
class FunnyText(ObjectType):
    class Meta:
        interfaces = (TextInterface,)

    def __resolve_reference(self, info, **kwargs):
        return FunnyText(id=self.id, body=f'funny_text_{self.id}')


@key(fields='id')
class FileNode(ObjectType):
    id = graphene.Int(required=True)
    name = graphene.String(required=True)

    def __resolve_reference(self, info, **kwargs):
        # todo test raise exception here
        return FileNode(id=self.id, name=f'file_{self.id}')


@key('id')
@key('primary_email')
class User(ObjectType):
    id = graphene.Int(required=True)
    primary_email = graphene.String()
    age = graphene.Int()

    def resolve_age(self, info):
        return 17

    def __resolve_reference(self, info, **kwargs):
        if self.id is not None:
            return User(id=self.id, primary_email=f'name_{self.id}@gmail.com')

        user_id = 1001 if self.primary_email == "frank@frank.com" else \
            hash(self.primary_email) % 10000000

        return User(id=user_id, primary_email=self.primary_email)


# to test that @key applied only to FileNode, but not to FileNodeAnother
class FileNodeAnother(ObjectType):
    id = graphene.Int(required=True)
    name = graphene.String(required=True)


class FunnyMutation(Mutation):
    result = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **data):
        return FunnyMutation(result='Funny')


class Mutation(ObjectType):
    funny_mutation = FunnyMutation.Field()


types = [
    FileNode,
    FunnyText,
    FileNodeAnother,
    User
]

schema = build_schema(mutation=Mutation, types=types)


def get_schema():
    """Return the defined schema."""
    return schema