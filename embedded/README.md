# Micropython OS for Versapanels

**Project Description**  
This project provides MicroPython support for VersaPanels, including integration with the LVGL graphics library.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Getting Started

1. **Clone the repository**  
   Use the following command to clone this repository and initialize submodules:
   ```bash
   git clone --recurse-submodules https://github.com/baseapp/affbotics_versapanel.git
   ```
   
2. **Navigate to the project directory**  
   Change directory to the embedded MicroPython folder:
   ```bash
   cd embedded/affbotics_micropython
   ```

3. **Build the firmware**  
   Run the following command to build the firmware for the ESP32 platform with the specified configurations:
   ```bash
   python3 make.py esp32 submodules clean mpy_cross BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT DISPLAY=st7789 INDEV=ft6x36 --usb-otg
   ```
    Run it without the `--usb-otg` for using the UART0

4. **Flash the firmware**  
   After a successful build, the script should give you the command to flash the firmware to your device, just change the `(port)` to your device port

5. **Configure in Thonny IDE**
   - Install [Thonny](https://thonny.org/) and open it
   - Go to `Run > Configure Interpreter`.
   - Select `MicroPython (ESP32)` as the interpreter and choose the correct port for your device, then click `OK`.

7. **Upload device files**  
   - In Thonny, navigate to `affbotics_versapanel/embedded/device_files`.
   - Select all files and folders in the left panel and upload them to the device.

8. **Soft restart the device**  
   - Click the `STOP` button at the top of Thonny IDE to perform a soft restart of the device.
   - Your device should now be running VersaOS.


## Adding your app to Versapanel
You can refer to apps/demo.py as a reference for creating your app
1. create a Python file in apps/your_app_name.py
2. import module lvgl
3. [icon conversion] and give it the same name as your app but with a .bin extension
4. Create functions `drawScreen()`, `clearScreen()` and `loop_task()`
   - When your app is imported and the `drawScreen()` function is called, this function acts like `setup()` function in Arduino.
   - The `loop_task()` function is called every 50 milliseconds, which acts like `loop()` in Arduino.
   - And the `clearScreen()` function is called when your app is ended, you can call the function lvgl clean function to clear the screen and remove the widgets from the memory and do any other cleanups
5. Save the file and do a soft or hard reboot for changes to take effect
