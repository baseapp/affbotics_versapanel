import init_board
import network
from machine import Pin
import time
import _thread
import os
import versaos

import welcome

import apps

Button0 = Pin(0, Pin.IN, Pin.PULL_UP)

app = 0
app_old = 1
app_ring = []

app_list = os.listdir('apps')

app_ring = [app.replace('.py', '') for app in app_list]

#import image_test
#image_test.drawScreen()

welcome.drawScreen()

#import img_test
#img_test.drawScreen()

#while True:
#    time.sleep(2)
    
import launcher

user_loop_module = None
user_lock = _thread.allocate_lock()
_thread.stack_size(8192)

pause_thread = False

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

while(True):
    time.sleep_ms(50)
    
    if(not Button0.value()):
        app = app +1
        if(app >= len(app_ring)):
            app = 0
    if(app_old == app):
        continue
    try:
        app_old = app
        main_module_old = __import__("apps." + app_ring[app_old])
        main_module = __import__("apps." + app_ring[app])
        
        module_old = getattr(main_module_old, app_ring[app_old])
        module = getattr(main_module, app_ring[app])
        
        pause_thread = True
        # close the previous app
        if hasattr(module_old, 'clearScreen'):
            module.clearScreen()
        else:
            print(f"{app_ring[app_old]}.py does not have an clearScreen() function")
        
        # Call the new drawScreen function
        if hasattr(module, 'drawScreen'):
            module.drawScreen()
        else:
            print(f"{app_ring[app]}.py does not have an drawScreen() function")
        
        # Set the loop function to call the active app's loop function
        if hasattr(module, 'loop_task'):
            with user_lock:
                user_loop_module = module.loop_task
        else:
            user_loop_module = None
            print(f"{app_ring[app]}.py does not have loop_task(); ignoring")
        pause_thread = False
        
    except ImportError as e:
        print(f"Module {app_ring[app]} could not be imported: {e}")

#wifi_scan.drawScreen()

#task_test.drawScreen()

#quote.drawScreen()

#keyboard_test.drawScreen()

#numclock.drawScreen()