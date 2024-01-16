import unittest

import pytest

import tests.factories as f
from apps.agents.agent.perceive import get_perceived_events
from apps.agents.agent.plan import plan
from apps.agents.constants import VISION_RADIUS
from apps.simulations.maze import Maze

pytestmark = pytest.mark.django_db


class TestPlan(unittest.TestCase):
    def test_get_next_tile(self):
        maze = Maze("the_ville")

        simulation = f.SimulationFactory()
        agent = f.AgentFactory(
            simulation=simulation, curr_position_x=68, curr_position_y=59
        )
        other_agent = f.AgentFactory(
            simulation=simulation, curr_position_x=68, curr_position_y=58
        )
        event = f.EventFactory(agent=other_agent, simulation=simulation)
        action_plan = plan(agent, simulation, maze, None, event)
        assert action_plan.planned_path
