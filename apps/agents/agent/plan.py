"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: plan.py
Description: This defines the "Plan" module for generative agents.
"""
import random

from apps.agents.agent.classes import ReactionType


def plan(agent, simulation, maze, new_day, retrieved):
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
    focused_event = False
    if retrieved.keys():
        focused_event = choose_retrieved(agent, retrieved)

    # Step 2: Once we choose an event, we need to determine whether the
    #         agent will take any actions for the perceived event. There are
    #         three possible modes of reaction returned by _should_react.
    #         a) "chat with {target_agent.name}"
    #         b) "react"
    #         c) False
    if focused_event:
        reaction_mode = should_react(agent, focused_event, simulation)
        if reaction_mode != ReactionType.DO_NOT_REACT:
            # If we do want to chat, then we generate conversation
            if reaction_mode[:9] == "chat with":
                _chat_react(maze, agent, focused_event, reaction_mode, simulation)
            elif reaction_mode[:4] == "wait":
                _wait_react(agent, reaction_mode)
            # elif reaction_mode == "do other things":
            #   _chat_react(agent, focused_event, reaction_mode, agents)

    # Step 3: Chat-related state clean up.
    # If the agent is not chatting with anyone, we clean up any of the
    # chat-related states here.
    if agent.scratch.act_event[1] != "chat with":
        agent.scratch.chatting_with = None
        agent.scratch.chat = None
        agent.scratch.chatting_end_time = None
    # We want to make sure that the agent does not keep conversing with each
    # other in an infinite loop. So, chatting_with_buffer maintains a form of
    # buffer that makes the agent wait from talking to the same target
    # immediately after chatting once. We keep track of the buffer value here.
    curr_agent_chat_buffer = agent.scratch.chatting_with_buffer
    for agent_name, buffer_count in curr_agent_chat_buffer.items():
        if agent_name != agent.scratch.chatting_with:
            agent.scratch.chatting_with_buffer[agent_name] -= 1

    return agent.scratch.act_address


def should_react(agent, focused_event, agents):
    # TODO implement
    return get_weighted_random_choice(
        [ReactionType.REACT, ReactionType.WAIT, ReactionType.DO_NOT_REACT],
        [0.85, 0.1, 0.05],
    )


def get_random_bool(true_percentage):
    random_number = random.randint(0, 99)
    return random_number < true_percentage


def get_weighted_random_choice(choices, weights):
    # The weights should sum up to 1
    return random.choices(choices, weights=weights)[0]
