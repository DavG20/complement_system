import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from django.contrib.auth import authenticate
from .models import profile


from django.contrib.auth import get_user_model

# from complements.schema import schema


class AppUserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Profile(DjangoObjectType):
    class Meta:
        model = profile


class RegisterUser(graphene.Mutation):
    user = graphene.Field(AppUserType)
    profile = graphene.Field(Profile)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        role = graphene.String(required=False)

    def mutate(self, info, username, password, email, role=None):
        user = get_user_model()(
            username=username,
            email=email,
            is_staff=True,
        )
        user.set_password(password)
        user.save()

        profile_obj = profile.objects.get(user=user.id)
        token = get_token(user)

        return RegisterUser(
            user=user,
            profile=profile_obj,
            token=token,
        )


class LoginUser(graphene.Mutation):
    user = graphene.Field(AppUserType)
    profile = graphene.Field(Profile)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)

        if user is None:
            raise Exception("Invalid credentials")

        profile_obj = profile.objects.get(user=user)
        token = get_token(user)

        return LoginUser(
            user=user,
            profile=profile_obj,
            token=token,
        )


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


class Query(graphene.ObjectType):
    whoami = graphene.Field(AppUserType)
    users = graphene.List(AppUserType)

    def resolve_whoami(self, info):
        user = info.context.user
        # Check to to ensure you're signed-in to see yourself
        if user.is_anonymous:
            raise Exception("Authentication Failure: Your must be signed in")
        return user

    def resolve_users(self, info):
        user = info.context.user
        print(user)
        # Check to ensure user is a 'manager' to see all users
        if user.is_anonymous:
            raise Exception("Authentication Failure: Your must be signed in")
        if user.profile.role != "manager":
            raise Exception("Authentication Failure: Must be Manager")
        return get_user_model().objects.all()


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
