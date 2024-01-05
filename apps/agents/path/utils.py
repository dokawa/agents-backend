import random

from apps.agents.constants import COLLISION_BLOCK_ID
from apps.agents.path.path_finder import get_path


def sample_tiles(target_tiles):
    # There are sometimes more than one tile returned from this (e.g., a table
    # may stretch many coordinates). So, we sample a few here. And from that
    # random sample, we will take the closest ones.
    if len(target_tiles) < 4:
        target_tiles = random.sample(list(target_tiles), len(target_tiles))
    else:
        target_tiles = random.sample(list(target_tiles), 4)
    return target_tiles


def solve_target_tile_conflicts(persona, maze, agents, target_tiles):
    # If possible, we want personas to occupy different tiles when they are
    # headed to the same location on the maze. It is ok if they end up on the
    # same time, but we try to lower that probability.
    # We take care of that overlap here.
    persona_name_set = {a.name for a in agents}
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
    return target_tiles


def get_shortest_path(persona, maze, target_tiles):
    # Now that we've identified the target tile, we find the shortest path to
    # one of the target tiles.

    curr_tile = (persona.curr_position_x, persona.curr_position_y)
    collision_maze = maze.collision_maze
    closest_target_tile = None
    path = None
    for tile in target_tiles[1:3]:
        # get_path takes a collision_mze and the curr_tile coordinate as
        # an input, and returns a list of coordinate tuples that becomes the
        # path.
        # e.g., [(0, 1), (1, 1), (1, 2), (1, 3), (1, 4)...]

        import time

        start_time = time.time()

        curr_path = get_path(collision_maze, curr_tile, tile, COLLISION_BLOCK_ID)

        end_time = time.time()

        # Calculate elapsed time
        elapsed_time = end_time - start_time
        print(f"start: {curr_tile} | end: {tile} | time: {elapsed_time}")

        if curr_path:
            if not closest_target_tile:
                closest_target_tile = tile
                path = curr_path
            elif len(curr_path) < len(path):
                closest_target_tile = tile
                path = curr_path
    return path
