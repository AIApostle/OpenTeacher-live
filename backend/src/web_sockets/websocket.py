from fastapi import APIRouter,WebSocket
from ..agent.live_agent import agent


router = APIRouter()

@router.websocket("/ws/opentutor")
async def opentutor_socket(websocket: WebSocket):
    await websocket.accept()

    # This calls the "Engine" and passes the student's connection to it
    await agent(websocket)



# what about client id, how to implement it
# --- Middleware ---
# Essential for allowing your Frontend (React/Vue) to talk to the Backend








