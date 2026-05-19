from fastapi import APIRouter, Depends

from app.services.user_service import update_username
from app.services.schemas.user_schemas import UserPublic, UserUpdate, UserUpdateResponse
from app.core.security import create_access_token
from dependency import get_current_user, get_db_master


router = APIRouter()


@router.get("/me", response_model=UserPublic)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    """Возвращает профиль текущего пользователя."""
    # current_user уже содержит "username", "role" из токена.
    # created_at пока нет в токене, поэтому для красивого ответа можно либо добавить created_at в токен,
    # либо сходить в БД. Пока что отдадим только username и role.
    # Если нужна дата создания, придётся дёрнуть БД (покажу ниже).
    return UserPublic(username=current_user["user_name"], user_role=current_user["user_role"])



@router.put("/me", response_model=UserUpdateResponse)
def change_my_username(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db_master)
):
    updated = update_username(conn, current_user["user_name"], user_update.new_username)
    # Создаём новый токен с новым username
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