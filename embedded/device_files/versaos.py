import machine
import time
import neopixel
import json
import os

#----- settings -----#
CONFIG_FILE = 'config.json'
# Load the configuration from the JSON file
def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except OSError:
        print(OSError)
        return {}  # Return an empty dictionary if the file does not exist

# Save the configuration to the JSON file
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# Set a configuration value
def set_config(key, value):
    config = load_config()
    config[key] = value
    save_config(config)

# Get a configuration value
def get_config(key, default=None):
    config = load_config()
    if key in config:
        return config[key], True
    else:
        return default, False

#----- Local time -----#
utc_offset_sec, _ = get_config('utc_offset')

def set_utc_offset(value):
    global utc_offset_sec
    utc_offset_sec = value
    set_config('utc_offset', value)

def get_utc_offset():
    return utc_offset_sec

#----- Buzzer-----#
BUZZ_CONFIG_KEY = "buzz_vol"
buzz_volume, _ = get_config(BUZZ_CONFIG_KEY)
buzz_pin = machine.Pin(12)
buzz_pwm = machine.PWM(buzz_pin)
buzz_pwm.freq(500)
buzz_pwm.duty(0)
buzz_pwm

def set_buzz_volume(vol):
    global buzz_volume
    buzz_volume = vol
    set_config(BUZZ_CONFIG_KEY, vol)

def get_buzz_volume():
    return buzz_volume

def buzz_start(freq = 500, duty = buzz_volume):
    global buzz_pwm
    buzz_pwm.freq(freq)
    buzz_pwm.duty(duty)
    
def buzz_stop():
    global buzz_pwm
    buzz_pwm.freq(500)
    buzz_pwm.duty(0)

def buzz_for(freq, on_duration, off_duration):
    buzz_pwm.freq(freq)
    buzz_pwm.duty(buzz_volume)
    time.sleep_ms(on_duration)
    buzz_stop()
    time.sleep_ms(off_duration)


#----- RGB LED -----#
led_pin = machine.Pin(38)
led_power_pin = machine.Pin(45, machine.Pin.OUT)
led = neopixel.NeoPixel(led_pin, 1)

def led_state(state, reset = False):
    global p45
    p45.value(state)
    if(reset):
        led[0] = (0, 0, 0)
    
def led_set(r, g, b):
    global p45
    global led
    p45.on()
    led[0] = (r, g, b)
    led.write()
    
#----- Display Brightness -----#
BRI_CONFIG_KEY = "buzz_vol"
buzz_volume, _ = get_config(BRI_CONFIG_KEY)

disp_led_pin = machine.Pin(48)
disp_led_pwm = machine.PWM(disp_led_pin)
disp_led_pwm.freq(500)
disp_led_pwm.duty(1023)
disp_led_pwm

def set_brightness(val):
    #val = int(val * 10.23)
    disp_led_pwm.duty(val)
    set_config(BRI_CONFIG_KEY, val)
