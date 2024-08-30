import lvgl as lv

def event_handler(source,evt):
    if  evt == lv.EVENT.VALUE_CHANGED:
        print("Value:",textarea.get_text())

def drawScreen():
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0x000000), 0)
    
    # create a keyboard and apply the styles
    keyb = lv.keyboard(scrn)
    
    # Label
    label1 = lv.label(scrn)
    label1.align(lv.ALIGN.TOP_MID,0,15)
    label1.set_text("Keyboard:")
    

    #Create a text area. The keyboard will write here
    ta=lv.textarea(scrn)
    ta.align(lv.ALIGN.TOP_MID,0,50)
    ta.set_text("")
    ta.set_one_line(True)
    max_h = 75

    # Assign the text area to the keyboard*/
    keyb.set_textarea(ta)    


def clearScreen():
    scrn = lv.screen_active()
    scrn.clean()