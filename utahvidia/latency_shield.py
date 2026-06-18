"""
[SYSTEM: UTAH-VIDIA // LATENCY SHIELD]
Driverless asynchronous frame reconstruction + host intercept layer.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Literal

import torch

from utahvidia.native_loader import load_cuda_extension

logger = logging.getLogger("utahvidia.latency_shield")

_NATIVE = None


def _get_native():
    global _NATIVE
    if _NATIVE is None:
        _NATIVE = load_cuda_extension(
            "utahvidia_latency_shield",
            ["native/latency_shield_kernel.cu", "native/latency_shield_bindings.cpp"],
        )
    return _NATIVE


def reconstruct_frames_torch(
    current: torch.Tensor,
    history: torch.Tensor,
    motion: torch.Tensor,
    *,
    alpha: float = 0.65,
) -> torch.Tensor:
    """PyTorch fallback: motion-aware blend between current and history frames."""
    h, w, _ = current.shape
    yy, xx = torch.meshgrid(
        torch.arange(h, device=current.device),
        torch.arange(w, device=current.device),
        indexing="ij",
    )
    sx = (xx.float() + motion[..., 0]).clamp(0, w - 1).long()
    sy = (yy.float() + motion[..., 1]).clamp(0, h - 1).long()
    warped_history = history[sy, sx]
    out = current * alpha + warped_history * (1.0 - alpha)
    out[..., 3] = 1.0
    return out


def reconstruct_frames(
    current: torch.Tensor,
    history: torch.Tensor,
    motion: torch.Tensor,
    *,
    alpha: float = 0.65,
    use_native: bool = True,
) -> torch.Tensor:
    """
    Interpolate a display-ready frame from current/history RGBA + motion field.

    *current*, *history*: ``H x W x 4`` float tensors (RGBA).
    *motion*: ``H x W x 2`` float tensor (dx, dy per pixel).
    """
    if current.shape != history.shape or current.dim() != 3 or current.size(-1) != 4:
        raise ValueError("current/history must be HxWx4")
    if motion.shape[:2] != current.shape[:2] or motion.size(-1) != 2:
        raise ValueError("motion must be HxWx2")

    native = _get_native() if use_native and current.is_cuda else None
    if native is not None:
        return native.reconstruct_frames_cuda(current, history, motion, alpha)
    return reconstruct_frames_torch(current, history, motion, alpha=alpha)


@dataclass
class ThermalProfile:
    name: str
    alpha: float
    block_occupancy_target: float


@dataclass
class JitProfiler:
    """
    Telemetry-driven kernel profile selection (host-side simulation).

    Hot-swaps reconstruction parameters based on thermal/occupancy telemetry.
    Full PTX module swapping requires CUDA Driver API deployment.
    """

    profiles: dict[str, ThermalProfile] = field(default_factory=lambda: {
        "PERFORMANCE_MAX": ThermalProfile("PERFORMANCE_MAX", 0.65, 1.0),
        "THERMAL_BYPASS": ThermalProfile("THERMAL_BYPASS", 0.55, 0.75),
    })
    current_profile: str = "PERFORMANCE_MAX"
    thermal_ceiling_c: float = 82.0

    def evaluate(self, core_temp_c: float, occupancy_ratio: float) -> ThermalProfile:
        optimal = "PERFORMANCE_MAX"
        if core_temp_c > self.thermal_ceiling_c or occupancy_ratio < 0.5:
            optimal = "THERMAL_BYPASS"
        if optimal != self.current_profile:
            logger.info("[UTAH-VIDIA] JIT profile hot-swap: %s -> %s", self.current_profile, optimal)
            self.current_profile = optimal
        return self.profiles[optimal]


@dataclass
class LatencyShieldIntercept:
    """
    Host-side intercept layer for frame reconstruction pipelines.

    Uses dedicated CUDA streams orthogonal to the primary render queue.
    """

    width: int
    height: int
    device: str = "cuda"
    profiler: JitProfiler = field(default_factory=JitProfiler)
    _stream: torch.cuda.Stream | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        if self.device == "cuda" and torch.cuda.is_available():
            self._stream = torch.cuda.Stream(priority=-1)
        else:
            self.device = "cpu"

    def dispatch(
        self,
        current: torch.Tensor,
        history: torch.Tensor,
        motion: torch.Tensor,
        *,
        core_temp_c: float = 65.0,
        occupancy_ratio: float = 0.9,
        use_native: bool = True,
    ) -> torch.Tensor:
        profile = self.profiler.evaluate(core_temp_c, occupancy_ratio)
        if self._stream is not None:
            with torch.cuda.stream(self._stream):
                out = reconstruct_frames(current, history, motion, alpha=profile.alpha, use_native=use_native)
            self._stream.synchronize()
            return out
        return reconstruct_frames(current, history, motion, alpha=profile.alpha, use_native=use_native)


HookMode = Literal["pytorch", "driver_api_stub"]


@dataclass
class DisplayHookConfig:
    """
    Host hook configuration.

    ``driver_api_stub`` documents the CUDA Driver API path; production Vulkan/DX12
    intercept requires platform-specific integration outside this package.
    """

    mode: HookMode = "pytorch"
    width: int = 1920
    height: int = 1080
    ptx_path: str = "kernels/utahvidia_kernel.ptx"

    def describe(self) -> str:
        if self.mode == "driver_api_stub":
            return (
                "[UTAH-VIDIA] Driver API intercept: cuInit -> cuModuleLoad(PTX) -> "
                "cuLaunchKernel on dedicated CUstream (bypasses OS display scheduler)."
            )
        return "[UTAH-VIDIA] PyTorch stream intercept active (portable demo path)."
