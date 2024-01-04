from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class SimulationViewset(viewsets.GenericViewSet):


    @action(detail=False, methods=['GET'])
    def move(self, request, pk=None, *args, **kwargs):

        return Response({'hue': 'br'})

    def list(self, request):
        return Response({'hue': 'br'})