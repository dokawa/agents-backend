import factory.fuzzy
from factory.django import DjangoModelFactory

from apps.agents.models import Agent
from apps.simulations.event_models import Event
from apps.simulations.models import Simulation


class AgentFactory(DjangoModelFactory):
    class Meta:
        model = Agent

    name = factory.Faker("name")
    simulation = factory.SubFactory("tests.factories.SimulationFactory")


class SimulationFactory(DjangoModelFactory):
    class Meta:
        model = Simulation

    name = factory.Faker("name")

    @factory.post_generation
    def agents(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        self.agents.add(*extracted)


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    agent = factory.SubFactory("tests.factories.AgentFactory")
    poignancy = factory.fuzzy.FuzzyInteger(1, 10)
    simulation = factory.SubFactory("tests.factories.SimulationFactory")
