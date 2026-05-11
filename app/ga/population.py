from app.services.generator import generate_random_timetable


def generate_population(db, size=5):

    population = []

    for _ in range(size):

        timetable = generate_random_timetable(db)

        population.append(timetable)

    return population