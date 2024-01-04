from rest_framework import viewsets
from .models import Agent
from .serializers import AgentSerializer
from rest_framework import mixins

class AgentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

