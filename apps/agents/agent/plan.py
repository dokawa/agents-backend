"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: plan.py
Description: This defines the "Plan" module for generative agents.
"""
import random

from apps.agents.agent.classes import ReactionType
from apps.agents.models import ActionPlanType
from apps.agents.path.utils import get_shortest_path
from apps.agents.utils import arena_addresses


def plan(agent, simulation, maze, new_day, selected):
    """
    Main cognitive function of the chain. It takes the retrieved memory and
    perception, as well as the maze and the first day state to conduct both
    the long term and short term planning for the persona.

    INPUT:
      maze: Current <Maze> instance of the world.
      personas: A dictionary that contains all persona names as keys, and the
                Persona instance as values.
      new_day: This can take one of the three values.
        1) <Boolean> False -- It is not a "new day" cycle (if it is, we would
           need to call the long term planning sequence for the persona).
        2) <String> "First day" -- It is literally the start of a simulation,
           so not only is it a new day, but also it is the first day.
        2) <String> "New day" -- It is a new day.
      retrieved: dictionary of dictionary. The first layer specifies an event,
                 while the latter layer specifies the "curr_event", "events",
                 and "thoughts" that are relevant.
    OUTPUT
      The target action address of the persona (persona.scratch.act_address).
    """
    from apps.agents.models import ActionPlan

    # PART 1: Generate the hourly schedule.
    # if new_day:
    #     _long_term_planning(persona, new_day)
    # PART 2: If the current action has expired, we want to create a new plan.
    # if agent.scratch.act_check_finished():
    #     _determine_action(agent, maze)
    # PART 3: If you perceived an event that needs to be responded to (saw
    # another agent), and retrieved relevant information.
    # Step 1: Retrieved may have multiple events represented in it. The first
    #         job here is to determine which of the events we want to focus
    #         on for the agent.
    #         <focused_event> takes the form of a dictionary like this:
    #         dictionary {["curr_event"] = <ConceptNode>,
    #                     ["events"] = [<ConceptNode>, ...],
    #                     ["thoughts"] = [<ConceptNode>, ...]}
    # Step 2: Once we choose an event, we need to determine whether the
    #         agent will take any actions for the perceived event. There are
    #         three possible modes of reaction returned by _should_react.
    #         a) "chat with {target_agent.name}"
    #         b) "react"
    #         c) "do not react"
    action_plan = agent.plan

    if finished_move_action(action_plan):
        action_plan.delete()

    if action_plan and action_plan.planned_path:
        return action_plan

    if selected:
        reaction_mode, other_agent = decide_reaction(agent, selected, simulation)
        if reaction_mode != ReactionType.DO_NOT_REACT:
            # If we do want to chat, then we generate conversation
            if reaction_mode == ReactionType.CHAT_WITH:
                # _chat_react(maze, agent, selected, reaction_mode, simulation)

                print(f" plan | existing plan: {action_plan}")

                if action_plan:
                    action_plan.delete()

                chat_message = "Hi"
                target_tile = other_agent.curr_tile()

                print(
                    f"  plan | agents involved | agent: {agent.name} other_agent: {other_agent.name}"
                )

                path = get_shortest_path(agent, maze, [target_tile])
                address = maze.get_address_from_tile(target_tile, "arena")
                print(f"  plan | path: {path}")
                description = f"Chatting with {other_agent.name}"
                pronunciatio = "💬💬💬U+1F4AC"

                agent.chatting_with = other_agent
                action_plan = ActionPlan.objects.create(
                    type=ActionPlanType.MOVE,
                    address=address,
                    description=description,
                    pronunciatio=pronunciatio,
                    chat=chat_message,
                    planned_path=path,
                )
                agent.plan = action_plan
                agent.save()
                return action_plan
            elif reaction_mode == ReactionType.WAIT:
                _wait_react(agent, reaction_mode)
            # elif reaction_mode == "do other things":
            #   _chat_react(agent, focused_event, reaction_mode, agents)

        # if address in maze.address_tiles:
        #     target_tiles = maze.address_tiles[plan]
        # else:
        #     maze.address_tiles[
        #         "Johnson Park:park:park garden"
        #     ]  # ERROR fallback
        # target_tiles = sample_tiles(target_tiles)

    # TODO remember to clean up
    # Step 3: Chat-related state clean up.
    # If the agent is not chatting with anyone, we clean up any of the
    # chat-related states here.
    # if agent.scratch.act_event[1] != "chat with":
    #     agent.scratch.chatting_with = None
    #     agent.scratch.chat = None
    #     agent.scratch.chatting_end_time = None
    # We want to make sure that the agent does not keep conversing with each
    # other in an infinite loop. So, chatting_with_buffer maintains a form of
    # buffer that makes the agent wait from talking to the same target
    # immediately after chatting once. We keep track of the buffer value here.
    # curr_agent_chat_buffer = agent.scratch.chatting_with_buffer
    # for agent_name, buffer_count in curr_agent_chat_buffer.items():
    #     if agent_name != agent.scratch.chatting_with:
    #         agent.scratch.chatting_with_buffer[agent_name] -= 1

    address = random.choice(arena_addresses)
    # print(f"======= plan | random address: {address}")
    target_tiles = list(maze.address_tiles[address])
    print(f" plan | random {agent.curr_tile()}")
    path = get_shortest_path(agent, maze, target_tiles)

    plan = ActionPlan.objects.create(
        type=ActionPlanType.MOVE,
        address=address,
        description="Random",
        pronunciatio="U+1F6B6",
        planned_path=path,
    )
    agent.plan = plan
    agent.save()
    return plan


def decide_reaction(agent, event, simulation):
    # TODO implement
    # reaction = get_weighted_random_choice(
    #     [ReactionType.REACT, ReactionType.WAIT, ReactionType.DO_NOT_REACT, ReactionType.CHAT_WITH],
    #     [0, 0, 0.1, 0.9],
    # )

    return ReactionType.CHAT_WITH, event.agent


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
