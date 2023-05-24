import ubluetooth
from functions import LEDController
from machine import UART

class ESP32_BLE():
    def __init__(self, name, connection_F):
        self.name = "ESP"
        self.connection_F = connection_F
        self.ble = ubluetooth.BLE()
        self.ble.config(gap_name="ESP")
        self.ble.config('gap_name')
        self.ble.active(False)
        self.ble.active(True)
        
        
        #self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()
        self.led_controller = LEDController(self)
        self.serial = UART(1, 9600,rx = 16,tx = 17)
        self.serial_buffer = b""
        

    def set_connection_status(self, status):
        self.connection_F = status
        print("connected")

    def ble_irq(self, event, data):
        #self.print_serial_data()
        if event == 1: #_IRQ_CENTRAL_CONNECT:
                       # A central has connected to this peripheral
            self.set_connection_status(True)
            #self.connected()

        elif event == 2: #_IRQ_CENTRAL_DISCONNECT:
                         # A central has disconnected from this peripheral.
            self.advertiser()
            self.set_connection_status(False)
            #self.disconnected()
            print("disconnect")
        elif event == 3: #_IRQ_GATTS_WRITE:
                         # A client has written to this characteristic or descriptor.          
            value = self.ble.gatts_read(self.rx)
            ble_msg = self.serial_buffer.decode('UTF-8').strip()
            print(ble_msg)

    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID  = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID  = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + 'n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = self.ble.gap_advertise(100, bytearray('\x02\x01\x02','UTF_8') + bytearray((len(name) + 1, 0x09),'UTF_8') + name,connectable = True)
        print(adv_data)
        print("Advertisement started")

        
# 
#     def print_serial_data(self):
#          while True:
#             data = self.serial.read()
#             if data :
#                 if data == b'on':
#                    self.serial.write(data)
#                    print("onn")
#                 if data == b'off':
#                     self.serial.write('led is off')
#                     print("OOFF")
#                 else :
#                     self.serial.write('invalid data')
#             



