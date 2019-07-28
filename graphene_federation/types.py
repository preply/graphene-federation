from graphene import Scalar, String


class _Any(Scalar):
    '''Anything'''

    __typename = String(required=True)

    @staticmethod
    def serialize(dt):
        return dt

    @staticmethod
    def parse_literal(node):
        return node

    @staticmethod
    def parse_value(value):
        return value
