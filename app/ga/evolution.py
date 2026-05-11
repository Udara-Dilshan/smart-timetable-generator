from app.ga.population import generate_population

from app.ga.fitness import calculate_fitness

from app.ga.selection import select_best

from app.ga.crossover import crossover

from app.ga.mutation import mutate

from app.ga.repair import repair_timetable


def evolve_timetable(db, generations=20):

    population = generate_population(db, size=6)

    best_solution = None

    best_fitness = 0

    for generation in range(generations):

        scored_population = []

        for timetable in population:

            repaired_timetable = repair_timetable(
                timetable
            )

            fitness = calculate_fitness(
                repaired_timetable
            )

            scored_population.append({

                "fitness_score": fitness,

                "timetable": repaired_timetable
            })

            # best tracking
            if fitness > best_fitness:

                best_fitness = fitness

                best_solution = repaired_timetable

        # select best
        best = select_best(scored_population)

        parent1 = best[0]["timetable"]

        parent2 = best[1]["timetable"]

        new_population = []

        for _ in range(6):

            child = crossover(parent1, parent2)

            mutated_child = mutate(child)

            repaired_child = repair_timetable(
                mutated_child
            )

            new_population.append(
                repaired_child
            )

        population = new_population

    return {

        "best_fitness": best_fitness,

        "best_timetable": best_solution
    }