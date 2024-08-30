# code to test parallel task
import lvgl as lv
import time

def task_1():
    print("I am task 1")
    scrn = lv.screen_active()
    label_wel = lv.label(scrn)
    inc = 0
    while(1):
        print("Hi from 1")
        label_wel.set_text("Hello %d" %inc)
        inc = inc+1
        time.sleep_ms(100)

def drawScreen():
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0x000000), 0)

    label_wel = lv.label(scrn)
    label_wel.set_x(95)
    label_wel.set_y(45)
    label_wel.set_text("Hello")
    task_1()
    