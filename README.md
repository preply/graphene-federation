# graphene-federation
Federation support for graphene

Build: [![CircleCI](https://circleci.com/gh/preply/graphene-federation.svg?style=svg)](https://circleci.com/gh/preply/graphene-federation)


Federation specs implementation on top of Python graphene lib 
https://www.apollographql.com/docs/apollo-server/federation/federation-spec/

Based on discussion: https://github.com/graphql-python/graphene/issues/953#issuecomment-508481652

Supports now:
* sdl (_service fields)  # make possible to add schema in federation (as is)
* `@key` decorator (entity support) # to perform Queries across service boundaries
    *  You can use multiple `@key` per each ObjectType
    ```python
        @key('id')
        @key('email')
        class User(ObjectType):
            id = Int(required=True)
            email = String()
        
            def __resolve_reference(self, info, **kwargs):
                if self.id is not None:
                    return User(id=self.id, email=f'name_{self.id}@gmail.com')
                return User(id=123, email=self.email)              
    ```
* extend  # extend remote types
* external  # mark field as external 
* requires  # mark that field resolver requires other fields to be pre-fetched
* provides  # to annotate the expected returned fieldset from a field on a base type that is guaranteed to be selectable by the gateway. 
    * **Base class should be decorated with `@provides`** as well as field on a base type that provides. Check example bellow:
    ```python
        import graphene
        from graphene_federation import provides
        
        @provides
        class ArticleThatProvideAuthorAge(graphene.ObjectType):
            id = Int(required=True)
            text = String(required=True)
            author = provides(Field(User), fields='age')
    ```


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

### __resolve_reference
* Each type which is decorated with `@key` or `@extend` is added to `_Entity` union
* `__resolve_reference` method can be defined for each type that is an entity. This method is called whenever an entity is requested as part of the fulfilling a query plan.
If not explicitly defined, default resolver is used. Default resolver just creates instance of type with passed fieldset as kwargs, see [`entity.get_entity_query`](graphene_federation/entity.py) for more details
* You should define `__resolve_reference`, if you need to extract object before passing it to fields resolvers (example: [FileNode](integration_tests/service_b/src/schema.py))
* You should not define `__resolve_reference`, if fileds resolvers need only data passed in fieldset (example: [FunnyText](integration_tests/service_a/src/schema.py))
* read more in [official documentation](https://www.apollographql.com/docs/apollo-server/api/apollo-federation/#__resolvereference)
------------------------


### Known issues:
1. decorators will not work properly
* on fields with capitalised letters with `auto_camelcase=True`, for example: `my_ABC_field = String()`
* on fields with custom names for example `some_field = String(name='another_name')`

---------------------------

For more details see [examples](examples/)

Or better check [integration_tests](integration_tests/)

Also cool [example](https://github.com/preply/graphene-federation/issues/1) of integration with Mongoengine


### For contribution:
#### Run tests:
* `make test`
* if you've changed Dockerfile or requirements run `make build` before `make test`

---------------------------

Also, you can read about how we've come to federation at Preply [here](https://medium.com/preply-engineering/apollo-federation-support-in-graphene-761a0512456d) 