from datetime import timedelta

from django.db import models
from django.db.models import JSONField
from model_utils.models import TimeStampedModel

from apps.agents.agent.classes import ActionPlanType
from apps.agents.agent.execute import execute
from apps.agents.agent.perceive import perceive
from apps.agents.agent.plan import plan
from apps.agents.agent.select import select
from apps.agents.constants import CHAT_COOLDOWN_IN_MINUTES
from apps.simulations.models import Simulation
from apps.simulations.utils import EventType


class Agent(TimeStampedModel):
    class Meta:
        unique_together = ("name", "sprite_name")

    name = models.CharField(max_length=50, unique=False)
    simulation = models.ForeignKey(
        Simulation,
        related_name="agents",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    sprite_name = models.CharField(max_length=50, unique=False)

    # These are denormalization
    curr_position_x = models.PositiveIntegerField(null=True, blank=True, default=0)
    curr_position_y = models.PositiveIntegerField(null=True, blank=True, default=0)

    plan = models.OneToOneField(
        "ActionPlan",
        null=True,
        blank=True,
        related_name="agent",
        on_delete=models.SET_NULL,
    )

    # This makes chatting_with relationship bidirectional
    # def save(self, *args, **kwargs):
    #     super(Agent, self).save(*args, **kwargs)
    #     if self.chatting_with:
    #         self.chatting_with.chatting_with = self

    def execute_step(self, simulation, maze):
        # """
        # This is the main cognitive function where our main sequence is called.
        #

        # # Updating persona's scratch memory with <curr_tile>.
        # self.scratch.curr_tile = curr_tile
        #
        # # We figure out whether the persona started a new day, and if it is a new
        # # day, whether it is the very first day of the simulations. This is
        # # important because we set up the persona's long term plan at the start of
        # # a new day.
        # new_day = False
        # if not self.scratch.curr_time:
        #     new_day = "First day"
        # elif (self.scratch.curr_time.strftime('%A %B %d')
        #       != curr_time.strftime('%A %B %d')):
        #     new_day = "New day"
        # self.scratch.curr_time = curr_time
        #
        # # Main cognitive sequence begins here.
        agents = simulation.agents.all()
        perceived = perceive(self, maze)
        selected = select(self, perceived, simulation.current_time())
        # retrieved = retrieve(self, simulation, selected)
        planned = plan(self, simulation, maze, None, selected)

        # # self.reflect()

        # # <execution> return the next_tile:
        # # <next_tile> is a x,y coordinate. e.g., (58, 9)
        # # <pronunciatio> is an emoji. e.g., "\ud83d\udca4"
        # # <description> is a string description of the movement. e.g.,
        # #   writing her next novel (editing her novel)
        # #   @ double studio:double studio:common room:sofa

        # plan = "the Ville:Giorgio Rossi's apartment:main room"
        return execute(self, maze, agents, planned)

    def update_position(self, x, y):
        self.curr_position_x = x
        self.curr_position_y = y
        self.save()

    def __str__(self):
        return f"{self.name} | ({self.curr_position_x}, {self.curr_position_y})"

    def curr_tile(self):
        return (self.curr_position_x, self.curr_position_y)

    def is_chatting(self):
        return self.last_event() and self.last_event().type == EventType.CHAT

    def get_interacting_with(self):
        last_event = self.last_event()
        if last_event:
            return last_event.interact_with

    def last_event(self):
        last_event = self.events.all().order_by("sim_time_created").last()
        return last_event

    def chatted_recently(self, other_agent, curr_time):
        last_event = self.last_event()
        if (
            last_event
            and last_event.interact_with == other_agent
            and last_event.sim_time_created - curr_time
            < timedelta(minutes=CHAT_COOLDOWN_IN_MINUTES)
        ):
            return True

        return False


class ActionPlan(models.Model):
    type = models.CharField(
        max_length=32, choices=ActionPlanType.choices, null=True, blank=True
    )
    simulation = models.ForeignKey(
        Simulation,
        related_name="action_plans",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)  # duration in seconds
    description = models.TextField(null=True, blank=True)
    pronunciatio = models.TextField(null=True, blank=True)

    chat = models.TextField(null=True, blank=True)

    interact_with = models.ForeignKey(
        Agent, null=True, blank=True, on_delete=models.CASCADE
    )
    planned_path = JSONField(null=True, blank=True, default=list)

    def advance_in_path(self):
        if self.planned_path:
            self.planned_path = self.planned_path[1:]
            self.save()

    def __str__(self):
        return f"{self.description}"

    def __repr__(self):
        return self.__str__()
