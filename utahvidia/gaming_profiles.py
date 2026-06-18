"""Gaming profile presets — all free, no unlock required."""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch

if TYPE_CHECKING:
    from utahvidia.reality_engine import UtahRealityEngine

DONATE_URL = "https://www.paypal.com/donate/?business=utah%40utahcreates.com"
DONATE_EMAIL = "utah@utahcreates.com"

GAMING_PROFILES: dict[str, dict] = {
    "competitive": {"alpha": 0.75, "speculative_horizon": 3, "virtual_gigabytes": 64},
    "cinematic": {"alpha": 0.55, "speculative_horizon": 3, "virtual_gigabytes": 64},
    "vr": {"alpha": 0.60, "speculative_horizon": 2, "virtual_gigabytes": 48},
    "max": {"alpha": 0.70, "speculative_horizon": 6, "virtual_gigabytes": 128},
    "vram": {"alpha": 0.65, "speculative_horizon": 4, "virtual_gigabytes": 256},
    "legend": {"alpha": 0.68, "speculative_horizon": 6, "virtual_gigabytes": 512},
}

DEFAULT_GAMING_PROFILE = "max"


def list_profiles() -> list[str]:
    return list(GAMING_PROFILES.keys())


def apply_gaming_profile(engine: UtahRealityEngine, profile_name: str = DEFAULT_GAMING_PROFILE) -> dict:
    """Apply a named gaming preset to a UtahRealityEngine instance."""
    if profile_name not in GAMING_PROFILES:
        raise KeyError(f"Unknown profile '{profile_name}'. Available: {list_profiles()}")

    cfg = GAMING_PROFILES[profile_name]
    if engine.latency_shield is not None:
        perf = engine.latency_shield.profiler.profiles.get("PERFORMANCE_MAX")
        thermal = engine.latency_shield.profiler.profiles.get("THERMAL_BYPASS")
        if perf:
            perf.alpha = cfg["alpha"]
        if thermal:
            thermal.alpha = max(0.45, cfg["alpha"] - 0.1)
    engine.intent_engine.horizon = cfg.get("speculative_horizon", 3)
    h = engine.intent_engine.horizon
    engine.intent_engine.latent_state = torch.zeros(h * 2)
    engine.vram_router.virtual_gigabytes = cfg.get("virtual_gigabytes", 64)
    return cfg


def donate_footer() -> str:
    return (
        f"\nUtah-Vid-ia is free (MIT). Optional donations: {DONATE_EMAIL}\n"
        f"{DONATE_URL}\n"
    )
