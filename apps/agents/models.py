from django.db import models
from model_utils.models import TimeStampedModel
from rest_framework.decorators import action


class Agent(TimeStampedModel):
    name = models.CharField(max_length=50, unique=False)
    sprite_name = models.CharField(max_length=50, unique=False)
    last_position_x = models.PositiveIntegerField(null=True, blank=True)
    last_position_y = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("name", "sprite_name")

    def __str__(self):
        return f"{self.name} | ({self.last_position_x}, {self.last_position_y})"


    def move(self, maze, personas, curr_tile, curr_time):
        # """
        # This is the main cognitive function where our main sequence is called.
        #
        # INPUT:
        #   maze: The Maze class of the current world.
        #   personas: A dictionary that contains all persona names as keys, and the
        #             Persona instance as values.
        #   curr_tile: A tuple that designates the persona's current tile location
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
        # # perceived = self.perceive(maze)
        # # retrieved = self.retrieve(perceived)
        # # plan = self.plan(maze, personas, new_day, retrieved)
        # # self.reflect()
        #
        # # <execution> is a triple set that contains the following components:
        # # <next_tile> is a x,y coordinate. e.g., (58, 9)
        # # <pronunciatio> is an emoji. e.g., "\ud83d\udca4"
        # # <description> is a string description of the movement. e.g.,
        # #   writing her next novel (editing her novel)
        # #   @ double studio:double studio:common room:sofa
        return self.execute(maze, personas, plan)

    def execute(persona, maze, personas, plan):
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
        if "<random>" in plan and persona.scratch.planned_path == []:
            persona.scratch.act_path_set = False

        # <act_path_set> is set to True if the path is set for the current action.
        # It is False otherwise, and means we need to construct a new path.
        if not persona.scratch.act_path_set:
            # <target_tiles> is a list of tile coordinates where the persona may go
            # to execute the current action. The goal is to pick one of them.
            target_tiles = None

            print('aldhfoaf/????')
            print(plan)

            if "<persona>" in plan:
                # Executing persona-persona interaction.
                target_p_tile = (personas[plan.split("<persona>")[-1].strip()]
                                 .scratch.curr_tile)
                potential_path = path_finder(maze.collision_maze,
                                             persona.scratch.curr_tile,
                                             target_p_tile,
                                             collision_block_id)
                if len(potential_path) <= 2:
                    target_tiles = [potential_path[0]]
                else:
                    potential_1 = path_finder(maze.collision_maze,
                                              persona.scratch.curr_tile,
                                              potential_path[int(len(potential_path) / 2)],
                                              collision_block_id)
                    potential_2 = path_finder(maze.collision_maze,
                                              persona.scratch.curr_tile,
                                              potential_path[int(len(potential_path) / 2) + 1],
                                              collision_block_id)
                    if len(potential_1) <= len(potential_2):
                        target_tiles = [potential_path[int(len(potential_path) / 2)]]
                    else:
                        target_tiles = [potential_path[int(len(potential_path) / 2 + 1)]]

            elif "<waiting>" in plan:
                # Executing interaction where the persona has decided to wait before
                # executing their action.
                x = int(plan.split()[1])
                y = int(plan.split()[2])
                target_tiles = [[x, y]]

            elif "<random>" in plan:
                # Executing a random location action.
                plan = ":".join(plan.split(":")[:-1])
                target_tiles = maze.address_tiles[plan]
                target_tiles = random.sample(list(target_tiles), 1)

            else:
                # This is our default execution. We simply take the persona to the
                # location where the current action is taking place.
                # Retrieve the target addresses. Again, plan is an action address in its
                # string form. <maze.address_tiles> takes this and returns candidate
                # coordinates.
                if plan not in maze.address_tiles:
                    maze.address_tiles["Johnson Park:park:park garden"]  # ERRORRRRRRR
                else:
                    target_tiles = maze.address_tiles[plan]

            # There are sometimes more than one tile returned from this (e.g., a tabe
            # may stretch many coordinates). So, we sample a few here. And from that
            # random sample, we will take the closest ones.
            if len(target_tiles) < 4:
                target_tiles = random.sample(list(target_tiles), len(target_tiles))
            else:
                target_tiles = random.sample(list(target_tiles), 4)
            # If possible, we want personas to occupy different tiles when they are
            # headed to the same location on the maze. It is ok if they end up on the
            # same time, but we try to lower that probability.
            # We take care of that overlap here.
            persona_name_set = set(personas.keys())
            new_target_tiles = []
            for i in target_tiles:
                curr_event_set = maze.access_tile(i)["events"]
                pass_curr_tile = False
                for j in curr_event_set:
                    if j[0] in persona_name_set:
                        pass_curr_tile = True
                if not pass_curr_tile:
                    new_target_tiles += [i]
            if len(new_target_tiles) == 0:
                new_target_tiles = target_tiles
            target_tiles = new_target_tiles

            # Now that we've identified the target tile, we find the shortest path to
            # one of the target tiles.
            curr_tile = persona.scratch.curr_tile
            collision_maze = maze.collision_maze
            closest_target_tile = None
            path = None
            for i in target_tiles:
                # path_finder takes a collision_mze and the curr_tile coordinate as
                # an input, and returns a list of coordinate tuples that becomes the
                # path.
                # e.g., [(0, 1), (1, 1), (1, 2), (1, 3), (1, 4)...]
                curr_path = path_finder(maze.collision_maze,
                                        curr_tile,
                                        i,
                                        collision_block_id)
                if not closest_target_tile:
                    closest_target_tile = i
                    path = curr_path
                elif len(curr_path) < len(path):
                    closest_target_tile = i
                    path = curr_path

            # Actually setting the <planned_path> and <act_path_set>. We cut the
            # first element in the planned_path because it includes the curr_tile.
            persona.scratch.planned_path = path[1:]
            persona.scratch.act_path_set = True

        # Setting up the next immediate step. We stay at our curr_tile if there is
        # no <planned_path> left, but otherwise, we go to the next tile in the path.
        ret = persona.scratch.curr_tile
        if persona.scratch.planned_path:
            ret = persona.scratch.planned_path[0]
            persona.scratch.planned_path = persona.scratch.planned_path[1:]

        description = f"{persona.scratch.act_description}"
        description += f" @ {persona.scratch.act_address}"

        execution = ret, persona.scratch.act_pronunciatio, description
        return execution