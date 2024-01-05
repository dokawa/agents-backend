"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: path_finder.py
Description: Implements various path finding functions for generative agents.
Some of the functions are defunct.
"""
import heapq
import random


def print_maze(maze):
    for row in maze:
        for item in row:
            print(item, end="")
        print()


def get_path(maze, start_tile, end_tile, collision_block_char, verbose=False):
    print(f"{start_tile} | {end_tile}")
    # Since we use tile as start and end
    # We have to invert since for a list of lists row => y and col => x
    start = (start_tile[1], start_tile[0])
    end = (end_tile[1], end_tile[0])

    path = path_finder_a_star(maze, start, end, collision_block_char, verbose)

    new_path = []
    if path:
        for i in path:
            new_path.append((i[1], i[0]))
        return new_path

    return None


def path_finder_a_star(maze, start, end, collision_block_value, verbose=False):
    class Node:
        def __init__(self, position, g, h, parent=None):
            self.position = position
            self.g = g
            self.h = h
            self.parent = parent

        def __lt__(self, other):
            return (self.g + self.h) < (other.g + other.h)

        def __repr__(self):
            return f"{self.position}"

    def heuristic(a, b):
        return (abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2) ** 0.5

    def return_path(current_node):
        path = []
        while current_node:
            # Since we input start and goal as tiles (x, y) and
            # the algorithm uses (row, col), we need to invert the path when returning
            path.append(current_node.position)
            current_node = current_node.parent
        return path[::-1]

    def a_star(grid, start, goal):
        if (
            grid[goal[0]][goal[1]] == collision_block_value
            or grid[start[0]][start[1]] == collision_block_value
        ):
            return None

        open_set = []
        closed_set = set()

        start_node = Node(start, 0, heuristic(start, goal))
        heapq.heappush(open_set, start_node)

        while open_set:
            # print(f"{len(open_set)} {len(closed_set)}")
            current_node = heapq.heappop(open_set)

            if current_node.position == goal:
                return return_path(current_node)

            closed_set.add(current_node.position)

            for neighbor_pos in neighbors(current_node.position, grid):
                if neighbor_pos in closed_set:
                    continue

                g = current_node.g + 1
                h = heuristic(neighbor_pos, goal)

                if any(node.position == neighbor_pos for node in open_set):
                    # Update the existing node in open_set if the new g value is lower
                    existing_node = next(
                        node for node in open_set if node.position == neighbor_pos
                    )
                    if g < existing_node.g:
                        existing_node.g = g
                        existing_node.parent = current_node
                else:
                    neighbor_node = Node(neighbor_pos, g, h, current_node)
                    heapq.heappush(open_set, neighbor_node)

        return None  # If no path is found

    def neighbors(position, grid):
        row, col = position

        if grid[row][col] == 32125:
            print(f"{type(grid[row][col])} {grid[row][col]}")
        if grid[row][col] == "32125":
            print(f"{type(grid[row][col])} {grid[row][col]}")

        neighbors_list = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        random.shuffle(neighbors_list)
        return [
            (row, col)
            for (row, col) in neighbors_list
            if 0 <= row < len(grid)
            and 0 <= col < len(grid[0])
            and grid[row][col] != collision_block_value
        ]

    return a_star(maze, start, end)
