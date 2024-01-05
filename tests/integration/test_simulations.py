from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestSimulation:
    def test_action_url(self, client):
        view_name = "simulation-move"

        url = reverse(view_name)

        assert url == "/simulations/simulation/move/"

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

    @patch("apps.agents.models.Agent.move")  # Mock the move method
    def test_move_path(self, mock_move, client, path):
        view_name = "simulation-move"
        # Set up the mock to return the coordinates of YourModel instances
        mock_move.return_value = path

        response = client.get(reverse(view_name))

        assert response.data == path
