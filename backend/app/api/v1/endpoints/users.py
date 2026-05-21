from fastapi import APIRouter, Depends

from app.services.user_service import update_username, get_user_profile
from app.services.schemas.user_schemas import UserPublic, UserUpdate, UserUpdateResponse
from app.core.security import create_access_token
from dependency import get_current_user, get_db_master, get_db_slave


router = APIRouter()

# @router.get("/me", response_model=UserPublic)
# def get_my_profile(current_user: dict = Depends(get_current_user)):
#     return UserPublic(username=current_user["username"], user_role=current_user["role"])

@router.put("/me", response_model=UserUpdateResponse)
def change_my_username(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_master)
):
    updated = update_username(conn, current_user["username"], user_update.new_username)
    new_token = create_access_token(
        username=updated["user_name"],
        user_role=updated["user_role"]
    )
    return UserUpdateResponse(
        access_token=new_token,
        username=updated["user_name"],
        user_role=updated["user_role"],
        created_at=updated.get("created_at")
    )



@router.get("/me")
def read_my_profile(
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_slave)
):
    return get_user_profile(conn, current_user["username"], current_user["role"])