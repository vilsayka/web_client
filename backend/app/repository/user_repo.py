from fastapi import HTTPException
from psycopg2 import errors
from typing import Optional


def get_user(conn, username: str) -> Optional[dict]:
    #try:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id_user, user_name, password_hash, is_active, user_role, created_at "
        "FROM users WHERE user_name = %s",
            (username,)
        )
        row = cur.fetchone()
        if row:
                return {
            "id_user": row[0],
            "user_name": row[1],
            "password_hash": row[2],
            "is_active": row[3],
            "user_role": row[4],
            "created_at": row[5]
        }
        return None
    #finally:
        #conn.close()


def create_user(conn, username: str, hashed_password: str) -> None:
    """Добавляет нового пользователя. Выбрасывает HTTPException 409 при дубликате имени."""
    try:
        with conn.cursor() as cur:
            cur.execute(
            "INSERT INTO users (user_name, password_hash, user_role) "
            "VALUES (%s, %s, 'customer')", (username, hashed_password)
            )
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Username already taken")
    finally:
        conn.close()


def update_user(conn, current_username: str, new_username: str) -> Optional[dict]:
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET user_name = %s WHERE user_name = %s "
                        "RETURNING id_user, user_name, password_hash, is_active, user_role, created_at ",
                        (new_username, current_username))
            row = cur.fetchone()
        conn.commit()
        if row:
            return {
                "id_user": row[0],
                "user_name": row[1],
                "password_hash": row[2],
                "is_active": row[3],
                "user_role": row[4],
                "created_at": row[5]
            }
        return None
    finally:
        conn.close()