from machine import Pin

led = Pin(2, Pin.OUT)
Timeout_led = 0
counter_led = 0
Timeout_led = 0
counter_led  = 0
led_F = 0
led_state = False
Conecction_F = False

def toggle_led() :
  global led_state
  #led.toggle()
# #   led_state = not led_state # invert the state of the LED
  led.value(not led.value())

def general_timer ():
    global Timeout_led , led_F,counter_led,Conecction_F
    Timeout_led += 1
    #reset 
    if (led_F == 0 and Timeout_led >500 and Conecction_F == False):
        Timeout_led = 0 
        toggle_led()  
    if (led_F == 1 and Timeout_led >50 ):
        Timeout_led = 0 
        counter_led += 1 
        toggle_led()
    if (led_F == 0 and Timeout_led >100 and counter_led < 4 and Conecction_F == True):
       Timeout_led = 0
       counter_led +=1
       toggle_led()
    if (led_F == 0 and Timeout_led >1000 and counter_led >= 4 and Conecction_F == True) :
       Timeout_led = 0
       counter_led  =0
       led.value(0)


def RST_PSP ():
    global counter_led , led_F
    led_F = 1
    while (counter_led <30 ):
        pass
    led_F = 0
    counter_led = 0
