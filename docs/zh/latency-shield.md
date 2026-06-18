# 延迟护盾 — 无驱动帧重建

## 问题

游戏引擎与厂商驱动 **串行化** 帧派发。CPU 队列阻塞 GPU 工作 → 微卡顿与输入延迟。

## 解决方案

**Utah-Vid-ia 延迟护盾** 拦截帧流，从以下来源合成中间帧：

- 当前帧（RGBA）
- 历史帧
- 逐像素运动向量

在显示管线等待驱动完成之前。

## 架构

```
Render engine → current/history/motion tensors
        ↓
LatencyShieldIntercept (dedicated CUDA stream)
        ↓
utahvidia_reconstruction_kernel (or PyTorch fallback)
        ↓
Display-ready frame
```

## 内核参数

| 参数 | 默认值 | 作用 |
|-------|---------|------|
| `BLOCK_DIM_X` | 32 | Warp 宽度 |
| `BLOCK_DIM_Y` | 8 | 占用率调优 |
| `alpha` | 0.65 | 当前帧与历史帧混合 |
| `SHARED_PADDING` | 1 | 避免 bank 冲突 |

## JIT 温控配置

`JitProfiler` 在模拟核心温度超过 82°C 时切换 `alpha` 与占用率目标 —— 完整 Driver API 部署中通过 `UtahvidiaJitProfiler` 进行 PTX 热替换的占位实现。

## API

```python
from utahvidia.latency_shield import LatencyShieldIntercept, reconstruct_frames

shield = LatencyShieldIntercept(1920, 1080)
out = shield.dispatch(current, history, motion, core_temp_c=75.0)
```

## 生产说明

- Alpha v0.3：张量级拦截，非内核模式显示钩子
- 原生 CUDA JIT 通过 `torch.utils.cpp_extension.load`
- 真正的 OS 绕过见 `microvisor.py`（**仅模拟**）

## 其他语言

[English](../en/latency-shield.md) · [日本語](../ja/latency-shield.md)

[返回游戏文档](gaming-index.md)
