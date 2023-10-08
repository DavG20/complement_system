from complaints.schema import schema as complements_schema
from app_user.schema import schema as app_user_schema


class MultiSchemaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "/complaints/graphql/" in request.path:
            schema = complements_schema
        elif "/app_users/graphql/" in request.path:
            schema = app_user_schema
        else:
            schema = complements_schema  # Use a default schema

        # Set the schema on the request object
        request.graphene_schema = schema

        response = self.get_response(request)
        return response
