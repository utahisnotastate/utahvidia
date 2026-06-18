"""
Neuromorphic Intent Prediction — speculative input rendering (negative latency demo).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import torch

logger = logging.getLogger("utahvidia.speculative_intent")

PREDICTION_HORIZON = 3


@dataclass
class IntentTelemetry:
    delta_x: float = 0.0
    delta_y: float = 0.0
    pressure_gradient: float = 0.0
    active_buttons: int = 0


@dataclass
class SpeculativeIntentEngine:
    """
    Predict future input trajectories and pre-render phantom frame buffers.
    """

    horizon: int = PREDICTION_HORIZON
    latent_state: torch.Tensor = field(default_factory=lambda: torch.zeros(PREDICTION_HORIZON * 2))
    phantom_buffers: list[torch.Tensor] = field(default_factory=list)

    def predict_trajectory(self, intent: IntentTelemetry) -> list[tuple[float, float]]:
        preds: list[tuple[float, float]] = []
        for t in range(self.horizon):
            scale = 1.1 + (t * 0.05)
            px = intent.delta_x * scale + self.latent_state[t * 2].item()
            py = intent.delta_y * scale + self.latent_state[t * 2 + 1].item()
            preds.append((px, py))
        return preds

    def render_phantoms(
        self,
        base_frame: torch.Tensor,
        intent: IntentTelemetry,
    ) -> list[torch.Tensor]:
        """Synthesize phantom frames by spatially shifting base frame per prediction."""
        h, w, c = base_frame.shape
        self.phantom_buffers = []
        for t, (px, py) in enumerate(self.predict_trajectory(intent)):
            phantom = torch.zeros_like(base_frame)
            shift_x = int(px) % w
            shift_y = int(py) % h
            phantom = torch.roll(base_frame, shifts=(shift_y, shift_x), dims=(0, 1))
            phantom[..., 0] += 0.01 * t
            self.phantom_buffers.append(phantom)
        return self.phantom_buffers

    def collapse(
        self,
        actual_intent: IntentTelemetry,
        predicted: IntentTelemetry,
    ) -> torch.Tensor | None:
        """Select phantom buffer when prediction matches actual input within tolerance."""
        if not self.phantom_buffers:
            return None
        err = abs(actual_intent.delta_x - predicted.delta_x) + abs(actual_intent.delta_y - predicted.delta_y)
        if err < 2.0:
            logger.info("[UTAH-VIDIA] Speculative collapse: zero-latency frame swap")
            return self.phantom_buffers[0]
        return self.phantom_buffers[min(1, len(self.phantom_buffers) - 1)]
