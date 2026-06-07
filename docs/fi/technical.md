# Utah-Vid-ia — Tekninen viite

## Pinon yleiskatsaus

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

Täydet kaaviot: [../ARCHITECTURE.md](../ARCHITECTURE.md)

## Moduulit

| Moduuli | Tiedosto | Vastuu |
|--------|------|----------------|
| Core | `utahvidia/core.py` | `GhostKernelLayer`, `UtahVidIaEngine`, `activate_ghost_layer()` |
| Compiler | `utahvidia/compiler.py` | `UtahVectorCompiler`, Triton JIT, CPU fallback |
| Osmotic | `utahvidia/osmotic.py` | `UtahOsmoticRouter`, async + sync routing |
| ZEO | `utahvidia/zeo_shield.py` | Prefetch streams, entropy heal, native loader |
| Orchestrator | `utahvidia/orchestrator.py` | `UtahSiliconOrchestrator` |
| Native | `zeo_shield_kernel.cu` | Tile prefetch + `entropy_shield` device fn |

## Vaatimukset

- Python ≥ 3.10
- PyTorch ≥ 2.0
- Valinnainen: Triton (Linux CUDA), NVCC (natiivi ZEO JIT)

## Asennus

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
pip install -e ".[compiler]"   # Linux + Triton when available
```

## API-pinta

### Orchestrator (suositeltu)

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

## Natiivi CUDA-laajennus

Ladataan laiskasti `torch.utils.cpp_extension.load` -kautta, kun:

- CUDA on käytettävissä
- NVCC on `PATH`:ssa
- Lähteet: `zeo_shield_kernel.cu`, `native/zeo_shield_bindings.cpp`

Pakota Python-polku: `zeo_prefetched_matmul(A, B, use_native=False)`

## Vertailumittaukset

```bash
utahvidia bench
utahvidia-bench --sizes 128 256 512 1024 --iters 20
```

Huom: ZEO-laattakernel on elementtikohtainen `A * B` suojametatiedoilla; vertaa viivekuvioita, ei GEMM-FLOP:eja.

## Testaus

```bash
pytest -q
```

## Laajennuspisteet

1. **Todellinen MLIR-vienti** — korvaa merkkijono-IR `GhostKernelLayer.translate()` -metodissa
2. **SPIR-V / ROCm -tausta** — liitä kääntäjän kääntöpolkuun
3. **Mukautetut pariteettilähteet** — yrityksen tarkistussummavarasto Entropy-Shieldille
4. **Aikatauluttajan integraatio** — K8s-laajennus, joka kutsuu `UtahOsmoticRouter`ia

## Versio

Nykyinen: **v0.2.0** (alpha)

[Takaisin indeksiin](index.md) · [CUDA-ohjelmoijille](cuda-programmers.md) · [Siirtymä](migration-guide.md)
