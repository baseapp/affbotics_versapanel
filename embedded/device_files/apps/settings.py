import lvgl as lv
import time
import sys

sys.path.append('../')
import versaos
import wifi_scan

settings_list = ['Brightness', 'Volume', 'WiFi', 'Time']
settings_symbols = [lv.SYMBOL.SETTINGS, lv.SYMBOL.VOLUME_MAX, lv.SYMBOL.WIFI, lv.SYMBOL.BELL]

settings_btns = None
selected_opt = ''
event_click = False

def event_handler_settings(event):
    global settings_btns
    global selected_opt
    global event_click
    
    obj_btn = event.get_target_obj()
    #print(lv.list.get_button_text(settings_btns, obj_btn))
    selected_opt = lv.list.get_button_text(settings_btns, obj_btn)
    event_click = True

def drawScreen():
    scr = lv.screen_active()
    
    label1 = lv.label(scr)
    label1.align(lv.ALIGN.TOP_MID,0,10)
    label1.set_text("Settings")
    
    global settings_btns
    settings_btns = lv.list(scr)
    settings_btns.set_size(240, 190)
    settings_btns.align(lv.ALIGN.CENTER, 0, 15)
    
    for i in range(len(settings_list)):
        btn_obj = settings_btns.add_button(settings_symbols[i], settings_list[i])
        btn_obj.add_event_cb(event_handler_settings, lv.EVENT.CLICKED, None)

slider_value = 0
got_value = False
slider_label = None
def slider_event_cb(e):
    global slider_value
    global slider_label
    slider = e.get_target_obj()
    slider_value = slider.get_value()
    slider_label.set_text("{:d}%".format(slider_value))
    slider_label.align_to(slider, lv.ALIGN.OUT_BOTTOM_MID, 0, 15)

def page_btn_cb(e):
    global got_value
    got_value = True

def draw_slider_page(title_text):
    global got_value
    global slider_value
    global slider_label
    
    clearScreen()
    scrn = lv.screen_active()
    
    slider_title = lv.label(scrn)
    slider_title.set_text(title_text)
    slider_title.align(lv.ALIGN.TOP_MID, 0, 20)
    
    slider = lv.slider(scrn)
    slider.center()
    slider.add_event_cb(slider_event_cb, lv.EVENT.VALUE_CHANGED, None)
    
    slider_label = lv.label(scrn)
    slider_label.set_text("0%")
    slider_label.align_to(slider, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
    
    btn_1 = lv.button(scrn)
    btn_1.align(lv.ALIGN.BOTTOM_MID, 0, -30)
    btn_1.add_event_cb(page_btn_cb, lv.EVENT.CLICKED, None)
    btn_txt = lv.label(btn_1)
    btn_txt.set_text('Done')
    
    while True:
        if(got_value):
            got_value = False
            return(slider_value)
            
def brightness_page():
    val = draw_slider_page('Brightness')
    val = int((val * 1023)/100)
    versaos.set_brightness(val)

def volume_page():
    val = draw_slider_page('Volume')
    val = int((val * 1023)/100)
    versaos.set_buzz_volume(val)

def wifi_page():
    clearScreen()
    wifi_scan.drawScreen()
    

def time_page():
    clearScreen()
    wifi_scan.get_UTC_offset()


def loop_task():
    global event_click
    
    if(not event_click):
        return
    
    event_click = False
    
    if(selected_opt == 'Brightness'):
        brightness_page()
    elif(selected_opt == 'Volume'):
        volume_page()
    elif(selected_opt == 'WiFi'):
        wifi_page()
    elif(selected_opt == 'Time'):
        time_page()
    
    clearScreen()
    time.sleep_ms(20)
    drawScreen()

def clearScreen():
    scr = lv.screen_active()
    scr.clean()