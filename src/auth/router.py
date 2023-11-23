from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from src import schemas
from src.auth.user_services import UserSelector, UserService
from src.db.connector import Database
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES


db = Database().connection

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register/", response_model=schemas.LiteUser, status_code=201)
async def register(user_data: schemas.UserCreate):
    selector = UserSelector()
    service = UserService()
    if selector.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this username already exists.",
        )
    user_id = service.create_user(
        db,
        username=user_data.username,
        password=user_data.password,
        is_admin=user_data.is_admin,
    )
    return user_id


@router.post("/login/", response_model=schemas.Token, status_code=200)
async def login(user_data: OAuth2PasswordRequestForm = Depends()):
    service = UserService()
    user = service.authenticate(
        db,
        user_data.username,
        user_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

