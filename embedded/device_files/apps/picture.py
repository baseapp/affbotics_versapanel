import lvgl as lv
import fs_driver
import time
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')

file_url = ["S:../wall_2.bin"]
file_type = ["RGB"]
file_num = 0

def drawScreen():
    global file_num
    
    scrn = lv.screen_active()
    img_1 = lv.image(scrn)
    img_1.set_pos(0,0)
    img_1.set_src(file_url[file_num])
    
    lable_1 = lv.label(scrn)
    lable_1.set_text("file: %s"%file_type[file_num])
    lable_1.set_align( lv.ALIGN.BOTTOM_MID)
    
    if(file_num >= len(file_url)):
        file_num = 0
    else:
        file_num = file_num +1
    
def clearScreen():
    scrn = lv.screen_active()
    scrn.clean()