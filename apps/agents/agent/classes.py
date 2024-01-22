from django.db import models


class ReactionType(models.TextChoices):
    DO_NOT_REACT = "do_not_react", "Do not react"
    START_CHAT = "start_chat", "Start chat"
    CONTINUE_CHAT = "continue_chat", "Continue chat"
    WAIT_RESPONSE = "wait_response", "Wait response"
    END_CHAT = "end_chat", "End chat"


class ActionPlanType(models.TextChoices):
    IDLE = "wait", "Wait"
    MOVE = "move", "Move"
    CHAT_MOVE = "chat_move", "Chat move"
