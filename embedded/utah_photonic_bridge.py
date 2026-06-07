"""
[SYSTEM: UTAH-VIDIA // PHOTONIC MATRIX BRIDGE]
[AUTHOR: GENERAL 23 // UTAH-1]
[PHYSICS: Optical Pulse Width Modulation (OPWM)

Flash this file to an M5Stack / ESP32 with MicroPython.
Pin 26/32 map to standard Grove UART pins repurposed for IR TX/RX.
"""

import machine
import time


class PhotonicBridge:
    def __init__(self, tx_pin, rx_pin):
        self.tx = machine.Pin(tx_pin, machine.Pin.OUT)
        self.rx = machine.Pin(rx_pin, machine.Pin.IN)

    def send_pulse(self, data_byte):
        for i in range(8):
            bit = (data_byte >> i) & 1
            self.tx.value(bit)
            time.sleep_us(10)
        self.tx.value(0)

    def read_pulse(self):
        return self.rx.value()


def route_swarm_data(bridge, data):
    print("[UTAH-VIDIA] Routing Photonic Packet:", data)
    bridge.send_pulse(data)


if __name__ == "__main__":
    bridge = PhotonicBridge(tx_pin=26, rx_pin=32)
    while True:
        route_swarm_data(bridge, 0x55)
        time.sleep(1)
