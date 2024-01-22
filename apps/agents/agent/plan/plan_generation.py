import random

from apps.agents.agent.classes import ActionPlanType
from apps.agents.agent.plan.utils import get_weighted_random_choice
from apps.agents.constants import SECONDS_PER_STEP
from apps.agents.path.utils import get_shortest_path
from apps.agents.utils import store_addresses


def _generate_idle_plan(agent, simulation):
    from apps.agents.models import ActionPlan

    description = "Idle"
    pronunciatio = "231B"

    plan = ActionPlan.objects.create(
        type=ActionPlanType.IDLE,
        simulation=simulation,
        start_time=simulation.current_time(),
        duration=random.randint(1, 4) * SECONDS_PER_STEP,
        description=description,
        pronunciatio=pronunciatio,
    )

    agent.plan = plan
    agent.save()
    return plan


def _generate_chat_plan(agent, other_agent, simulation, maze):
    from apps.agents.models import ActionPlan

    #
    chat_message = "Hi"
    target_tiles = maze.get_nearby_tiles(
        other_agent.curr_tile(), 1, include_reference_tile=False
    )

    path = get_shortest_path(agent, maze, target_tiles)

    address = maze.get_address_from_tile(other_agent.curr_tile(), "arena")
    description = f"Chat with {other_agent.name}"
    pronunciatio = "1F4AC"

    plan = ActionPlan.objects.create(
        type=ActionPlanType.CHAT_MOVE,
        simulation=simulation,
        start_time=simulation.current_time(),
        address=address,
        description=description,
        pronunciatio=pronunciatio,
        chat=chat_message,
        planned_path=path,
        interact_with=other_agent,
    )
    agent.plan = plan
    agent.save()

    return plan


def _generate_wait_response_plan(agent, simulation):
    from apps.agents.models import ActionPlan

    description = "Waiting chat response"
    pronunciatio = "1F5E8"

    plan = ActionPlan.objects.create(
        type=ActionPlanType.IDLE,
        simulation=simulation,
        start_time=simulation.current_time(),
        duration=random.randint(1, 4) * SECONDS_PER_STEP,
        description=description,
        pronunciatio=pronunciatio,
    )

    agent.plan = plan
    agent.save()

    return plan


def _generate_random_plan(agent, simulation, maze):
    from apps.agents.models import ActionPlan

    reaction_type = get_weighted_random_choice(
        [ActionPlanType.IDLE, ActionPlanType.MOVE], [0.5, 0.5]
    )
    # reaction_type = ActionPlanType.MOVE

    if reaction_type == ActionPlanType.MOVE:
        address = random.choice(store_addresses)
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
