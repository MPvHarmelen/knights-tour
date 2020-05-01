"""
Moves are coded like we do circles and pi and sine and stuff:
- +2, +1
- +1, +2
- -1, +2
- -2, +1
- -2, -1
- -1, -2
- +1, -2
- +2, -1
"""
import random
import numpy as np

INITIAL_POSITION = {
    f'{x:0>3b}{y:0>3b}': np.array([x, y])
    for x in range(8)
    for y in range(8)
}

MOVE_TO_CHANGE = {
    '000': np.array([+2, +1]),
    '001': np.array([+1, +2]),
    '010': np.array([-1, +2]),
    '011': np.array([-2, +1]),
    '100': np.array([-2, -1]),
    '101': np.array([-1, -2]),
    '110': np.array([+1, -2]),
    '111': np.array([+2, -1]),
}


def fitness(individual: str):
    position = INITIAL_POSITION[individual[:6]].copy()

    positions = {tuple(position)}

    for i in range(6, len(individual), 3):
        position += MOVE_TO_CHANGE[individual[i:i+3]]
        p = tuple(position)
        if position.max() >= 8 or position.min() < 0 or p in positions:
            # Illegal position or repetition
            break
        positions.add(p)

    return len(positions) - 1


def selection(population, fitness=None, cum_weights=None):
    if cum_weights is None:
        fitness = np.asarray(fitness) + 1
        cum_weights = fitness.cumsum().astype(float)
        cum_weights /= cum_weights.max()
    return random.choices(population, cum_weights=cum_weights, k=2)


def crossover(probability, clara, lucy):
    if random.random() < probability:
        pt = random.choice(range(1, len(clara)))
        clara, lucy = clara[:pt] + lucy[pt:], lucy[:pt] + clara[pt:]
    return clara, lucy


def mutate(individual, probability):
    indices = np.nonzero(
        np.random.uniform(size=len(individual)) < probability
    )[0]
    chunks = []
    head = 0
    for i in indices:
        chunks.append(individual[head:i])
        chunks.append('0' if individual[i] == '1' else '1')
        head = i + 1
    chunks.append(individual[head:len(individual)])
    return ''.join(chunks)
