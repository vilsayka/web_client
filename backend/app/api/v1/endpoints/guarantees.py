from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.services.guarantee_service import create_guarantee, get_service_guarantees_for_user
from app.services.schemas.guarantee import GuaranteeCreate, GuaranteePublic
from dependency import get_current_user, get_db_master


router = APIRouter()

@router.post("/", response_model=GuaranteePublic, status_code=201)
def create_guarantee_request(
    req: GuaranteeCreate,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_master)
):
    """Создать обращение по гарантии (только для заказчика)."""
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can create guarantee requests")
    return create_guarantee(conn, current_user["user_id"], req.model_dump())


@router.get("/", response_model=List[GuaranteePublic])
def get_my_guarantees(
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_master)
):
    if current_user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can view their guarantee requests")
    return get_service_guarantees_for_user(conn, current_user["user_id"])