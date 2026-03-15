from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..agent.live_agent import agent
from .connect_manager import manager
import asyncio

router = APIRouter()

@router.websocket("/ws/opentutor/{client_id}")
async def opentutor_socket(websocket: WebSocket, client_id: str):

    await manager.connect(client_id, websocket)

    try:
        while True:

            data = await websocket.receive_json()

            action = data.get("action")

            # START SESSION
            if action == "start_session":

                print(f"Starting AI tutor for {client_id}")

                await agent(websocket,client_id)

              #  asyncio.create_task(
               #     agent(websocket, client_id) )

            # END SESSION
            elif action == "end_session":

                print(f"Ending session for {client_id}")

                # optional: cancel running tasks here

    except WebSocketDisconnect:

        manager.disconnect(client_id)


"""
async def opentutor_socket(websocket: WebSocket):
    await websocket.accept()

    # This calls the "Engine" and passes the student's connection to it
    await agent(websocket)


"""
# what about client id, how to implement it
# --- Middleware ---
# Essential for allowing your Frontend (React/Vue) to talk to the Backend








