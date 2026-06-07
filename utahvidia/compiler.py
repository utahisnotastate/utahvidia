"""
[SYSTEM: UTAH-VIDIA // VECTOR COMPILER]
[PHYSICS: Binary Real-Time Rewriting (BRTR) of compute kernels]
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable

import torch

logger = logging.getLogger("utahvidia.compiler")

try:
    import triton
    import triton.language as tl

    _TRITON_AVAILABLE = True
except ImportError:
    triton = None  # type: ignore[assignment]
    tl = None  # type: ignore[assignment]
    _TRITON_AVAILABLE = False


@dataclass
class SiliconGeometry:
    """Detected GPU capabilities used for BRTR tuning."""

    vendor: str
    capability: tuple[int, int] | None
    name: str


class UtahVectorCompiler:
    """
    JIT compiler brain: detects silicon geometry and rewrites kernels at runtime.

    When Triton + CUDA are present, kernels compile to device-specific machine
    code. Otherwise a portable PyTorch fallback is used.
    """

    def __init__(self):
        self.geometry = self._detect_geometry()
        logger.info(
            "[UTAH-VIDIA] Detecting Silicon Geometry: %s (%s)",
            self.geometry.capability,
            self.geometry.name,
        )

    @staticmethod
    def _detect_geometry() -> SiliconGeometry:
        if torch.cuda.is_available():
            idx = torch.cuda.current_device()
            cap = torch.cuda.get_device_capability(idx)
            name = torch.cuda.get_device_name(idx)
            return SiliconGeometry("cuda", cap, name)
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return SiliconGeometry("mps", None, "Apple MPS")
        return SiliconGeometry("cpu", None, "CPU")

    def compile(self, kernel_logic: Callable[..., Any]) -> Callable[..., Any]:
        """Invoke Binary Real-Time Rewrite via Triton JIT when available."""
        logger.info("[UTAH-VIDIA] Invoking Binary Real-Time Rewrite...")
        if _TRITON_AVAILABLE and self.geometry.vendor == "cuda":
            return triton.jit(kernel_logic)  # type: ignore[union-attr]
        return kernel_logic

    def block_size_for_arch(self, default: int = 128) -> int:
        """Pick a block size tuned to the detected architecture."""
        if self.geometry.capability and self.geometry.capability[0] >= 8:
            return 256
        return default


if _TRITON_AVAILABLE:

    @triton.jit  # type: ignore[misc]
    def utah_vector_kernel(x_ptr, y_ptr, n_elements, BLOCK_SIZE: tl.constexpr):  # type: ignore[name-defined]
        pid = tl.program_id(0)
        block_start = pid * BLOCK_SIZE
        offsets = block_start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < n_elements
        x = tl.load(x_ptr + offsets, mask=mask)
        y = x * 2.0
        tl.store(y_ptr + offsets, y, mask=mask)

else:

    def utah_vector_kernel(*_args: Any, **_kwargs: Any) -> None:
        raise RuntimeError("Triton is not installed; use trigger_compiler fallback path.")


def _torch_fallback(data_stream: torch.Tensor) -> torch.Tensor:
    """Portable fallback when BRTR/Triton path is unavailable."""
    logger.info("[UTAH-VIDIA] BRTR fallback: executing via PyTorch on %s", data_stream.device)
    return data_stream * 2.0


def trigger_compiler(data_stream: torch.Tensor) -> torch.Tensor:
    """
    Compile and execute the Utah vector kernel against *data_stream*.

    Uses Triton on CUDA; falls back to pure PyTorch elsewhere.
    """
    compiler = UtahVectorCompiler()

    if not _TRITON_AVAILABLE or compiler.geometry.vendor != "cuda":
        return _torch_fallback(data_stream)

    optimized_kernel = compiler.compile(utah_vector_kernel)
    n = data_stream.numel()
    output = torch.empty_like(data_stream)
    block = compiler.block_size_for_arch(128)
    grid = (triton.cdiv(n, block),)  # type: ignore[union-attr]

    optimized_kernel[grid](data_stream, output, n, BLOCK_SIZE=block)
    return output
