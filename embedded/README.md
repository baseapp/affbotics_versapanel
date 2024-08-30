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

