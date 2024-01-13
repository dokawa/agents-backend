import unittest

import numpy as np
import pytest

import tests.factories as f
from apps.agents.agent.retrieve import (
    annotate_importance,
    annotate_recency,
    annotate_relevance,
    annotate_score,
    retrieve,
)
from tests.utils import generate_random_normalized_vector

pytestmark = pytest.mark.django_db


class TestRetrieve(unittest.TestCase):
    def test_relevance(self):
        agent = f.AgentFactory()
        simulation = f.SimulationFactory()

        # Creating a vector in EventFactory was returning the same one for both
        # TODO check how to create it in factory
        event_1 = f.EventFactory(
            agent=agent,
            simulation=simulation,
            embedding=generate_random_normalized_vector(),
        )
        event_2 = f.EventFactory(
            agent=agent,
            simulation=simulation,
            embedding=generate_random_normalized_vector(),
        )

        assert not np.array_equal(event_1.embedding, event_2.embedding)

        relevance = annotate_relevance(agent.events.all(), "")

        assert relevance[0] != relevance[1]

    #
    def test_importance(self):
        agent = f.AgentFactory()
        simulation = f.SimulationFactory()
        f.EventFactory(
            agent=agent,
            simulation=simulation,
        )
        f.EventFactory(
            agent=agent,
            simulation=simulation,
        )

        importance = annotate_importance(agent.events.all())

        assert 0 < importance[0].importance <= 1
        assert 0 < importance[1].importance <= 1

    def test_recency(self):
        agent = f.AgentFactory()
        simulation = f.SimulationFactory()
        event_1 = f.EventFactory(
            agent=agent,
            simulation=simulation,
        )
        event_2 = f.EventFactory(
            agent=agent,
            simulation=simulation,
        )

        assert event_2.created > event_1.created

        recency = annotate_recency(agent.events.all())

        newest = recency[0]
        oldest = recency[1]

        assert newest.recency > oldest.recency  # Newest have larger score value
        assert newest.created > oldest.created  # Newest has larger created time
        assert newest.recency == 1  # Newest has max recency
        assert oldest.recency < 1  # Older has less than max recency

    def test_score(self):
        agent = f.AgentFactory()
        simulation = f.SimulationFactory()

        # Creating a vector in EventFactory was returning the same one for both
        # TODO check how to create it in factory
        f.EventFactory(
            agent=agent,
            simulation=simulation,
            embedding=generate_random_normalized_vector(),
        )
        f.EventFactory(
            agent=agent,
            simulation=simulation,
            embedding=generate_random_normalized_vector(),
        )

        events = agent.events.all()
        annotated_recency = annotate_recency(events)
        annotated_importance = annotate_importance(annotated_recency)
        annotated_relevance = annotate_relevance(annotated_importance, "")
        annotated_score = annotate_score(annotated_relevance)

        assert annotated_score[0].score != 0
        assert annotated_score[1].score != 0

    def test_retrieve(self):
        agent = f.AgentFactory()
        simulation = f.SimulationFactory()

        # Creating a vector in EventFactory was returning the same one for both
        # TODO check how to create it in factory
        f.EventFactory(
            agent=agent,
            simulation=simulation,
            embedding=generate_random_normalized_vector(),
        )
        f.EventFactory(
            agent=agent,
            simulation=simulation,
            embedding=generate_random_normalized_vector(),
        )

        action = "doing something"
        retrieved = retrieve(agent, simulation, [action])

        assert retrieved[action][0].score != 0
