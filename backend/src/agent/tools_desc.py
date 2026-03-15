


#Draw Shape Tool


draw_tool_desc = """
Draws a geometric shape on the student's whiteboard using Tldraw.

Supported Shapes:
- rectangle
- ellipse
- triangle
- diamond
- pentagon
- hexagon
- octagon
- star
- rhombus
- rhombus-2
- oval
- trapezoid
- cloud
- heart
- arrow-right
- arrow-left
- arrow-up
- arrow-down
- x-box
- check-box

User Input Translation:
If the user requests a shape not directly supported, convert it to the closest supported shape:
- circle → ellipse
- square → rectangle (width = height)
- box → rectangle
- rounded rectangle → rectangle
- sphere → ellipse
- oval → oval
- arrow → arrow-right

Parameters:
- id: string (Required)
    Unique identifier for the shape. Must start with "shape:".
- shape: string (Required)
    Shape type to draw. Must be one of the supported shapes.
- x: number (Required)
    X-coordinate for the shape’s top-left corner.
- y: number (Required)
    Y-coordinate for the shape’s top-left corner.
- width: number (Optional)
    Width of the shape. Defaults to 120.
- height: number (Optional)
    Height of the shape. Defaults to 120.

Notes:
- Ensure `id` is unique per shape; duplicate IDs will overwrite existing shapes.
- If user asks for "circle" or "square", the AI should translate to the corresponding Tldraw supported shape automatically.
- Shapes can be moved or resized after creation using move_item or adjust_item_size tools.
"""

#2. Write Text Tool
write_tool_desc = """
Writes text on the whiteboard.

Parameters:
- id: string (Required)
    Unique identifier for the text object. Must start with "shape:".
- text: string (Required)
    The content to write (letters, numbers, symbols, emojis).
- x: number (Required)
    X-coordinate for the top-left corner of the text box.
- y: number (Required)
    Y-coordinate for the top-left corner of the text box.
- width: number (Optional)
    Width of the text box. Defaults to auto-size.
- height: number (Optional)
    Height of the text box. Defaults to auto-size.
- style: object (Optional)
    Optional styling: font-size, bold, italic, underline, color.

Notes:
- Text will appear immediately at the specified coordinates.
- To simulate handwriting, send text in small chunks or with delays.
- Can later be moved or resized using move_item or adjust_item_size tools.
"""

#3. Move Item Tool
move_item_desc = """
Moves an existing shape or text object to a new position on the whiteboard.

Parameters:
- shape_id: string (Required)
    The ID of the shape or text object to move.
- x: number (Required)
    New X-coordinate for the object.
- y: number (Required)
    New Y-coordinate for the object.

Notes:
- The object must exist; otherwise, the command will be ignored.
- Use this tool for repositioning shapes or text without changing their size.
"""

#4. Delete Tool
delete_tool_desc = """
Deletes a specific object from the whiteboard.

Parameters:
- shape_id: string (Required)
    The ID of the object (shape or text) to delete.

Notes:
- Deletes only the specified object.
- If the shape_id does not exist, the action is ignored.
- Can be combined with clear_board to remove multiple objects at once.
"""

#5. Clear Board Tool
clear_tool_desc = """
Removes all objects (shapes and text) from the whiteboard.

Parameters: None

Notes:
- Deletes everything on the current page.
- Cannot be undone unless objects are re-created.
- Useful to reset the whiteboard quickly.
"""

#6. Adjust Item Size Tool
adjust_item_size_desc = """
Adjusts the width and height of an existing shape or text object.

Parameters:
- shape_id: string (Required)
    The ID of the object to resize.
- width: number (Required)
    New width for the object.
- height: number (Required)
    New height for the object.

Notes:
- Can be used to make shapes larger or smaller.
- For text objects, changing width and height can adjust wrapping and bounding box size.
"""

#7. Draw Curve Tool
draw_curve_tool_desc = """
Draws a freeform curved line on the whiteboard.

Parameters:
- id: string (Required)
    Unique identifier for the curve. Must start with "shape:".
- points: array of {x: number, y: number} (Required)
    Coordinates through which the curve passes.
- stroke_width: number (Optional)
    Thickness of the curve. Default is 2.
- stroke_color: string (Optional)
    Color of the curve. Default is black.

Notes:
- Points define the curve path.
- Can be moved or resized after drawing.
- Can simulate freehand drawing by sending many small segments sequentially.
"""

#8. Draw Straight Line Tool
draw_straight_line_tool_desc = """
Draws a straight line on the whiteboard.

Parameters:
- id: string (Required)
    Unique identifier for the line. Must start with "shape:".
- x1: number (Required)
    Starting X-coordinate of the line.
- y1: number (Required)
    Starting Y-coordinate of the line.
- x2: number (Required)
    Ending X-coordinate of the line.
- y2: number (Required)
    Ending Y-coordinate of the line.
- stroke_width: number (Optional)
    Thickness of the line. Default is 2.
- stroke_color: string (Optional)
    Color of the line. Default is black.

Notes:
- Use this tool for straight edges, connectors, or arrows.
- Can be moved or resized after creation using move_item or adjust_item_size tools.
"""







