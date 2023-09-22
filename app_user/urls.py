from django.urls import path
from graphene_django.views import GraphQLView


urlpatterns = [
    path("graphql/app_users/", GraphQLView.as_view(graphiql=True)),
]
