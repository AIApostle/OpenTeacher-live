from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Dictionary format: { "client_id": websocket_object }
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"📡 Student {client_id} connected.")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"❌ Student {client_id} disconnected.")

    async def send_personal_message(self, message: dict, client_id: str):
        # Target only ONE specific student
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            import json
            await websocket.send_json(message)
            await websocket.send_text(json.dumps(message))

manager = ConnectionManager()