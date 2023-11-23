from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.status import HTTP_400_BAD_REQUEST

from src import schemas
from src.auth.user_services import UserSelector, UserService
from src.db.connector import Database


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


@router.post("/login/", response_model=bool, status_code=200)
async def login(user_data: schemas.UserLogin):
    service = UserService()
    result = service.check_user_password(
        db,
        user_data.username,
        user_data.password,
    )
    return result
