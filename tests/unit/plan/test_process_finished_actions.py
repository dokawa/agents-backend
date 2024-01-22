import unittest

import pytest

import tests.factories as f
from apps.agents.agent.classes import ActionPlanType
from apps.agents.agent.plan.process_finished_actions import _process_finished_actions
from apps.agents.constants import INITIAL_DATE, SECONDS_PER_STEP
from apps.simulations.maze import Maze

pytestmark = pytest.mark.django_db


class TestFinishedActions(unittest.TestCase):
    def test_delete_if_move_finished(self):
        maze = Maze("the_ville")

        simulation = f.SimulationFactory()
        other_agent = f.AgentFactory(
            simulation=simulation, curr_position_x=68, curr_position_y=60
        )
        action_plan = f.ActionPlanFactory(
            type=ActionPlanType.MOVE, interact_with=other_agent, planned_path=[]
        )
        agent = f.AgentFactory(
            simulation=simulation,
            curr_position_x=68,
            curr_position_y=59,
            plan=action_plan,
        )

        assert agent.plan

        _process_finished_actions(agent, simulation, maze)

        agent.refresh_from_db()
        assert agent.plan is None

    def test_delete_if_idle_finished(self):
        maze = Maze("the_ville")

        simulation = f.SimulationFactory()

        action_plan = f.ActionPlanFactory(
            type=ActionPlanType.IDLE, start_time=INITIAL_DATE, duration=SECONDS_PER_STEP
        )
        agent = f.AgentFactory(
            simulation=simulation,
            curr_position_x=68,
            curr_position_y=59,
            plan=action_plan,
        )

        assert agent.plan
        _process_finished_actions(agent, simulation, maze)
        agent.refresh_from_db()
        assert agent.plan is None
