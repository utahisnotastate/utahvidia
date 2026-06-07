"""
[SYSTEM: UTAH-VIDIA // ZEO-SHIELD ENGINE]
Top-level entry point — delegates to the integrated package.
"""

from utahvidia.zeo_shield import (
    NeuralStatePrefetcher,
    PrefetchJob,
    ZeoShieldEngine,
    build_parity_lattice,
    entropy_shield_tensor,
    zeo_prefetched_matmul,
)

__all__ = [
    "NeuralStatePrefetcher",
    "PrefetchJob",
    "ZeoShieldEngine",
    "build_parity_lattice",
    "entropy_shield_tensor",
    "zeo_prefetched_matmul",
]

if __name__ == "__main__":
    import torch

    engine = ZeoShieldEngine()
    n = 256
    device = "cuda" if torch.cuda.is_available() else "cpu"
    A = torch.randn(n, n, device=device)
    B = torch.randn(n, n, device=device)

    out = engine.matmul_shielded(A, B)
    corrupted = engine.inject_bit_flip(out, 42, delta=0.5)
    healed = engine.heal(corrupted, out)

    delta = (corrupted - out).abs().max().item()
    residual = (healed - out).abs().max().item()
    print(f"[UTAH-VIDIA] ZEO-Shield OK — max corruption={delta:.4f}, post-heal={residual:.4f}")
