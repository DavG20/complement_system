import graphene
from app_user.schema import Query as AppUserQuery, Mutation as AppUserMutation
from complaints.schema import Query as ComplaintQuery, Mutation as ComplaintMutation


class Query(AppUserQuery, ComplaintQuery, graphene.ObjectType):
    pass


class Mutation(AppUserMutation, ComplaintMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
