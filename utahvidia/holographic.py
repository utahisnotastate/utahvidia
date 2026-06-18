"""
Holographic Tensor Primitives — procedural weight synthesis (VRAM annihilator demo).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import torch

logger = logging.getLogger("utahvidia.holographic")


@dataclass
class HolographicTensorCore:
    """
    Synthesize weight blocks from a tiny latent seed instead of loading full weights.

    Demonstrates Kolmogorov-complexity-style procedural matrices for inference demos.
    """

    latent_dim: int = 128
    block_size: int = 16
    seed: int = 42

    def _synthesize_block(self, latent: torch.Tensor, block_idx: int, device: torch.device) -> torch.Tensor:
        gen = torch.Generator(device=device)
        gen.manual_seed(self.seed + block_idx * 9973 + int(latent.sum().item() * 1000) % 100000)
        block = torch.randn(self.block_size, self.block_size, generator=gen, device=device)
        bias = latent[block_idx % latent.numel()].item()
        return block * bias

    def forward_block(
        self,
        activations: torch.Tensor,
        latent: torch.Tensor,
        block_idx: int = 0,
    ) -> torch.Tensor:
        """Multiply activation tile against procedurally synthesized weights."""
        device = activations.device
        w = self._synthesize_block(latent, block_idx, device)
        if activations.dim() == 2:
            tile = activations[: self.block_size, : self.block_size]
            return tile @ w
        return activations @ w[: activations.size(-1), : activations.size(-1)]

    def memory_footprint_bytes(self) -> int:
        """Latent seed only — weights never stored."""
        return self.latent_dim * 4
