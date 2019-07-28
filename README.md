# graphene-federation
Federation support for graphene

Draft version, of federation specs implementation on top of Python graphene lib 
https://www.apollographql.com/docs/apollo-server/federation/federation-spec/

Use at your own risk

Based on discussion: https://github.com/graphql-python/graphene/issues/953#issuecomment-508481652

Supports now:
* sdl (_service fields)  # make possible to add schema in federation (as is)
* @key decorator (entity support) # to perform Queries across service boundaries


Todo implement:
* @requires
* @external
* @provides


```python
import graphene
from graphene_federation import build_schema, key

@key(fields='id')  # mark File as Entity and add in EntityUnion https://www.apollographql.com/docs/apollo-server/federation/federation-spec/#key
class File(graphene.ObjectType):
    id = graphene.Int(required=True)
    name = graphene.String()

    def resolve_id(self, info, **kwargs):
        return 1

    def resolve_name(self, info, **kwargs):
        return self.name

    def __resolve_reference(self, info, **kwargs):  # https://www.apollographql.com/docs/apollo-server/api/apollo-federation/#__resolvereference
        return get_file_by_id(self.id)
```

For more details see [examples](examples/entities.py)