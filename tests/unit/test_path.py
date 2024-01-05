import unittest

from apps.agents.constants import COLLISION_BLOCK_ID
from apps.agents.path.path_finder import get_path
from apps.simulations.maze import Maze


class TestAStar(unittest.TestCase):
    def test_return_path_for_same_place(self):
        # noqa
        maze = [
            # 0    1    2    3    4    5    6    7    8    9    10   11   12
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # 0
            [" ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],  # 1
            ["#", " ", "#", " ", " ", "#", "#", " ", " ", " ", "#", " ", "#"],  # 2
            ["#", " ", "#", " ", " ", "#", "#", " ", "#", " ", "#", " ", "#"],  # 3
            ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],  # 4
            ["#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#"],  # 5
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " "],  # 6
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # 7
        ]
        # noqa
        path = get_path(maze, [0, 1], [0, 1], "#")

        assert path == [(0, 1)]

    def test_return_path_straight_line(self):
        # noqa
        maze = [
            # 0    1    2    3    4    5    6    7    8    9    10   11   12
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # 0
            [" ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],  # 1
            ["#", " ", "#", " ", " ", "#", "#", " ", " ", " ", "#", " ", "#"],  # 2
            ["#", " ", "#", " ", " ", "#", "#", " ", "#", " ", "#", " ", "#"],  # 3
            ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],  # 4
            ["#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#"],  # 5
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " "],  # 6
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # 7
        ]
        # noqa
        path = get_path(maze, [3, 1], [7, 1], "#")

        assert path == [(3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

    def test_return_path_u_turn(self):
        # noqa
        maze = [
            # 0    1    2    3    4    5    6    7    8    9    10   11   12
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # 0
            [" ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],  # 1
            ["#", " ", "#", " ", " ", "#", "#", " ", " ", " ", "#", " ", "#"],  # 2
            ["#", " ", "#", " ", " ", "#", "#", " ", "#", " ", "#", " ", "#"],  # 3
            ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],  # 4
            ["#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#"],  # 5
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " "],  # 6
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # 7
        ]
        # noqa
        path = get_path(maze, [2, 4], [2, 6], "#")

        assert path == [(2, 4), (3, 4), (3, 5), (3, 6), (2, 6)]

    def test_maze_path(self):
        # noqa
        maze = Maze("the_ville")
        # noqa
        path = get_path(maze.collision_maze, [2, 4], [2, 6], COLLISION_BLOCK_ID)

        assert path == [(2, 4), (2, 5), (2, 6)]

    def test_return_longer_path(self):
        # noqa
        maze = [
            # 0    1    2    3    4    5    6    7    8    9    10   11   12
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # 0
            [" ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],  # 1
            ["#", " ", "#", " ", " ", "#", "#", " ", " ", " ", "#", " ", "#"],  # 2
            ["#", " ", "#", " ", " ", "#", "#", " ", "#", " ", "#", " ", "#"],  # 3
            ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],  # 4
            ["#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#"],  # 5
            ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " "],  # 6
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],  # 7
        ]
        # noqa
        path = get_path(maze, [0, 1], [12, 6], "#")

        assert path == [
            (0, 1),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 4),
            (3, 4),
            (4, 4),
            (5, 4),
            (5, 5),
            (5, 6),
            (6, 6),
            (7, 6),
            (8, 6),
            (9, 6),
            (9, 5),
            (9, 4),
            (10, 4),
            (11, 4),
            (11, 5),
            (11, 6),
            (12, 6),
        ]

    def test_maze_long_path(self):
        # noqa
        maze = Maze("the_ville")
        # noqa
        start = (68, 58)
        end = (80, 19)

        assert maze.collision_maze[start[1]][start[0]] != COLLISION_BLOCK_ID
        assert maze.collision_maze[end[1]][end[0]] != COLLISION_BLOCK_ID
        path = get_path(maze.collision_maze, start, end, COLLISION_BLOCK_ID)

        assert path[0] == start
        assert path[-1] == end
        assert all(  # the path differs by just one in either x or y
            abs(a - c) + abs(b - d) == 1 for (a, b), (c, d) in zip(path, path[1:])
        )

    def test_return_none_if_start_or_end_is_collision(self):
        maze = Maze("the_ville")

        collision = (50, 70)
        not_collision = (68, 58)

        path = get_path(
            maze.collision_maze, collision, not_collision, COLLISION_BLOCK_ID
        )
        assert not path
        path = get_path(
            maze.collision_maze, not_collision, collision, COLLISION_BLOCK_ID
        )
        assert not path
