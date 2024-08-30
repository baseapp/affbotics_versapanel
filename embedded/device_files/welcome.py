# welcome screen
import lvgl as lv
import network
import time
import fs_driver
import ntptime
import wifi_scan
import io
import versaos

val_set_conn = 0

string1 = "."
def updateDots():
    global string
    if string1 == ".":
        string1 = ".."
    elif string1 == "..":
        string1 = "..."
    elif string1 == "...":
        string1 = "...."
    else:
        string1 = "."


def event_handler_yes(evt):
    global val_set_conn
    val_set_conn = 2
def event_handler_no(evt):
    global val_set_conn
    val_set_conn = 1

def drawWifiConn():
    scrn = lv.screen_active()
    label1 = lv.label(scrn)
    label1.align(lv.ALIGN.TOP_MID,0,40)
    label1.set_text("Connect to WiFi?")
    
    button_no = lv.button(scrn)
    button_no.align(lv.ALIGN.TOP_MID,-40,90)
    button_no.add_event_cb(event_handler_no, lv.EVENT.CLICKED, None)
    no_text = lv.label(button_no)
    no_text.set_text("Later")
    
    style1 = lv.style_t()
    style1.set_bg_color(lv.color_hex3(0x093))
    button_yes = lv.button(scrn)
    button_yes.add_style(style1, 0)
    button_yes.align(lv.ALIGN.TOP_MID,40,90)
    button_yes.add_event_cb(event_handler_yes, lv.EVENT.CLICKED, None)
    yes_text = lv.label(button_yes)
    yes_text.set_text("Sure")
    
    # TODO: Set up wifi or setup ntp here
    global val_set_conn
    while(1):
        if(val_set_conn != 0):
            scrn.clean()
            if(val_set_conn == 2):
                wifi_scan.drawScreen()
                break
            else:
                break
        time.sleep_ms(100)
    
def drawScreen():
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0x000000), 0)
    
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    myfont = lv.binfont_create("S:../font_24.bin")
    
    label_wel = lv.label(scrn)
    label_wel.align(lv.ALIGN.TOP_MID,0,50)
    label_wel.set_style_text_font(myfont, 0)
    label_wel.set_text("Welcome")
    time.sleep_ms(100)
    label_wel.delete()
    
    val_ssid, exists = versaos.get_config('wifi_ssid')
    val_pass, exists = versaos.get_config('wifi_pass')
    
    if(exists):
        wifi_scan.connect_wifi(val_ssid, val_pass)
        wifi_scan.checkConn()
    else:
        drawWifiConn()

    # Set UTC offset
    val, exists = versaos.get_config('utc_offset')
    if(exists):
        utc_off_sec = int(val)
    else:
        wifi_scan.get_UTC_offset()
    
    sta_if = network.WLAN(network.STA_IF);
    if(sta_if.isconnected()):
        try:
            ntptime.settime()
        except Exception as e:
            print("Unable to set NTP")
            print(e)

    
    
def clearScreen():
    scrn = lv.screen_active()
    scrn.clean()
    
