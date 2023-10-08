import graphene

import app_user.schema
import complaints.schema 
import complaints.schema_relay



class Query(app_user.schema.Query, complaints.schema.Query,complaints.schema_relay.RelayQuery, graphene.ObjectType):
    pass


class Mutation(app_user.schema.Mutation, complaints.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
