from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class GuaranteeCreate(BaseModel):
    order_id: int
    defective_component_id: int
    problem_description: str = Field(..., min_length=10, max_length=300)

class GuaranteePublic(BaseModel):
    id_repair_warranty: int
    id_order: int
    id_defective_component: int
    date_references: date
    problem_description: str
    status_repair: str
    created_at: datetime
    date_repair_completion: Optional[date] = None