import random


def select(agent, events, curr_time):
    """
    Retrieved elements have multiple core "curr_events". We need to choose one
    event to which we are going to react to. We pick that event here.
    INPUT
      agent: Current <Agent> instance whose action we are determining.
      perceived: A list of <Events> that were retrieved from the
                 the persona's events. This dictionary takes the
                 following form:
                 dictionary[event.description] =
                   {["curr_event"] = <ConceptNode>,
                    ["events"] = [<ConceptNode>, ...],
                    ["thoughts"] = [<ConceptNode>, ...] }
    """
    # Always choose persona first. We remove same agent

    priority = [event for event in events if (can_select(agent, event, curr_time))]

    if priority:
        return random.choice(priority)
    # TODO check if need to skip idle
    return None


def can_select(agent, event, curr_time):
    other_agent = event.agent
    return (
        agent != other_agent  # do not act on himself
        and event.agent.events.exists()
        and not event.agent.get_interacting_with()
        and not agent.chatted_recently(other_agent, curr_time)
    )
