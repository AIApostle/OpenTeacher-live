from fastapi import FastAPI,websockets,WebSocketDisconnect,WebSocketException
from .web_sockets.websocket import router as routes
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes)

@app.get("/")
async def health_check():
    return {"status": "online", "message": "OpenTutor Engine is running"}
    

if __name__ == "__main__":
    # Runs the server on localhost:8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)






























