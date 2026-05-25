

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError
import jwt

from app.repository.user_repo import get_user
from database import get_master_connection, get_slave_connection

#from fastapi.security import OAuth2PasswordBearer

from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM

def get_db_master():
    conn = get_master_connection()
    try:
        yield conn
    finally:
        conn.close()


def get_db_slave():
    conn = get_slave_connection()
    try:
        yield conn
    finally:
        conn.close()


# def get_current_user(token: str = Depends(oauth2_scheme), conn = Depends(get_db_slave)) -> dict:
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                           detail="Could not validate credentials",
#                                           headers={"WWW-Authenticate": "Bearer"},)
#     try: 
#         payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
#         username: str = payload.get("sub")
#         print(payload)
#         if username is None:
#             raise credentials_exception
#     except jwt.PyJWTError:
#         raise credentials_exception
    
#     user = get_user(conn, username)
#     if user is None:
#         raise credentials_exception
#     return user

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> dict:
    """Извлекает токен, проверяет его и возвращает пользователя из payload."""
    token = credentials.credentials  # получаем строку токена
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("user_role")
        user_id: int = payload.get("user_id")  
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username": username, "role": role, "user_id" : user_id}


def require_role(*allowed_roles: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions. Недостаточно прав.")
        return current_user
    return role_checker


require_admin = require_role("admin")
require_customer = require_role("customer")
require_importer = require_role("importer")
