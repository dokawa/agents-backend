import unittest

import tests.factories as f
from apps.simulations.utils import (  # Replace 'your_module' with the actual module containing the function
    format_step_response,
    get_maze_meta,
)


class TestGetSimulationMeta(unittest.TestCase):
    def test_get_simulation_meta(self):
        result = get_maze_meta("the_ville/matrix")
        # Assert that the function returns the expected result
        assert result is not None

    def test_response_format(self):
        agent = f.AgentFactory()
        path = [[0, 1], [0, 2]]
        formatted_data = format_step_response(0, [agent], path)

        assert 0 in formatted_data
        assert agent.name in formatted_data[0]
        assert formatted_data[0][agent.name] == path[0]
