from typing import Optional

from datetime import datetime
from pydantic import BaseModel, Field


class UserId(BaseModel):
    id: int


class UserDisplay(UserId):
    username: str = Field(max_length=50)
    is_admin: bool


class UserLogin(BaseModel):
    username: str = Field(max_length=50)
    password: str


class UserCreate(UserLogin):
    username: str = Field(max_length=50)
    password: str
    is_admin: bool


class User(UserCreate):
    id: int


class Chat(BaseModel):
    id: int
    customer: Optional[User]
    admin: Optional[User]


class Message(BaseModel):
    chat: Chat
    datetime: datetime
    text: str = Field(max_length=500)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
