# Migration Guide — CUDA / PyTorch → Utah-Vid-ia

This guide helps teams adopt Utah-Vid-ia incrementally without stopping production training or inference.

## Migration principles

1. **Shadow first** — run Utah-Vid-ia parallel to existing jobs; compare outputs and latency.
2. **One layer at a time** — orchestrator → osmotic routing → ZEO → native kernels.
3. **Keep rollback** — feature flag the import; no big-bang rewrite.

## Phase 0 — Inventory (1 week)

Document:

- [ ] PyTorch vs raw CUDA vs Triton usage
- [ ] GPU models and drivers in each environment
- [ ] Multi-GPU topology (NVLink, PCIe)
- [ ] Critical latency SLOs and error budgets

Install Utah-Vid-ia on a dev machine:

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
utahvidia all
pytest -q
```

## Phase 1 — Ghost layer observability (1–2 weeks)

**Goal:** IR audit trail without changing numerics.

```python
from utahvidia import activate_ghost_layer
import torch

with activate_ghost_layer(verbose=True) as ghost:
    # wrap your existing torch calls
    result = ghost.wrap("matmul", torch.matmul)(a, b)

for record in ghost.history:
    print(record.op_name, record.target_ir)
```

**Exit criteria:** All hot-path ops logged; no measurable regression in p99 latency.

## Phase 2 — Osmotic routing (2–4 weeks)

**Goal:** Spread batch jobs across GPUs by pressure, not hard-coded device IDs.

Before:

```python
with torch.cuda.device(0):
    out = model(batch)
```

After:

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
out = router.route_sync(forward_fn, batch)
```

**Exit criteria:** Improved utilization on multi-GPU nodes; no correctness drift on golden tests.

## Phase 3 — Orchestrator unify (2–4 weeks)

**Goal:** Single API for ghost + routing + ZEO hooks.

```python
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
out = orch.execute_shielded_matmul(a, b)
pipeline_out = orch.run_llm_stress_demo(hidden=4096, layers=your_layer_count)
```

Replace ad-hoc device logic with orchestrator calls behind a config flag:

```python
USE_UTAH = os.getenv("UTAHVIDIA", "0") == "1"

if USE_UTAH:
    out = orch.execute_shielded_matmul(a, b)
else:
    out = torch.matmul(a, b)
```

## Phase 4 — Vector compiler / Triton (optional, Linux CUDA)

```bash
pip install -e ".[compiler]"
```

```python
from utahvidia.compiler import trigger_compiler
out = trigger_compiler(data_tensor)
```

Use for element-wise custom ops before porting full GEMM to Triton.

## Phase 5 — Native ZEO kernel (optional)

Requires NVCC. Benchmark before enabling in production:

```bash
utahvidia bench
```

Enable per workload:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul
out = zeo_prefetched_matmul(a, b, use_native=True)
```

## Phase 6 — Entropy healing (research / batch only)

Do **not** enable healing on live training loss paths without validation.

```python
from utahvidia import ZeoShieldEngine
engine = ZeoShieldEngine()
restored = engine.heal(corrupted, reference_clean)
```

## Rollback checklist

- Set `UTAHVIDIA=0`
- Remove orchestrator wrapper imports
- Keep ghost logs disabled (`verbose=False`)

## Validation matrix

| Test | Pass condition |
|------|----------------|
| Numerical parity | `torch.allclose(baseline, utah, rtol=..., atol=...)` |
| Latency | p99 within agreed budget |
| Multi-GPU | Utilization σ decreased |
| Soak test | 24h batch job, zero new OOM classes |

## From other stacks

| Source stack | Notes |
|--------------|-------|
| **Pure CUDA C++** | Wrap at PyTorch boundary first, or bind custom extension like `zeo_shield_bindings.cpp` |
| **JAX** | Not supported directly; export to PyTorch or call Python orchestrator via subprocess |
| **TensorFlow** | Same — use TFX/PyTorch bridge or port hot path |
| **ROCm PyTorch** | Osmotic + ghost work; native ZEO CUDA kernel is NVIDIA-only today |

## Support

Issues: [GitHub Issues](https://github.com/utahisnotastate/utahvidia/issues)  
Donate: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

[Back to index](index.md) · [CUDA programmers](cuda-programmers.md)
