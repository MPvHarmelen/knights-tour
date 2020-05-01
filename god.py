import random
import itertools as it

import numpy as np


class God:
    def __init__(self, worker):
        self.worker = worker

    @staticmethod
    def initialise_population(population_size, individual_size):
        """Individual size in bits."""
        return tuple(
            ''.join(random.choice('01') for _ in range(individual_size))
            for _ in range(population_size)
        )

    def __call__(self, population_size, crossover_probability,
                 mutation_probability, n_generations, individual_size=195):
        if population_size % 2:
            raise ValueError("Population size must be divisible by two.")

        population = self.initialise_population(
            population_size, individual_size)
        for generation in range(n_generations):
            fitness = np.fromiter(
                map(self.worker.fitness, population), dtype=int)
            cum_weights = (fitness + 1).cumsum().astype(float)
            cum_weights /= cum_weights.max()
            yield max(fitness)
            population = self.new_population(
                population,
                crossover_probability, mutation_probability,
                cum_weights=cum_weights
            )
        yield max(map(self.worker.fitness, population))

    def new_population(self, population, crossover_probability,
                       mutation_probability, fitness=None, cum_weights=None):
        worker = self.worker
        return tuple(
            worker.mutate(baby, mutation_probability)
            for baby in it.chain.from_iterable(      # babies
                worker.crossover(
                    crossover_probability,
                    *worker.selection(population, cum_weights=cum_weights)
                )
                for _ in range(len(population) // 2)
            )
        )
