from django.db import models


class ReactionType(models.TextChoices):
    WAIT = "wait", "Wait"
    REACT = "react", "React"
    DO_NOT_REACT = "do_not_react", "Do not react"
    CHAT_WITH = "chat_with", "Chat with"


class ActionPlanType(models.TextChoices):
    WAIT = "wait", "Wait"
    MOVE = "move", "Move"
    DO_NOT_REACT = "do_not_react", "Do not react"
    CHAT_WITH = "chat_with", "Chat with"
