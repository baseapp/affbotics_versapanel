#import init_board
import lvgl as lv
import fs_driver
import time
import network
import ntptime
import versaos

utc_offset_sec = 0

scrn = lv.screen_active()
time_txt_hr = 0
time_txt_min = 0
time_txt_yr = 0
time_txt_mntNum = 0
time_txt_dtNum = 0
time_txt_mnt = 0
time_txt_day = 0
warning_msg = 0

icon = "./data/clock.png"

mntTxt = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
dayTxt = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def drawClock():
    global scrn
    global time_txt_hr
    global time_txt_min
    global time_txt_yr
    global time_txt_mntNum
    global time_txt_dtNum
    global time_txt_mnt
    global time_txt_day
    global warning_msg
    
    time_txt_hr = lv.label(scrn)
    time_txt_min = lv.label(scrn)
    time_txt_yr = lv.label(scrn)
    time_txt_mntNum = lv.label(scrn)
    time_txt_dtNum = lv.label(scrn)
    time_txt_mnt = lv.label(scrn)
    time_txt_day = lv.label(scrn)
    
    warning_msg = lv.label(scrn)
    warning_msg.align(lv.ALIGN.TOP_MID, 0, 10)
    warning_msg.set_text("")
    
    scrn.set_style_bg_color(lv.color_hex(0x000000), 0)
    
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    
    myfont_en = lv.binfont_create("S:../font_big2.bin")
    myfont_en2 = lv.binfont_create("S:../font_24.bin")
    
    time_txt_hr.set_x(75)
    time_txt_hr.set_y(45)
    time_txt_hr.set_style_text_font(myfont_en, 0)
    time_txt_hr.set_text("00")
    
    time_txt_min.set_x(75)
    time_txt_min.set_y(135)
    time_txt_min.set_style_text_font(myfont_en, 0)
    time_txt_min.set_text("00")
    
    obj_bar = lv.obj(scrn)
    obj_bar.set_x(172)
    obj_bar.set_y(40)
    obj_bar.set_width(4)
    obj_bar.set_height(162)
    # Bar style
    obj_bar_style_MAIN = lv.style_t()
    obj_bar_style_MAIN.init()
    obj_bar_style_MAIN.set_radius(0)
    obj_bar_style_MAIN.set_bg_color(lv.color_hex(0x00FFFF))
    obj_bar_style_MAIN.set_border_width(0)
    obj_bar.add_style(obj_bar_style_MAIN, lv.PART.MAIN)
    
    time_txt_yr.set_x(186)
    time_txt_yr.set_y(40)
    time_txt_yr.set_style_text_font(myfont_en2, 0)
    time_txt_yr.set_text("0000")
    
    time_txt_mntNum.set_x(186)
    time_txt_mntNum.set_y(64)
    time_txt_mntNum.set_style_text_font(myfont_en2, 0)
    time_txt_mntNum.set_text("00")
    
    time_txt_dtNum.set_x(186)
    time_txt_dtNum.set_y(88)
    time_txt_dtNum.set_style_text_font(myfont_en2, 0)
    time_txt_dtNum.set_text("00")
    
    time_txt_mnt.set_x(186)
    time_txt_mnt.set_y(154)
    time_txt_mnt.set_style_text_font(myfont_en2, 0)
    time_txt_mnt.set_text("na")
    
    time_txt_day.set_x(186)
    time_txt_day.set_y(178)
    time_txt_day.set_style_text_font(myfont_en2, 0)
    time_txt_day.set_text("na")
    
def addZero(val):
    str_val = ""
    if(val<10):
        str_val = "0%d"%val
    else:
        str_val = str(val)
    return(str_val)

def updateNtp():
    global warning_msg
    sta_if = network.WLAN(network.STA_IF);
    if(sta_if.isconnected()):
        try:
            ntptime.settime()
            warning_msg.set_text("")
            print("NTP updated")
        except Exception as e:
            print("Unable to set NTP")
            print(e)

def drawTime():
    global scrn
    global time_txt_hr
    global time_txt_min
    global time_txt_yr
    global time_txt_mntNum
    global time_txt_dtNum
    global time_txt_mnt
    global time_txt_day
    global warning_msg
    
    #UTC_OFFSET = (utc_offset_hour * 60 * 60) + (utc_offset_minute * 60)
    #UTC_OFFSET = utc_offset_sign * UTC_OFFSET
    
    local_time = time.localtime(time.time() + versaos.get_utc_offset())
    yr = local_time[0]
    mn = local_time[1]
    dt = local_time[2]
    hr = local_time[3]
    mi = local_time[4]
    se = local_time[5]
    we = local_time[6]
    
    # TODO: move this to versaos code
    if(yr == 2000):
        warning_msg.set_text("Time Not Synced to NTP Server")
        updateNtp()
    
    # Hour
    time_txt_hr.set_text(addZero(hr))

    # Minute
    time_txt_min.set_text(addZero(mi))

    # Year
    time_txt_yr.set_text(addZero(yr))

    # Month
    time_txt_mntNum.set_text(addZero(mn))

    # Date
    time_txt_dtNum.set_text(addZero(dt))

    # Month Txt
    time_txt_mnt.set_text(mntTxt[mn])

    # Day
    time_txt_day.set_text(dayTxt[we])

def drawTimeTask():
    drawTime()
    time.sleep_ms(1000)

def drawScreen():
    drawClock()
    #drawTimeTask()

def loop_task():
    drawTimeTask()

def clearScreen():
    scrn = lv.screen_active()
    scrn.clean()