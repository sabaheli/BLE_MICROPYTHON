import ubluetooth
from functions import LEDController


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
        self.rx_buffer = b""

    def set_connection_status(self, status):
        self.connection_F = status

    def ble_irq(self, event, data):
        if event == 1: #_IRQ_CENTRAL_CONNECT:
                       # A central has connected to this peripheral
            self.set_connection_status(True)
            #self.connected()

        elif event == 2: #_IRQ_CENTRAL_DISCONNECT:
                         # A central has disconnected from this peripheral.
            self.advertiser()
            self.set_connection_status(False)
            self.disconnected()
        
        elif event == 3: #_IRQ_GATTS_WRITE:
                         # A client has written to this characteristic or descriptor.          
            value = self.ble.gatts_read(self.rx)
            self.rx_buffer += value
            if b"\n" in self.rx_buffer:
                lines = self.rx_buffer.split(b"\n")
                self.rx_buffer = lines[-1]
                for line in lines[:-1]:
                    line = line.strip().decode()
                    if line == "on":
                        print("yeeeesss")
                        print(line[0])
                    if line == "off":
                        print("nooooo")
                        print(line)

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
        adv_data = bytearray(b'x02\x01\x06') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)
        print("rn")


