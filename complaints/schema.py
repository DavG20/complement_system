import graphene
from graphene_django.types import DjangoObjectType
from graphene import InputObjectType
from graphene import Mutation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from graphql_jwt.decorators import superuser_required


from complaints.models import Complaint


class ComplaintType(DjangoObjectType):
    class Meta:
        model = Complaint


class ComplaintInputType(InputObjectType):
    content = graphene.String()


class ComplaintUpdateInputTypeByUser(InputObjectType):
    content = graphene.String()


class ComplaintUpdateInputTypeByAdmin(InputObjectType):
    status = graphene.String()


class CreateComplaint(Mutation):
    class Arguments:
        input_data = ComplaintInputType()

    complaint = graphene.Field(ComplaintType)

    def mutate(self, info, input_data):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to create a complaint.")
        if user.is_superuser:
            raise Exception("admin can't create a complaint.")
        complaint = Complaint(user=user, **input_data)
        complaint.save()
        return CreateComplaint(complaint=complaint)


class UpdateComplaintByUser(Mutation):
    class Arguments:
        input_data = ComplaintUpdateInputTypeByUser()
        input_id = graphene.Int()

    complaint = graphene.Field(ComplaintType)

    def mutate(self, info, input_id, input_data):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to update a Complaint.")

        try:
            complaint = Complaint.objects.get(id=input_id, user=user)
        except Complaint.DoesNotExist:
            raise Exception("complaint not found.")
        complaint.content = input_data.content
        complaint.save()
        return UpdateComplaintByUser(complaint=complaint)


class UpdateComplaintByAdmin(Mutation):
    class Arguments:
        Complaint_id = graphene.Int()
        input_data = ComplaintUpdateInputTypeByAdmin()

    Complaint = graphene.Field(ComplaintType)

    @superuser_required
    def mutate(self, info, Complaint_id, input_data):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to update a Complaint.")

        try:
            Complaint = Complaint.objects.get(id=Complaint_id, user=user)
        except Complaint.DoesNotExist:
            raise Exception("Complaint not found.")

        for attr, value in input_data.items():
            setattr(Complaint, attr, value)

        Complaint.save()
        return UpdateComplaintByAdmin(Complaint=Complaint)


class DeleteComplaint(Mutation):
    class Arguments:
        Complaint_id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, Complaint_id):
        user = info.context.user
        complaint = None
        if user.is_anonymous:
            raise Exception("You must be logged in to delete a complaint.")

        try:
            complaint = Complaint.objects.get(id=Complaint_id, user=user)
            complaint.delete()
            return DeleteComplaint(success=True)
        except Complaint.DoesNotExist:
            raise Exception("Complaint not found.")


class Query(graphene.ObjectType):
    Complaints = graphene.List(ComplaintType)

    @superuser_required
    def resolve_Complaints(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to view Complaints.")
        return Complaint.objects.all()

    Complaints_by_user = graphene.List(ComplaintType)

    def resolve_Complaints_by_user(self, info):
        user = info.context.user
        if user:
            return Complaint.objects.filter(user=user)


class Mutation(graphene.ObjectType):
    create_Complaint = CreateComplaint.Field()
    update_Complaintbyuser = UpdateComplaintByUser.Field()
    update_Complaintbyadmin = UpdateComplaintByAdmin.Field()
    delete_Complaint = DeleteComplaint.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
