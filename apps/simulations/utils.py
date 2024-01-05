import csv
import json

from django.contrib.staticfiles import finders


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


def format_step_response(starting_step, agents, paths):
    from collections import defaultdict

    response = defaultdict(dict)

    print(paths)
    largest_path_length = max((len(path) for path in paths.values() if path))
    for i in range(starting_step, starting_step + largest_path_length):
        for agent in agents:
            path = paths[agent.name]
            index = i - starting_step
            if path and index < len(path):
                response[index].update({agent.name: path[index]})
    return response


def get_agent_handle(agent_name):
    return agent_name.replace(" ", "_").lower()
