from datetime import timezone

from apps.agents.agent.classes import ActionPlanType


def _process_finished_actions(agent, simulation, maze):
    if not agent.plan:
        return

    action_plan = agent.plan

    if finished_move_action(action_plan):
        action_plan.delete()
        agent.plan = None
        agent.save()

    elif finished_idle_action(action_plan, simulation):
        action_plan.delete()
        agent.plan = None
        agent.save()


def finished_move_action(action_plan):
    return (
        action_plan
        and action_plan.type == ActionPlanType.MOVE
        and not action_plan.planned_path
    )


def finished_chat_move_action(action_plan):
    return (
        action_plan
        and action_plan.type == ActionPlanType.CHAT_MOVE
        and not action_plan.planned_path
    )


def finished_idle_action(action_plan, simulation):
    from datetime import timedelta

    return (
        action_plan
        and action_plan.type == ActionPlanType.IDLE
        and action_plan.start_time + timedelta(seconds=action_plan.duration)
        == simulation.current_time().astimezone(timezone.utc)
    )
