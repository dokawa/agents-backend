from django.db import models
from model_utils.models import TimeStampedModel

from apps.agents.agent.perceive import perceive
from apps.agents.agent.retrieve import retrieve
from apps.agents.agent.select import select
from apps.agents.path.utils import get_shortest_path, sample_tiles
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

    class Meta:
        unique_together = ("name", "sprite_name")

    def __str__(self):
        return f"{self.name} | ({self.curr_position_x}, {self.curr_position_y})"

    def curr_tile(self):
        return (self.curr_position_x, self.curr_position_y)

    def get_last_event(self):
        last_event = self.events.all().order_by("created").last()
        return last_event

    def step(self, simulation, maze, curr_tile, curr_time):
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
        retrieved = retrieve(self, simulation, selected)
        # plan = self.plan(maze, agents, new_day, retrieved)
        # # self.reflect()
        #
        # # <execution> is a triple set that contains the following components:
        # # <next_tile> is a x,y coordinate. e.g., (58, 9)
        # # <pronunciatio> is an emoji. e.g., "\ud83d\udca4"
        # # <description> is a string description of the movement. e.g.,
        # #   writing her next novel (editing her novel)
        # #   @ double studio:double studio:common room:sofa

        plan = "the Ville:Giorgio Rossi's apartment:main room"
        return self.execute(maze, agents, plan)

    def execute(self, maze, personas, plan):
        """
        Given a plan (action's string address), we execute the plan (actually
        outputs the tile coordinate path and the next coordinate for the
        persona).

        INPUT:
          persona: Current <Persona> instance.
          maze: An instance of current <Maze>.
          personas: A dictionary of all personas in the world.
          plan: This is a string address of the action we need to execute.
             It comes in the form of "{world}:{sector}:{arena}:{game_objects}".
             It is important that you access this without doing negative
             indexing (e.g., [-1]) because the latter address elements may not be
             present in some cases.
             e.g., "dolores double studio:double studio:bedroom 1:bed"

        OUTPUT:
          execution
        """
        # if "<random>" in plan and persona.scratch.planned_path == []:
        #     persona.scratch.act_path_set = False

        # <act_path_set> is set to True if the path is set for the current action.
        # It is False otherwise, and means we need to construct a new path.
        # if not persona.scratch.act_path_set:
        #     # <target_tiles> is a list of tile coordinates where the persona may go
        #     # to execute the current action. The goal is to pick one of them.
        #     target_tiles = None
        #
        #     print('aldhfoaf/????')
        #     print(plan)
        #
        #     if "<persona>" in plan:
        #         # Executing persona-persona interaction.
        #         target_p_tile = (personas[plan.split("<persona>")[-1].strip()]
        #                          .scratch.curr_tile)
        #         potential_path = get_path(maze.collision_maze,
        #                                      [persona.curr_position_x, persona.curr_position_y],
        #                                      target_p_tile,
        #                                      COLLISION_BLOCK_ID)
        #         if len(potential_path) <= 2:
        #             target_tiles = [potential_path[0]]
        #         else:
        #             potential_1 = get_path(maze.collision_maze,
        #                                       [persona.curr_position_x, persona.curr_position_y],
        #                                       potential_path[int(len(potential_path) / 2)],
        #                                       COLLISION_BLOCK_ID)
        #             potential_2 = get_path(maze.collision_maze,
        #                                       [persona.curr_position_x, persona.curr_position_y],
        #                                       potential_path[int(len(potential_path) / 2) + 1],
        #                                       COLLISION_BLOCK_ID)
        #             if len(potential_1) <= len(potential_2):
        #                 target_tiles = [potential_path[int(len(potential_path) / 2)]]
        #             else:
        #                 target_tiles = [potential_path[int(len(potential_path) / 2 + 1)]]

        # elif "<waiting>" in plan:
        #     # Executing interaction where the persona has decided to wait before
        #     # executing their action.
        #     x = int(plan.split()[1])
        #     y = int(plan.split()[2])
        #     target_tiles = [[x, y]]
        #
        # elif "<random>" in plan:
        #     # Executing a random location action.
        #     plan = ":".join(plan.split(":")[:-1])
        #     target_tiles = maze.address_tiles[plan]
        #     target_tiles = random.sample(list(target_tiles), 1)

        # else:
        # This is our default execution. We simply take the persona to the
        # location where the current action is taking place.
        # Retrieve the target addresses. Again, plan is an action address in its
        # string form. <maze.address_tiles> takes this and returns candidate
        # coordinates.

        if plan in maze.address_tiles:
            target_tiles = maze.address_tiles[plan]
        else:
            maze.address_tiles["Johnson Park:park:park garden"]  # ERRORRRRRRR

        target_tiles = sample_tiles(target_tiles)

        # solve_target_tile_conflicts(self, maze, personas, target_tiles)

        # Setting up the next immediate step. We stay at our curr_tile if there is
        # no <planned_path> left, but otherwise, we go to the next tile in the path.
        # ret = [self.curr_position_x, self.curr_position_y]
        # if self.scratch.planned_path:
        #     ret = self.scratch.planned_path[0]
        #     self.scratch.planned_path = self.scratch.planned_path[1:]
        #
        # description = f"{self.scratch.act_description}"
        # description += f" @ {self.scratch.act_address}"
        #
        # execution = ret, self.scratch.act_pronunciatio, description

        path = get_shortest_path(self, maze, target_tiles)

        # # Actually setting the <planned_path> and <act_path_set>. We cut the
        # # first element in the planned_path because it includes the curr_tile.
        # persona.scratch.planned_path = path[1:]
        # persona.scratch.act_path_set = True

        return path
