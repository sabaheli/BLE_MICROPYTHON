from machine import Pin , Timer
import ble
from functions import LEDController

ble_msg = ""
ble = ble.ESP32_BLE("ESP32BLE")
led_controller = LEDController()
led_controller.timer.init(period=1, mode=Timer.PERIODIC, callback=lambda t: led_controller.general_timer())
led_controller.RST_PSP()

while True:
   pass