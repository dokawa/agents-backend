import unittest

import pytest

import tests.factories as f
from apps.simulations.utils import EventType

pytestmark = pytest.mark.django_db


class TestAgent(unittest.TestCase):
    def test_is_chatting(self):
        simulation = f.SimulationFactory()
        agent_1 = f.AgentFactory(
            simulation=simulation, curr_position_x=68, curr_position_y=59
        )

        f.EventFactory(
            type=EventType.CHAT_START,
            agent=agent_1,
            simulation=simulation,
            description="Chatting event",
        )

        assert agent_1.is_chatting()

    # def test_are_both_chatting(self):
    #     simulation = f.SimulationFactory()
    #     agent_1 = f.AgentFactory(
    #         simulation=simulation, curr_position_x=68, curr_position_y=59
    #     )
    #     agent_2 = f.AgentFactory(
    #         simulation=simulation, curr_position_x=68, curr_position_y=59
    #     )
    #
    #     f.EventFactory(
    #         type=EventType.CHAT_START,
    #         agent=agent_1,
    #         interact_with=agent_2,
    #         simulation=simulation,
    #         description="Chatting event",
    #         sim_time_created=datetime.now(),
    #     )
    #
    #     assert agent_1.is_chatting()
    #     assert agent_2.is_chatting()
