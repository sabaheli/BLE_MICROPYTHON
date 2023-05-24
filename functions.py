from machine import Pin, Timer ,UART



class LEDController:
        def __init__(self, ble_instance):
            
            self.timeout_led = 0
            self.counter_led = 0
            self.led_F = 0
            self.led_state = False
            self.connection_F = False
            self.led = Pin(2, Pin.OUT)
            self.timer = Timer(0)
            self.ble_instance = ble_instance
            self.serial = UART(1, 9600,rx = 16,tx = 17)
            self.serial_buffer = b""

        def toggle_led(self):
            self.led.value(not self.led.value())

        def general_timer(self):
            self.timeout_led += 1
            # reset
            if (self.led_F == 0 and self.timeout_led > 500 and self.ble_instance.connection_F == False):
                self.timeout_led = 0
                self.toggle_led()
            if (self.led_F == 1 and self.timeout_led > 50):
                print("timeout_led:", self.timeout_led)
                print("counter_led:", self.counter_led)
                print("led_F:", self.led_F)
                print("connection_F:", self.ble_instance.connection_F)
                self.timeout_led = 0
                self.counter_led += 1
                self.toggle_led()
            if (self.led_F == 0 and self.timeout_led > 100 and self.counter_led < 4 and self.ble_instance.connection_F == True):
                self.timeout_led = 0
                self.counter_led += 1
                self.toggle_led()
            if (self.led_F == 0 and self.timeout_led > 1000 and self.counter_led >= 4 and self.ble_instance.connection_F == True):
                self.timeout_led = 0
                self.counter_led = 0
                self.led.value(0)

            # Check for data on the serial port
            data = self.serial.read()
            if data is not None:
                print("Received data:", data)
        def RST_PSP(self):
            print("?")
            self.led_F = 1
            while (self.counter_led < 30):
                pass
            self.led_F = 0
            self.counter_led = 0
            #self.ble_instance.set_connection_status(False)  # Set the initial connection status to True









