# Utah-Vid-ia — CUDA 程序员指南

您已经习惯用 kernel、stream 和 occupancy 来思考。本指南将 CUDA 概念映射到 Utah-Vid-ia 模块，并展示最小集成路径。

## 心智模型映射

| CUDA 世界 | Utah-Vid-ia 对应 |
|-----------|------------------|
| `nvcc` / PTX | `UtahVectorCompiler` + Triton BRTR |
| CUDA runtime API | PyTorch + 可选 `zeo_shield_kernel.cu` |
| `cudaMemcpyAsync` 预取 | `NeuralStatePrefetcher` 双流 |
| 多 GPU `cudaSetDevice` | `UtahOsmoticRouter.route_sync` |
| ECC / 错误恢复 | `entropy_shield` / `engine.heal()` |
| 自定义 `__global__` kernel | 扩展 `zeo_shield_kernel.cu` 或 Triton kernel |

## 何时用 Utah-Vid-ia vs 原生 CUDA

**适合 Utah-Vid-ia：**

- 技术栈里已有 PyTorch（或 ATen）
- 需要编排与可移植钩子，又不想重写每个 kernel
- 正在原型化多 GPU 流体调度

**继续用原生 CUDA：**

- 需要手工调优 warp 级 kernel，零 Python 开销
- 依赖无 PyTorch 路径的 CUDA 专用库（cuDNN 自定义 op 等）
- 生产环境今天就需要认证工具链

## 快速集成

### 1. 即插即用 orchestrator（PyTorch 张量）

```python
import torch
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
a = torch.randn(1024, 1024, device="cuda")
b = torch.randn(1024, 1024, device="cuda")
c = orch.execute_shielded_matmul(a, b)
```

### 2. 在现有 torch op 上使用 Ghost layer

```python
from utahvidia import activate_ghost_layer, UtahVidIaEngine
import torch

engine = UtahVidIaEngine()
x = torch.randn(4096, 4096, device="cuda")

with activate_ghost_layer() as ghost:
    matmul = ghost.wrap("matmul", torch.matmul)
    y = engine.execute_optimized(matmul, x, x)

print(ghost.history[-1].target_ir)  # utah.mlir.matmul @ device(cuda) -> spirv
```

### 3. 原生 ZEO kernel（CUDA C++）

源文件：

- `zeo_shield_kernel.cu` — `launch_zeo_kernel`、共享内存分块、`entropy_shield`
- `native/zeo_shield_bindings.cpp` — PyTorch 扩展

Python 在首次调用时自动加载：

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul

out = zeo_prefetched_matmul(a, b, use_native=True)
```

要求：`PATH` 中有 NVCC，PyTorch 带 CUDA。

### 4. 自定义 kernel 扩展点

向 `zeo_shield_kernel.cu` 添加 device 函数，经 bindings 暴露，从 `ZeoShieldEngine` 调用。

模式：

```cpp
extern "C" void launch_zeo_kernel(..., cudaStream_t stream);
```

在 bindings 中使用 `at::cuda::getCurrentCUDAStream()`，以遵循 PyTorch stream 语义。

## Stream 与预取

`NeuralStatePrefetcher` 对应**计算 / 预取 stream 重叠**：

```python
from utahvidia.zeo_shield import NeuralStatePrefetcher, PrefetchJob
import torch

prefetcher = NeuralStatePrefetcher()
semantic = torch.randn(768, device="cuda")  # prompt embedding proxy

jobs = [
    PrefetchJob("layer0", torch.matmul, (a, w0), {}),
    PrefetchJob("layer1", torch.matmul, (a, w1), {}),
]
prefetcher.predict_from_embedding(semantic, jobs)
out = prefetcher.execute_current(jobs[0])
```

与手动写法对比：

```cpp
cudaStream_t compute, prefetch;
kernel_compute<<<..., compute>>>(...);
cudaMemcpyAsync(..., prefetch);
```

## Entropy shield vs ECC

CUDA ECC 在**内存控制器层面检测并纠正**。

Utah-Vid-ia Entropy-Shield 在软件中**将数值向参考 parity 格点混合**——适用于优雅降级演示与研究，**不能**替代数据中心 ECC 策略。

```python
from utahvidia import ZeoShieldEngine

engine = ZeoShieldEngine()
clean = kernel_output.clone()
corrupted = clean.clone()
corrupted[0, 0] += 1.0  # simulate flip
healed = engine.heal(corrupted, clean)
```

## 调试

```bash
utahvidia zeo -v          # verbose logging
pytest tests/test_zeo_shield.py -v
```

常见问题：

| 现象 | 处理 |
|------|------|
| 原生扩展编译失败 | 安装 CUDA toolkit，确保 `nvcc` 在 PATH 中 |
| 缺少 Triton | `pip install triton`（Linux）；使用 PyTorch 回退 |
| 比 `torch.matmul` 慢 | ZEO 分块 op 是逐元素演示 kernel，不是 GEMM |

## 下一步

- [迁移指南](migration-guide.md) — 分阶段 CUDA → Utah-Vid-ia
- [技术参考](technical.md) — 完整模块列表

[返回索引](index.md)
