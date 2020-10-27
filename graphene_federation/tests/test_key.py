import pytest

from graphql import graphql

from graphene import ObjectType, ID, String, Field

from ..entity import key
from ..main import build_schema


def test_multiple_keys():
    @key("identifier")
    @key("email")
    class User(ObjectType):
        identifier = ID()
        email = String()

    class Query(ObjectType):
        user = Field(User)

    schema = build_schema(query=Query)
    assert (
        str(schema)
        == """schema {
  query: Query
}

type Query {
  user: User
  _entities(representations: [_Any]): [_Entity]
  _service: _Service
}

type User {
  identifier: ID
  email: String
}

scalar _Any

union _Entity = User

type _Service {
  sdl: String
}
"""
    )
    # Check the federation service schema definition language
    query = """
    query {
        _service {
            sdl
        }
    }
    """
    result = graphql(schema, query)
    assert not result.errors
    assert (
        result.data["_service"]["sdl"].strip()
        == """
type Query {
  user: User
}

type User @key(fields: "email") @key(fields: "identifier") {
  identifier: ID
  email: String
}
""".strip()
    )


def test_key_non_existing_field_failure():
    """
    Test that using the key decorator and providing a field that does not exist fails.
    """
    with pytest.raises(AssertionError) as err:

        @key("potato")
        class A(ObjectType):
            id = ID()

    assert 'Field "potato" does not exist on type "A"' == str(err.value)


def test_compound_primary_keys_failure():
    """
    Compound primary keys are not implemented as of now so this test checks that at least the user get
    an explicit failure.
    """

    class Organization(ObjectType):
        id = ID()

    with pytest.raises(NotImplementedError) as err:

        @key("id organization { id }")
        class User(ObjectType):
            id = ID()
            organization = Field(Organization)

    assert "Compound primary keys are not supported." == str(err.value)
