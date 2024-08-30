import init_board
import lvgl as lv
import task_handler
import math

CANVAS_WIDTH  = 240
CANVAS_HEIGHT = 240

# Get the active screen
scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0x101010), 0)

label_num = lv.draw_label_dsc_t()
label_num.init()
label_num.color = lv.color_hex(0xFFFFFF)

W = const(240)
H = const(240)
R = const(120)
CX = const(120)
CY = const(120)

#create canvas
cbuf=bytearray(CANVAS_WIDTH * CANVAS_HEIGHT * 2)
canvas = lv.canvas(scrn)
canvas.set_buffer(cbuf,CANVAS_WIDTH,CANVAS_HEIGHT, lv.COLOR_FORMAT.RGB565)
canvas.align(lv.ALIGN.CENTER,0,0)
canvas.fill_bg(lv.color_hex(0xFFFFFF), lv.OPA.COVER);
canvas.transform(canvas, 45, LV_IMG_ZOOM_NONE, 0, 0, CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, True)

label_num_style_MAIN = lv.style_t()
label_num_style_MAIN.init()
label_num_style_MAIN.set_text_color(lv.color_hex(0xFF0000))

def drawRotRect(w, r1, r2, angle, c):
    w2, ll, a = w // 2, r2 - r1, (angle + 270) * (math.pi / 180)
    coord = array.array("h", [0, -w2, ll, -w2, ll, w2, 0, w2])
    x, y = math.ceil(W // 2 + r1 * math.cos(a)), math.ceil(
        H // 2 + r1 * math.sin(a)
    )
    g.poly(x, y, coord, c, True, a)

def dial():
    label_nums = {}
    r = R - 10
    for i in range(1, 13):
        a = i * math.pi / 180
        x = CX + math.ceil(math.sin(a * 30) * r)
        y = CY - math.ceil(math.cos(a * 30) * r)
        if i == 12 or i == 11 or i == 1:
            y += 3
        s = str(i)
        label_nums[i] = lv.label(canvas)
        label_nums[i].set_x(x)
        label_nums[i].set_y(y)
        label_nums[i].set_text(s)
        label_nums[i].add_style(label_num_style_MAIN, lv.PART.MAIN)
        
dial()

# Set up task handler
th = task_handler.TaskHandler()