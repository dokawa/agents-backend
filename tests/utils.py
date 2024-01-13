import numpy as np

from apps.agents.constants import VECTOR_DIMENSION


def generate_random_normalized_vector():
    np.random.seed()
    random_vector = np.random.rand(VECTOR_DIMENSION)
    normalized_vector = random_vector / np.linalg.norm(random_vector)
    return normalized_vector
