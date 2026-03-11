import asyncio
from google.genai import types
from google import genai



async def draw_on_board(shape: str, x: int, y: int):
    """ this draws on white board"""
    print("drew on the board")
    return "i have drawn on the board"

async def write_on_board(text: str, x: int, y: int):
    """ this writes on the board"""
    print("wrote on the board")
    return "I have written on the board"
async def clear_board():
    """ this clears the white board"""
    print("cleared board")
    return "I have cleared the board"
async def delete_item(item: str, x: int, y: int): 
    """this deletes a particular item on the board"""
    print("deleted the item")
    return "i have deleted the last item"


# mapping to function declaration

WHITEBOARD_TOOL_MAP = {
    "async_draw": draw_on_board,
    "clear_whiteboard": clear_board,
    "write_board": write_on_board,
    "delete_item" : delete_item
}

tools = {"function_declarations" : [
        # Tool 1: The Drawing Tool
        {
            "name": "async_draw",
            "description": "Draws a specific shape on the student's whiteboard.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "shape": {"type": "STRING"},
                    "x": {"type": "INTEGER"},
                    "y": {"type": "INTEGER"}},
                    "required": ["shape", "x", "y"]
                    },
             
            "behavior": "NON_BLOCKING"
        },


        # Tool 2: The Clear Tool 

        {
            "name": "clear_whiteboard",
            "description": "Removes all drawings from the whiteboard.",
            "parameters": {
                "type": "OBJECT",
                "properties": {}, # No arguments needed for clearing
            },
            "behavior": "NON_BLOCKING"
        },


        # Tool 3: The write tool

        {
            "name" : "write_board",
            "description" : "writes letters, numbers, symbols and other things to the whiteboard",
            "parameters" : {
                "type" : "OBJECT",
                "properties" : {
                    "text" : {"type" : "STRING"},
                    "x" : {"type" : "INTEGER"},
                    "y" : {"type" : "INTEGER"}
                }, # will include some properties
                "required" : ["text","x","y"]
            },
            
            "behavior" : "NON_BLOCKING"
        },

        # tool 4: the delete tool

        {
            "name" : "delete_item",
            "description" : "deletes selected items on the whiteboard",
            "parameters" : {
                "type" : "OBJECT",
                "properties" : {
                    "item" : {"type" : "STRING" },
                    "x" : {"type" : "INTEGER"},
                    "y" : {"type" : "INTEGER"}
                },
                "required" : ["item", "x", "y"]
            },
            "behavior" : "NON_BLOCKING"
        }




    ]
}


# tools handler
async def tools_handler(session, tool_call):

    # 1. This list holds ALL your results for this turn
    all_responses = []

    # 2. Loop through every action requested (Parallel Processing)

    for fc in tool_call.function_calls:
        #print(f"AI requested tool: {fc.name} with args: {fc.args}")

        # 3. Look up the actual function in your map
        func = WHITEBOARD_TOOL_MAP.get(fc.name)

        
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
            "response": {"result" : result}    # The data from our Python function
        })

    # 4. SEND EVERYTHING BACK AT ONCE
    # This is the 'Batched' approach that Gemini prefers
    await session.send_tool_response(function_responses=all_responses)
    #await session.send_tool_response(  function_responses=all_responses)
