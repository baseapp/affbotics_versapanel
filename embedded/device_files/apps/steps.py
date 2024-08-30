import lvgl as lv
import fs_driver

def drawScreen():
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0x000000), 0)
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    myfont_en = lv.binfont_create("S:/font_24.bin")
    
    arc = lv.arc(scrn)
    arc.set_end_angle(200)
    arc.set_size(150,150)
    arc.align(lv.ALIGN.CENTER,0,0)
    
    label1 = lv.label(scrn)
    label1.set_x(175)
    label1.set_y(65)
    label1.set_style_text_font(myfont_en, 0)
    label1.set_text("STEPS: 24")
    label1.align(lv.ALIGN.BOTTOM_MID, 0, -30)
    

def clearScreen():
    scrn = lv.screen_active()
    scrn.clean()