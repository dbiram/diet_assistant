from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite DB setup
DATABASE_URL = "sqlite:///./diet.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class MealLog(Base):
    __tablename__ = "meal_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    food_name = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    workout_type = Column(String)
    duration_minutes = Column(Float)
    calories_burned = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
