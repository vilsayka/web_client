from fastapi import APIRouter, Depends, HTTPException
  # создадим ниже
from app.services.component_service import get_component
from app.services.schemas.misc import CompatibilityRequest, CompatibilityResponse
from app.services.compatibility import perform_compatibility_check
from dependency import get_db_slave


router = APIRouter()

@router.post("/check", response_model=CompatibilityResponse)
def check_compatibility(request: CompatibilityRequest, conn = Depends(get_db_slave)):
    # Загрузим все компоненты по их id
    components = []
    for cid in request.component_ids:
        comp = get_component(conn, cid)
        if not comp:
            raise HTTPException(status_code=404, detail=f"Component with id {cid} not found")
        components.append(comp)
    
    conflicts = perform_compatibility_check(components)
    return CompatibilityResponse(
        compatible=len(conflicts) == 0,
        conflicts=conflicts
    )