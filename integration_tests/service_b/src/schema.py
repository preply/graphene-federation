from graphene import ObjectType, String, Int, Field
from graphene_federation import build_schema, key


@key(fields='id')
class FileNode(ObjectType):
    id = Int(required=True)
    name = String(required=True)

    def __resolve_reference(self, info, **kwargs):
        # todo test raise exception here
        return FileNode(id=self.id, name=f'file_{self.id}')


class Query(ObjectType):
    # todo support query w/o root fields
    file = Field(lambda: FileNode)


schema = build_schema(Query, types=[FileNode])
