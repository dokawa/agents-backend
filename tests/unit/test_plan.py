import unittest

import pytest

import tests.factories as f
from apps.agents.agent.classes import ActionPlanType
from apps.agents.agent.plan import finished_wait_action, plan
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

    def test_finished_wait_action(self):
        simulation = f.SimulationFactory()
        action_plan = f.ActionPlanFactory(
            type=ActionPlanType.IDLE,
            start_time=simulation.current_time(),
            duration=1 * 10,
        )

        simulation.advance_step()
        assert simulation.step == 2
        assert finished_wait_action(action_plan, simulation)

    # def test_chatting_with(self):
    #     maze = Maze("the_ville")
    #     simulation = f.SimulationFactory()
    #     chatting_1 = f.AgentFactory(
    #         simulation=simulation, curr_position_x=68, curr_position_y=59
    #     )
    #     chatting_2 = f.AgentFactory(
    #         simulation=simulation, curr_position_x=68, curr_position_y=59
    #     )
    #
    #     other_agent = f.AgentFactory(
    #         simulation=simulation, curr_position_x=68, curr_position_y=58
    #     )
    #     event = f.EventFactory(
    #         agent=chatting_2, simulation=simulation, description="Chatting event"
    #     )
    #
    #     plan(chatting_1, simulation, maze, None, event)
    #
    #     assert chatting_1.chatting_with == chatting_2
    #     assert chatting_2.chatting_with == chatting_1
    #
    #     plan(other_agent, simulation, maze, None, event)
