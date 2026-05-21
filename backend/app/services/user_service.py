from typing import Optional

from fastapi import HTTPException
from psycopg2 import errors

from app.core.security import hash_password, verify_password
from app.repository.user_repo import create_user, get_user, update_user
from app.repository.importer_repo import get_importer


def authenticate(conn, username: str, password: str) -> Optional[dict]:
    user = get_user(conn, username)
    if not user or not verify_password(password, user["password_hash"]):
        return None
    return user


def register(conn, username: str, password: str) -> dict:
    hashed = hash_password(password)
    try:
        create_user(conn,username,hashed)
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Username is already taken")
    return {"username": username, "user_role": "customer"}


def update_username(conn, current_username: str, new_username: str) -> dict:
    updated = update_user(conn, current_username, new_username)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated





def get_user_profile(conn, username: str, role: str) -> dict:
    user = get_user(conn, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = {
        "username": user["user_name"],
        "user_role": user["user_role"],
        "created_at": user.get("created_at")
    }

    if role == "importer":
        imp = get_importer(conn, user["id_user"])
        if imp:
            profile["full_name"] = imp.get("full_name")
            profile["email"] = imp.get("email")
            profile["telephone"] = imp.get("telephone")
    # для customer/admin ничего дополнительного не добавляем

    return profile