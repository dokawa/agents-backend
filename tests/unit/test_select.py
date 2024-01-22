import unittest

import pytest

import tests.factories as f
from apps.agents.agent.select import select
from apps.simulations.utils import EventType

pytestmark = pytest.mark.django_db


class TestSelect(unittest.TestCase):
    def test_choose_agent_first(self):
        agent = f.AgentFactory()
        agent_2 = f.AgentFactory()
        simulation = f.SimulationFactory()

        event_1 = f.EventFactory(
            agent=agent,
            simulation=simulation,
        )
        event_2 = f.EventFactory(
            agent=agent_2,
            simulation=simulation,
        )

        perceived = [event_1, event_2]

        chosen = select(agent, perceived, simulation.current_time())

        assert not agent.is_chatting()
        assert chosen.agent == agent_2

    def test_do_not_pick_own_event(self):
        agent = f.AgentFactory()

        simulation = f.SimulationFactory()

        event = f.EventFactory(
            agent=agent,
            simulation=simulation,
        )

        perceived = [event]

        chosen = select(agent, perceived, simulation.current_time())

        assert chosen is None

    def test_do_not_select_chatting_with(self):
        simulation = f.SimulationFactory()
        agent = f.AgentFactory(
            simulation=simulation, curr_position_x=68, curr_position_y=59
        )

        event_agent = f.AgentFactory(
            simulation=simulation,
            curr_position_x=68,
            curr_position_y=58,
        )

        event = f.EventFactory(
            agent=agent,
            type=EventType.CHAT_START,
            simulation=simulation,
            interact_with=event_agent,
        )

        chosen = select(agent, [event], simulation.current_time())

        assert chosen is None
