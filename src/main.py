from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.connector import Database
from src.auth.user_services import UserSelector
from src import schemas
from src.auth.router import router as auth_router
from src.chat.router import router as chat_router
from src.config import ALLOWED_ORIGINS

db = Database().connection

app = FastAPI(title="Service Chat")


origins = ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/user/{username}", response_model=Optional[schemas.UserDisplay])
async def get_by_username(username: str):
    user = UserSelector().get_user_by_username(db, username)
    return user


app.include_router(auth_router)
app.include_router(chat_router)


@app.on_event("shutdown")
async def shutdown_event():
    Database().close()
