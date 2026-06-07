# Utah-Vid-ia — 技术参考

## 栈概览

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

完整架构图：[../ARCHITECTURE.md](../ARCHITECTURE.md)

## 模块

| 模块 | 文件 | 职责 |
|------|------|------|
| Core | `utahvidia/core.py` | `GhostKernelLayer`、`UtahVidIaEngine`、`activate_ghost_layer()` |
| Compiler | `utahvidia/compiler.py` | `UtahVectorCompiler`、Triton JIT、CPU 回退 |
| Osmotic | `utahvidia/osmotic.py` | `UtahOsmoticRouter`、异步与同步路由 |
| ZEO | `utahvidia/zeo_shield.py` | 预取流、熵修复、原生加载器 |
| Orchestrator | `utahvidia/orchestrator.py` | `UtahSiliconOrchestrator` |
| Native | `zeo_shield_kernel.cu` | 分块预取 + `entropy_shield` 设备函数 |

## 环境要求

- Python ≥ 3.10
- PyTorch ≥ 2.0
- 可选：Triton（Linux CUDA）、NVCC（原生 ZEO JIT）

## 安装

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
pip install -e ".[compiler]"   # Linux + Triton when available
```

## API 接口

### Orchestrator（推荐）

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

## 原生 CUDA 扩展

在以下条件满足时，通过 `torch.utils.cpp_extension.load` 懒加载：

- CUDA 可用
- `PATH` 中有 NVCC
- 源文件：`zeo_shield_kernel.cu`、`native/zeo_shield_bindings.cpp`

强制走 Python 路径：`zeo_prefetched_matmul(A, B, use_native=False)`

## 基准测试

```bash
utahvidia bench
utahvidia-bench --sizes 128 256 512 1024 --iters 20
```

说明：ZEO 分块内核是逐元素 `A * B` 并附带 shield 元数据；请比较延迟模式，而非 GEMM FLOPs。

## 测试

```bash
pytest -q
```

## 扩展点

1. **真实 MLIR 导出** — 在 `GhostKernelLayer.translate()` 中替换字符串 IR
2. **SPIR-V / ROCm 后端** — 接入编译器编译路径
3. **自定义 parity 源** — 企业级 Entropy-Shield 校验和存储
4. **调度器集成** — K8s device plugin 调用 `UtahOsmoticRouter`

## 版本

当前：**v0.2.0**（alpha）

[返回索引](index.md) · [CUDA 程序员](cuda-programmers.md) · [迁移指南](migration-guide.md)
