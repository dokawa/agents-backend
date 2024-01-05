from rest_framework import serializers

from .models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ("id", "name", "sprite_name", "curr_tile")
