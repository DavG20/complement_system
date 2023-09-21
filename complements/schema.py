import graphene
from graphene_django.types import DjangoObjectType
from graphene import InputObjectType
from graphene import Mutation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from graphql_jwt.decorators import superuser_required


from complements.models import Complement


class ComplementType(DjangoObjectType):
    class Meta:
        model = Complement


class ComplementInputType(InputObjectType):
    content = graphene.String()
    status = graphene.String()


class ComplementUpdateInputTypeByUser(InputObjectType):
    content = graphene.String()


class ComplementUpdateInputTypeByAdmin(InputObjectType):
    status = graphene.String()


class CreateComplement(Mutation):
    class Arguments:
        input_data = ComplementInputType()

    complement = graphene.Field(ComplementType)

    def mutate(self, info, input_data):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to create a complement.")

        complement = Complement(user=user, **input_data)
        complement.save()
        return CreateComplement(complement=complement)


class UpdateComplementByUser(Mutation):
    class Arguments:
        complement_id = graphene.Int()
        input_data = ComplementUpdateInputTypeByUser()

    complement = graphene.Field(ComplementType)

    @login_required
    def mutate(self, info, complement_id, input_data):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to update a complement.")

        try:
            complement = Complement.objects.get(id=complement_id, user=user)
        except Complement.DoesNotExist:
            raise Exception("Complement not found.")

        for attr, value in input_data.items():
            setattr(complement, attr, value)

        complement.save()
        return UpdateComplementByUser(complement=complement)


class UpdateComplementByAdmin(Mutation):
    class Arguments:
        complement_id = graphene.Int()
        input_data = ComplementUpdateInputTypeByAdmin()

    complement = graphene.Field(ComplementType)

    @login_required
    @superuser_required
    def mutate(self, info, complement_id, input_data):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to update a complement.")

        try:
            complement = Complement.objects.get(id=complement_id, user=user)
        except Complement.DoesNotExist:
            raise Exception("Complement not found.")

        for attr, value in input_data.items():
            setattr(complement, attr, value)

        complement.save()
        return UpdateComplementByAdmin(complement=complement)


class DeleteComplement(Mutation):
    class Arguments:
        complement_id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, complement_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to delete a complement.")

        try:
            complement = Complement.objects.get(id=complement_id, user=user)
            complement.delete()
            return DeleteComplement(success=True)
        except Complement.DoesNotExist:
            raise Exception("Complement not found.")


class Query(graphene.ObjectType):
    complements = graphene.List(ComplementType)

    @superuser_required
    def resolve_complements(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to view complements.")
        return Complement.objects.all()

    complements_by_user = graphene.List(ComplementType)

    def resolve_complements_by_user(self, info):
        user = info.context.user
        if user:
            return Complement.objects.filter(user=user)


class Mutation(graphene.ObjectType):
    create_complement = CreateComplement.Field()
    update_complementbyuser = UpdateComplementByUser.Field()
    update_complementbyadmin = UpdateComplementByAdmin.Field()
    delete_complement = DeleteComplement.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
