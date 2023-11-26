import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from src import schemas
from src.exceptions import DoesNotExist
from src.auth.user_services import UserSelector
from src.db.connector import Database
from src.chat.chat_services import ChatSelector, ChatService
from src.ws_manager import ws_connector

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

db = Database().connection

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.get("/", response_model=list[schemas.ChatVerbose])
async def get_all_chats(token: Annotated[str, Depends(oauth2_scheme)]):
    UserSelector().get_admin_by_token_or_403(db, token)
    chats = ChatSelector().get_all_chats_verbose(db)
    return chats


@router.post("/", response_model=schemas.ChatId)
async def create_chat(token: Annotated[str, Depends(oauth2_scheme)]):
    user = UserSelector().get_user_by_token_or_401(db, token)
    chat_id = ChatService().get_or_create_chat_by_customer_id(db, user["id"])
    return chat_id


@router.get("/{chat_id}", response_model=schemas.Chat)
async def get_chat_by_id(
        token: Annotated[str, Depends(oauth2_scheme)], chat_id: int):
    UserSelector().get_admin_by_token_or_403(db, token)
    chat = ChatSelector().get_chat_by_id(db, chat_id)
    if chat is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    return chat


@router.get("/{chat_id}/history", response_model=list[schemas.MessageDisplay])
async def get_chat_history_by_id(
        token: Annotated[str, Depends(oauth2_scheme)], chat_id: int):
    user = UserSelector().get_user_by_token_or_401(db, token)
    chat_selector = ChatSelector()
    if not user["is_admin"]:
        chat = chat_selector.get_chat_by_id(db, chat_id)
        if user["id"] != chat["customer_id"]:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                headers={"WWW-Authenticate": "Bearer"},
            )
    messages = chat_selector.get_chat_history_by_id(db, chat_id)
    return messages


@router.get("/{chat_id}/accept")
async def accept_chat(
        token: Annotated[str, Depends(oauth2_scheme)], chat_id: int):
    admin = UserSelector().get_admin_by_token_or_403(db, token)
    ChatService().link_chat_to_admin(db, chat_id, admin["id"])


@router.websocket("/ws/{chat_id}/{token}")
async def websocket_chat(websocket: WebSocket, chat_id, token):
    user = UserSelector().get_user_by_token(db, token)
    username = user['username']
    user_id = user['id']
    await ws_connector.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            if data:
                date_time = datetime.datetime.utcnow()
                ChatService().insert_message(
                    db, chat_id, user_id, date_time, data)

                opponent = ChatSelector().get_chat_opponent(
                    db, chat_id, user_id)


                await ws_connector.send_personal_msg(
                    msg=data,
                    from_user=username,
                    date_time=date_time,
                    websocket=websocket,
                )
                if opponent_username := opponent["username"]:
                    opponent_ws = ws_connector.active_connections.get(
                        opponent_username)
                    if opponent_ws:
                        await ws_connector.send_personal_msg(
                            msg=data,
                            from_user=username,
                            date_time=date_time,
                            websocket=opponent_ws,
                        )

    except WebSocketDisconnect:
        await ws_connector.disconnect(username=username)


@router.get("/ws/users")
async def get_active_users():
    return {'users': ws_connector.usernames}
