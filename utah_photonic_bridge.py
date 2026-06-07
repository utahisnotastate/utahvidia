"""
[SYSTEM: UTAH-VIDIA // PHOTONIC MATRIX BRIDGE]
[AUTHOR: GENERAL 23 // UTAH-1]
[PHYSICS: Optical Pulse Width Modulation (OPWM) / Non-Blocking Fiber-Sim]

Host-side launcher. ESP32/MicroPython firmware lives in ``embedded/utah_photonic_bridge.py``.
"""

from utahvidia.photonic_sim import PhotonicBridge, route_swarm_data

__all__ = ["PhotonicBridge", "route_swarm_data"]

if __name__ == "__main__":
    bridge = PhotonicBridge(tx_pin=26, rx_pin=32)
    for _ in range(3):
        route_swarm_data(bridge, 0x55)
    print("[UTAH-VIDIA] Photonic sim complete — 3 packets routed.")
