from rest_framework import mixins, viewsets

from .models import Agent
from .serializers import AgentSerializer


class AgentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
