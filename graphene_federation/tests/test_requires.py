import pytest

from graphql import graphql

from graphene import Field, ID, Int, ObjectType, String

from .. import graphql_compatibility
from ..extend import extend, external, requires
from ..main import build_schema


def test_chain_requires_failure():
    """
    Check that we can't nest call the requires method on a field.
    """
    with pytest.raises(AssertionError) as err:

        @extend("id")
        class A(ObjectType):
            id = external(ID())
            something = requires(requires(String(), fields="id"), fields="id")

    assert "Can't chain `requires()` method calls on one field." == str(err.value)


def test_requires_multiple_fields():
    """
    Check that requires can take more than one field as input.
    """

    @extend("sku")
    class Product(ObjectType):
        sku = external(ID())
        size = external(Int())
        weight = external(Int())
        shipping_estimate = requires(String(), fields="size weight")

    class Query(ObjectType):
        product = Field(Product)

    schema = build_schema(query=Query)
    assert (
        graphql_compatibility.get_schema_str(schema)
        == """schema {
  query: Query
}

type Product {
  sku: ID
  size: Int
  weight: Int
  shippingEstimate: String
}

type Query {
  product: Product
  _entities(representations: [_Any]): [_Entity]
  _service: _Service
}

scalar _Any

union _Entity = Product

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
    result = graphql_compatibility.perform_graphql_query(schema, query)
    assert not result.errors
    assert (
        result.data["_service"]["sdl"].strip()
        == """
extend type Product  @key(fields: "sku") {
  sku: ID @external
  size: Int @external
  weight: Int @external
  shippingEstimate: String @requires(fields: "size weight")
}

type Query {
  product: Product
}
""".strip()
    )


def test_requires_multiple_fields_as_list():
    """
    Check that requires can take more than one field as input.
    """

    @extend("sku")
    class Product(ObjectType):
        sku = external(ID())
        size = external(Int())
        weight = external(Int())
        shipping_estimate = requires(String(), fields=["size", "weight"])

    class Query(ObjectType):
        product = Field(Product)

    schema = build_schema(query=Query)
    assert (
        graphql_compatibility.get_schema_str(schema)
        == """schema {
  query: Query
}

type Product {
  sku: ID
  size: Int
  weight: Int
  shippingEstimate: String
}

type Query {
  product: Product
  _entities(representations: [_Any]): [_Entity]
  _service: _Service
}

scalar _Any

union _Entity = Product

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
    result = graphql_compatibility.perform_graphql_query(schema, query)
    assert not result.errors
    assert (
        result.data["_service"]["sdl"].strip()
        == """
extend type Product  @key(fields: "sku") {
  sku: ID @external
  size: Int @external
  weight: Int @external
  shippingEstimate: String @requires(fields: "size weight")
}

type Query {
  product: Product
}
""".strip()
    )


def test_requires_with_input():
    """
    Test checking that the issue https://github.com/preply/graphene-federation/pull/47 is resolved.
    """

    @extend("id")
    class Acme(ObjectType):
        id = external(ID(required=True))
        age = external(Int())
        foo = requires(Field(String, someInput=String()), fields="age")

    class Query(ObjectType):
        acme = Field(Acme)

    schema = build_schema(query=Query)
    assert (
        graphql_compatibility.get_schema_str(schema)
        == """schema {
  query: Query
}

type Acme {
  id: ID!
  age: Int
  foo(someInput: String): String
}

type Query {
  acme: Acme
  _entities(representations: [_Any]): [_Entity]
  _service: _Service
}

scalar _Any

union _Entity = Acme

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
    result = graphql_compatibility.perform_graphql_query(schema, query)
    assert not result.errors
    assert (
        result.data["_service"]["sdl"].strip()
        == """
extend type Acme  @key(fields: "id") {
  id: ID! @external
  age: Int @external
  foo(someInput: String): String @requires(fields: "age")
}

type Query {
  acme: Acme
}
""".strip()
    )
