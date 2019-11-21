from .entity import register_entity
extended_types = {}


def register_extend_type(typename, Type):
    extended_types[typename] = Type


def extend(fields: str):
    def decorator(Type):
        if hasattr(Type, '_sdl'):
            raise RuntimeError("Can't extend type which is already extended or has @key")
        register_entity(Type.__name__, Type)
        register_extend_type(Type.__name__, Type)
        setattr(Type, '_sdl', '@key(fields: "%s")' % fields)
        return Type
    return decorator


def external(field):
    field._external = True
    return field


def requires(field, fields: str):
    field._requires = fields
    return field
