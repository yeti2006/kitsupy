def return_if_error(
    errors=(
        KeyError,
        TypeError,
    ),
    default_value=None,
):
    def decorator(func):
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                return default_value

        return new_func

    return decorator


# def _decorate_class_with_decorator(decorater):
#     def decorate(cls):
#         for attr in cls.__dict__:
#             if callable(getattr(cls, attr)):
#                 if not attr.startswith("_"):
#                     setattr(cls, attr, decorater(getattr(cls, attr)))

#         return cls

#     return decorate
