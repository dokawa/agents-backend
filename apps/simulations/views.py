from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.agents.models import Agent
from apps.simulations.event_model import Event
from apps.simulations.maze import Maze
from apps.simulations.serializers import EventSerializer
from apps.simulations.utils import EventType, format_step_response


class SimulationViewSet(viewsets.GenericViewSet):
    @action(detail=True, methods=["GET"])
    def step(self, request, pk=None, *args, **kwargs):
        maze = Maze(self, "the_ville")
        agents = Agent.objects.all()
        for agent in agents:
            action = agent.get_last_action()
            tile = agent.curr_tile()
            maze.add_event_from_tile(action, tile)

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


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=False, methods=["POST"])
    def create_move(self, request, *args, **kwargs):
        events_data = request.data
        events_data = [{"type": EventType.MOVEMENT, **data} for data in events_data]

        serializer = self.get_serializer(data=events_data, many=True)
        serializer.is_valid(raise_exception=True)

        created = False

        filtered_events_data = []
        for data in serializer.validated_data:
            agent = data.get("agent")
            x = data.get("position_x")
            y = data.get("position_y")

            if agent.curr_position_x != x or agent.curr_position_y != y:
                agent.curr_position_x = x
                agent.curr_position_y = y
                agent.save()
                filtered_events_data.append(data)
                self.perform_create(serializer)

                if not created:
                    created = True

        headers = self.get_success_headers(serializer.data)

        if created:
            return Response(serializer.data, status=201, headers=headers)

        return Response(
            {"detail": "Request processed successfully, but no objects were created."},
            status=200,
            headers=headers,
        )
