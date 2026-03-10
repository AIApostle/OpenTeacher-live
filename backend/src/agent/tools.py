import asyncio


async def draw_on_board(shape: str, x: int, y: int):
    """ this draws on white board"""
    pass

async def write_on_board(text: str, x: int, y: int):
    """ this writes on the board"""
    pass
async def clear_board():
    """ this clears the white board"""
    pass
async def delete_item(item: str, x: int, y: int): 
    """this deletes a particular item on the board"""
    pass
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
                    "y": {"type": "INTEGER"},
                    "color": {"type": "STRING"}
                },
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
            },
            "required" : ["text","x","y"], # willl add required
            "behaviour" : "NON_BLOCKING"
        }
    ]
}


def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())
