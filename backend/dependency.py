

from fastapi import Depends, HTTPException, status
import jwt

from app.repository.user_repo import get_user
from database import get_connection

from fastapi.security import OAuth2PasswordBearer

from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM

def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def get_current_user(token: str = Depends(oauth2_scheme), conn = Depends(get_db)) -> dict:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"},)
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = get_user(conn, username)
    if user is None:
        raise credentials_exception
    return user
