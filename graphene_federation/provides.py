from graphene import Field

provides_parent_types = set()


def provides(field, fields: str = None):
    """

    :param field: base type (when used as decorator) or field of base type
    :param fields:
    :return:
    """
    if fields is None:  # used as decorator on base type
        if isinstance(field, Field):
            raise RuntimeError("Please specify fields")
        provides_parent_types.add(field)
    else:  # used as wrapper over field
        field._provides = fields
    return field
