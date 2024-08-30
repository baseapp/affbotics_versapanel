import lvgl as lv
import urequests
import json
import fs_driver

label_3 = None

def event_btn_cb():
    print("Button pressed")

def drawScreen():
    global label_3
    
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0x000000), 0)
    
    label_1 = lv.label(scrn)
    label_1.align(lv.ALIGN.TOP_MID, 0, 30)
    label_1.set_text("This is a Top aligned label")
    
    label_2 = lv.label(scrn)
    label_2.set_x(10)
    label_2.set_y(10)
    label_2.set_text("Hello Im at (10,10)")
    
    label_3 = lv.label(scrn)
    label_3.align(lv.ALIGN.TOP_MID, 0, 0)

    # Load Font
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    myfont_1 = lv.binfont_create("S:../font_24.bin")
    myfont_2 = lv.binfont_create("S:../font_20.bin")
    
    label_3 = lv.label(scrn)
    label_3.align(lv.ALIGN.CENTER, 0, -30)
    label_3.set_style_text_font(myfont_2, 0)
    label_3.set_text("This is an example for font")
    
    
    btn_1 = lv.button(scrn)
    btn_1.align(lv.ALIGN.BOTTOM_MID, 0, -10)
    
    btn_label = lv.label(btn_1)
    btn_label.set_text("Button")
    

counter = 0

def loop_task():
    global counter
    global label_3
    
    scrn = lv.screen_active()
    
    if(counter >= 240):
        counter = 0

    label_3.set_text("Im at pos %d"%counter)
    label_3.set_y(counter)
    
    counter = counter + 1

def clearScreen():
    scrn = lv.screen_active()
    scrn.clean()