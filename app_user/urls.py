from django.urls import path
from graphene_django.views import GraphQLView

from app_user.schema import schema


urlpatterns = [
    path("graphql/app_users/", GraphQLView.as_view(graphiql=True, schema=schema)),
]
