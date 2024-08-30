import lvgl as lv
import urequests
import json
import fs_driver
import time

url = "https://api.quotable.io/random?maxLength=160"

def getQuote():
    response = None
    try:
        # Send a GET request to the URL
        response = urequests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Fetch the 'content' field from the JSON data
            quote_content = data.get("content", "No content found")
            quote_author = data.get("author", "Someone")
            
            quote_content = quote_content + "  -" + quote_author
            
            response.close()
            # Print the quote content
            return(quote_content)
        else:
            response.close()
            return("Failed to fetch the quote")

    except Exception as e:
        if(response):
            response.close()
        return("An error occurred")

qt_txt = None
btn_evnt = True

def fetch_btn_cb(evnt):
    global btn_evnt
    btn_evnt = True

def drawScreen():
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0x000000), 0)

    # Load Font
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'S')
    myfont_head = lv.binfont_create("S:../font_24.bin")
    myfont = lv.binfont_create("S:../font_20.bin")
    
    qt_title = lv.label(scrn)
    qt_title.set_text("Quote")
    qt_title.align(lv.ALIGN.TOP_MID, 0, 40)
    qt_title.set_style_text_font(myfont_head, 0)
    
    global qt_txt
    global btn_evnt
    btn_evnt = True
    
    qt_txt = lv.label(scrn)
    qt_txt.set_width(300)
    qt_txt.set_long_mode(lv.label.LONG.WRAP)
    qt_txt.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
    qt_txt.set_align(lv.ALIGN.CENTER)
    
    qt_txt.align(lv.ALIGN.CENTER, 0, 0)
    qt_txt.set_style_text_font(myfont, 0)
    qt_txt.set_text("")
    
    btn_1 = lv.button(scrn)
    btn_1.align(lv.ALIGN.BOTTOM_MID, 0, -20)
    btn_1.add_event_cb(fetch_btn_cb, lv.EVENT.CLICKED, None)
    btn_txt = lv.label(btn_1)
    btn_txt.set_text('Refresh')
    

def loop_task():
    global qt_txt
    global btn_evnt
    
    if(btn_evnt):
        btn_evnt = False
        qt_txt.set_text("Thinking...")
        quote = getQuote()
        qt_txt.set_text(quote)
    time.sleep_ms(10)

def clearScreen():
    scrn = lv.screen_active()
    scrn.clean()