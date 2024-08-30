#Focus app

import lvgl as lv
import time
import fs_driver

arc = ""
label_2 = ""
scrn = ""
ui_Button1 = ""
ui_Button2 = ""
label_ico = ""
ui_BtnLabel2 = ""
ui_BtnLabel1 = ""
btnmat = ""

#icon = "./data/focus.png"

timer_opts = ["1","3","5","\n", "10","15","20","\n","30","45","60", ""]

page_mode = 0 # 0->set_mode / 1->run_mode
prev_page_mode = 1

time_pass = 0
time_total = 3 * 60
run_state = 0

def event_handler_pause(evt):
    global page_mode
    global run_state
    global ui_BtnLabel1
    global ui_BtnLabel2
    global label_ico
    global time_pass
    
    # if Settings page then go to run_mode
    if(page_mode == 0):
        page_mode = 1
        return
    
    btn_txt = ""
    run_state = not run_state
    
    if(run_state):
        btn_txt = "Pause"
        label_ico.set_text("")
        ui_BtnLabel2.set_text("Reset")
    else:
        btn_txt = "Start"
        label_ico.set_text(lv.SYMBOL.PAUSE)
        
    ui_BtnLabel1.set_text(btn_txt)

def event_handler_reset(evt):
    global page_mode
    global time_pass
    global run_state
    global ui_BtnLabel1
    global ui_BtnLabel2
    global label_ico
    global label_2
    global arc
    
    # Set mode to settings
    if(ui_BtnLabel2.get_text() == "End"):
        page_mode = 0
        return
    
    time_pass = 0
    run_state = 0
    ui_BtnLabel1.set_text("Start")
    label_ico.set_text(lv.SYMBOL.PAUSE)
    ui_BtnLabel2.set_text("End")
    label_2.set_text("00:00")
    arc.set_value(1)


def event_handler_matrix(evt):
    global btnmat
    global page_mode
    global time_total
    
    btn_id = btnmat.get_selected_button()
    btn_txt = btnmat.get_button_text(btn_id)
    time_total = 60 * int(btn_txt)
    page_mode = 1

def drawFocusMode():
    global arc
    global label_2
    global scrn
    global ui_BtnLabel1
    global ui_BtnLabel2
    global label_ico
    global ui_Button2
    global ui_Button1
    global btnmat
    
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0x000000), 0)
    
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    myfont = lv.binfont_create("S:../font_24.bin")
    
    label_1 = lv.label(scrn)
    label_1.align(lv.ALIGN.TOP_LEFT,10,10)
    label_1.set_style_text_font(myfont, 0)
    label_1.set_text("Focus")
    
    btnmat = lv.buttonmatrix(scrn)
    btnmat.set_map(timer_opts)
    btnmat.set_width(240)
    btnmat.set_height(180)
    btnmat.align(lv.ALIGN.CENTER, 0, 10)
    btnmat.set_style_radius( 10, lv.PART.ITEMS | lv.STATE.DEFAULT )
    btnmat.set_style_bg_color(lv.color_hex(0x1d8bf9), lv.PART.ITEMS | lv.STATE.DEFAULT )
    btnmat.set_style_bg_opa(0, lv.PART.MAIN| lv.STATE.DEFAULT )
    btnmat.set_style_border_width( 0, lv.PART.MAIN | lv.STATE.DEFAULT )
    btnmat.set_style_pad_gap(10, lv.PART.MAIN| lv.STATE.DEFAULT )
    
    btnmat.add_event_cb(event_handler_matrix, lv.EVENT.VALUE_CHANGED, None)
    
    arc = lv.arc(scrn)
    arc.add_flag(lv.obj.FLAG.HIDDEN)
    arc.set_end_angle(200)
    arc.set_size(150,150)
    arc.align(lv.ALIGN.LEFT_MID,10,10)
    arc.remove_flag(lv.obj.FLAG.CLICKABLE)
    arc.set_value(1)
    arc.set_bg_angles(0,360)
    arc.set_rotation(270)
    arc.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.KNOB | lv.STATE.DEFAULT )
    arc.set_style_bg_opa(0, lv.PART.KNOB| lv.STATE.DEFAULT )
    arc.set_style_arc_width( 18, lv.PART.MAIN | lv.STATE.DEFAULT )
    arc.set_style_arc_width( 18, lv.PART.INDICATOR | lv.STATE.DEFAULT )
    
    label_2 = lv.label(arc)
    label_2.align(lv.ALIGN.CENTER, 0, 0)
    label_2.set_style_text_font(myfont, 0)
    label_2.set_text("00:00")
    
    label_ico = lv.label(arc)
    label_ico.align(lv.ALIGN.CENTER, 0, 25)
    label_ico.set_text(lv.SYMBOL.PAUSE)
    
    ui_Button1 = lv.button(scrn)
    ui_Button1.add_flag(lv.obj.FLAG.HIDDEN)
    ui_Button1.set_width(100)
    ui_Button1.set_height(50)
    ui_Button1.set_x(90)
    ui_Button1.set_y(-30)
    ui_Button1.set_align(lv.ALIGN.CENTER)
    #ui_Button1.remove_flag(lv.obj.FLAG.SCROLLABLE)
    #ui_Button1.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
    ui_Button1.set_style_radius( 25, lv.PART.MAIN | lv.STATE.DEFAULT )
    ui_Button1.add_event_cb(event_handler_pause, lv.EVENT.CLICKED, None)

    ui_BtnLabel1 = lv.label(ui_Button1)
    ui_BtnLabel1.set_text("Start")
    ui_BtnLabel1.set_width(lv.SIZE_CONTENT)
    ui_BtnLabel1.set_height(lv.SIZE_CONTENT)
    ui_BtnLabel1.set_align( lv.ALIGN.CENTER)

    ui_Button2 = lv.button(scrn)
    ui_Button2.add_flag(lv.obj.FLAG.HIDDEN)
    ui_Button2.set_width(100)
    ui_Button2.set_height(50)
    ui_Button2.set_x(90)
    ui_Button2.set_y(50)
    ui_Button2.set_align( lv.ALIGN.CENTER)
    ui_Button2.set_style_radius( 25, lv.PART.MAIN | lv.STATE.DEFAULT )
    ui_Button2.set_style_bg_color(lv.color_hex(0xFF5959), lv.PART.MAIN | lv.STATE.DEFAULT )
    ui_Button2.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
    ui_Button2.add_event_cb(event_handler_reset, lv.EVENT.CLICKED, None)

    ui_BtnLabel2 = lv.label(ui_Button2)
    ui_BtnLabel2.set_text("Reset")
    ui_BtnLabel2.set_width(lv.SIZE_CONTENT)
    ui_BtnLabel2.set_height(lv.SIZE_CONTENT)
    ui_BtnLabel2.set_align( lv.ALIGN.CENTER)
    
def mode_settings():
    global ui_Button2
    global ui_Button1
    global ui_BtnLabel1
    global arc
    global btnmat
    
    ui_Button2.add_flag(lv.obj.FLAG.HIDDEN)
    ui_Button1.add_flag(lv.obj.FLAG.HIDDEN)
    ui_BtnLabel1.set_text("Start")
    arc.add_flag(lv.obj.FLAG.HIDDEN)
    btnmat.remove_flag(lv.obj.FLAG.HIDDEN)
    

def mod_run():
    global ui_Button2
    global ui_Button1
    global ui_BtnLabel1
    global ui_BtnLabel2
    global label_2
    global arc
    global time_total
    global btnmat
    
    ui_Button2.remove_flag(lv.obj.FLAG.HIDDEN)
    ui_Button1.remove_flag(lv.obj.FLAG.HIDDEN)
    arc.remove_flag(lv.obj.FLAG.HIDDEN)
    btnmat.add_flag(lv.obj.FLAG.HIDDEN)
    
    time_min = time_total // 60
    time_sec = time_total % 60
        
    time_str = addZero(time_min) + ":" + addZero(time_sec)
    label_2.set_text(time_str)
    ui_BtnLabel2.set_text("End")
    

def addZero(val):
    str_val = ""
    if(val<10):
        str_val = "0%d"%val
    else:
        str_val = str(val)
    return(str_val)

def updateScreen():
    global page_mode
    global prev_page_mode
    global scrn
    global arc
    global label_2
    global time_pass
    global time_total
    global run_state
    global label_ico
    
    if(prev_page_mode != page_mode):
        prev_page_mode = page_mode
        if(page_mode):
            mod_run()
        else:
            mode_settings()
        
    if(page_mode == 0):
        time.sleep_ms(100)
        return
        
    if(run_state):
        time_pass = time_pass +1
        time_perc = (time_pass/time_total) * 100
        if(time_perc <1):
            time_perc = 1
        arc.set_value(int(time_perc))
        
        time_min = time_pass // 60
        time_sec = time_pass % 60
        
        time_str = addZero(time_min) + ":" + addZero(time_sec)
        label_2.set_text(time_str)
            
        time.sleep_ms(1000)
        
    if(time_pass >= time_total):
        run_state = 0
        label_ico.set_text(lv.SYMBOL.STOP)
        run_state = 0
    
def drawScreen():
    global prev_page_mode
    global page_mode
    global time_pass
    global run_state
    
    prev_page_mode = 1
    page_mode = 0
    time_pass = 0
    run_state = 0
    
    drawFocusMode()

def loop_task():
    updateScreen()

def clearScreen():
    scrn = lv.screen_active()
    scrn.clean()
    