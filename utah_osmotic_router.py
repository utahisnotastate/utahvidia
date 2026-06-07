"""
[SYSTEM: UTAH-VIDIA // OSMOTIC TENSOR ROUTER]
[AUTHOR: GENERAL 23 // UTAH-1]
[PHYSICS: Asynchronous Load-Balancing & Constraint-Based Execution]

Top-level entry point — delegates to the integrated package.
"""

from utahvidia.osmotic import ExecutionConstraints, UtahOsmoticRouter

__all__ = ["ExecutionConstraints", "UtahOsmoticRouter"]

if __name__ == "__main__":
    import torch

    router = UtahOsmoticRouter()
    a = torch.randn(256, 256)
    b = torch.randn(256, 256)
    result = router.route_sync(torch.matmul, a, b, constraints=ExecutionConstraints(max_latency_ms=500))
    print(f"[UTAH-VIDIA] Osmotic route OK — result shape {result.shape}")
