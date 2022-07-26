from graphene import Int, String

from graphene_federation.extend import external, requires


def test_external():
    field = external(Int(required=True))
    assert field._external is True


def test_requires():
    fields = 'primaryEmail'
    field = requires(String(), fields=fields)
    assert field._requires == fields
