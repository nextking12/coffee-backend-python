from pydantic import BaseModel, Field
from typing import Optional

class CoffeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Coffee name")
    type: str = Field(..., min_length=1, max_length=50, description="Coffee type")
    origin: str = Field(..., min_length=1, max_length=50, description="Coffee origin")
    grind_size: float = Field(..., min_length=1, max_length=50, description="Grind size")
    weight_in_grams: float = Field(..., gt=0, description="Weight must be positive")

class CoffeeCreate(CoffeeBase):
    pass 

class CoffeeUpdate(CoffeeBase):
   
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    origin: Optional[str] = Field(None, min_length=1, max_length=50)
    grind_size: Optional[float] = Field(None, min_length=1, max_length=50)
    weight_in_grams: Optional[float] = Field(None, gt=0)

class CoffeeResponse(CoffeeBase):
    """
    Schema for API responses
    Like your entity converted to JSON in Java
    """
    id: int
    
    class Config:
        # This allows Pydantic to work with SQLAlchemy models
        # Like @JsonIgnore or custom serialization in Java
        from_attributes = True