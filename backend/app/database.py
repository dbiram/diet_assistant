from sqlalchemy import Column, Integer, String, Float, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DB_PATH =  "/var/data/diet.db"

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
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

class LLMLog(Base):
    __tablename__ = "llm_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    prompt = Column(Text)
    response = Column(Text)
    tokens_in = Column(Integer)
    tokens_out = Column(Integer)
    latency_seconds = Column(Float)
    model = Column(String)
    status = Column(String)  
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()