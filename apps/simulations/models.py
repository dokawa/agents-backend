from datetime import datetime

from django.db import models
from model_utils.models import TimeStampedModel

from apps.agents.constants import INITIAL_DATE, SECONDS_PER_STEP


class Simulation(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    step = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{ self.id } | {self.name}"

    def current_time(self):
        return INITIAL_DATE + datetime.timedelta(seconds=self.step * SECONDS_PER_STEP)
