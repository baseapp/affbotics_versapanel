import init_board
import lvgl as lv

scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0x000000), 0)

def on_value_changed(_):
    print('VALUE_CHANGED:', slider.get_value())


slider = lv.slider(scrn)
slider.set_size(200, 20)
slider.center()
slider.add_event_cb(on_value_changed, lv.EVENT.VALUE_CHANGED, None)

label = lv.label(scrn)
label.set_text('HELLO WORLD!')
label.align(lv.ALIGN.CENTER, 0, -50)

import task_handler

th = task_handler.TaskHandler()