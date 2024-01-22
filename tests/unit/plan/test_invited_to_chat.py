import unittest
from unittest.mock import patch

import pytest

import tests.factories as f
from apps.agents.agent.classes import ActionPlanType, ReactionType
from apps.agents.agent.plan.plan import plan
from apps.simulations.maze import Maze
from apps.simulations.utils import EventType

pytestmark = pytest.mark.django_db


class TestInvitedToChat(unittest.TestCase):
    @patch(
        "apps.agents.agent.plan.plan_generation.get_weighted_random_choice",
        return_value=ReactionType.DO_NOT_REACT,
    )
    def test_return_same_plan_if_do_not_react(self, w_random_choice_mock):
        maze = Maze("the_ville")

        simulation = f.SimulationFactory()
        other_agent = f.AgentFactory(
            simulation=simulation, curr_position_x=0, curr_position_y=0
        )
        action_plan = f.ActionPlanFactory(
            type=ActionPlanType.CHAT_MOVE, interact_with=other_agent, planned_path=None
        )
        agent = f.AgentFactory(
            simulation=simulation,
            curr_position_x=68,
            curr_position_y=59,
            plan=action_plan,
        )
        f.EventFactory(
            type=EventType.CHAT_START,
            agent=other_agent,
            interact_with=agent,
            simulation=simulation,
        )

        assert agent.plan
        agent_plan = plan(agent, simulation, maze, None, None)

        assert agent.plan == agent_plan
