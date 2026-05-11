from sqlalchemy import Column, Integer, String
from app.database import Base

class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    faculty_name = Column(String, unique=True, nullable=False)