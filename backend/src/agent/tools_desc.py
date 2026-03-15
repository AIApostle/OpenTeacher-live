
# this is for describing what each does and how to use them for the agent

draw_tool_desc = """
Draws a specific shape on the student's whiteboard. for squares, use a rectangle with equal width and height, each shape_id should be unique, shape ID must start with 'shape' , this are the shapes and their configuration, square 
Draw a geometric shape on the whiteboard.

This tool supports only the shapes provided by the tldraw library.

If the user asks for a shape not listed (for example "circle" or "square"),
convert it to the closest supported shape.

Examples:
circle → ellipse
square → rectangle
box → rectangle
arrow → arrow-right
rectangle
ellipse
triangle
diamond
pentagon
hexagon
octagon
star
rhombus
rhombus-2
oval
trapezoid
cloud
heart
arrow-right
arrow-left
arrow-up
arrow-down
x-box
check-box



id: string
Unique shape ID starting with "shape:"

shape: string
Must be one of the supported shapes

x: number
X position on the whiteboard

y: number
Y position on the whiteboard

width: number
Shape width

height: number
Shape height

Translate user language to supported shapes.

circle → ellipse
square → rectangle (width = height)
box → rectangle
rounded rectangle → rectangle
sphere → ellipse
oval → oval


"""

write_tool_desc =  """
writes letters, numbers, symbols and other things to the whiteboard

"""

move_item_desc = """
this is used to move objects or shapes on the screen
"""

delete_tool_desc = """
deletes selected items on the whiteboard, use their shape_id,text_id or position on screen being shared

"""

clear_tool_desc = """
"Removes all drawings from the whiteboard."

"""

adjust_item_size_desc = """
this is to adjust the size of any object,shape,letters on the whiteboard

"""