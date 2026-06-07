# 迁移指南 — CUDA / PyTorch → Utah-Vid-ia

本指南帮助团队增量采用 Utah-Vid-ia，而无需停止生产训练或推理。

## 迁移原则

1. **影子先行** — 与现有作业并行运行 Utah-Vid-ia；比较输出与延迟。
2. **逐层推进** — orchestrator → osmotic 路由 → ZEO → 原生 kernel。
3. **保留回滚** — 用 feature flag 控制 import；避免大爆炸式重写。

## 阶段 0 — 盘点（1 周）

记录：

- [ ] PyTorch vs 原生 CUDA vs Triton 使用情况
- [ ] 各环境中的 GPU 型号与驱动
- [ ] 多 GPU 拓扑（NVLink、PCIe）
- [ ] 关键延迟 SLO 与错误预算

在开发机上安装 Utah-Vid-ia：

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
utahvidia all
pytest -q
```

## 阶段 1 — Ghost layer 可观测性（1–2 周）

**目标：** IR 审计轨迹，不改变数值结果。

```python
from utahvidia import activate_ghost_layer
import torch

with activate_ghost_layer(verbose=True) as ghost:
    # wrap your existing torch calls
    result = ghost.wrap("matmul", torch.matmul)(a, b)

for record in ghost.history:
    print(record.op_name, record.target_ir)
```

**退出标准：** 所有热路径 op 已记录；p99 延迟无可测量回归。

## 阶段 2 — Osmotic 路由（2–4 周）

**目标：** 按压力而非硬编码 device ID 在 GPU 间分配批作业。

之前：

```python
with torch.cuda.device(0):
    out = model(batch)
```

之后：

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
out = router.route_sync(forward_fn, batch)
```

**退出标准：** 多 GPU 节点利用率提升；golden 测试无正确性漂移。

## 阶段 3 — Orchestrator 统一（2–4 周）

**目标：** ghost + 路由 + ZEO 钩子的单一 API。

```python
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
out = orch.execute_shielded_matmul(a, b)
pipeline_out = orch.run_llm_stress_demo(hidden=4096, layers=your_layer_count)
```

用 orchestrator 调用替换零散 device 逻辑，放在配置 flag 之后：

```python
USE_UTAH = os.getenv("UTAHVIDIA", "0") == "1"

if USE_UTAH:
    out = orch.execute_shielded_matmul(a, b)
else:
    out = torch.matmul(a, b)
```

## 阶段 4 — 向量编译器 / Triton（可选，Linux CUDA）

```bash
pip install -e ".[compiler]"
```

```python
from utahvidia.compiler import trigger_compiler
out = trigger_compiler(data_tensor)
```

在将完整 GEMM 移植到 Triton 之前，用于逐元素自定义 op。

## 阶段 5 — 原生 ZEO kernel（可选）

需要 NVCC。生产启用前先 benchmark：

```bash
utahvidia bench
```

按工作负载启用：

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul
out = zeo_prefetched_matmul(a, b, use_native=True)
```

## 阶段 6 — 熵修复（仅研究 / 批处理）

未经验证，**不要**在实时训练 loss 路径上启用 healing。

```python
from utahvidia import ZeoShieldEngine
engine = ZeoShieldEngine()
restored = engine.heal(corrupted, reference_clean)
```

## 回滚清单

- 设置 `UTAHVIDIA=0`
- 移除 orchestrator 包装 import
- 关闭 ghost 日志（`verbose=False`）

## 验证矩阵

| 测试 | 通过条件 |
|------|----------|
| 数值 parity | `torch.allclose(baseline, utah, rtol=..., atol=...)` |
| 延迟 | p99 在约定预算内 |
| 多 GPU | 利用率 σ 下降 |
| Soak 测试 | 24h 批作业，无新增 OOM 类型 |

## 来自其他技术栈

| 源技术栈 | 说明 |
|----------|------|
| **纯 CUDA C++** | 先在 PyTorch 边界包装，或像 `zeo_shield_bindings.cpp` 一样绑定自定义扩展 |
| **JAX** | 无直接支持；导出到 PyTorch 或通过 subprocess 调用 Python orchestrator |
| **TensorFlow** | 同上 — 使用 TFX/PyTorch 桥接或移植热路径 |
| **ROCm PyTorch** | Osmotic + ghost 可用；原生 ZEO CUDA kernel 目前仅 NVIDIA |

## 支持

Issue：[GitHub Issues](https://github.com/utahisnotastate/utahvidia/issues)  
捐赠：[utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

[返回索引](index.md) · [CUDA 程序员](cuda-programmers.md)
