from fastapi import FastAPI
from app.database import engine, Base
from app.models.timetable import Timetable
from app.models.faculty import Faculty
from app.models.department import Department
from app.models.lecturer import Lecturer
from app.models.hall import Hall
from app.models.subject import Subject
from app.services.generator import generate_random_timetable
from sqlalchemy.orm import Session
from fastapi import Depends
from app.services.generator import generate_random_timetable
from app.database import get_db
from app.ga.population import generate_population
from app.ga.fitness import calculate_fitness
from app.models.lecturer import Lecturer
from app.models.hall import Hall
from app.models.subject import Subject
from app.models.timetable import Timetable
from app.ga.selection import select_best
from app.ga.crossover import crossover
from app.ga.mutation import mutate
from app.ga.evolution import evolve_timetable

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Smart Scheduler API Running"}

@app.get("/test-db")
def test_db():
    try:
        connection = engine.connect()
        connection.close()
        return {"message": "Database connected successfully"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/generate")
def generate(db: Session = Depends(get_db)):

    timetable = generate_random_timetable(db)

    return {
        "generated_timetable": timetable
    }

@app.get("/seed-data")
def seed_data(db: Session = Depends(get_db)):

    lecturers = [

    Lecturer(

        lecturer_name="Dr. Nimal",

        max_hours_per_day=6,

        preferred_days="Monday,Wednesday",

        unavailable_day="Friday",

        unavailable_slot=6
    ),

    Lecturer(

        lecturer_name="Prof. Sachini",

        max_hours_per_day=5,

        preferred_days="Tuesday,Thursday",

        unavailable_day="Monday",

        unavailable_slot=1
    ),

    Lecturer(

        lecturer_name="Dr. Silva",

        max_hours_per_day=4,

        preferred_days="Friday",

        unavailable_day="Wednesday",

        unavailable_slot=3
    )
]
    halls = [

        Hall(
            hall_name="ICT Lab 01",
            hall_type="ICT Lab",
            capacity=60,
            building="Tech Block"
        ),

        Hall(
            hall_name="Lecture Hall A",
            hall_type="Lecture Hall",
            capacity=120,
            building="Main Block"
        ),

        Hall(
            hall_name="Smart Room 01",
            hall_type="Smart Room",
            capacity=80,
            building="Innovation Block"
        )
    ]

    subjects = [

    Subject(
        subject_code="SE101",
        subject_name="Programming Fundamentals",
        credits=3,
        session_type="Practical",
        preferred_hall_type="ICT Lab"
    ),

    Subject(
        subject_code="SE102",
        subject_name="Database Systems",
        credits=2,
        session_type="Lecture",
        preferred_hall_type="Lecture Hall"
    ),

    Subject(
        subject_code="SE103",
        subject_name="Discrete Mathematics",
        credits=3,
        session_type="Lecture",
        preferred_hall_type="Lecture Hall"
    ),

    Subject(
        subject_code="SE104",
        subject_name="Computer Architecture",
        credits=2,
        session_type="Lecture",
        preferred_hall_type="Smart Room"
    ),

    Subject(
        subject_code="SE105",
        subject_name="Communication Skills",
        credits=1,
        session_type="Lecture",
        preferred_hall_type="Lecture Hall"
    )
]

    db.add_all(lecturers)
    db.add_all(halls)
    db.add_all(subjects)

    db.commit()

    return {
        "message": "Sample data inserted successfully"
    }

@app.get("/view-timetable")
def view_timetable(db: Session = Depends(get_db)):

    timetable = db.query(Timetable).all()

    results = []

    for entry in timetable:

        results.append({

            "id": entry.id,

            "subject_id": entry.subject_id,

            "lecturer_id": entry.lecturer_id,

            "hall_id": entry.hall_id,

            "day": entry.day,

            "start_slot": entry.start_slot,

            "duration": entry.duration
        })

    return {
        "saved_timetable": results
    }

@app.get("/ga-test")
def ga_test(db: Session = Depends(get_db)):

    population = generate_population(db, size=5)

    results = []

    for timetable in population:

        fitness = calculate_fitness(timetable)

        results.append({

            "fitness_score": fitness,

            "timetable": timetable
        })

    return {
        "population": results
    }

@app.get("/ga-evolve")
def ga_evolve(db: Session = Depends(get_db)):

    population = generate_population(db, size=6)

    scored_population = []

    for timetable in population:

        fitness = calculate_fitness(timetable)

        scored_population.append({

            "fitness_score": fitness,

            "timetable": timetable
        })

    # selection
    best = select_best(scored_population)

    parent1 = best[0]["timetable"]

    parent2 = best[1]["timetable"]

    # crossover
    child = crossover(parent1, parent2)

    # mutation
    mutated_child = mutate(child)

    child_fitness = calculate_fitness(mutated_child)

    return {

        "parent_1_fitness": best[0]["fitness_score"],

        "parent_2_fitness": best[1]["fitness_score"],

        "child_fitness": child_fitness,

        "child_timetable": mutated_child
    }

@app.get("/ga-optimize")
def ga_optimize(db: Session = Depends(get_db)):

    result = evolve_timetable(

        db=db,

        generations=30
    )

    return result