import unittest

import pytest

import tests.factories as f
from apps.agents.agent.select import select

pytestmark = pytest.mark.django_db


class TestPick(unittest.TestCase):
    def test_choose_agent_first(self):
        agent = f.AgentFactory()
        agent_2 = f.AgentFactory()
        simulation = f.SimulationFactory()

        # Creating a vector in EventFactory was returning the same one for both
        # TODO check how to create it in factory
        event_1 = f.EventFactory(
            agent=agent,
            simulation=simulation,
        )
        event_2 = f.EventFactory(
            agent=agent_2,
            simulation=simulation,
        )

        perceived = [event_1, event_2]

        chosen = select(agent, perceived)

        assert chosen.agent == agent_2
