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
        other_agent = f.AgentFactory(curr_position_x=81, curr_position_y=46)
        agent = f.AgentFactory(curr_position_x=81, curr_position_y=45)

        maze = Maze("the_ville")
        nearby_tiles = maze.get_nearby_tiles(agent.curr_tile(), VISION_RADIUS)
        event = f.EventFactory(agent=other_agent)
        maze.add_event_from_tile(event, other_agent.curr_tile())
        perception = get_perceived_events(maze, nearby_tiles, agent)
        assert any([other_agent == event.agent for event in perception])
