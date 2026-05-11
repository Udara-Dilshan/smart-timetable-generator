def select_best(population_results):

    sorted_population = sorted(

        population_results,

        key=lambda x: x["fitness_score"],

        reverse=True
    )

    return sorted_population[:2]