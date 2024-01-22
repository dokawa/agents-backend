import unittest
from unittest.mock import patch

import pytest

import tests.factories as f
from apps.agents.agent.classes import ActionPlanType, ReactionType
from apps.agents.agent.plan.plan import plan
from apps.simulations.maze import Maze
from apps.simulations.utils import EventType

pytestmark = pytest.mark.django_db


class TestIsChatting(unittest.TestCase):
    @patch(
        "apps.agents.agent.plan.plan._decide_chat_reaction",
        return_value=ReactionType.WAIT_RESPONSE,
    )
    def test_return_same_plan_if_do_not_react(self, decide_reaction_mock):
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

        # Enter was_invited_to_chat
        f.EventFactory(
            type=EventType.CHAT_START,
            agent=other_agent,
            interact_with=agent,
            simulation=simulation,
        )

        assert agent.plan
        agent_plan = plan(agent, simulation, maze, None, None)

        assert agent_plan.type == ActionPlanType.IDLE

    @patch(
        "apps.agents.agent.plan.plan._decide_chat_reaction",
        return_value=ReactionType.END_CHAT,
    )
    @patch(
        "apps.agents.agent.plan.plan_generation.get_weighted_random_choice",
        return_value=ActionPlanType.IDLE,
    )
    def test_return_idle_if_end_chat(self, w_random_choice_mock, decide_reaction_mock):
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

        # Enter was_invited_to_chat
        f.EventFactory(
            type=EventType.CHAT_START,
            agent=other_agent,
            interact_with=agent,
            simulation=simulation,
        )

        assert agent.plan
        agent_plan = plan(agent, simulation, maze, None, None)

        assert agent_plan.type == ActionPlanType.IDLE

    # @patch(
    #     "apps.agents.agent.plan.plan._decide_chat_reaction",
    #     return_value=ReactionType.END_CHAT,
    # )
    # @patch(
    #     "apps.agents.agent.plan.plan_generation.get_weighted_random_choice",
    #     return_value=ActionPlanType.MOVE,
    # )
    # def test_return_move_if_end_chat(self, w_random_choice_mock, decide_reaction_mock):
    #     maze = Maze("the_ville")
    #
    #     simulation = f.SimulationFactory()
    #     other_agent = f.AgentFactory(
    #         simulation=simulation, curr_position_x=0, curr_position_y=0
    #     )
    #     action_plan = f.ActionPlanFactory(
    #         type=ActionPlanType.CHAT_MOVE,
    #         interact_with=other_agent,
    #         planned_path=[
    #             (58, 68)
    #         ],  # this makes it an unfinished move action for finished_move_action flow
    #     )
    #     agent = f.AgentFactory(
    #         simulation=simulation,
    #         curr_position_x=68,
    #         curr_position_y=59,
    #         plan=action_plan,
    #     )
    #
    #     # Enter was_invited_to_chat
    #     f.EventFactory(
    #         type=EventType.CHAT_START,
    #         agent=other_agent,
    #         interact_with=agent,
    #         simulation=simulation,
    #     )
    #
    #     assert agent.plan
    #     agent_plan = plan(agent, simulation, maze, None, None)
    #
    #     w_random_choice_mock.assert_called_once()
    #     decide_reaction_mock.assert_called_once()
    #
    #     assert agent_plan.type == ActionPlanType.MOVE
