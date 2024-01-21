import unittest

from apps.agents.constants import COLLISION_BLOCK_ID
from apps.simulations.maze import Maze


class TestMaze(unittest.TestCase):
    def test_maze_collision_format(self):
        maze = Maze("the_ville")
        collision_maze = maze.collision_maze
        assert any(COLLISION_BLOCK_ID in s for s in collision_maze)

    def test_maze(self):
        maze = Maze("the_ville")
        # Assert that the function returns the expected result
        # self.assertEqual(maze.address_tiles, "the Ville:Giorgio Rossi's apartment")

        address = maze.address_tiles["the Ville:Giorgio Rossi's apartment:main room"]
        assert (86, 17) in address
        assert (86, 18) in address
        assert (87, 17) in address
        assert (87, 18) in address

    def test_include_nearby_tiles(self):
        maze = Maze("the_ville")

        tile = (68, 58)
        near = maze.get_nearby_tiles(tile, 1, False)
        assert near
        assert tile not in near
        near = maze.get_nearby_tiles(tile, 1)
        assert tile in near

    def test_target_tiles(self):
        maze = Maze("the_ville")
        plan = "the Ville:Giorgio Rossi's apartment:main room"
        target_tiles = maze.address_tiles[plan]

        assert target_tiles == {
            (90, 24),
            (86, 20),
            (87, 19),
            (86, 17),
            (86, 23),
            (87, 25),
            (87, 22),
            (89, 19),
            (89, 25),
            (89, 22),
            (88, 20),
            (88, 17),
            (88, 23),
            (90, 20),
            (90, 17),
            (90, 23),
            (87, 18),
            (86, 22),
            (87, 21),
            (89, 18),
            (86, 19),
            (86, 25),
            (87, 24),
            (89, 21),
            (89, 24),
            (88, 19),
            (88, 25),
            (90, 22),
            (88, 22),
            (90, 19),
            (90, 25),
            (87, 20),
            (86, 18),
            (87, 17),
            (87, 23),
            (89, 20),
            (86, 21),
            (89, 17),
            (89, 23),
            (86, 24),
            (88, 18),
            (88, 21),
            (90, 18),
            (88, 24),
            (90, 21),
        }

    # @patch("sys.stdout", new_callable=StringIO)
    # def test_print_message(self, mock_stdout):
    #     maze = Maze("the_ville")
    #
    #     maze.print_collision()
    #     printed_output = mock_stdout.getvalue().strip()
    #     self.assertIn(" ".join(maze.collision_maze[0]), printed_output)
