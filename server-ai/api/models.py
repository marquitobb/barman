from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Command(BaseModel):
    text: str

class Step(BaseModel):
    device: str
    duration: float
    description: str

class DrinkInstructions(BaseModel):
    name: str
    description: str
    steps: List[Step]

class DrinkRequest(BaseModel):
    text: str

class Ingredient(BaseModel):
    name: str
    percentage: float
    device: str

class DrinkResponse(BaseModel):
    success: bool = False
    message: Optional[str]
    name: str
    description: str
    ingredients: List[Ingredient]

class Motor(BaseModel):
    id: int
    name: str
    content: str
    device: str
    capacity: float
    current_level: float

class MotorUpdate(BaseModel):
    content: str