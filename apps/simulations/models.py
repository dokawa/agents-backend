from django.db import models
from model_utils.models import TimeStampedModel

from apps.agents.models import Agent


class Simulation(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{ self.id } | {self.name}"


class Event(TimeStampedModel):
    simulation = models.ForeignKey(
        Simulation, related_name="event", on_delete=models.CASCADE
    )
    agent = models.ForeignKey(Agent, related_name="agent", on_delete=models.PROTECT)
    step = models.PositiveIntegerField(default=0)
