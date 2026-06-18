# Gaming Stack — Technical Reference

## UtahRealityEngine

Unified orchestrator extending `UtahSiliconOrchestrator`:

```python
from utahvidia import UtahRealityEngine
import torch

engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=1920, height=1080))
print(engine.bootstrap_gaming_enclave())

h, w = 1080, 1920
current = torch.rand(h, w, 4, device=engine.device)
history = torch.rand(h, w, 4, device=current.device)
motion = torch.zeros(h, w, 2, device=current.device)

frame = engine.reconstruct_frame(current, history, motion)
upscaled = engine.perceptual_upscale_path(current[..., :3])
phantom = engine.speculative_render_cycle(current, mouse_delta=(2.0, -1.0))
```

## Module map

| Extension | Module | Native CUDA |
|-----------|--------|-------------|
| Latency Shield | `utahvidia/latency_shield.py` | `native/latency_shield_kernel.cu` |
| Osmotic VRAM | `utahvidia/vram_osmotic.py` | VMM stub (Driver API in prod) |
| Photonic Multi-GPU | `utahvidia/photonic_multi.py` | PyTorch multi-device |
| Holographic weights | `utahvidia/holographic.py` | PyTorch procedural |
| Fractal Hyper-Graph | `utahvidia/fractal_graph.py` | PyTorch |
| Speculative intent | `utahvidia/speculative_intent.py` | PyTorch |
| Microvisor | `utahvidia/microvisor.py` | **Simulation only** |

## Latency Shield kernel

- Block: `32 x 8` (256 threads, warp-aligned)
- Shared memory padding `[BLOCK_DIM_X + 1]` for bank conflict mitigation
- Grid-stride loops for arbitrary resolution
- Host: dedicated `torch.cuda.Stream(priority=-1)`

## Hook layer strategy

| Path | Pros | Cons |
|------|------|------|
| **PyTorch stream intercept** (default) | Portable, pip install | Not true display driver hook |
| **CUDA Driver API** (`cuModuleLoad` PTX) | Bypass runtime bloat | Needs PTX build + platform integration |
| **Vulkan/DX12 layer** | Engine-native | Reintroduces API scheduler |

Recommended rollout: PyTorch shadow path → Driver API beta → platform partnership.

## Benchmarks

```bash
utahvidia gaming
utahvidia latency
```

[Latency Shield detail](latency-shield.md) · [Architecture Mermaid](../ARCHITECTURE.md)
