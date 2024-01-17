from collections import defaultdict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.agents.serializers import AgentSerializer
from apps.simulations.event_models import Event
from apps.simulations.maze import Maze
from apps.simulations.models import Simulation
from apps.simulations.serializers import EventSerializer
from apps.simulations.utils import EventType, format_response


class SimulationViewSet(viewsets.GenericViewSet):
    queryset = Simulation.objects.all()

    @action(detail=True, methods=["GET"])
    def step(self, request, pk=None, *args, **kwargs):
        simulation = self.get_object()
        maze = Maze("the_ville")

        agents = simulation.agents.all()
        for agent in agents:
            event = self.get_or_create_last_event(agent, simulation, maze)
            tile = agent.curr_tile()
            maze.add_event_from_tile(event, tile)

        paths = defaultdict(dict)
        for agent in agents:
            print(f"simulationViewset | agent: {agent.name}")
            next_tile = agent.execute_step(simulation, maze)
            if next_tile:
                paths[agent.name] = next_tile
                # Event.objects.create(type=EventType.MOVEMENT, agent=agent, simulation=simulation, position_x=next_tile[0], position_y=next_tile[1])

            print(f"  simulationViewset | agent: {agent.name} next_tile: {next_tile}")

        # serializer = AgentSerializer(agents, many=True)
        response = format_response(simulation.step, agents, paths)
        simulation.advance_step()
        return Response(response)

    @action(detail=True, methods=["GET"])
    def agents(self, request, pk=None, *args, **kwargs):
        simulation = self.get_object()
        serializer = AgentSerializer(simulation.agents.all(), many=True)
        return Response(serializer.data)

    def get_or_create_last_event(self, agent, simulation, maze):
        # If a user does not have an event, we create a movement one
        last_event = agent.get_last_event()
        if last_event:
            return last_event

        x, y = agent.curr_tile()
        event = Event.objects.create(
            agent=agent,
            address=maze.get_address_from_tile((x, y), "arena"),
            type=EventType.MOVEMENT,
            simulation=simulation,
            position_x=x,
            position_y=y,
            description="Agent initial position",
        )
        return event

    # @action(detail=False, methods=["GET"])
    # def print_collision(self, request, pk=None, *args, **kwargs):
    #     maze = Maze("the_ville")
    #     maze.print_collision()
    #     return Response()

    @action(detail=True, methods=["GET"])
    def reset_count(self, request, pk=None, *args, **kwargs):
        simulation = self.get_object()
        simulation.reset_count()
        return Response({})


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
