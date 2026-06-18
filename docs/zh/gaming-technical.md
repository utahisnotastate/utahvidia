# 游戏技术栈 — 技术参考

## UtahRealityEngine

扩展 `UtahSiliconOrchestrator` 的统一编排器：

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

## 模块映射

| 扩展 | 模块 | 原生 CUDA |
|-----------|--------|-------------|
| 延迟护盾 | `utahvidia/latency_shield.py` | `native/latency_shield_kernel.cu` |
| 渗透式 VRAM | `utahvidia/vram_osmotic.py` | VMM 桩（生产环境 Driver API） |
| 光子多 GPU | `utahvidia/photonic_multi.py` | PyTorch 多设备 |
| 全息权重 | `utahvidia/holographic.py` | PyTorch 程序化 |
| 分形超图 | `utahvidia/fractal_graph.py` | PyTorch |
| 推测意图 | `utahvidia/speculative_intent.py` | PyTorch |
| Microvisor | `utahvidia/microvisor.py` | **仅模拟** |

## 延迟护盾内核

- 线程块：`32 x 8`（256 线程，对齐 warp）
- 共享内存填充 `[BLOCK_DIM_X + 1]` 缓解 bank 冲突
- 网格步进循环支持任意分辨率
- 主机：专用 `torch.cuda.Stream(priority=-1)`

## 钩子层策略

| 路径 | 优点 | 缺点 |
|------|------|------|
| **PyTorch 流拦截**（默认） | 可移植，pip 安装 | 非真实显示驱动钩子 |
| **CUDA Driver API**（`cuModuleLoad` PTX） | 绕过运行时臃肿 | 需要 PTX 构建与平台集成 |
| **Vulkan/DX12 层** | 引擎原生 | 重新引入 API 调度器 |

推荐 rollout：PyTorch 影子路径 → Driver API beta → 平台合作。

## 基准测试

```bash
utahvidia gaming
utahvidia latency
```

## 其他语言

[English](../en/gaming-technical.md) · [日本語](../ja/gaming-technical.md)

[延迟护盾详解](latency-shield.md) · [架构 Mermaid](../ARCHITECTURE.md)
