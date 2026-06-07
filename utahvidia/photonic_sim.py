"""
Desktop simulator for the Photonic Matrix Bridge.

The production firmware targets ESP32/MicroPython (see ``embedded/``).
This module lets you test OPWM routing logic on any host Python runtime.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

logger = logging.getLogger("utahvidia.photonic")


@dataclass
class PhotonicBridge:
    """
    Simulated optical pulse driver.

    On embedded hardware, ``tx``/``rx`` map to GPIO pins; here they are
    in-memory boolean channels.
    """

    tx_pin: int
    rx_pin: int
    _tx_state: int = 0
    _rx_buffer: list[int] = field(default_factory=list)

    def send_pulse(self, data_byte: int) -> None:
        """Emit an 8-bit OPWM pulse train on the simulated TX line."""
        for i in range(8):
            bit = (data_byte >> i) & 1
            self._tx_state = bit
            time.sleep(0.00001)  # 10 µs pulse — scaled down in sim
        self._tx_state = 0

    def read_pulse(self) -> int:
        """Return the current RX line state (simulated)."""
        return self._tx_state

    def receive_byte(self, data_byte: int) -> None:
        """Inject a byte as if received on the photonic RX channel."""
        self._rx_buffer.append(data_byte)


def route_swarm_data(bridge: PhotonicBridge, data: int) -> None:
    """Route a photonic packet through the matrix (simulated)."""
    logger.info("[UTAH-VIDIA] Routing Photonic Packet: 0x%02x", data)
    bridge.send_pulse(data)
    bridge.receive_byte(data)
