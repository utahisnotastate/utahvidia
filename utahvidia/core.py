"""
[SYSTEM: UTAH-VIDIA // KERNEL GHOSTING LAYER]
[PHYSICS: Just-In-Time Kernel Translation (JIT-KT)]
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator

import torch

logger = logging.getLogger("utahvidia.core")

# Ops routed through the ghost translation pipeline.
_GHOST_OPS: dict[str, Callable[..., torch.Tensor]] = {}
_LAYER_ACTIVE = False


@dataclass
class TranslationRecord:
    """Audit trail entry for a ghosted kernel call."""

    op_name: str
    target_ir: str
    device: str


@dataclass
class GhostKernelLayer:
    """
    Intercepts tensor operator dispatch and records JIT-KT translation.

    Instead of binding directly to vendor drivers, calls pass through a
    hardware-agnostic intermediate representation (MLIR-shaped stub today).
    """

    verbose: bool = True
    history: list[TranslationRecord] = field(default_factory=list)

    def translate(self, op_name: str, device: str) -> str:
        """Produce a portable IR label for the intercepted operation."""
        ir = f"utah.mlir.{op_name} @ device({device}) -> spirv"
        self.history.append(TranslationRecord(op_name, ir, device))
        if self.verbose:
            logger.info("[UTAH-VIDIA] Intercepting: Kernel Ghosting active — %s", ir)
        return ir

    def wrap(self, op_name: str, fn: Callable[..., torch.Tensor]) -> Callable[..., torch.Tensor]:
        """Return a callable that routes *fn* through the ghost layer."""

        def ghosted(*args: Any, **kwargs: Any) -> torch.Tensor:
            device = _resolve_device(args)
            self.translate(op_name, device)
            return fn(*args, **kwargs)

        return ghosted


def _resolve_device(args: tuple[Any, ...]) -> str:
    for arg in args:
        if isinstance(arg, torch.Tensor):
            return str(arg.device)
    return "cpu"


class UtahVidIaEngine:
    """Bridge that executes tensor work through the JIT translation pipeline."""

    def __init__(self, *, verbose: bool = True):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.ghost = GhostKernelLayer(verbose=verbose)

    def execute_optimized(self, func: Callable[..., torch.Tensor], *args: Any, **kwargs: Any) -> torch.Tensor:
        """
        Convert the call to a hardware-agnostic IR state, then execute.

        Today this records MLIR-shaped metadata and delegates to PyTorch;
        the hook points are stable for plugging in real MLIR/SPIR-V backends.
        """
        op_name = getattr(func, "__name__", "anonymous")
        if self.ghost.verbose:
            logger.info("[UTAH-VIDIA] Converting call to hardware-agnostic SPIR-V state...")
        self.ghost.translate(op_name, self.device)
        return func(*args, **kwargs)

    def matmul_demo(self, m: int = 512, n: int = 512, k: int = 512) -> torch.Tensor:
        """Run a representative GEMM through the ghost layer."""
        x = torch.randn(m, k, device=self.device)
        y = torch.randn(k, n, device=self.device)
        return self.execute_optimized(torch.matmul, x, y)


def _install_ghost_ops(layer: GhostKernelLayer) -> None:
    global _GHOST_OPS
    _GHOST_OPS = {
        "add": layer.wrap("add", torch.add),
        "mul": layer.wrap("mul", torch.mul),
        "matmul": layer.wrap("matmul", torch.matmul),
    }


def _restore_ghost_ops() -> None:
    global _GHOST_OPS
    _GHOST_OPS = {}


@contextmanager
def activate_ghost_layer(*, verbose: bool = True) -> Iterator[GhostKernelLayer]:
    """
    Context manager that activates kernel ghosting for common torch ops.

    Usage::

        with activate_ghost_layer() as ghost:
            z = ghost.wrap("add", torch.add)(x, y)
    """
    global _LAYER_ACTIVE
    layer = GhostKernelLayer(verbose=verbose)
    _install_ghost_ops(layer)
    _LAYER_ACTIVE = True
    try:
        yield layer
    finally:
        _restore_ghost_ops()
        _LAYER_ACTIVE = False


def ghost_add(input: torch.Tensor, other: torch.Tensor, *, alpha: float = 1) -> torch.Tensor:
    """Ghost-layer add; uses registered wrapper when the layer is active."""
    if _LAYER_ACTIVE and "add" in _GHOST_OPS:
        return _GHOST_OPS["add"](input, other, alpha=alpha)
    return torch.add(input, other, alpha=alpha)


# Register a custom CPU implementation hook (Batch 1 seed behavior).
try:
    _lib = torch.library.Library("utahvidia", "DEF")
    _lib.define("ghost_add(Tensor input, Tensor other, float alpha=1) -> Tensor")

    @torch.library.impl(_lib, "ghost_add", "CompositeExplicitAutograd")
    def _ghost_add_impl(input: torch.Tensor, other: torch.Tensor, alpha: float = 1) -> torch.Tensor:
        return ghost_add(input, other, alpha=alpha)
except Exception:  # pragma: no cover - library may already exist in reload scenarios
    pass
