from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from jose import JWTError

from src import schemas
from src.auth.user_services import UserSelector, UserService
from src.db.connector import Database
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

db = Database().connection

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register/", response_model=schemas.UserId, status_code=201)
async def register(user_data: schemas.UserCreate):
    selector = UserSelector()
    service = UserService()
    if selector.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
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
        data={"sub": {"username": user["username"], "is_admin": user["is_admin"]}},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "is_admin": user["is_admin"],
    }


@router.get("/me/", response_model=schemas.UserDisplay)
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = UserSelector().get_user_by_token(db, token)
    except (ValueError, JWTError):
        raise credentials_exception
    if not user:
        raise credentials_exception
    return user
