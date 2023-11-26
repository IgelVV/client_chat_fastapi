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
    customer_id: Optional[int]
    admin_id: Optional[int]


class ChatId(BaseModel):
    id: int


class ChatVerbose(BaseModel):
    id: int
    customer: Optional[str]
    admin: Optional[str]


class Message(BaseModel):
    id: int
    chat_id: int
    from_user_id: int
    datetime: datetime
    text: str = Field(max_length=500)


class MessageDisplay(BaseModel):
    text: str
    from_user: str
    datetime: datetime


class MessagePost(BaseModel):
    chat_id: int
    datetime: Optional[datetime]
    text: str = Field(max_length=500)


class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool


class TokenData(BaseModel):
    username: str | None = None
