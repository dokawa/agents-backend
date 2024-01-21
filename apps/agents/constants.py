# Random setup
import random

SEED = 1337
random.seed(SEED)

COLLISION_BLOCK_ID = 32125

VISION_RADIUS = 8
ATTENTION_BANDWIDTH = 8
RETENTION = 8

EMBEDDING_MODEL = "all-MiniLM-L12-v1"
VECTOR_DIMENSION = 384
MAX_TOKENS = 512

# Associative memory
AGENT_RECENCY_WEIGHT = 1
AGENT_RELEVANCE_WEIGHT = 1
AGENT_IMPORTANCE_WEIGHT = 1
RECENCY_DECAY = 0.995

GLOBAL_RECENCY_WEIGHT = 0.5
GLOBAL_RELEVANCE_WEIGHT = 3
GLOBAL_IMPORTANCE_WEIGHT = 2


# Date
from datetime import datetime

from django.utils import timezone

CHAT_COOLDOWN_IN_MINUTES = 10
INITIAL_DATE = timezone.make_aware(
    datetime(2024, 1, 1), timezone.get_default_timezone()
)


SECONDS_PER_STEP = 10
