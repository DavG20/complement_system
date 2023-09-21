import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import authenticate, login, logout
from .models import AppUser
from complements.schema import schema


class AppUserType(DjangoObjectType):
    class Meta:
        model = AppUser


class RegisterUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()

    user = graphene.Field(AppUserType)
    token = graphene.String()

    def mutate(self, info, email, password, first_name=None, last_name=None):
        # Create a new user with the provided information
        user = AppUser.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name
        )
        # Authenticate the user
        user = authenticate(username=email, password=password)
        if user:
            # Login the user and generate a token
            login(info.context, user)
            token = get_token(user)
            return RegisterUser(user=user, token=token)
        else:
            raise Exception("User creation failed")


class LoginUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(AppUserType)
    token = graphene.String()

    def mutate(self, info, email, password):
        user = authenticate(username=email, password=password)
        if user:
            # No need to call 'login' here; 'graphql_jwt' handles token generation.
            token = get_token(user)
            return LoginUser(user=user, token=token)
        else:
            raise Exception("Invalid credentials")


class LogoutUser(graphene.Mutation):
    success = graphene.Boolean()

    @login_required
    def mutate(self, info):
        user = info.context.user
        if user.is_authenticated:
            # Invalidate the JWT token
            info.context.token = None
            return LogoutUser(success=True)
        else:
            raise Exception("User not authenticated")


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    
