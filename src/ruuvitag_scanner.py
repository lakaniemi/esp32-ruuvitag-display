import bluetooth
from micropython import const

_IRQ_SCAN_RESULT = const(1 << 4)

class RuuviTagScanner:

    def __init__(self):
        self.ble = bluetooth.BLE()
        # Trigger only on IRQ_SCAN_RESULT events
        self.ble.irq(self.scan_result, trigger=0x10)

    def scan_result(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            _, addr, _, _, adv_data = data

            # We must copy these as they are only references to shared data
            # managed by the bluetooth module.
            device_addr = bytes(addr)
            broadcast_data = bytes(adv_data)

            # In order to not cause out of bounds crashes
            if len(broadcast_data) < 7:
                return

            # RuuviTags have 0x99 and 0x04 as the 6th and 7th byte in
            # advertisement data
            if broadcast_data[5] == 0x99 and broadcast_data[6] == 0x04:
                # Stringify the address (example: de:4d:ef:cf:92:7b)
                address_str = ':'.join('{:x}'.format(b) for b in device_addr)
                # The actual content of the broadcast
                sensor_data = broadcast_data[7:]

                print('found ruuvitag: ' + address_str + ' with data: ' + str(sensor_data))

    def start(self):
        self.ble.active(True)
        # Scan interval 30s = 3000000us (microseconds)
        # Scan duration 5s = 5000000us
        # 0 = Scan forever
        self.ble.gap_scan(0, 30000000, 5000000)

    def stop(self):
        self.ble.active(False)
