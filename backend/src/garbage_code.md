


await session.send_tool_response(
                    types.LiveClientToolResponse(
                        function_responses=[
                            types.LiveClientFunctionResponse(
                                name=call.name,
                                id=call.id,
                                response=result
                            )
                        ]
                    )
                )




async def receive_from_gemini(session):
    async for response in session.receive():
        # Handle Tool Calls
        if response.tool_call:
            for call in response.tool_call.function_calls:
                # 1. Execute your local function
                result = []
                
                # 2. Send the result back so the model can continue speaking
                await session.send_tool_response(
                    types.LiveClientToolResponse(
                        function_responses=[
                            types.LiveClientFunctionResponse(
                                name=call.name,
                                id=call.id,
                                response=result
                            )
                        ]
                    )
                )


async def tools_handler(session, tool_call):
    # 1. This list holds ALL your results for this turn
    all_responses = []

    # 2. Loop through every action requested (Parallel Processing)
    for fc in WHITEBOARD_TOOL_MAP.function_calls:
        
        if fc.name == "async_draw":
            # Unpack Gemini's args and run your Python code
            result = await draw_on_board(**fc.args)
        
        elif fc.name == "write_board":
            result = await write_on_board(**fc.args)
            
        elif fc.name == "clear_whiteboard":
            result = await clear_board()
        elif fc.name == "delete_item":
            result = await delete_item(**fc.args)
        
        # 3. Add this specific 'Receipt' to our batch list
        all_responses.append({
            "name": fc.name,
            "id": fc.id,           # Critical: Match the ID Gemini gave us
            "response": result      # The data from our Python function
        })

    # 4. SEND EVERYTHING BACK AT ONCE
    # This is the 'Batched' approach that Gemini prefers
    await session.send_tool_response(function_responses=all_responses)

#run tools
async def run_tools(session):
    async for response in session.receive():
        if response.tool_call:
            # This is where you call your Python functions!
            await tools_handler(session, response.tool_call)

"""
async def receive_from_gemini(session):
    '''
    Background worker that routes Gemini's responses to the right place.
    '''
    while True:
        async for response in session.receive():
            # A. HANDLE TOOLS (Whiteboard/Agentic Actions)
            if response.tool_call:
                # We call your tools_handler here
                await tools_handler(session, response.tool_call)
            
            # B. HANDLE AUDIO (AI Speaking)
            #while True:
        # turn = session.receive()
        # async for response in turn:
            if (response.server_content and response.server_content.model_turn):
                for part in response.server_content.model_turn.parts:
                    if part.inline_data and isinstance(part.inline_data.data, bytes):
                        await audio_queue_output.put(part.inline_data.data)

                

            # Empty the queue on interruption to stop playback
            while not audio_queue_output.empty():
                audio_queue_output.get_nowait()
"""
"""
        if message.server_content and message.server_content.model_turn:
            parts = message.server_content.model_turn.parts
            for part in parts:
                if part.inline_data and isinstance(part.inline_data.data, bytes):
                    # Put audio bytes into a queue for play_ai_audio() to handle
                    audio_queue_output.put_nowait(part.inline_data.data)
"""
"""
async def receive_from_gemini(session):
    '''
    Background worker that routes responses (Audio & Tools).
    '''
    async for response in session.receive():
        # 1. Access the model turn data
        if response.server_content and response.server_content.model_turn:
            parts = response.server_content.model_turn.parts
            
            for part in parts:
                # ROUTE A: Handle Tool Calls (Function Calling)
                if part.call: 
                    # 'part.call' contains the tool name and arguments
                    await tools_handler(session, part.call)
                
                # ROUTE B: Handle Audio (AI Speaking)
                elif part.inline_data:
                    # Audio bytes are stored in part.inline_data.data
                    audio_data = part.inline_data.data
                    await audio_queue_output.put(audio_data)

        # 2. Handle Interruptions (Optional but recommended)
        # If the user speaks, clear the output queue to stop "stale" AI audio
        if response.server_content and response.server_content.interrupted:
            while not audio_queue_output.empty():
                try:
                    audio_queue_output.get_nowait()
                except Exception:
                    break
"""

        # Handle Audio (as you already have)
        if response.server_content and response.server_content.model_turn:
            for part in response.server_content.model_turn.parts:
                if part.inline_data:
                    await audio_queue_output.put(part.inline_data.data)




"""
def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())

"""


   tg.create_task(listen_to_audio())
                tg.create_task(send_live_video(live_session))
                tg.create_task(send_realtime_audio(live_session))
                tg.create_task(receive_response_from_ai(live_session))
                #tg.create_task(receive_from_gemini(live_session))
                tg.create_task(play_ai_audio())
                tg.create_task(share_screen(live_session))
                #tg.create_task(run_tools(live_session))



    #for fc in WHITEBOARD_TOOL_MAP.function_calls:
    '''
    for part in tool_call.candidates[0].content.parts:
        if not part.function_call:
            continue
        fc = part.function_call
        result = None
    ''' 



       # if not response.tool_call:
        #return




        from fastapi import APIRouter,WebSocket,WebSocketDisconnect
from ..agent.live_agent import agent
from .connect_manager import manager # Import the manager


router = APIRouter()

# The URL is now: ws://localhost:8000/ws/opentutor/STUDENT_NAME
@router.websocket("/ws/opentutor/{client_id}")
async def opentutor_socket(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    
    try:
        # Passes the client_id to the agent so it knows who it's talking to
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








