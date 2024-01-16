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

    def test_return_two_steps(self, client):
        view_name = "simulation-step"
        simulation = f.SimulationFactory()
        f.AgentFactory(simulation=simulation)

        url = reverse(view_name, args=[simulation.id])

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 1 in response.data
        assert response.data

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 2 in response.data

    def test_reset_simulation_count(self, client):
        step_view_name = "simulation-step"
        simulation = f.SimulationFactory()
        f.AgentFactory(simulation=simulation)

        url = reverse(step_view_name, args=[simulation.id])

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 1 in response.data

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 2 in response.data

        # Make a reset call
        reset_view_name = "simulation-reset-count"
        reset_url = reverse(reset_view_name, args=[simulation.id])
        response = client.get(reset_url)
        assert response.status_code == status.HTTP_200_OK

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 1 in response.data
