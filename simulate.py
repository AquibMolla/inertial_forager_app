# simulate.py

import numpy as np
from numba import njit

@njit
def simulate_forager(width, height, max_energy, laziness, max_steps=100000):
    space = np.ones((width + 1, height + 1), dtype=np.uint8)
    x = y = width // 2
    space[x, y] = 0  # Start position is eaten

    path = np.empty((max_steps, 2), dtype=np.int32)
    energy_track = np.empty(max_steps, dtype=np.int32)

    path[0, 0], path[0, 1] = x, y
    energy = max_energy
    energy_track[0] = energy
    step = 1
    is_resting = False

    dirs = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])

    while energy > 0 and step < max_steps:
        energy -= 1

        if is_resting:
            if np.random.rand() > laziness:
                is_resting = False
        else:
            move = dirs[np.random.randint(0, 4)]
            x = min(max(0, x + move[0]), width)
            y = min(max(0, y + move[1]), height)

            if space[x, y]:
                space[x, y] = 0
                energy = max_energy
                if np.random.rand() < laziness:
                    is_resting = True

        path[step, 0], path[step, 1] = x, y
        energy_track[step] = energy
        step += 1

    return path[:step], energy_track[:step], space
