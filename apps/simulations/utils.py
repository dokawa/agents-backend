import csv
import json

from django.contrib.staticfiles import finders
from django.db import models


def get_maze_meta(matrix_path):
    try:
        static_file_path = finders.find(f"{matrix_path}/maze_meta_info.json")
        # Read the content of the file
        with open(static_file_path, "r") as json_file:
            json_meta = json.load(json_file)

        return json_meta
    except FileNotFoundError:
        return None


def read_file_to_list(curr_file, header=False, strip_trail=True):
    """
    Reads in a csv file to a list of list. If header is True, it returns a
    tuple with (header row, all rows)
    ARGS:
      curr_file: path to the current csv file.
    RETURNS:
      List of list where the component lists are the rows of the file.
    """
    if not header:
        analysis_list = []
        with open(curr_file) as f_analysis_file:
            data_reader = csv.reader(f_analysis_file, delimiter=",")
            for count, row in enumerate(data_reader):
                if strip_trail:
                    row = [i.strip() for i in row]
                analysis_list += [row]
        return analysis_list
    else:
        analysis_list = []
        with open(curr_file) as f_analysis_file:
            data_reader = csv.reader(f_analysis_file, delimiter=",")
            for count, row in enumerate(data_reader):
                if strip_trail:
                    row = [i.strip() for i in row]
                analysis_list += [row]
        return analysis_list[0], analysis_list[1:]


def format_simulation_response(starting_step, agents, paths):
    from collections import defaultdict

    response = defaultdict(dict)

    largest_path_length = max((len(path) for path in paths.values() if path), default=0)
    for i in range(starting_step, starting_step + largest_path_length):
        for agent in agents:
            path = paths[agent.name]
            index = i - starting_step
            if path[index] and index < len(path):
                response[index + 1].update(
                    {
                        agent.name: {
                            "movement": path[index],
                            "pronunciatio": "💬💬💬1F4AC",
                        }
                    }
                )
    return response


def format_response(agents, simulation, paths):
    from collections import defaultdict

    response = defaultdict(dict)
    step = simulation.step

    for agent in agents:
        response[step][agent.name] = {"pronunciatio": agent.plan.pronunciatio}
        # if paths[agent.name]:
        #     response[step][agent.name].update({"movement": paths[agent.name]})
        next_tile = paths[agent.name] if paths[agent.name] else agent.curr_tile()
        response[step][agent.name].update({"movement": next_tile})
        response[step][agent.name].update(
            {
                "plan": {
                    "description": agent.plan.description,
                    "duration": agent.plan.duration,
                }
            }
        )

    response["meta"] = simulation.current_time()
    return response


def get_agent_handle(agent_name):
    return agent_name.replace(" ", "_").lower()


class EventType(models.TextChoices):
    MOVEMENT = "movement", "Movement"
    THOUGHT = "thought", "Thought"
    OCCURENCE = "occurence", "Occurence"
    CHAT = "chat", "Chat"
    CHAT_START = "chat_start", "Chat start"
    CHAT_END = "chat_end", "Chat end"
