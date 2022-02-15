import pytest
from graphene import ObjectType, ID, String
from ..extend import extend


def test_extend_non_existing_field_failure():
    """
    Test that using the key decorator and providing a field that does not exist fails.
    """
    with pytest.raises(AssertionError) as err:

        @extend("potato")
        class A(ObjectType):
            id = ID()

    assert 'Field "potato" does not exist on type "A"' == str(err.value)


def test_multiple_extend_failure():
    """
    Test that the extend decorator can't be used more than once on a type.
    """
    with pytest.raises(AssertionError) as err:

        @extend("id")
        @extend("potato")
        class A(ObjectType):
            id = ID()
            potato = String()

    assert "Can't extend type which is already extended or has @key" == str(err.value)
