import datetime

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket
        print(f'{username} is connected to websocket.')

    async def disconnect(self, username: str):
        self.active_connections.pop(username, None)
        print(f'{username} is disconnected to websocket.')

    async def send_personal_msg(
            self,
            msg: str,
            from_user: str,
            date_time,
            websocket: WebSocket,
    ):
        await websocket.send_json(
            {
                'text': msg,
                "from_user": from_user,
                "datetime": str(date_time),
            }
        )

    async def broadcast(
            self,
            msg: str,
            from_user: str,
            date_time,
    ):
        for connection in self.active_connections.values():
            await connection.send_json(
                {
                    'text': msg,
                    "from": from_user,
                    "datetime": str(date_time),
                }
            )


ws_connector = ConnectionManager()
