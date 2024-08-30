import init_board
import lvgl as lv
import math
import task_handler

# Colors
ORANGE = lv.color_hex(0xF1C271)
LIGHTGREY = lv.color_hex(0xC8C8C8)
WHITE = lv.color_hex(0xFFFFFF)
BLACK = lv.color_hex(0x000000)
GREEN = lv.color_hex(0x00FF00)
GREY = lv.color_hex(0x808080)

# Global variables
output = ""

# Create active screen
scrn = lv.screen_active()
scrn.set_style_bg_color(BLACK, 0)

# Create output label
output_label = lv.label(scrn)
output_label.set_size(312, 40)
output_label.align(lv.ALIGN.TOP_MID, 0, 2)
output_label.set_style_text_color(WHITE, 0)
# Increase text size using scale
output_label.set_style_text_font(lv.font_default(), 0)
# output_label.set_style_text_scale(200, 0)  # Scale text to 200% of original size

def update_output():
    output_label.set_text(output)

def action(event):
    global output
    btn = event.get_target()
    s = btn.get_child(0).get_text()  # Get text from the label child of the button
    
    if s == "C":
        output = ""
    elif s == "=":
        try:
            output = str(eval(output.replace("^", "**")))[:12]
        except:
            output = "Error"
    else:
        output += s
    
    update_output()

# Create button grid
button_grid = lv.obj(scrn)
button_grid.set_size(312, 192)
button_grid.align(lv.ALIGN.BOTTOM_MID, 0, -2)
button_grid.set_layout(lv.LAYOUT.GRID)
button_grid.set_style_pad_row(4, 0)
button_grid.set_style_pad_column(4, 0)

fields = "789+(" "456-)" "123*^" "C0./="

for j in range(4):
    for i in range(5):
        s = fields[j * 5 + i]
        btn = lv.button(button_grid)
        btn.set_size(60, 44)
        btn.add_event_cb(action, lv.EVENT.CLICKED, None)
        
        if s in "0123456789.":
            btn.set_style_bg_color(LIGHTGREY, 0)
        else:
            btn.set_style_bg_color(ORANGE, 0)
        
        btn.set_style_text_color(BLACK, 0)
        
        label = lv.label(btn)
        label.set_text(s)
        label.center()

        #button_grid.set_grid_cell(btn, j, i, 1, 1)

update_output()

# Task handler
th = task_handler.TaskHandler()