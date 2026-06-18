"""
GPU Unlock Patron Program — local unlock for Pro Gaming Profiles.

Open-source core remains free. Patrons who donate via PayPal (memo GPU-UNLOCK)
activate Pro presets via env var or ~/.utahvidia/patron.unlock
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utahvidia.reality_engine import UtahRealityEngine

PAYPAL_DONATE = "https://www.paypal.com/donate/?business=utah%40utahcreates.com"
PAYPAL_EMAIL = "utah@utahcreates.com"
UNLOCK_MEMO = "GPU-UNLOCK"

FREE_PROFILES = {
    "competitive": {"alpha": 0.75, "speculative_horizon": 3, "virtual_gigabytes": 64},
    "cinematic": {"alpha": 0.55, "speculative_horizon": 3, "virtual_gigabytes": 64},
    "vr": {"alpha": 0.60, "speculative_horizon": 2, "virtual_gigabytes": 48},
}

PATRON_PROFILES = {
    "patron_max": {"alpha": 0.70, "speculative_horizon": 6, "virtual_gigabytes": 128, "use_native": True},
    "patron_vram": {"alpha": 0.65, "speculative_horizon": 4, "virtual_gigabytes": 256, "use_native": True},
    "patron_legend": {"alpha": 0.68, "speculative_horizon": 6, "virtual_gigabytes": 512, "use_native": True},
}


def _patron_file() -> Path:
    return Path.home() / ".utahvidia" / "patron.unlock"


def is_patron_unlocked() -> bool:
    if os.getenv("UTAHVIDIA_PATRON", "").strip() in ("1", "true", "yes", UNLOCK_MEMO):
        return True
    path = _patron_file()
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8").strip().upper()
    return UNLOCK_MEMO in content or content.startswith("GPU")


@dataclass
class PatronStatus:
    unlocked: bool
    source: str
    available_profiles: list[str]
    paypal_email: str = PAYPAL_EMAIL
    donate_url: str = PAYPAL_DONATE

    def banner(self) -> str:
        if self.unlocked:
            return "[UTAH-VIDIA] Patron unlock: ACTIVE — Pro Gaming Profiles enabled."
        return (
            "[UTAH-VIDIA] Patron unlock: inactive. Donate with memo GPU-UNLOCK -> "
            f"{PAYPAL_DONATE}"
        )


def patron_status() -> PatronStatus:
    if os.getenv("UTAHVIDIA_PATRON", "").strip() in ("1", "true", "yes", UNLOCK_MEMO):
        source = "UTAHVIDIA_PATRON environment variable"
    elif _patron_file().is_file():
        source = str(_patron_file())
    else:
        source = "none"
    profiles = list_profiles()
    return PatronStatus(
        unlocked=is_patron_unlocked(),
        source=source,
        available_profiles=profiles,
    )


def list_profiles() -> list[str]:
    profiles = list(FREE_PROFILES.keys())
    if is_patron_unlocked():
        profiles.extend(PATRON_PROFILES.keys())
    return profiles


def apply_gaming_profile(engine: UtahRealityEngine, profile_name: str) -> dict:
    """Apply a named gaming preset to a UtahRealityEngine instance."""
    all_profiles = {**FREE_PROFILES, **(PATRON_PROFILES if is_patron_unlocked() else {})}
    if profile_name not in all_profiles:
        if profile_name in PATRON_PROFILES:
            raise PermissionError(
                f"Profile '{profile_name}' requires patron unlock. "
                f"Donate to {PAYPAL_EMAIL} with memo {UNLOCK_MEMO}. See docs/en/gpu-unlock-patron.md"
            )
        raise KeyError(f"Unknown profile '{profile_name}'. Available: {list(all_profiles.keys())}")

    cfg = all_profiles[profile_name]
    if engine.latency_shield is not None and engine.latency_shield.profiler.profiles.get("PERFORMANCE_MAX"):
        engine.latency_shield.profiler.profiles["PERFORMANCE_MAX"].alpha = cfg["alpha"]
        engine.latency_shield.profiler.profiles["THERMAL_BYPASS"].alpha = max(0.45, cfg["alpha"] - 0.1)
    engine.intent_engine.horizon = cfg.get("speculative_horizon", 3)
    engine.vram_router.virtual_gigabytes = cfg.get("virtual_gigabytes", 64)
    return cfg


def create_patron_unlock_file() -> Path:
    """Create patron unlock file (for post-donation setup)."""
    path = _patron_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{UNLOCK_MEMO}\n", encoding="utf-8")
    return path
