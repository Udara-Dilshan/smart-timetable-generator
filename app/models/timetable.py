from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Timetable(Base):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)

    subject_id = Column(Integer, ForeignKey("subjects.id"))

    lecturer_id = Column(Integer, ForeignKey("lecturers.id"))

    hall_id = Column(Integer, ForeignKey("halls.id"))

    day = Column(String)

    start_slot = Column(Integer)

    duration = Column(Integer)