# Игровой стек — техническая справка

## UtahRealityEngine

Единый оркестратор, расширяющий `UtahSiliconOrchestrator`:

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

## Карта модулей

| Расширение | Модуль | Native CUDA |
|------------|--------|-------------|
| Latency Shield | `utahvidia/latency_shield.py` | `native/latency_shield_kernel.cu` |
| Osmotic VRAM | `utahvidia/vram_osmotic.py` | VMM stub (Driver API в prod) |
| Photonic Multi-GPU | `utahvidia/photonic_multi.py` | PyTorch multi-device |
| Holographic weights | `utahvidia/holographic.py` | PyTorch procedural |
| Fractal Hyper-Graph | `utahvidia/fractal_graph.py` | PyTorch |
| Speculative intent | `utahvidia/speculative_intent.py` | PyTorch |
| Microvisor | `utahvidia/microvisor.py` | **Только симуляция** |

## Ядро Latency Shield

- Block: `32 x 8` (256 threads, warp-aligned)
- Shared memory padding `[BLOCK_DIM_X + 1]` для mitigation bank conflict
- Grid-stride loops для произвольного разрешения
- Host: dedicated `torch.cuda.Stream(priority=-1)`

## Стратегия hook-слоя

| Путь | Плюсы | Минусы |
|------|-------|--------|
| **PyTorch stream intercept** (default) | Portable, pip install | Не настоящий display driver hook |
| **CUDA Driver API** (`cuModuleLoad` PTX) | Обход runtime bloat | Нужен PTX build + интеграция платформы |
| **Vulkan/DX12 layer** | Engine-native | Возвращает API scheduler |

Рекомендуемый rollout: PyTorch shadow path → Driver API beta → platform partnership.

## Бенчмарки

```bash
utahvidia gaming
utahvidia latency
```

[Latency Shield detail](latency-shield.md) · [Architecture Mermaid](../ARCHITECTURE.md)

**Другие языки:** [English](../en/gaming-technical.md) · [Eesti](../et/gaming-technical.md) · [Русский](../ru/gaming-technical.md) · [Suomi](../fi/gaming-technical.md)
