
# OpenTutor Backend: Agentic Live Learning Engine

OpenTutor is a real-time, multimodal AI pedagogical agent designed to provide an interactive tutoring experience. This backend serves as a high-performance bridge between student clients and the Gemini 2.0 Live API.

## 🚀 Overview

The backend manages a "Double-WebSocket" architecture:

1. **Student-to-Backend:** A FastAPI-hosted WebSocket that receives raw audio, video frames, and screen-share data from the student.
2. **Backend-to-Gemini:** A persistent connection to Google's Multimodal Live API that processes high-frequency sensory input and generates real-time vocal and tool-based responses.

## 🛠️ Tech Stack

* **Language:** Python 3.13+
* **Framework:** FastAPI (Asynchronous Web Server), Google GenAI and Google ADK
* **AI Engine:** Google Gemini 2.0 Live (Multimodal API)
* **Concurrency:** Python `asyncio` with `TaskGroup` for parallel sensory processing.
* **Package Manager:** `uv` (Recommended) or `pip`.

## 📂 Project Structure

```text
OpenTeacher/
|
|___ backend/
|   ├              
    ├── src/  
    │   ├── web_sockets/
    |   |__ |__ __init__.py
    │   │   └── websocket.py    # APIRouter for frontend WebSocket connections
    │   ├── agent/
    │   │   ├── live_agent.py   # Core logic: manages the Gemini session & tasks
    │   │   ├── prompt.md       # Routes Gemini outputs (Audio vs. Tools)
    │   │   └── tasks.py        # Individual async tasks (Video Send, Audio Recv)
    |   |   |__ tools.py      # Function declarations (Draw, Write, Clear, Search)
    |   |   |__  __init__.py    # this makes my python code an importable python package
    |   |   
    │   └──  main.py             # Entry point; hosts the FastAPI app and routers
    |   
    |____ .dockerignore
    |____ Dockerfile
    |____ pyproject.toml # this host all the dependencies for this project
    |____ .python-version
    |____ uv.lock
    |____ .gitignore 
    └──_ .env                   # Environment variables (API Keys)
|   
|___ Frontend/              # the fromtend
|   |____README.md       # this is for documenting the frontend set up
|
|___docker-compose.yml      # for containerization
|
|___README.md               # documenting the whole project set up both frontend and backend

```


## 🧠 System Architecture & Data Flow

1. **Ingestion:** The backend receives binary chunks (PCM audio/JPEG frames) from the frontend via the `APIRouter` WebSocket.
2. **Forwarding:** These chunks are pushed immediately into the Gemini `live_session` without blocking the main thread.
3. **Dispatching:** A dedicated `Dispatcher` task monitors Gemini's output.
* **Audio:** Pushed to a shared `asyncio.Queue` to be streamed back to the student.
* **Tool Calls:** JSON instructions for `async_draw` or `write_board` are intercepted and forwarded to the frontend to trigger UI updates.



## 🎨 Agent Tools (The Whiteboard API)

The agent is equipped with a custom toolset to interact with the student's workspace:

| Tool | Parameters | Description |
| --- | --- | --- |
| `async_draw` | `shape`, `x`, `y`, `color` | Renders geometric shapes at specific coordinates. |
| `write_board` | `text`, `x`, `y` | Annotates the board with text or formulas. |
| `clear_whiteboard` | None | Resets the student's canvas. |
| `delete_item` | `item_id` | Removes specific objects from the workspace. |
| `Google Search` | `query` | Fetches real-time academic or factual data. |


## ⚙️ Installation & Setup

1. **Clone the Repository:**
```bash
git clone https://github.com/your-repo/opentutor-backend.git
cd opentutor-backend

```
**Note**: python must be installed on your system, 3.13 preferrably because of pyaudio



2. **Set Up Environment:**
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here

```


3.**navigate to the backend directory from the root directory**
```bash 
cd backend
```

4. **Install Dependencies and create a virtual environment:**
Using `uv`:
```bash
uv sync
``` 
this automatically installs all the dependencies and packages

4.**running the agent**
*run the agent*
from the backend directory run the agent using the command
```bash
uv run python -m src.agent.live_agent
```
this will instantiate the live agent, just say "Hi OpenTutor"

you can ask the agent to search anything online or draw a hypothetical shape just for testing



