from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src import schemas
from src.auth.user_services import UserSelector, UserService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register/", response_model=schemas.LiteUser, status_code=201)
async def register(user_data: schemas.UserCreate):
    selector = UserSelector()
    service = UserService()
    if selector.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this username already exists.",
        )
    user_id = service.create_user(
        username=user_data.username,
        password=user_data.password,
        is_admin=user_data.is_admin,
    )
    return user_id
