"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: plan.py
Description: This defines the "Plan" module for generative agents.
"""
import random
from datetime import timezone

from apps.agents.agent.classes import ReactionType
from apps.agents.constants import SECONDS_PER_STEP
from apps.agents.models import ActionPlanType
from apps.agents.path.utils import get_shortest_path
from apps.agents.utils import meeting_addresses


def plan(agent, simulation, maze, new_day, event):
    # If a move action is finished
    _process_finished_move_actions(agent, simulation, maze)

    if agent.plan:
        return agent.plan

    if agent.is_chatting():
        return _process_chat_action(agent, simulation, maze)
    # if the perceived agent is not chatting
    elif event_agent_is_available_to_chat(event):
        return _decide_to_chat(agent, simulation, event.agent, maze)
    else:
        return _generate_random_action(agent, simulation, maze)

    #     return _process_event(agent, event, simulation, maze)
    # else:
    #     return _generate_random_action(agent, maze)


def event_agent_is_available_to_chat(event):
    return event and event.agent and not event.agent.is_chatting()


def _process_finished_move_actions(agent, simulation, maze):
    action_plan = agent.plan
    if finished_chat_move_action(action_plan):
        neighbor_tiles = maze.get_nearby_tiles(
            agent.curr_tile(), 1, include_reference_tile=True
        )
        other_agent = action_plan.interact_with

        if other_agent.is_chatting():
            print(
                f"  plan | {agent.name} gave up on chatting with {other_agent.name} because they are already chatting"
            )
            agent.plan = _generate_random_action(agent, simulation, maze)
            agent.save()
        elif other_agent.curr_tile() in neighbor_tiles:
            print(f"  plan | {agent.name} started chatting with {other_agent.name}")
            create_chat_event(agent, other_agent, simulation)
            create_chat_event(other_agent, agent, simulation)
        else:
            print(
                f"  plan | {agent.name} gave up on chatting with {other_agent.name} because they are not here"
            )
            agent.plan = _generate_chat_plan(agent, simulation, other_agent, maze)
            agent.save()
        action_plan.delete()
        # TODO make another gpt decision given that it came from a chat plan

    elif finished_move_action(action_plan):
        action_plan.delete()

    elif finished_wait_action(action_plan, simulation):
        action_plan.delete()


def _decide_to_chat(agent, simulation, other_agent, maze):
    decision = get_weighted_random_choice(
        [ReactionType.START_CHAT, ReactionType.DO_NOT_REACT], [0.7, 0.3]
    )
    if decision == ReactionType.START_CHAT:
        return _generate_chat_plan(agent, simulation, other_agent, maze)
    # TODO chat gpt decision here
    else:
        return _generate_random_action(agent, simulation, maze)


def create_chat_event(agent, chat_with, simulation, end=False):
    from apps.simulations.event_models import Event
    from apps.simulations.utils import EventType

    Event.objects.create(
        type=EventType.END_CHAT if end else EventType.CHAT,
        agent=agent,
        interact_with=chat_with,
        simulation=simulation,
        description=f"Chatting with {chat_with.name}",
        sim_time_created=simulation.current_time(),
        position_x=agent.curr_position_x,
        position_y=agent.curr_position_y,
    )


def _process_chat_action(agent, simulation, maze):
    other_agent = agent.last_event.interacting_with

    reaction_mode = decide_chat_reaction(agent, other_agent)

    if reaction_mode == ReactionType.CONTINUE_CHAT:
        print(f"  plan | {agent.name} will continue chatting with {other_agent.name}")
        return _generate_chat_plan(agent, simulation, other_agent, maze)
    elif reaction_mode == ReactionType.WAIT_RESPONSE:
        print(f"  plan | {agent.name} is waiting for {other_agent.name} response")
        # Don't do anything, don't move
        return _generate_wait_response_plan(agent, simulation)
    elif reaction_mode == ReactionType.END_CHAT:
        # TODO get end chat message
        print(f"  plan | {agent.name} ended chat with {other_agent.name}")
        create_chat_event(agent, other_agent, simulation, end=True)
        create_chat_event(other_agent, agent, simulation, end=True)
        return _generate_random_action(agent, simulation, maze)

    # TODO
    # elif reaction_mode == ReactionType.WAIT:
    #     _wait_react(agent, reaction_mode)


def _generate_wait_response_plan(agent, simulation):
    from apps.agents.models import ActionPlan

    description = "Waiting chat response"
    pronunciatio = "1F5E8"

    action_plan = ActionPlan.objects.create(
        type=ActionPlanType.IDLE,
        simulation=simulation,
        start_time=simulation.current_time(),
        duration=random.randint(1, 10) * SECONDS_PER_STEP,
        description=description,
        pronunciatio=pronunciatio,
    )
    agent.plan = action_plan
    agent.save()
    return action_plan


def _generate_idle_plan(agent, simulation):
    from apps.agents.models import ActionPlan

    description = "Idle"
    pronunciatio = "231B"

    action_plan = ActionPlan.objects.create(
        type=ActionPlanType.IDLE,
        simulation=simulation,
        start_time=simulation.current_time(),
        duration=random.randint(1, 10) * SECONDS_PER_STEP,
        description=description,
        pronunciatio=pronunciatio,
    )
    agent.plan = action_plan
    agent.save()
    return action_plan


def _generate_chat_plan(agent, simulation, other_agent, maze):
    from apps.agents.models import ActionPlan

    chat_message = "Hi"
    target_tiles = maze.get_nearby_tiles(
        agent.curr_tile(), 1, include_reference_tile=False
    )

    if agent.plan:
        return agent.plan

    path = get_shortest_path(agent, maze, target_tiles)

    address = maze.get_address_from_tile(other_agent.curr_tile(), "arena")
    description = f"Chat with {other_agent.name}"
    pronunciatio = "1F4AC"

    action_plan = ActionPlan.objects.create(
        type=ActionPlanType.CHAT_WITH,
        simulation=simulation,
        start_time=simulation.current_time(),
        address=address,
        description=description,
        pronunciatio=pronunciatio,
        chat=chat_message,
        planned_path=path,
        interact_with=other_agent,
    )
    agent.plan = action_plan
    agent.save()
    return action_plan


def _generate_random_action(agent, simulation, maze):
    from apps.agents.models import ActionPlan

    reaction_type = get_weighted_random_choice(
        [ActionPlanType.IDLE, ActionPlanType.MOVE], [0.8, 0.2]
    )
    # reaction_type = ActionPlanType.MOVE

    if reaction_type == ActionPlanType.MOVE:
        address = random.choice(meeting_addresses)
        target_tiles = list(maze.address_tiles[address])
        path = get_shortest_path(agent, maze, target_tiles)

        plan = ActionPlan.objects.create(
            type=ActionPlanType.MOVE,
            start_time=simulation.current_time(),
            simulation=simulation,
            address=address,
            description="Random move",
            pronunciatio="1F6B6",
            planned_path=path,
        )
    else:
        plan = _generate_idle_plan(agent, simulation)

    agent.plan = plan
    agent.save()

    return plan


def decide_chat_reaction(agent, other_agent):
    # Agent is waiting for answer if last chat event is from him
    if agent.last_event().sim_time_created > other_agent.last_event().sim_time_created:
        return ReactionType.WAIT_RESPONSE
    # Agent is replying if last chat event was from the other user
    elif (
        agent.last_event().sim_time_created < other_agent.last_event().sim_time_created
    ):
        return get_weighted_random_choice(
            [ReactionType.CONTINUE_CHAT, ReactionType.END_CHAT],
            [0.7, 0.3],
        )
    else:
        raise Exception


def get_random_bool(true_percentage):
    random_number = random.randint(0, 99)
    return random_number < true_percentage


def get_weighted_random_choice(choices, weights):
    # The weights should sum up to 1
    return random.choices(choices, weights=weights)[0]


def finished_move_action(action_plan):
    return (
        action_plan
        and action_plan.type == ActionPlanType.MOVE
        and not action_plan.planned_path
    )


def finished_chat_move_action(action_plan):
    return (
        action_plan
        and action_plan.type == ActionPlanType.CHAT_WITH
        and not action_plan.planned_path
    )


def finished_wait_action(action_plan, simulation):
    from datetime import timedelta

    return (
        action_plan
        and action_plan.type == ActionPlanType.IDLE
        and action_plan.start_time + timedelta(seconds=action_plan.duration)
        == simulation.current_time().astimezone(timezone.utc)
    )
