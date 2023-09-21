from functools import wraps
from graphql import GraphQLError


def admin_required():
    def decorator(func):
        @wraps(func)
        def wrapper(cls, root, info, *args, **kwargs):
            user = info.context.user

            if not user.is_superuser:
                raise GraphQLError(
                    "You are not an admin and not allowed to access this resource."
                )

            return func(cls, root, info, *args, **kwargs)

        return wrapper

    return decorator
