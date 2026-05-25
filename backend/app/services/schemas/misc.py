from pydantic import BaseModel

class CompatibilityRequest(BaseModel):
    component_ids: list[int]

class CompatibilityResponse(BaseModel):
    compatible: bool
    conflicts: list[str] = []