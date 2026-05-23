from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OrderCreate(BaseModel):
    component_ids: List[int] = Field(..., min_length=1)
    warranty_period: int = Field(..., gt=0)

class StatusUpdate(BaseModel):
    new_status: str

class OrderPublic(BaseModel):
    id_order: int
    id_customer: int
    id_importer: Optional[int] = None
    customer_name: Optional[str] = None      
    importer_name: Optional[str] = None      
    status_order: str
    date_assembly: Optional[datetime] = None
    warranty_period: int
    created_at: datetime
    total_price: Optional[float] = None
    components: Optional[List[dict]] = None