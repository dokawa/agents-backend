import unittest

import pytest

import tests.factories as f
from apps.agents.agent.classes import ActionPlanType
from apps.agents.agent.plan.plan import plan
from apps.simulations.maze import Maze

pytestmark = pytest.mark.django_db


class TestOngoingPlan(unittest.TestCase):
    def test_return_same_plan_if_do_not_react(self):
        maze = Maze("the_ville")

        simulation = f.SimulationFactory()
        other_agent = f.AgentFactory(
            simulation=simulation, curr_position_x=0, curr_position_y=0
        )
        action_plan = f.ActionPlanFactory(
            type=ActionPlanType.CHAT_MOVE,
            interact_with=other_agent,
            planned_path=[
                (58, 68)
            ],  # this makes it an unfinished move action for finished_move_action flow
        )
        agent = f.AgentFactory(
            simulation=simulation,
            curr_position_x=68,
            curr_position_y=59,
            plan=action_plan,
        )

        assert agent.plan
        agent_plan = plan(agent, simulation, maze, None, None)

        assert agent_plan == action_plan
