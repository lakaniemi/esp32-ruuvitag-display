# main.py

import utime as time
import machine

def start():
    pin = machine.Pin(2, machine.Pin.OUT)

    # Hello world! Blink LED on the board forever :)
    while True:
        pin.on()
        time.sleep_ms(1000)
        pin.off()
        time.sleep_ms(1000)
