from fastapi import APIRouter,WebSocket,WebSocketDisconnect
from ..agent.live_agent import agent
from .connect_manager import manager # Import the manager


router = APIRouter()

# The URL is now: ws://localhost:8000/ws/opentutor/STUDENT_NAME
@router.websocket("/ws/opentutor/{client_id}")
async def opentutor_socket(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    
    try:
        # Pass the client_id to the agent so it knows who it's talking to
        await agent(websocket,client_id) 
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









# --- Middleware ---
# Essential for allowing your Frontend (React/Vue) to talk to the Backend








