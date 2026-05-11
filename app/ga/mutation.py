import random


DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]


def mutate(timetable):

    random_entry = random.choice(timetable)

    random_entry["day"] = random.choice(DAYS)

    random_entry["start_slot"] = random.randint(1, 7)

    return timetable