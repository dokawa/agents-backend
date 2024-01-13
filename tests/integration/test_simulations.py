import pytest
from django.urls import reverse
from rest_framework import status

import tests.factories as f

pytestmark = pytest.mark.django_db


class TestSimulation:
    def test_action_url(self, client):
        view_name = "simulation-step"
        simulation = f.SimulationFactory()
        f.AgentFactory(simulation=simulation)

        url = reverse(view_name, args=[simulation.id])

        # assert url == f"/simulations/simulation/{simulation.id}/step/"

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
