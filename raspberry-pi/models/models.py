
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class MotorRequest(BaseModel):
    device: str
    duration: float

class DrinkRequest(BaseModel):
    ingredients: List[Dict[str, Any]]

class ApiResponse(BaseModel):
    success: bool
    message: str

