provides_parent_types = []


def register_provides_parent_type(typename, Type):
    provides_parent_types[typename] = Type


def provides(field, fields: str, parent_type: callable):
    field._provides = fields
    provides_parent_types.append(parent_type)
    return field
