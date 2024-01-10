from django.db import models
from model_utils.models import TimeStampedModel


class Simulation(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{ self.id } | {self.name}"
