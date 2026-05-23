




from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.schemas.user_schemas import Token, UserCreate, UserPublic
from app.core.security import create_access_token
from app.services.user_service import authenticate, register
from dependency import get_db_master, get_db_slave
    
router = APIRouter()


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
           conn = Depends(get_db_slave)):
    user = authenticate(conn, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    #access_token = create_access_token(data={"sub" : user["user_name"], "user_role" : user["user_role"]})
    access_token = create_access_token(username=user["user_name"], user_role=user["user_role"], user_id=user["id_user"])
    return Token(access_token=access_token)


@router.post("/register", response_model=UserPublic, status_code=201) #201 - успешное создание ресурса
def register_user(user_in: UserCreate, conn = Depends(get_db_master)): #response_model - то что возвращается в ответе
    new_user = register(conn, user_in.username, user_in.password)
    return UserPublic(username=new_user["username"], user_role=new_user["user_role"])
