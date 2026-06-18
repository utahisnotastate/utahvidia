"""
Utah-Vid-ia Asymptotic Reality Engine — unified gaming + compute orchestrator.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import torch

from utahvidia.fractal_graph import FractalHyperGraph
from utahvidia.holographic import HolographicTensorCore
from utahvidia.latency_shield import DisplayHookConfig, LatencyShieldIntercept
from utahvidia.microvisor import MicrovisorConfig, UtahMicrovisor
from utahvidia.orchestrator import UtahSiliconOrchestrator
from utahvidia.photonic_multi import PhotonicMultiBridge
from utahvidia.speculative_intent import IntentTelemetry, SpeculativeIntentEngine
from utahvidia.vram_osmotic import OsmoticVramRouter

logger = logging.getLogger("utahvidia.reality_engine")


@dataclass
class UtahRealityEngine(UtahSiliconOrchestrator):
    """
    End-state orchestrator: latency shield, osmotic VRAM, photonic multi-GPU,
    holographic inference, fractal distributed graph, speculative intent, microvisor sim.
    """

    latency_shield: LatencyShieldIntercept | None = None
    vram_router: OsmoticVramRouter = field(default_factory=lambda: OsmoticVramRouter(virtual_gigabytes=64))
    photonic_bridge: PhotonicMultiBridge = field(default_factory=PhotonicMultiBridge)
    holographic: HolographicTensorCore = field(default_factory=HolographicTensorCore)
    fractal: FractalHyperGraph = field(default_factory=FractalHyperGraph)
    intent_engine: SpeculativeIntentEngine = field(default_factory=SpeculativeIntentEngine)
    microvisor: UtahMicrovisor = field(
        default_factory=lambda: UtahMicrovisor(MicrovisorConfig(simulation_only=True))
    )
    display_hook: DisplayHookConfig = field(default_factory=DisplayHookConfig)

    def __post_init__(self) -> None:
        w, h = self.display_hook.width, self.display_hook.height
        dev = self.device if self.device != "cpu" else "cpu"
        if self.latency_shield is None:
            self.latency_shield = LatencyShieldIntercept(w, h, device=dev if dev != "cpu" else "cpu")

    def bootstrap_gaming_enclave(self) -> dict[str, str]:
        """Initialize simulated bare-metal gaming path."""
        return {
            "microvisor": self.microvisor.isolate_physical_function(),
            "hid": self.microvisor.map_hid_to_vram(),
            "display_hook": self.display_hook.describe(),
        }

    def reconstruct_frame(
        self,
        current: torch.Tensor,
        history: torch.Tensor,
        motion: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        assert self.latency_shield is not None
        return self.latency_shield.dispatch(current, history, motion, **kwargs)

    def perceptual_upscale_path(
        self,
        low_res: torch.Tensor,
        latent: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """Low-res baseline + holographic tensor synthesis demo."""
        if latent is None:
            latent = torch.randn(self.holographic.latent_dim, device=low_res.device)
        block_out = self.holographic.forward_block(low_res, latent)
        if low_res.dim() == 3:
            upscaled = torch.nn.functional.interpolate(
                low_res.permute(2, 0, 1).unsqueeze(0),
                scale_factor=2,
                mode="bilinear",
                align_corners=False,
            ).squeeze(0).permute(1, 2, 0)
            upscaled[..., :3] = upscaled[..., :3] * 0.5 + 0.5
            return upscaled
        return block_out

    def speculative_render_cycle(
        self,
        base_frame: torch.Tensor,
        mouse_delta: tuple[float, float],
        actual_click: bool = False,
    ) -> torch.Tensor:
        predicted = IntentTelemetry(delta_x=mouse_delta[0], delta_y=mouse_delta[1])
        self.intent_engine.render_phantoms(base_frame, predicted)
        actual = IntentTelemetry(
            delta_x=mouse_delta[0] + (0.1 if actual_click else 0.0),
            delta_y=mouse_delta[1],
            active_buttons=1 if actual_click else 0,
        )
        collapsed = self.intent_engine.collapse(actual, predicted)
        return collapsed if collapsed is not None else base_frame

    def distributed_weight_step(
        self,
        weights: torch.Tensor,
        predicted_grad: torch.Tensor,
        step: int,
    ) -> torch.Tensor:
        return self.fractal.assimilate(weights, predicted_grad, step)
