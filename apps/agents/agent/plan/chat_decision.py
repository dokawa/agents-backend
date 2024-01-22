from apps.agents.agent.classes import ReactionType
from apps.agents.agent.plan.plan_generation import (
    _generate_chat_plan,
    _generate_random_plan,
)
from apps.agents.agent.plan.utils import create_chat_event, get_weighted_random_choice
from apps.agents.colored_print import print_green
from apps.simulations.utils import EventType


def _decide_to_chat(agent, simulation, other_agent, maze):
    decision = get_weighted_random_choice(
        [ReactionType.START_CHAT, ReactionType.DO_NOT_REACT], [0.7, 0.3]
    )
    if decision == ReactionType.START_CHAT:
        print_green(f"{agent.name} will start chat with {other_agent.name}")
        create_chat_event(agent, other_agent, simulation, EventType.CHAT_START)
        return _generate_chat_plan(agent, other_agent, simulation, maze)
    # TODO chat gpt decision here
    else:
        return _generate_random_plan(agent, simulation, maze)


def _decide_chat_reaction(agent, other_agent):
    # Agent is waiting for answer if last chat event is from him
    # if should_wait(agent, other_agent):
    #     return ReactionType.WAIT_RESPONSE
    # # Agent is replying if last chat event was from the other user
    # else:
    #     return get_weighted_random_choice(
    #         [ReactionType.CONTINUE_CHAT, ReactionType.END_CHAT],
    #         [0.9, 0.1],
    #     )

    if should_talk(agent, other_agent):
        return get_weighted_random_choice(
            [ReactionType.CONTINUE_CHAT, ReactionType.END_CHAT],
            [0.9, 0.1],
        )
    else:
        return ReactionType.WAIT_RESPONSE


# def should_wait(agent, other_agent):
#     is_chat_starter = agent.is_chat_starter() and not other_agent.has_last_chat(agent)
#     is_not_turn_to_talk = not other_agent.has_last_chat(agent)
#     return is_chat_starter or is_not_turn_to_talk


def should_talk(agent, other_agent):
    return other_agent.is_chat_starter() or other_agent.has_last_chat(agent)
