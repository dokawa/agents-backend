"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: perceive.py
Description: This defines the "Perceive" module for generative agents.
"""
import math
import sys

from apps.agents.constants import ATTENTION_BANDWIDTH, RETENTION, VISION_RADIUS
from apps.agents.memory_structures.utils import get_embedding

sys.path.append("../../")

from operator import itemgetter


def generate_poig_score(persona, event_type, description):
    # if "is idle" in description:
    #     return 1
    #
    # if event_type == "event":
    #     return run_gpt_prompt_event_poignancy(persona, description)[0]
    # elif event_type == "chat":
    #     return run_gpt_prompt_chat_poignancy(persona,
    #                                          persona.scratch.act_description)[0]
    return None


def perceive(persona, maze):
    """
    Perceives events around the persona and saves it to the memory, both events
    and spaces.

    We first perceive the events nearby the persona, as determined by its
    <vision_r>. If there are a lot of events happening within that radius, we
    take the <att_bandwidth> of the closest events. Finally, we check whether
    any of them are new, as determined by <retention>. If they are new, then we
    save those and return the <ConceptNode> instances for those events.

    INPUT:
      persona: An instance of <Persona> that represents the current persona.
      maze: An instance of <Maze> that represents the current maze in which the
            persona is acting in.
    OUTPUT:
      ret_events: a list of <ConceptNode> that are perceived and new.
    """
    # PERCEIVE SPACE
    # We get the nearby tiles given our current tile and the persona's vision
    # radius.
    nearby_tiles = maze.get_nearby_tiles(persona.curr_tile(), VISION_RADIUS)

    # save_spatial_memory(maze, nearby_tiles, persona)

    perceived_events = get_perceived_events(maze, nearby_tiles, persona)

    ret_events = store_and_get_events(perceived_events, persona)

    return ret_events


def store_and_get_events(perceived_events, persona):
    # Storing events.
    # <ret_events> is a list of <ConceptNode> instances from the persona's
    # associative memory.
    ret_events = []
    for p_event in perceived_events:
        s, p, o, desc = p_event
        if not p:
            # If the object is not present, then we default the event to "idle".
            p = "is"
            o = "idle"
            desc = "idle"
        desc = f"{s.split(':')[-1]} is {desc}"
        p_event = (s, p, o)

        # We retrieve the latest persona.scratch.retention events. If there is
        # something new that is happening (that is, p_event not in latest_events),
        # then we add that event to the a_mem and return it.
        latest_events = persona.a_mem.get_summarized_latest_events(RETENTION)
        if p_event not in latest_events:
            # We start by managing keywords.
            keywords = set()
            sub = p_event[0]
            obj = p_event[2]
            if ":" in p_event[0]:
                sub = p_event[0].split(":")[-1]
            if ":" in p_event[2]:
                obj = p_event[2].split(":")[-1]
            keywords.update([sub, obj])

            # Get event embedding
            # desc_embedding_in = desc
            # if "(" in desc:
            #     desc_embedding_in = (desc_embedding_in.split("(")[1]
            #                          .split(")")[0]
            #                          .strip())
            # if desc_embedding_in in persona.a_mem.embeddings:
            #     event_embedding = persona.a_mem.embeddings[desc_embedding_in]
            # else:
            #     event_embedding = get_embedding(desc_embedding_in)
            # event_embedding_pair = (desc_embedding_in, event_embedding)
            # TODO use the method above
            event_embedding_pair = (None, None)

            # Get event poignancy.
            # Poignancy here is the intensity of perceived importance of the event
            # event_poignancy = generate_poig_score(persona,
            #                                       "event",
            #                                       desc_embedding_in)

            # If we observe the persona's self chat, we include that in the memory
            # of the persona here.
            # TODO use the method above
            event_poignancy = None

            chat_node_ids = []
            if p_event[0] == f"{persona.name}" and p_event[1] == "chat with":
                curr_event = persona.scratch.act_event
                if persona.scratch.act_description in persona.a_mem.embeddings:
                    chat_embedding = persona.a_mem.embeddings[
                        persona.scratch.act_description
                    ]
                else:
                    chat_embedding = get_embedding(persona.scratch.act_description)
                chat_embedding_pair = (persona.scratch.act_description, chat_embedding)
                chat_poignancy = generate_poig_score(
                    persona, "chat", persona.scratch.act_description
                )
                chat_node = persona.a_mem.add_chat(
                    persona.scratch.curr_time,
                    None,
                    curr_event[0],
                    curr_event[1],
                    curr_event[2],
                    persona.scratch.act_description,
                    keywords,
                    chat_poignancy,
                    chat_embedding_pair,
                    persona.scratch.chat,
                )
                chat_node_ids = [chat_node.node_id]

            # Finally, we add the current event to the agent's memory.
            ret_events += [
                persona.a_mem.add_event(
                    persona.scratch.curr_time,
                    None,
                    s,
                    p,
                    o,
                    desc,
                    keywords,
                    event_poignancy,
                    event_embedding_pair,
                    chat_node_ids,
                )
            ]
            # persona.scratch.importance_trigger_curr -= event_poignancy
            persona.scratch.importance_ele_n += 1
    return ret_events


def get_perceived_events(maze, nearby_tiles, persona):
    # PERCEIVE EVENTS.
    # We will perceive events that take place in the same arena as the
    # persona's current arena.
    curr_arena_path = maze.get_tile_path(persona.curr_tile(), "arena")
    print(curr_arena_path)
    # We do not perceive the same event twice (this can happen if an object is
    # extended across multiple tiles).
    percept_events_set = set()
    # We will order our percept based on the distance, with the closest ones
    # getting priorities.
    percept_events_list = []
    # First, we put all events that are occurring in the nearby tiles into the
    # percept_events_list
    for tile in nearby_tiles:
        tile_details = maze.access_tile(tile)

        if tile_details["events"]:
            if maze.get_tile_path(tile, "arena") == curr_arena_path:
                # This calculates the distance between the persona's current tile,
                # and the target tile.
                dist = math.dist(
                    [tile[0], tile[1]],
                    persona.curr_tile(),
                )
                # Add any relevant events to our temp set/list with the distant info.
                for event in tile_details["events"]:
                    if event not in percept_events_set:
                        percept_events_list += [[dist, event]]
                        percept_events_set.add(event)
    # We sort, and perceive only persona.scratch.att_bandwidth of the closest
    # events. If the bandwidth is larger, then it means the persona can perceive
    # more elements within a small area.
    percept_events_list = sorted(percept_events_list, key=itemgetter(0))
    perceived_events = []
    for dist, event in percept_events_list[:ATTENTION_BANDWIDTH]:
        perceived_events += [event]
    return perceived_events
