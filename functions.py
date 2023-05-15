from machine import Pin, Timer

class LEDController:
    def __init__(self):
        self.timeout_led = 0
        self.counter_led = 0
        self.led_F = 0
        self.led_state = False
        self.connection_F = False
        self.led = Pin(2, Pin.OUT)
        self.timer = Timer(0)

    def toggle_led(self):
        self.led.value(not self.led.value())

    def general_timer(self):
        self.timeout_led += 1
        # reset
        if (self.led_F == 0 and self.timeout_led > 500 and self.connection_F == False):
            self.timeout_led = 0
            self.toggle_led()
        if (self.led_F == 1 and self.timeout_led > 50):
            self.timeout_led = 0
            self.counter_led += 1
            self.toggle_led()
        if (self.led_F == 0 and self.timeout_led > 100 and self.counter_led < 4 and self.connection_F == True):
            self.timeout_led = 0
            self.counter_led += 1
            self.toggle_led()
        if (self.led_F == 0 and self.timeout_led > 1000 and self.counter_led >= 4 and self.connection_F == True):
            self.timeout_led = 0
            self.counter_led = 0
            self.led.value(0)

    def RST_PSP(self):
        self.led_F = 1
        while (self.counter_led < 30):
            pass
        self.led_F = 0
        self.counter_led = 0
