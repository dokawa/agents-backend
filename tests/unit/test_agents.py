import unittest

import pytest

import tests.factories as f

pytestmark = pytest.mark.django_db


class TestSelect(unittest.TestCase):
    def test_one_to_one(self):
        agent_1 = f.AgentFactory()
        agent_2 = f.AgentFactory()
        simulation = f.SimulationFactory()

        f.EventFactory(
            agent=agent_1,
            simulation=simulation,
        )
        f.EventFactory(
            agent=agent_2,
            simulation=simulation,
        )

        agent_1.chatting_with = agent_2

        agent_1.save()

        assert agent_1.chatting_with == agent_2
        assert agent_2.chatting_with == agent_1
