from machine import Pin, Timer
import ble
from functions import LEDController

ble_msg = ""
connection_F = False

ble_instance = ble.ESP32_BLE("ESP", connection_F)
led_controller = LEDController(ble_instance)
led_controller.timer.init(period=1, mode=Timer.PERIODIC, callback=lambda t: led_controller.general_timer())
led_controller.RST_PSP()

while True:
    pass




