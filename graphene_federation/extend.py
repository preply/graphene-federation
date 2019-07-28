extended_types = {}


def register_extend_type(typename, Type):
    extended_types[typename] = Type


def extend(fields: str):
    def decorator(Type):
        register_extend_type(Type.__name__, Type)
        setattr(Type, '_sdl', '@key(fields: "%s")' % fields)
        return Type
    return decorator


def external(field):
    field._external = True
    return field
