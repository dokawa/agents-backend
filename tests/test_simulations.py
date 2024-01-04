from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestSimulation(APITestCase):
    def test_action_url(self):
        view_name = 'simulation-move'

        url = reverse(view_name)

        self.assertEqual(url, '/simulations/simulations/move/')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)