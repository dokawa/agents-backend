"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: retrieve.py
Description: This defines the "Retrieve" module for generative agents.
"""

from django.db.models import F, FloatField, Func, Window
from django.db.models.functions import Rank
from pgvector.django import CosineDistance

from apps.agents.constants import (
    GLOBAL_IMPORTANCE_WEIGHT,
    GLOBAL_RECENCY_WEIGHT,
    GLOBAL_RELEVANCE_WEIGHT,
    RECENCY_DECAY,
)
from apps.agents.memory_structures.utils import get_embedding


def annotate_recency(events_queryset):
    recency_order = "-created"
    annotated_events = (
        events_queryset.order_by("-created")
        .annotate(rank=Window(expression=Rank(), order_by=(recency_order)))
        .annotate(
            recency=Func(
                RECENCY_DECAY, F("rank") - 1, function="POW", output_field=FloatField()
            )
        )
    )
    return annotated_events


def annotate_importance(events_queryset):
    annotated_importance = events_queryset.annotate(importance=F("poignancy") / 10.0)
    return annotated_importance


def annotate_relevance(events_queryset, focal_pt):
    focal_embedding = get_embedding(focal_pt)
    annotated_relevance = events_queryset.annotate(
        relevance=CosineDistance("embedding", focal_embedding)
    )
    return annotated_relevance


def annotate_score(events_queryset):
    # Computing the final scores that combines the component values.
    # Note to self: test out different weights. in the future, these weights should likely be learned,
    # perhaps through an RL-like process.
    annotated_score = events_queryset.annotate(
        score=F("recency") * GLOBAL_RECENCY_WEIGHT
        + F("relevance") * GLOBAL_RELEVANCE_WEIGHT
        + F("importance") * GLOBAL_IMPORTANCE_WEIGHT
    )

    return annotated_score


def retrieve(agent, simulation, focal_points, n_count=30):
    """
    Given the current persona and focal points (focal points are events or
    thoughts for which we are retrieving), we retrieve a set of nodes for each
    of the focal points and return a dictionary.

    INPUT:
      persona: The current persona object whose memory we are retrieving.
      focal_points: A list of focal points (string description of the events or
                    thoughts that is the focus of current retrieval).
    OUTPUT:
      retrieved: A dictionary whose keys are a string focal point, and whose
                 values are a list of Node object in the agent's associative
                 memory.

    Example input:
      persona = <persona> object
      focal_points = ["How are you?", "Jane is swimming in the pond"]
    """
    # <retrieved> is the main dictionary that we are returning
    events = agent.events.all()
    retrieved = dict()
    for focal_pt in focal_points:
        scored_events = get_scored_events(events, focal_pt, n_count)
        # scored_events.update(sim_time_last_accessed=simulation.current_time())
        retrieved[focal_pt] = scored_events

    return retrieved


def get_scored_events(events, focal_pt, n_count):
    annotated_recency = annotate_recency(events)
    annotated_importance = annotate_importance(annotated_recency)
    annotated_relevance = annotate_relevance(annotated_importance, focal_pt)
    annotated_score = annotate_score(annotated_relevance)
    highest = annotated_score.order_by("score")[:n_count]

    return highest
