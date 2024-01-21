import unittest
from datetime import timedelta

import pytest

import tests.factories as f
from apps.agents.constants import INITIAL_DATE
from apps.simulations.utils import (  # Replace 'your_module' with the actual module containing the function
    format_simulation_response,
    get_maze_meta,
)

pytestmark = pytest.mark.django_db


class TestGetSimulationMeta(unittest.TestCase):
    def test_get_simulation_meta(self):
        result = get_maze_meta("the_ville/matrix")
        # Assert that the function returns the expected result
        assert result is not None

    def test_response_format(self):
        agent = f.AgentFactory()
        path = [[0, 1], [0, 2]]
        formatted_data = format_simulation_response(0, [agent], {agent.name: path})

        step = 1
        assert step in formatted_data
        assert agent.name in formatted_data[step]
        assert formatted_data[step][agent.name]["movement"] == path[0]

    def test_current_time(self):
        simulation = f.SimulationFactory(step=1)
        assert simulation.current_time() == INITIAL_DATE + timedelta(seconds=10)
        simulation = f.SimulationFactory(step=2)
        assert simulation.current_time() == INITIAL_DATE + timedelta(seconds=20)
