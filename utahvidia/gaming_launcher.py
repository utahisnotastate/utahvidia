"""
One-click Utah-Vid-ia Gaming Unlock launcher.

Runs the full Asymptotic Reality Engine with the max gaming profile applied.
Packaged as UtahVidia-Gaming.exe for users without Git/Python setup.
"""

from __future__ import annotations

import sys
import time

import torch

from utahvidia.gaming_profiles import DEFAULT_GAMING_PROFILE, apply_gaming_profile, donate_footer
from utahvidia.latency_shield import DisplayHookConfig
from utahvidia.reality_engine import UtahRealityEngine


def run_gaming_unlock(*, width: int = 640, height: int = 360, profile: str = DEFAULT_GAMING_PROFILE) -> int:
    print("=" * 60)
    print("  UTAH-VIDIA GAMING UNLOCK")
    print("  Full stack enabled — no install, no unlock file needed")
    print("=" * 60)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("  GPU: none detected (CPU demo mode)")

    engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=width, height=height))
    cfg = apply_gaming_profile(engine, profile)
    print(f"  Profile: {profile} (alpha={cfg['alpha']}, virtual VRAM={cfg['virtual_gigabytes']} GB)")

    print("\n[1/4] Boot gaming enclave...")
    for k, v in engine.bootstrap_gaming_enclave().items():
        print(f"  {k}: {v}")

    print("\n[2/4] Latency shield frame reconstruction...")
    current = torch.rand(height, width, 4, device=device)
    history = torch.rand(height, width, 4, device=device)
    motion = torch.randn(height, width, 2, device=device) * 0.3
    t0 = time.perf_counter()
    frame = engine.reconstruct_frame(current, history, motion)
    if device == "cuda":
        torch.cuda.synchronize()
    ms = (time.perf_counter() - t0) * 1000
    print(f"  OK: {tuple(frame.shape)} in {ms:.2f} ms")

    print("\n[3/4] Perceptual upscale + speculative intent...")
    latent = torch.randn(engine.holographic.latent_dim, device=device)
    upscaled = engine.perceptual_upscale_path(current[..., :3], latent)
    speculative = engine.speculative_render_cycle(current, (1.5, -0.5))
    print(f"  Upscale: {tuple(upscaled.shape)} | Speculative: {tuple(speculative.shape)}")

    print("\n[4/4] Fractal + holographic paths...")
    w = torch.randn(64, device=device)
    g = torch.randn(64, device=device)
    engine.fractal.ring.push(1, g)
    engine.distributed_weight_step(w, g, step=1)
    print(f"  Holographic seed bytes: {engine.holographic.memory_footprint_bytes()}")

    print("\n" + "=" * 60)
    print("  GAMING UNLOCK COMPLETE — all profiles active")
    print("=" * 60)
    print(donate_footer())
    return 0


def main() -> None:
    try:
        code = run_gaming_unlock()
    except KeyboardInterrupt:
        print("\nCancelled.")
        code = 130
    except Exception as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        code = 1

    if getattr(sys, "frozen", False):
        input("\nPress Enter to exit...")
    sys.exit(code)


if __name__ == "__main__":
    main()
