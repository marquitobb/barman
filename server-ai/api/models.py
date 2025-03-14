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