# graphene-federation
Federation support for graphene

Build: [![CircleCI](https://circleci.com/gh/erebus1/graphene-federation.svg?style=svg)](https://circleci.com/gh/erebus1/graphene-federation)


Draft version, of federation specs implementation on top of Python graphene lib 
https://www.apollographql.com/docs/apollo-server/federation/federation-spec/

Use at your own risk

Based on discussion: https://github.com/graphql-python/graphene/issues/953#issuecomment-508481652

Supports now:
* sdl (_service fields)  # make possible to add schema in federation (as is)
* @key decorator (entity support) # to perform Queries across service boundaries
* extend  # extend remote types
* external  # mark field as external 

Todo implement:
* @requires
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


```python
import graphene
from graphene_federation import build_schema


class Query(graphene.ObjectType):
    ...
    pass

schema = build_schema(Query)  # add _service{sdl} field in Query
```


```python
import graphene
from graphene_federation import external, extend

@extend(fields='id')
class Message(graphene.ObjectType):
    id = external(graphene.Int(required=True))

    def resolve_id(self, **kwargs):
        return 1

```
For more details see [examples](examples/)

Or better check [integration_tests](integration_tests/)

Also cool [example](https://github.com/erebus1/graphene-federation/issues/1) of integration with Mongoengine


### For contribution:
#### Run tests:
* `make test`
* if you've changed Dockerfile or requirements run `make build` before `make test`