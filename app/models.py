from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()

class Coffee(Base):
    __tablename__ = "espresso_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    type = Column(String(50), nullable=False)
    origin = Column(String(50), nullable=False)
    grind_size = Column(Float, nullable=False)
    weight_in_grams = Column(Float, nullable=False)