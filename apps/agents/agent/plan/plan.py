import random

from apps.agents.agent.classes import ReactionType
from apps.agents.agent.plan.chat_decision import _decide_chat_reaction, _decide_to_chat
from apps.agents.agent.plan.plan_generation import (
    _generate_chat_plan,
    _generate_random_plan,
    _generate_wait_response_plan,
)
from apps.agents.agent.plan.process_finished_actions import (
    _process_finished_actions,
    finished_chat_move_action,
)
from apps.agents.agent.plan.utils import create_chat_event, get_weighted_random_choice
from apps.agents.colored_print import (
    print_blue,
    print_cyan,
    print_green,
    print_magenta,
    print_red,
    print_yellow,
)
from apps.simulations.utils import EventType


def plan(agent, simulation, maze, new_day, event):
    # If a move action is finished
    _process_finished_actions(agent, simulation, maze)

    # This allows the agent to change plans
    if agent.was_invited_to_chat():
        # TODO decide with gpt to chat or end
        decision = get_weighted_random_choice(
            [ReactionType.CONTINUE_CHAT, ReactionType.DO_NOT_REACT], [0.9, 0.1]
        )
        if decision == ReactionType.CONTINUE_CHAT:
            print_green(f"{agent.name} accepted chat")
            create_chat_event(
                agent,
                agent.get_last_interacted_with().agent,
                simulation,
                EventType.CHAT,
            )
            return _generate_wait_response_plan(agent, simulation)

    elif agent.is_chatting():
        return _process_chat_action(agent, simulation, maze)
    elif event_agent_is_available_to_chat(event):
        return _decide_to_chat(agent, simulation, event.agent, maze)
    elif finished_chat_move_action(agent.plan):
        return _follow_up_chat_move_action(agent, maze, simulation)
    elif has_ongoing_plan(agent, simulation):
        return agent.plan
    # if the perceived agent is not chatting
    else:
        print_magenta(f"{agent.name} went random")
        return _generate_random_plan(agent, simulation, maze)


def _follow_up_chat_move_action(agent, maze, simulation):
    if agent.plan:
        agent.plan.delete()

    # TODO make another gpt decision given that it came from a chat plan
    neighbor_tiles = maze.get_nearby_tiles(
        agent.curr_tile(), 1, include_reference_tile=True
    )

    other_agent = agent.plan.interact_with
    # If it found the other agent

    if other_agent.curr_tile() not in neighbor_tiles:
        print_yellow(
            f"  plan | {agent.name} will try to find {other_agent.name} because they are not here"
        )
        return _generate_chat_plan(agent, other_agent, simulation, maze)

    elif other_agent.is_chatting():
        print_yellow(
            f"  plan | {agent.name} gave up on chatting with {other_agent.name} because they are already chatting"
        )
        return _generate_random_plan(agent, simulation, maze)
    else:
        print_green(f"  plan | {agent.name} started chatting with {other_agent.name}")
        create_chat_event(agent, other_agent, simulation, EventType.CHAT_START)
        return _generate_wait_response_plan(agent, simulation)


def _process_chat_action(agent, simulation, maze):
    if agent.plan:
        agent.plan.delete()

    print_cyan(f"{agent.name} process")
    if agent.was_invited_to_chat():
        other_agent = agent.get_last_interacted_with().agent
    else:
        other_agent = agent.last_event().interact_with

    reaction_mode = _decide_chat_reaction(agent, other_agent)

    if reaction_mode == ReactionType.CONTINUE_CHAT:
        print_blue(
            f"  plan | {agent.name} will continue chatting with {other_agent.name}"
        )
        create_chat_event(agent, other_agent, simulation, EventType.CHAT)
        plan = _generate_chat_plan(agent, other_agent, simulation, maze)
    elif reaction_mode == ReactionType.WAIT_RESPONSE:
        print_blue(f"  plan | {agent.name} is waiting for {other_agent.name} response")
        # Don't do anything, don't move
        plan = _generate_wait_response_plan(agent, simulation)
    elif reaction_mode == ReactionType.END_CHAT:
        # TODO get end chat message
        print_red(f"  plan | {agent.name} ended chat with {other_agent.name}")
        create_chat_event(agent, other_agent, simulation, EventType.CHAT_END)
        create_chat_event(other_agent, agent, simulation, EventType.CHAT_END)
        plan = _generate_random_plan(agent, simulation, maze)
    else:
        raise Exception

    agent.plan = plan
    agent.save()
    return plan


def event_agent_is_available_to_chat(event):
    return event and event.agent and not event.agent.is_chatting()


def has_ongoing_plan(agent, simulation):
    return agent.plan and (
        agent.plan.planned_path or not agent.plan.expires(simulation.current_time())
    )


def get_random_bool(true_percentage):
    random_number = random.randint(0, 99)
    return random_number < true_percentage
