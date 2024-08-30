from machine import Pin, SPI
import lcd_bus
import os

spi_bus = SPI.Bus(
    host=2,
    miso=3,
    mosi=2,
    sck=42
)

bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    dc= 47,
    cs=1,
    freq=64000000,
)

buf1 = bus.allocate_framebuffer(int(240 * 320 * 2 / 10), lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA)
buf2 = bus.allocate_framebuffer(int(240 * 320 * 2 / 10), lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA)

import st7789
import lvgl as lv

lv.init()

display = st7789.ST7789(
    data_bus=bus,
    display_width=240,
    display_height=320,
    frame_buffer1=buf1,
    frame_buffer2=buf2,
    reset_pin=40,
    reset_state=st7789.STATE_LOW,
    #power_pin=-1,
    #backlight_pin=48,
    color_space=lv.COLOR_FORMAT.RGB565,
    color_byte_order=st7789.BYTE_ORDER_BGR,
    rgb565_byte_swap=True,
)

powerSwitch = Pin(21, Pin.OUT)
powerSwitch.value(0)

display.set_power(1)
display.set_rotation(lv.DISPLAY_ROTATION._90)
display.init()
display.set_params(display._INVOFF)
display.set_backlight(100)

scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0x000000), 0)
scrn.clean()

from i2c import I2C
import ft6x36

i2c_bus = I2C.Bus(host=0, scl=10, sda=9)
touch_i2c = I2C.Device(i2c_bus, ft6x36.I2C_ADDR, ft6x36.BITS)
indev = ft6x36.FT6x36(touch_i2c)

import task_handler
th = task_handler.TaskHandler(duration=1)

try:
    os.mkdir("settings")
    print("First boot")
except OSError as e:
    if e == errno.EEXIST:
        print("eexist")

