# Mängude virn — tehniline viide

## UtahRealityEngine

Ühtne orkestraator, laiendades `UtahSiliconOrchestrator`-it:

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

## Moodulite kaart

| Laiendus | Moodul | Natiivne CUDA |
|----------|--------|---------------|
| Latency Shield | `utahvidia/latency_shield.py` | `native/latency_shield_kernel.cu` |
| Osmotic VRAM | `utahvidia/vram_osmotic.py` | VMM stub (Driver API tootmises) |
| Photonic Multi-GPU | `utahvidia/photonic_multi.py` | PyTorch multi-device |
| Holographic weights | `utahvidia/holographic.py` | PyTorch procedural |
| Fractal Hyper-Graph | `utahvidia/fractal_graph.py` | PyTorch |
| Speculative intent | `utahvidia/speculative_intent.py` | PyTorch |
| Microvisor | `utahvidia/microvisor.py` | **Ainult simulatsioon** |

## Latency Shield tuum

- Plokk: `32 x 8` (256 lõime, warp-aligned)
- Jagatud mälu padding `[BLOCK_DIM_X + 1]` bank conflict leevendamiseks
- Grid-stride loops suvalise resolutsiooni jaoks
- Host: pühendatud `torch.cuda.Stream(priority=-1)`

## Hook kihi strateegia

| Tee | Plussid | Miinused |
|-----|---------|----------|
| **PyTorch stream intercept** (vaikimisi) | Portable, pip install | Mitte tõeline display driver hook |
| **CUDA Driver API** (`cuModuleLoad` PTX) | Mööda runtime paisumist | Vajab PTX build + platvormi integratsiooni |
| **Vulkan/DX12 layer** | Engine-native | Taas toob API scheduleri |

Soovitatud rollout: PyTorch shadow path → Driver API beta → platvormi partnerlus.

## Võrdlustestid

```bash
utahvidia gaming
utahvidia latency
```

[Latency Shield detail](latency-shield.md) · [Arhitektuur Mermaid](../ARCHITECTURE.md)

**Teised keeled:** [English](../en/gaming-technical.md) · [Eesti](../et/gaming-technical.md) · [Русский](../ru/gaming-technical.md) · [Suomi](../fi/gaming-technical.md)
