def execute(agent, maze, personas, plan):
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

    # solve_target_tile_conflicts(self, maze, personas, target_tiles)

    # Setting up the next immediate step. We stay at our curr_tile if there is
    # no <planned_path> left, but otherwise, we go to the next tile in the path.
    # print(f"  execute | planned path: {plan.planned_path} {plan.description} ")
    if plan.planned_path:
        next_tile = plan.planned_path[0]
        plan.advance_in_path()
        agent.update_position(next_tile[0], next_tile[1])
        return next_tile

    # ret = [self.curr_position_x, self.curr_position_y]
    # if self.scratch.planned_path:
    #     ret = self.scratch.planned_path[0]
    #     self.scratch.planned_path = self.scratch.planned_path[1:]
    #
    # description = f"{self.scratch.act_description}"
    # description += f" @ {self.scratch.act_address}"
    #
    # execution = ret, self.scratch.act_pronunciatio, description

    # # Actually setting the <planned_path> and <act_path_set>. We cut the
    # # first element in the planned_path because it includes the curr_tile.
    # persona.scratch.planned_path = path[1:]
    # persona.scratch.act_path_set = True
