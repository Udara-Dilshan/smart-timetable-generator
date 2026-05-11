import random


def crossover(parent1, parent2):

    child = []

    split = len(parent1) // 2

    child.extend(parent1[:split])

    child.extend(parent2[split:])

    return child