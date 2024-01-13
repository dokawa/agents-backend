from django.db import models
from model_utils.models import TimeStampedModel
from pgvector.django import VectorField

from apps.agents.constants import VECTOR_DIMENSION
from apps.agents.models import Agent
from apps.simulations.models import Simulation
from apps.simulations.utils import EventType


class Event(TimeStampedModel):
    agent = models.ForeignKey(Agent, related_name="events", on_delete=models.CASCADE)
    interacting_with = models.ForeignKey(
        Agent, null=True, blank=True, on_delete=models.CASCADE
    )

    simulation = models.ForeignKey(
        Simulation, related_name="events", on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=10, choices=EventType.choices, null=True, blank=True
    )
    embedding = VectorField(dimensions=VECTOR_DIMENSION, null=True)

    position_x = models.PositiveIntegerField(null=True, blank=True, default=0)
    position_y = models.PositiveIntegerField(null=True, blank=True, default=0)

    sim_time_created = models.DateTimeField(null=True, blank=True)
    sim_time_expiration = models.DateTimeField(null=True, blank=True)
    sim_time_last_accessed = models.DateTimeField(null=True, blank=True)

    address = models.CharField(max_length=255, null=True, blank=True)
    visual_representation = models.CharField(max_length=15, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    poignancy = models.PositiveIntegerField(null=True, blank=True)

    subject = models.CharField(max_length=255, null=True, blank=True)
    predicate = models.CharField(max_length=255, null=True, blank=True)
    object = models.CharField(max_length=255, null=True, blank=True)

    def spo_summary(self):
        return (self.subject, self.predicate, self.object)

    def __repr__(self):
        return f"{self.address}"
