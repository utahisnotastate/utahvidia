"""
[SYSTEM: UTAH-VIDIA // LATENCY SHIELD]
Top-level entry — driverless asynchronous frame reconstruction.
"""

from utahvidia.latency_shield import (
    DisplayHookConfig,
    JitProfiler,
    LatencyShieldIntercept,
    reconstruct_frames,
)
from utahvidia.reality_engine import UtahRealityEngine

__all__ = [
    "DisplayHookConfig",
    "JitProfiler",
    "LatencyShieldIntercept",
    "reconstruct_frames",
    "UtahRealityEngine",
]

if __name__ == "__main__":
    import torch

    engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=640, height=360))
    print(engine.bootstrap_gaming_enclave())

    h, w = 360, 640
    device = engine.device if engine.device != "cpu" else "cpu"
    current = torch.rand(h, w, 4, device=device)
    history = torch.rand(h, w, 4, device=device)
    motion = torch.zeros(h, w, 2, device=device)

    out = engine.reconstruct_frame(current, history, motion)
    print(f"[UTAH-VIDIA] Latency shield OK — frame {tuple(out.shape)}")
