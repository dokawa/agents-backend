import random


def get_weighted_random_choice(choices, weights):
    # The weights should sum up to 1
    return random.choices(choices, weights=weights)[0]


def create_chat_event(agent, chat_with, simulation, type):
    from apps.simulations.event_models import Event

    Event.objects.create(
        type=type,
        agent=agent,
        interact_with=chat_with,
        simulation=simulation,
        description=f"Chatting with {chat_with.name}",
        sim_time_created=simulation.current_time(),
        position_x=agent.curr_position_x,
        position_y=agent.curr_position_y,
    )
