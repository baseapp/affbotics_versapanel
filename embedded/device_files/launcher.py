import init_board
import network
from machine import Pin
import time
import _thread
import os
import lvgl as lv
import usys as sys
#import fs_driver

import versaos
import welcome
import apps

app = 0
app_old = 1
app_ring = []
selected_app = 0
app_event_triggered = False
button_itr_triggered = False

app_list = os.listdir('apps')
app_ring = [app.replace('.py', '') for app in app_list if app.endswith('.py')]
app_buttons = []

user_loop_module = None
user_lock = _thread.allocate_lock()
_thread.stack_size(8192)

pause_thread = False

def file_exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

def user_app_loop():
    global user_loop_module
    
    while(1):
        time.sleep_ms(50) # TODO: Add 50ms delay if the user loop dont have any delays
        if(pause_thread):
            continue
        with user_lock:
            if(callable(user_loop_module)):
                user_loop_module()

user_loop_thread = _thread.start_new_thread(user_app_loop, ())

def start_app(app_num):
    global user_loop_module
    global pause_thread

    main_module = __import__("apps." + app_ring[app_num])
    module = getattr(main_module, app_ring[app_num])

    if hasattr(module, 'drawScreen'):
            module.drawScreen()
    else:
        print(f"{app_ring[app_num]}.py does not have an drawScreen() function")
    
    pause_thread = True
    # Set the loop function to call the active app's loop function
    if hasattr(module, 'loop_task'):
        with user_lock:
            user_loop_module = module.loop_task
    else:
        with user_lock:
            user_loop_module = None
        print(f"{app_ring[app]}.py does not have loop_task(); ignoring")
    pause_thread = False

def close_app(app_num):
    global user_loop_module
    global pause_thread

    pause_thread = True
    with user_lock:
        user_loop_module = None
    pause_thread = False

    main_module = __import__("apps." + app_ring[app_num])
    module = getattr(main_module, app_ring[app_num])

    if hasattr(module, 'drawScreen'):
            module.clearScreen()
    else:
        print(f"{app_ring[app_num]}.py does not have an clearScreen() function")


def event_app_icon_cb(evnt):
    global selected_app
    global app_event_triggered

    obj = evnt.get_target_obj()
    app_name = obj.get_child(1).get_text()
    print(app_name)
    selected_app = app_ring.index(app_name)
    app_event_triggered = True


scrn = lv.screen_active()

# create an array of 12 objects and align them in a grid of 4x3
horizontal_spacing = 16
vertical_spacing = 5
margin_left = 35
margin_top = 10

image_cache = {}

def open_img(src):
    with open(src, 'rb') as f:
        bin_data = f.read()

    bin_image_dsc = lv.image_dsc_t({
        "header": {"w": 50, "h": 50, "cf": lv.COLOR_FORMAT.RGB565},
        'data_size': len(bin_data) - 12,
        'data': bin_data[12:]
    })
    return bin_image_dsc

def fetch_img(src):
    if src in image_cache:
        return image_cache[src]
    else:
        img_data = open_img(src)
        image_cache[src] = img_data
        return img_data


def draw_launcher():
    scrn.clean()
    for i in range(12):
        # check if the app exists
        if(i >= len(app_ring)):
            break
        obj_button = lv.obj(scrn)
        app_buttons.append(obj_button)
        obj_button.remove_style_all()
        obj_button.set_size(50, 70)
        x = (i % 4) * (50 + horizontal_spacing) + margin_left
        y = (i // 4) * (70 + vertical_spacing) + margin_top
        obj_button.align(lv.ALIGN.TOP_LEFT, x, y)
        obj_button.remove_flag(lv.obj.FLAG.SCROLLABLE )
        obj_button.add_event_cb(event_app_icon_cb, lv.EVENT.CLICKED, None)

        app_icon = lv.image(obj_button)
        app_icon.align(lv.ALIGN.TOP_MID, 0, 0)
        
        file_src = "./apps/data/" + app_ring[i] + ".bin"
        if(file_exists(file_src)):
            app_icon.set_src(fetch_img(file_src))
        else:
            app_icon.set_src(fetch_img("./no_img.bin"))
            
        app_label = lv.label(obj_button)
        app_label.set_text(app_ring[i])
        app_label.align(lv.ALIGN.BOTTOM_MID, 0, -3)

def clear_launcher():
    scrn.clean()

def itr_button_cb(pin):
    global button_itr_triggered
    button_itr_triggered = True

pin_back = Pin(0, Pin.IN, Pin.PULL_UP)
pin_back.irq(trigger=Pin.IRQ_FALLING, handler=itr_button_cb)

draw_launcher()

while True:
    if(app_event_triggered):
        app_event_triggered = False
        clear_launcher()
        start_app(selected_app)
    if(button_itr_triggered):
        button_itr_triggered = False
        close_app(selected_app)
        draw_launcher()
    time.sleep_ms(50)
    
