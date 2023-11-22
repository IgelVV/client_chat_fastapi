from typing import Optional

from datetime import datetime
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    username: str = Field(max_length=50)
    password: str
    is_admin: bool


class Chat(BaseModel):
    id: int
    customer: Optional[User]
    admin: Optional[User]


class Message(BaseModel):
    chat: Chat
    datetime: datetime
    text: str = Field(max_length=500)
