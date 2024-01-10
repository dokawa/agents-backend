import unittest

import pytest

import tests.factories as f
from apps.agents.agent.perceive import get_perceived_events
from apps.agents.constants import VISION_RADIUS
from apps.simulations.maze import Maze

pytestmark = pytest.mark.django_db


class TestPerceive(unittest.TestCase):
    def test_nearby_tiles(self):
        maze = Maze("the_ville")

        agent = f.AgentFactory(curr_position_x=68, curr_position_y=58)
        nearby_tiles = maze.get_nearby_tiles(agent.curr_tile(), VISION_RADIUS)
        assert nearby_tiles

    def test_perceived_events(self):
        maze = Maze("the_ville")

        f.AgentFactory(curr_position_x=81, curr_position_y=46)

        agent = f.AgentFactory(curr_position_x=81, curr_position_y=45)

        nearby_tiles = maze.get_nearby_tiles(agent.curr_tile(), VISION_RADIUS)

        simulation = f.SimulationFactory(agents=[agent])
        maze.add_simulation_events(simulation)
        perception = get_perceived_events(maze, nearby_tiles, agent)
        assert any([agent.name == p[1][0] for p in perception if p[1]])
