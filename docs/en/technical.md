# Utah-Vid-ia — Technical Reference

## Stack overview

```
Application (PyTorch / custom)
        ↓
UtahSiliconOrchestrator  ← unified entry
        ↓
┌───────────────────────────────────────────┐
│ GhostKernelLayer   (IR intercept)         │
│ UtahVectorCompiler (Triton BRTR / fallback)│
│ UtahOsmoticRouter  (multi-GPU pressure)   │
│ ZeoShieldEngine    (prefetch + heal)      │
│ zeo_shield_kernel.cu (optional native)    │
└───────────────────────────────────────────┘
        ↓
CUDA / ROCm / CPU (via PyTorch)
```

Full diagrams: [../ARCHITECTURE.md](../ARCHITECTURE.md)

## Modules

| Module | File | Responsibility |
|--------|------|----------------|
| Core | `utahvidia/core.py` | `GhostKernelLayer`, `UtahVidIaEngine`, `activate_ghost_layer()` |
| Compiler | `utahvidia/compiler.py` | `UtahVectorCompiler`, Triton JIT, CPU fallback |
| Osmotic | `utahvidia/osmotic.py` | `UtahOsmoticRouter`, async + sync routing |
| ZEO | `utahvidia/zeo_shield.py` | Prefetch streams, entropy heal, native loader |
| Orchestrator | `utahvidia/orchestrator.py` | `UtahSiliconOrchestrator` |
| Native | `zeo_shield_kernel.cu` | Tile prefetch + `entropy_shield` device fn |

## Requirements

- Python ≥ 3.10
- PyTorch ≥ 2.0
- Optional: Triton (Linux CUDA), NVCC (native ZEO JIT)

## Install

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
pip install -e ".[compiler]"   # Linux + Triton when available
```

## API surface

### Orchestrator (recommended)

```python
from utahvidia import UtahSiliconOrchestrator
import torch

orch = UtahSiliconOrchestrator()
A, B = torch.randn(512, 512), torch.randn(512, 512)
out = orch.execute_shielded_matmul(A, B)
layers = orch.run_llm_stress_demo(hidden=256, layers=8)
```

### Ghost layer

```python
from utahvidia import UtahVidIaEngine, activate_ghost_layer
import torch

engine = UtahVidIaEngine()
with activate_ghost_layer() as ghost:
    fn = ghost.wrap("add", torch.add)
    result = engine.execute_optimized(fn, x, y)
# ghost.history contains IR audit records
```

### ZEO-Shield

```python
from utahvidia import ZeoShieldEngine

engine = ZeoShieldEngine()
out = engine.matmul_shielded(A, B)
healed = engine.heal(corrupted_tensor, clean_reference)
```

### Osmotic routing

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
result = router.route_sync(torch.matmul, a, b)
```

## Native CUDA extension

Loaded lazily via `torch.utils.cpp_extension.load` when:

- CUDA available
- NVCC on `PATH`
- Sources: `zeo_shield_kernel.cu`, `native/zeo_shield_bindings.cpp`

Force Python path: `zeo_prefetched_matmul(A, B, use_native=False)`

## Benchmarks

```bash
utahvidia bench
utahvidia-bench --sizes 128 256 512 1024 --iters 20
```

Note: ZEO tile kernel is element-wise `A * B` with shield metadata; compare latency patterns, not GEMM FLOPs.

## Testing

```bash
pytest -q
```

## Extension points

1. **Real MLIR export** — replace string IR in `GhostKernelLayer.translate()`
2. **SPIR-V / ROCm backend** — plug into compiler compile path
3. **Custom parity sources** — enterprise checksum store for Entropy-Shield
4. **Scheduler integration** — K8s device plugin calling `UtahOsmoticRouter`

## Version

Current: **v0.2.0** (alpha)

[Back to index](index.md) · [CUDA programmers](cuda-programmers.md) · [Migration](migration-guide.md)
