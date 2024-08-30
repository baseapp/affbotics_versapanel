import lvgl as lv
import time
import fs_driver

def event_handler_appswitch(evnt):
    print("clicked: ")
    print(evnt)

def drawScreen():
    scrn = lv.screen_active()
    label_1 = lv.label(scrn)
    label_1.align(lv.ALIGN.TOP_MID, 0, 5)
    label_1.set_text("Home")
    
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    
    img_1 = lv.image(scrn)
    img_2 = lv.image(scrn)
    img_3 = lv.image(scrn)
    #img_4 = lv.image(scrn)
    #img_5 = lv.image(scrn)
    #img_6 = lv.image(scrn)
    #img_7 = lv.image(scrn)
    #img_8 = lv.image(scrn)
    #img_9 = lv.image(scrn)
    #img_10 = lv.image(scrn)
    #img_11 = lv.image(scrn)
    #img_12 = lv.image(scrn)
    
    img_1.set_src("S:./apps/data/settings_x.png")
    img_2.set_src("S:./apps/data/calculator.png")
    img_3.set_src("S:./apps/data/calendar.png")
    #img_4.set_src("S:/clock.png")
    #img_5.set_src("S:/quote.png")
    #img_6.set_src("S:/house.png")
    #img_7.set_src("S:/news.png")
    #img_8.set_src("S:/notes.png")
    #img_9.set_src("S:/focus.png")
    #img_10.set_src("S:/weather.png")
    #img_11.set_src("S:/spotify.png")
    #img_12.set_src("S:/bitcoin.png")
    
    img_1.align(lv.ALIGN.TOP_LEFT, 30, 35)
    img_2.align(lv.ALIGN.TOP_LEFT, 30, 105)
    img_3.align(lv.ALIGN.TOP_LEFT, 30, 175)
    
    #img_4.align(lv.ALIGN.TOP_LEFT, 100, 35)
    #img_5.align(lv.ALIGN.TOP_LEFT, 100, 105)
    #img_6.align(lv.ALIGN.TOP_LEFT, 100, 175)
    
    #img_7.align(lv.ALIGN.TOP_LEFT, 170, 35)
    #img_8.align(lv.ALIGN.TOP_LEFT, 170, 105)
    #img_9.align(lv.ALIGN.TOP_LEFT, 170, 175)
    
    #img_10.align(lv.ALIGN.TOP_LEFT, 240, 35)
    #img_11.align(lv.ALIGN.TOP_LEFT, 240, 105)
    #img_12.align(lv.ALIGN.TOP_LEFT, 240, 175)
    
    img_1.add_flag(lv.obj.FLAG.CLICKABLE)
    img_2.add_flag(lv.obj.FLAG.CLICKABLE)
    img_3.add_flag(lv.obj.FLAG.CLICKABLE)
    
    img_1.add_event_cb(event_handler_appswitch, lv.EVENT.CLICKED, None)
    img_2.add_event_cb(event_handler_appswitch, lv.EVENT.CLICKED, None)
    img_3.add_event_cb(event_handler_appswitch, lv.EVENT.CLICKED, None)
    
    
    while True:
        time.sleep(1)
    