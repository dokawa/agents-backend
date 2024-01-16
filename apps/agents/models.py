from django.db import models
from django.db.models import JSONField
from model_utils.models import TimeStampedModel

from apps.agents.agent.classes import ActionPlanType
from apps.agents.agent.execute import execute
from apps.agents.agent.perceive import perceive
from apps.agents.agent.plan import plan
from apps.agents.agent.select import select
from apps.simulations.models import Simulation


class Agent(TimeStampedModel):
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

    chatting_with = models.OneToOneField(
        "Agent", null=True, blank=True, on_delete=models.SET_NULL
    )
    plan = models.OneToOneField(
        "ActionPlan",
        null=True,
        blank=True,
        related_name="agent",
        on_delete=models.SET_NULL,
    )

    class Meta:
        unique_together = ("name", "sprite_name")

    def __str__(self):
        return f"{self.name} | ({self.curr_position_x}, {self.curr_position_y})"

    def curr_tile(self):
        return (self.curr_position_x, self.curr_position_y)

    def get_last_event(self):
        last_event = self.events.all().order_by("created").last()
        return last_event

    def execute_step(self, simulation, maze, curr_tile, curr_time):
        # """
        # This is the main cognitive function where our main sequence is called.
        #
        # INPUT:
        #   maze: The Maze class of the current world.
        #   personas: A dictionary that contains all agent instances
        #   curr_tile: A tuple that designates the agent's current tile location
        #              in (row, col) form. e.g., (58, 39)
        #   curr_time: datetime instance that indicates the game's current time.
        # OUTPUT:
        #   execution: A triple set that contains the following components:
        #     <next_tile> is a x,y coordinate. e.g., (58, 9)
        #     <pronunciatio> is an emoji.
        #     <description> is a string description of the movement. e.g.,
        #     writing her next novel (editing her novel)
        #     @ double studio:double studio:common room:sofa
        # """
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
        selected = select(self, perceived)
        # retrieved = retrieve(self, simulation, selected)
        planned = plan(self, simulation, maze, None, selected)

        # # self.reflect()
        #
        # # <execution> is a triple set that contains the following components:
        # # <next_tile> is a x,y coordinate. e.g., (58, 9)
        # # <pronunciatio> is an emoji. e.g., "\ud83d\udca4"
        # # <description> is a string description of the movement. e.g.,
        # #   writing her next novel (editing her novel)
        # #   @ double studio:double studio:common room:sofa

        # plan = "the Ville:Giorgio Rossi's apartment:main room"
        return execute(self, maze, agents, planned)


class ActionPlan(models.Model):
    type = models.CharField(
        max_length=32, choices=ActionPlanType.choices, null=True, blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pronunciatio = models.TextField(null=True, blank=True)

    chat = models.TextField(null=True, blank=True)
    chatting_with_buffer = models.JSONField(null=True, blank=True, default=dict)
    chatting_end_time = models.DateTimeField(null=True, blank=True)

    planned_path = JSONField(null=True, blank=True, default=list)

    def advance_in_path(self):
        if self.planned_path:
            self.planned_path = self.planned_path[1:]
            self.save()

    def __str__(self):
        return f"{self.description}"

    def __repr__(self):
        return self.__str__()
