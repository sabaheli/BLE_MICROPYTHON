from machine import Timer
from ble import ESP32_BLE
from led import toggle_led, general_timer, RST_PSP

ble_msg = ""
is_ble_connected = False

Timeout_led = 0
counter_led  = 0
led_F = 0
led_state = False
Conecction_F = False
 
tim = Timer(0)

tim.init(period=1, mode=Timer.PERIODIC, callback=lambda  t: general_timer())
  
ble = ESP32_BLE("ESP32BLE")
RST_PSP()
while True:
    pass
