# Utah-Vid-ia — tehniline viide

## Virna ülevaade

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

Täielikud diagrammid: [../ARCHITECTURE.md](../ARCHITECTURE.md)

## Moodulid

| Moodul | Fail | Vastutus |
|--------|------|----------|
| Core | `utahvidia/core.py` | `GhostKernelLayer`, `UtahVidIaEngine`, `activate_ghost_layer()` |
| Compiler | `utahvidia/compiler.py` | `UtahVectorCompiler`, Triton JIT, CPU fallback |
| Osmotic | `utahvidia/osmotic.py` | `UtahOsmoticRouter`, async + sync routing |
| ZEO | `utahvidia/zeo_shield.py` | Prefetch streams, entropy heal, native loader |
| Orchestrator | `utahvidia/orchestrator.py` | `UtahSiliconOrchestrator` |
| Native | `zeo_shield_kernel.cu` | Tile prefetch + `entropy_shield` device fn |

## Nõuded

- Python ≥ 3.10
- PyTorch ≥ 2.0
- Valikuline: Triton (Linux CUDA), NVCC (native ZEO JIT)

## Paigaldus

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
pip install -e ".[compiler]"   # Linux + Triton when available
```

## API pind

### Orkestreerija (soovitatav)

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

### Osmootiline marsruutimine

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
result = router.route_sync(torch.matmul, a, b)
```

## Natiivne CUDA laiendus

Laaditakse laisalt `torch.utils.cpp_extension.load` kaudu, kui:

- CUDA on saadaval
- NVCC on `PATH`-is
- Allikad: `zeo_shield_kernel.cu`, `native/zeo_shield_bindings.cpp`

Sunnitud Python tee: `zeo_prefetched_matmul(A, B, use_native=False)`

## Võrdlustestid

```bash
utahvidia bench
utahvidia-bench --sizes 128 256 512 1024 --iters 20
```

Märkus: ZEO plaadi tuum on elementide kaupa `A * B` koos shield metaandmetega; võrdle latentsusmustreid, mitte GEMM FLOPs-e.

## Testimine

```bash
pytest -q
```

## Laienduspunktid

1. **Tõeline MLIR eksport** — asenda string IR `GhostKernelLayer.translate()`-is
2. **SPIR-V / ROCm backend** — ühenda kompilaatori kompileerimistee
3. **Kohandatud pariteedi allikad** — ettevõtte kontrollsumma hoidla Entropy-Shield jaoks
4. **Ajastaja integratsioon** — K8s seadme plugin, mis kutsub `UtahOsmoticRouter`-it

## Versioon

Praegune: **v0.2.0** (alfa)

[Tagasi indeksisse](index.md) · [CUDA programmeerijatele](cuda-programmers.md) · [Migratsioon](migration-guide.md)
