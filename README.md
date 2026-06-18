# Utah-Vid-ia

**Universal Compute Bridge** — hardware-agnostic GPU middleware that abstracts vendor lock-in through kernel ghosting, binary real-time rewriting, osmotic multi-GPU routing, ZEO-Shield pre-fetching, and photonic interconnect simulation.

> Repository: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)

## Documentation

**[docs/README.md](docs/README.md)** — language picker

### Gamers

| Guide | Link |
|-------|------|
| **Tutorial (start here)** | [docs/en/gaming-tutorial.md](docs/en/gaming-tutorial.md) |
| **GPU Unlock Patron** | [docs/en/gpu-unlock-patron.md](docs/en/gpu-unlock-patron.md) — donate → Pro profiles forever |
| Gaming hub | [docs/en/gaming-index.md](docs/en/gaming-index.md) |

```bash
utahvidia gaming    # demo
utahvidia patron    # check unlock / donate link
```

**Unlock:** PayPal [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com) · memo **`GPU-UNLOCK`**

### All languages

| English | 中文 | Eesti | Русский | Suomi | 日本語 |
|---------|------|-------|---------|-------|--------|
| [en/](docs/en/) | [zh/](docs/zh/) | [et/](docs/et/) | [ru/](docs/ru/) | [fi/](docs/fi/) | [ja/](docs/ja/) |

## Architecture

```
Ghost Kernel  →  Vector Compiler  →  Osmotic Router  →  ZEO-Shield  →  Silicon
   core.py         compiler.py         osmotic.py       zeo_shield.py   .cu kernel
                                                          orchestrator.py
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for Mermaid diagrams of the ZEO-Shield flow.

| Module | Role |
|--------|------|
| `utahvidia_core.py` | JIT kernel ghosting — intercepts ops, records MLIR-shaped IR |
| `utahvidia_compiler.py` | Triton BRTR vector compiler with PyTorch fallback |
| `utah_osmotic_router.py` | Multi-GPU load-balanced "fluid silicon" router |
| `utah_zeo_shield.py` | Pre-Sight prefetch + Entropy lattice shield |
| `zeo_shield_kernel.cu` | Native CUDA prefetch tile kernel + manifold correction |
| `utah_photonic_bridge.py` | Host sim; ESP32 firmware in `embedded/` |

## Install

```bash
py -m pip install -e ".[dev]"
```

Optional Triton (CUDA vector compiler, Linux):

```bash
py -m pip install -e ".[compiler]"
```

Native ZEO CUDA extension JIT-compiles via PyTorch on first use when CUDA + NVCC are available.

## Quick start

```bash
# All subsystem demos (ghost, compiler, osmotic, photonic, zeo, orchestrator)
utahvidia

# ZEO-Shield demo
utahvidia zeo

# Unified Silicon-Transparency orchestrator
utahvidia orchestrator

# Asymptotic Reality Engine (gaming stack)
utahvidia gaming

# Latency shield frame reconstruction
utahvidia latency

# Benchmark vs torch.matmul
utahvidia bench
# or
utahvidia-bench --sizes 128 256 512
```

### Python API

```python
from utahvidia import UtahSiliconOrchestrator, ZeoShieldEngine
import torch

# Full stack: ghost + osmotic + zeo shield
orch = UtahSiliconOrchestrator()
A, B = torch.randn(512, 512), torch.randn(512, 512)
out = orch.execute_shielded_matmul(A, B)

# Pre-sight pipeline (LLM-layer stress simulation)
layers = orch.run_llm_stress_demo(hidden=256, layers=8)

# Direct ZEO access
engine = ZeoShieldEngine()
result = engine.matmul_shielded(A, B)
```

## Embedded photonic node

Flash `embedded/utah_photonic_bridge.py` to an ESP32/M5Stack with MicroPython. Connect IR LED (TX pin 26) and phototransistor (RX pin 32) on the Grove bus.

## Professional pitch surface

The `UtahSiliconOrchestrator` is the drop-in **Silicon-Transparency API**:

- **Predictive Manifold Pre-fetching** via `NeuralStatePrefetcher`
- **Autonomic Entropy-Shielding** via `entropy_shield_tensor` + `zeo_shield_kernel.cu`
- **Cluster fluidity** via `UtahOsmoticRouter`

## Status

Alpha prototype (v0.3.0). Includes **Asymptotic Reality Engine** for gaming: latency shield frame reconstruction, osmotic VRAM simulation, photonic multi-GPU, holographic weights, fractal hyper-graph, and speculative intent. Microvisor is simulation-only.

## License

MIT
