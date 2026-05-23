from pydantic import BaseModel, Field
from typing import Dict, Any

class ComponentCreate(BaseModel):
    title: str = Field(..., max_length=50)
    manufacturer: str = Field(..., max_length=50)
    model: str = Field(..., max_length=50)
    warranty_period: int = 0
    price_complete: float = Field(..., gt=0)
    quantity_accessories: int = 0
    specifications: Dict[str, Any] = {}

class ComponentPublic(BaseModel):
    id: int
    name: str
    description: str
    price: float
