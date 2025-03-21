from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DrinkRequest(BaseModel):
    text: str

class Ingredient(BaseModel):
    name: str
    percentage: float
    device: str

class DrinkResponse(BaseModel):
    success: bool
    message: Optional[str]
    name: str
    description: str
    ingredients: List[Ingredient]