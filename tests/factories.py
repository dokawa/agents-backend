import factory

from apps.agents.models import Agent


class AgentFactory(factory.Factory):
    class Meta:
        model = Agent

    name = factory.Faker("name")
