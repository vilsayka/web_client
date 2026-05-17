from fastapi import APIRouter, Depends
from dependency import get_current_user


router = APIRouter()


@router.get("/me")
def read_user_me(current_user: dict = Depends(get_current_user)):
    return current_user