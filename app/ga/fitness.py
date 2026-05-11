def calculate_fitness(timetable):

    score = 100

    for entry in timetable:

        start = entry["start_slot"]

        duration = entry["duration"]

        end = start + duration - 1

        # late evening penalty
        if end >= 9:

            score -= 10

        # lunch penalty
        for slot in range(start, end + 1):

            if slot == 5:

                score -= 20

    return score