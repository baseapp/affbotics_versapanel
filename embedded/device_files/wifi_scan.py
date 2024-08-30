# app to connect to wifi
import lvgl as lv
import network
import time
import asyncio
import io
import versaos

wifi_buttons = ""
# wifi_buttons.add_flag(lv.obj.FLAG.HIDDEN)
selected_ssid = ""
sta_if = network.WLAN(network.STA_IF);
connection_status = 0

def dispMessage(messg):
    print(messg)
    scrn = lv.screen_active()
    
    #create style
    style_shadow = lv.style_t()
    style_shadow.init()
    style_shadow.set_shadow_width(10)
    style_shadow.set_shadow_spread(5)
    LV_COLOR_BLUE=lv.color_hex3(0xF)
    style_shadow.set_shadow_color(LV_COLOR_BLUE)

    panel1 = lv.obj(scrn)
    panel1.set_width(200)
    panel1.set_height(100)
    panel1.set_align( lv.ALIGN.CENTER)
    panel1.remove_flag(lv.obj.FLAG.SCROLLABLE)
    panel1.add_style(style_shadow, 0)
    
    label1 = lv.label(panel1)
    label1.align(lv.ALIGN.CENTER,0,0)
    label1.set_text(messg)

def checkConn():
    dispMessage("Connecting to WiFi")
    while(1):
        time.sleep_ms(1000)
        if(sta_if.status() == network.STAT_WRONG_PASSWORD):
            sta_if.disconnect()
            dispMessage("Wrong Password")
            time.sleep_ms(2000)
            clearScreen()
            time.sleep_ms(100)
            drawScreen()
            break
        elif(sta_if.isconnected()):
            print("connected")
            dispMessage("Connected to Wifi")
            time.sleep_ms(1000)
            break

def store_wifi_cred(wifissid, wifipass):
    versaos.set_config('wifi_ssid', wifissid)
    versaos.set_config('wifi_pass', wifipass)
    

def connect_wifi(wifissid, wifipass):
    sta_if.active(True)
    sta_if.connect(wifissid, wifipass)

def ta_event_handler(event):
    global sta_if
    global connection_status
    textarea = event.get_target_obj()
    #sta_if.connect(selected_ssid, textarea.get_text())
    wifi_pass = textarea.get_text()
    connect_wifi(selected_ssid, wifi_pass)
    store_wifi_cred(selected_ssid, wifi_pass)
    connection_status = 1
    
def getWifiPass(ssid_str):
    global selected_ssid
    selected_ssid = ssid_str
    scrn = lv.screen_active()
    scrn.clean()
    keyb = lv.keyboard(scrn)
    # Label
    label1 = lv.label(scrn)
    label1.align(lv.ALIGN.TOP_MID,0,15)
    label1.set_text("Password for %s:" %ssid_str)
    #Create a text area
    ta=lv.textarea(scrn)
    ta.align(lv.ALIGN.TOP_MID,0,50)
    ta.set_text("")
    ta.set_one_line(True)
    ta.add_event_cb(ta_event_handler, lv.EVENT.READY, None)
    max_h = 75
    # Assign the text area to the keyboard*/
    keyb.set_textarea(ta)    


def event_handler_wifi(event):
    global wifi_buttons
    obj_btn = event.get_target_obj()
    print(lv.list.get_button_text(wifi_buttons, obj_btn))
    ssid_selected = lv.list.get_button_text(wifi_buttons, obj_btn)
    getWifiPass(ssid_selected)


val_got_utc = 0
def ta_event_handler(event):
    global val_got_utc
    textarea = event.get_target_obj()
    val_utc = textarea.get_text()
    print (val_utc)
    val_utc = val_utc.split('.')
    offset_hr = 0
    if(val_utc[0] != ''):
        offset_hr = int(val_utc[0])
    offset_min = 0
    if(len(val_utc)>1):
        offset_min = int(val_utc[1])
    
    utc_off_sec = (offset_hr * 60 * 60) + (offset_min * 60)
    print("UTC off sec: %d"%utc_off_sec)
    versaos.set_utc_offset(utc_off_sec)
    val_got_utc = 1
    

def get_UTC_offset():
    scrn = lv.screen_active()
    scrn.clean()
    label_utc1 = lv.label(scrn)
    label_utc1.align(lv.ALIGN.TOP_MID,0,20)
    label_utc1.set_text("Enter timezone offset HH.MM")
    
    keyb = lv.keyboard(scrn)
    keyb.set_mode(lv.keyboard.MODE.NUMBER) 
    
    ta=lv.textarea(scrn)
    ta.align(lv.ALIGN.TOP_MID,0,50)
    ta.set_text("")
    ta.set_one_line(True)
    ta.add_event_cb(ta_event_handler, lv.EVENT.READY, None)
    keyb.set_textarea(ta)
    global val_got_utc
    while(1):
        time.sleep_ms(100)
        if(val_got_utc == 1):
            val_got_utc = 0
            return

def drawScreen():
    global connection_status
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0x000000), 0)
    
    label1 = lv.label(scrn)
    label1.align(lv.ALIGN.TOP_MID,0,60)
    label1.set_text("Scanning for WiFi")
    print("Scanning for wifi")
    time.sleep_ms(100)
    
    global sta_if
    sta_if.active(True)
    res = sta_if.scan()
    
    ssid_list = [ssid.decode('utf-8') for ssid, _, _, _, _, _ in res]

    print("Got ssid list")
    # print(ssid_list)
    label1.align(lv.ALIGN.TOP_MID,0,10)
    label1.set_text("Available Networks")
    
    #wifi_buttons = lv.list(scrn)
    global wifi_buttons
    wifi_buttons = lv.list(lv.screen_active())
    #wifi_buttons.remove_flag(lv.obj.FLAG.HIDDEN)
    wifi_buttons.set_size(260, 190)
    wifi_buttons.align(lv.ALIGN.CENTER, 0, 15)
    
    for wifi_name in ssid_list:
        if(wifi_name == ''):
            continue
        btn_obj = wifi_buttons.add_button(None, wifi_name)
        btn_obj.add_event_cb(event_handler_wifi, lv.EVENT.CLICKED, None)

    # Block the code until user select a ssid and enter password
    while(1):
        time.sleep_ms(100)
        if(connection_status):
            connection_status = 0
            break
    checkConn()

    
def clearScreen():
    scrn = lv.screen_active()
    scrn.clean()
    
# scanning 
#Display a scrollable list of availabel networks

# clicking a button calls the same function but with diff string

# display keyboard and get the password

#show connecting icon