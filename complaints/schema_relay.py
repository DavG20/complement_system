
import django_filters
import graphene 
from  graphene_django.filter import DjangoFilterConnectionField

from graphene_django.types import DjangoObjectType
from .models import Complaint

class ComplaintFilter(django_filters.FilterSet):
    
    class Meta:
        model = Complaint 
        fields = ['status' , 'content']


class ComplaintNode(DjangoObjectType):
    class Meta:
        model = Complaint
        
        interfaces = (graphene.relay.Node, )

class RelayQuery(graphene.ObjectType):
    
    relay_complaint = graphene.relay.Node.Field(ComplaintNode)
    
    relay_complaints = DjangoFilterConnectionField(ComplaintNode, filterset_class=ComplaintFilter )
