
## Running the Frontend Locally (recommended)

This guide explains how to run the OpenTutor Frontend locally for development.

The frontend is built using:

React

Vite

tldraw

It connects to the backend through a WebSocket.

## 1. Prerequisites

Make sure you have the following installed:

Node.js (version 18 or higher)

npm (comes with Node.js)

Git

## Check installation:

node -v
npm -v

## 2. Clone the Repository
git clone https://github.com/your-repo/opentutor-frontend.git
cd opentutor-frontend

## 3. Install Dependencies

Install all required packages (including tldraw):

npm install


This installs everything listed in package.json.

## 4. Start the Development Server

Run the frontend locally:

npm run dev


This will start the development server.

You should see something like:

VITE v5.x.x  ready in 300 ms

➜  Local:   http://localhost:5173/

## 5. Open the Application

Open your browser and go to:

http://localhost:5173


You should now see the OpenTutor whiteboard interface.

## 6. Backend Requirement

The frontend communicates with the backend through a WebSocket connection.

Make sure the backend is running at:

http://localhost:8000


Example WebSocket endpoint used in the frontend:

ws://localhost:8000/ws/opentutor/{client_id}


**Example:**

ws://localhost:8000/ws/opentutor/Saviour

## 7. Starting a Session

Open the whiteboard.

Click Start Session.

The frontend will connect to the backend WebSocket.

The AI teacher can now draw and write on the whiteboard.

Project Structure
opentutor-frontend
│
├── src
│   ├── App.jsx
│   ├── main.jsx
│
├── public
│
├── package.json
├── vite.config.js
└── README.md

Common Issues
Node Version Too Old

If you see errors installing dependencies, check Node version:

node -v


Install the latest version from:

https://nodejs.org

WebSocket Not Connecting

Make sure the backend is running:

http://localhost:8000

Port Already in Use

If port 5173 is busy, Vite will automatically select another port.

Example:

http://localhost:5174

Development Notes

This mode uses Vite's development server, which provides:

Hot reload

Fast builds

Live updates during development

This setup is recommended for local development and debugging.
