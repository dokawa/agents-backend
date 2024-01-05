from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.agents.models import Agent
from apps.simulations.maze import Maze
from apps.simulations.utils import format_step_response


class SimulationViewset(viewsets.GenericViewSet):
    @action(detail=False, methods=["GET"])
    def move(self, request, pk=None, *args, **kwargs):
        maze = Maze("the_ville")
        agents = Agent.objects.all()

        paths = {}
        for agent in agents:
            print(f"{agent.name}")
            paths[agent.name] = agent.move(maze, agents, None, None)
        # serializer = AgentSerializer(agents, many=True)
        response = format_step_response(0, agents, paths)
        return Response(response)

    @action(detail=False, methods=["GET"])
    def print_collision(self, request, pk=None, *args, **kwargs):
        maze = Maze("the_ville")
        maze.print_collision()
        return Response()
