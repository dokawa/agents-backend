import random

from apps.simulations.utils import EventType


def select(agent, perceived):
    """
    Retrieved elements have multiple core "curr_events". We need to choose one
    event to which we are going to react to. We pick that event here.
    INPUT
      persona: Current <Persona> instance whose action we are determining.
      retrieved: A dictionary of <Events> that were retrieved from the
                 the persona's associative memory. This dictionary takes the
                 following form:
                 dictionary[event.description] =
                   {["curr_event"] = <ConceptNode>,
                    ["events"] = [<ConceptNode>, ...],
                    ["thoughts"] = [<ConceptNode>, ...] }
    """
    # Always choose persona first. We remove same agent
    priority = [
        event
        for event in perceived
        if (event.agent != agent and not event.agent.chatting_with)
    ]
    if priority:
        selected = random.choice(priority)
        print(f"  selected: {selected}")

    # priority = [
    #     event
    #     for event in perceived
    #     if event.type == EventType.OCCURENCE or event.type == EventType.ACTION
    # ]
    # if priority:
    #     return random.choice(priority)
    # TODO check if need to skip idle
    return None
