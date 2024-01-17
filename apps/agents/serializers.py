from rest_framework import serializers

from .models import ActionPlan, Agent


class ActionPlanReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionPlan
        fields = ("description",)


class AgentSerializer(serializers.ModelSerializer):
    plan = ActionPlanReadSerializer()

    class Meta:
        model = Agent
        fields = ("id", "name", "sprite_name", "curr_tile", "plan")
