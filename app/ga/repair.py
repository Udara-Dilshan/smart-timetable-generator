import random

from app.services.conflict_checker import has_conflict


DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]


def repair_timetable(timetable):

    repaired = []

    for entry in timetable:

        valid = False

        while not valid:

            overlap = has_conflict(

                repaired,

                entry
            )

            lecturer_conflict = False

            hall_conflict = False

            for existing in repaired:

                existing_start = existing["start_slot"]

                existing_end = (
                    existing_start +
                    existing["duration"] - 1
                )

                new_start = entry["start_slot"]

                new_end = (
                    new_start +
                    entry["duration"] - 1
                )

                same_day = (
                    existing["day"] ==
                    entry["day"]
                )

                overlap_slots = not (

                    new_end < existing_start
                    or
                    new_start > existing_end
                )

                if same_day and overlap_slots:

                    # lecturer clash
                    if (
                        existing["lecturer_id"] ==
                        entry["lecturer_id"]
                    ):

                        lecturer_conflict = True

                    # hall clash
                    if (
                        existing["hall_id"] ==
                        entry["hall_id"]
                    ):

                        hall_conflict = True

            if (
                not overlap
                and
                not lecturer_conflict
                and
                not hall_conflict
            ):

                repaired.append(entry)

                valid = True

            else:

                # repair by random reassignment
                entry["day"] = random.choice(DAYS)

                entry["start_slot"] = random.randint(1, 7)

    return repaired