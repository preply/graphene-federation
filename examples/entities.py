import graphene
from graphene_federation import build_schema, key


def get_file_by_id(id):
    return File(**{'id': id, 'name': 'test_name'})


@key(fields='id')
class File(graphene.ObjectType):
    id = graphene.Int(required=True)
    name = graphene.String()

    def resolve_id(self, info, **kwargs):
        return 1

    def resolve_name(self, info, **kwargs):
        return self.name

    def __resolve_reference(self, info, **kwargs):
        return get_file_by_id(self.id)


class Query(graphene.ObjectType):
    file = graphene.Field(File)

    def resolve_file(self, **kwargs):
        return None   # no direct access


schema = build_schema(Query)

query = '''
    query getSDL {
      _service {
         sdl
      }
    }
'''
result = schema.execute(query)
print(result.data)
# OrderedDict([('_service', OrderedDict([('sdl', '   type File @key(fields: "id") {   id: Int!   name: String }  extend type Query {   hello: String   file: File } ')]))])

query ='''
    query entities($_representations: [_Any!]!) {
      _entities(representations: $_representations) {
        ... on File {
          id
          name
        }
      }
    }
    
'''

result = schema.execute(query, variables={
    "_representations": [
      {
        "__typename": "File",
        "id": 1
      }
    ]
})
print(result.data)
# OrderedDict([('_entities', [OrderedDict([('id', 1), ('name', 'test_name')])])])
