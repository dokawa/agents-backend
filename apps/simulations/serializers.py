from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from ..agents.models import Agent
from .event_models import Event
from .models import Simulation


class EventSerializer(serializers.ModelSerializer):
    agent = PrimaryKeyRelatedField(queryset=Agent.objects.all(), write_only=True)
    simulation = PrimaryKeyRelatedField(
        queryset=Simulation.objects.all(), write_only=True
    )
    type = serializers.CharField()

    class Meta:
        model = Event
        fields = ["agent", "type", "simulation", "position_x", "position_y"]
