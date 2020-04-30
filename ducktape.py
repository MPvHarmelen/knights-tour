#! /usr/bin/env python3
from god import God
import operations

if __name__ == '__main__':
    ARGV_OVERRIDE = None
    # ARGV_OVERRIDE = [
    #     '1000',
    # ]

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        'n_generations',
        metavar='generations',
        type=int,
    )
    parser.add_argument(
        '-p', '--population-size',
        type=int,
        default=10 ** 3,
    )
    parser.add_argument(
        '-c', '--crossover-probability',
        type=float,
        default=.8
    )
    parser.add_argument(
        '-m', '--mutation-probability',
        type=float,
        default=.005
    )
    generations = God(operations)(**vars(parser.parse_args(ARGV_OVERRIDE)))
    for generation, fitness in enumerate(generations):
        print(generation, fitness)
