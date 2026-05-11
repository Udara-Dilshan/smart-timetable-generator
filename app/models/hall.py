from sqlalchemy import Column, Integer, String
from app.database import Base

class Hall(Base):
    __tablename__ = "halls"

    id = Column(Integer, primary_key=True, index=True)

    hall_name = Column(String, nullable=False)

    hall_type = Column(String)

    capacity = Column(Integer)

    building = Column(String)