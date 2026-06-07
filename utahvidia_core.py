"""
[SYSTEM: UTAH-VIDIA // KERNEL GHOSTING LAYER]
[AUTHOR: GENERAL 23 // UTAH-1]
[PHYSICS: Just-In-Time Kernel Translation (JIT-KT)]

Top-level entry point — delegates to the integrated package.
"""

from utahvidia.core import (
    GhostKernelLayer,
    UtahVidIaEngine,
    activate_ghost_layer,
    ghost_add,
)

__all__ = ["GhostKernelLayer", "UtahVidIaEngine", "activate_ghost_layer", "ghost_add"]

if __name__ == "__main__":
    import torch

    engine = UtahVidIaEngine()
    x = torch.randn(1024, 1024)
    y = torch.randn(1024, 1024)

    with activate_ghost_layer() as ghost:
        add_fn = ghost.wrap("add", torch.add)
        result = engine.execute_optimized(add_fn, x, y)

    print("[UTAH-VIDIA] Translation Success: Operator executed without driver lock-in.")
    print(f"Result shape: {result.shape}, device: {result.device}")
