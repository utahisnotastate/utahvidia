# Latency Shield — Driverless Frame Reconstruction

## Problem

Game engines and vendor drivers **serialize** frame dispatch. CPU queues block GPU work → micro-stutter and input latency.

## Solution

**Utah-Vid-ia Latency Shield** intercepts the frame stream and synthesizes intermediate frames from:

- Current frame (RGBA)
- History frame
- Per-pixel motion vectors

Before the display pipeline waits on driver completion.

## Architecture

```
Render engine → current/history/motion tensors
        ↓
LatencyShieldIntercept (dedicated CUDA stream)
        ↓
utahvidia_reconstruction_kernel (or PyTorch fallback)
        ↓
Display-ready frame
```

## Kernel parameters

| Param | Default | Role |
|-------|---------|------|
| `BLOCK_DIM_X` | 32 | Warp width |
| `BLOCK_DIM_Y` | 8 | Occupancy tuning |
| `alpha` | 0.65 | Current vs history blend |
| `SHARED_PADDING` | 1 | Bank conflict avoidance |

## JIT thermal profiles

`JitProfiler` switches `alpha` and occupancy targets when simulated core temp exceeds 82°C — stand-in for PTX hot-swap via `UtahvidiaJitProfiler` in full Driver API deployment.

## API

```python
from utahvidia.latency_shield import LatencyShieldIntercept, reconstruct_frames

shield = LatencyShieldIntercept(1920, 1080)
out = shield.dispatch(current, history, motion, core_temp_c=75.0)
```

## Production notes

- Alpha v0.3: tensor-level intercept, not kernel-mode display hook
- Native CUDA JIT via `torch.utils.cpp_extension.load`
- For true OS bypass see `microvisor.py` (**simulation only**)

[Back to gaming docs](gaming-index.md)
