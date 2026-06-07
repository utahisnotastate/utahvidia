# Utah-Vid-ia for CUDA Programmers

You already think in kernels, streams, and occupancy. This guide maps CUDA concepts to Utah-Vid-ia modules and shows minimal integration paths.

## Mental model map

| CUDA world | Utah-Vid-ia equivalent |
|------------|------------------------|
| `nvcc` / PTX | `UtahVectorCompiler` + Triton BRTR |
| CUDA runtime API | PyTorch + optional `zeo_shield_kernel.cu` |
| `cudaMemcpyAsync` prefetch | `NeuralStatePrefetcher` dual streams |
| Multi-GPU `cudaSetDevice` | `UtahOsmoticRouter.route_sync` |
| ECC / error recovery | `entropy_shield` / `engine.heal()` |
| Custom `__global__` kernel | Extend `zeo_shield_kernel.cu` or Triton kernel |

## When to use Utah-Vid-ia vs raw CUDA

**Use Utah-Vid-ia when:**

- PyTorch (or ATen) is already in the stack
- You want orchestration + portability hooks without rewriting every kernel
- You are prototyping multi-GPU fluid scheduling

**Stay on raw CUDA when:**

- You need hand-tuned warp-level kernels with zero Python overhead
- You depend on CUDA-specific libraries with no PyTorch path (cuDNN custom ops, etc.)
- Production requires certified toolchains today

## Quick integration

### 1. Drop-in orchestrator (PyTorch tensors)

```python
import torch
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
a = torch.randn(1024, 1024, device="cuda")
b = torch.randn(1024, 1024, device="cuda")
c = orch.execute_shielded_matmul(a, b)
```

### 2. Ghost layer on existing torch ops

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

### 3. Native ZEO kernel (CUDA C++)

Sources:

- `zeo_shield_kernel.cu` — `launch_zeo_kernel`, shared-memory tile, `entropy_shield`
- `native/zeo_shield_bindings.cpp` — PyTorch extension

Python auto-loads on first call:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul

out = zeo_prefetched_matmul(a, b, use_native=True)
```

Requirements: NVCC on `PATH`, PyTorch with CUDA.

### 4. Custom kernel extension point

Add device functions to `zeo_shield_kernel.cu`, expose via bindings, call from `ZeoShieldEngine`.

Pattern:

```cpp
extern "C" void launch_zeo_kernel(..., cudaStream_t stream);
```

Use `at::cuda::getCurrentCUDAStream()` in bindings to respect PyTorch stream semantics.

## Streams and prefetch

`NeuralStatePrefetcher` mirrors **compute / prefetch stream overlap**:

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

Compare to manual:

```cpp
cudaStream_t compute, prefetch;
kernel_compute<<<..., compute>>>(...);
cudaMemcpyAsync(..., prefetch);
```

## Entropy shield vs ECC

CUDA ECC **detects and corrects** at memory-controller level.

Utah-Vid-ia Entropy-Shield **blends values toward a reference parity lattice** in software — useful for graceful degradation demos and research, **not** a substitute for datacenter ECC policy.

```python
from utahvidia import ZeoShieldEngine

engine = ZeoShieldEngine()
clean = kernel_output.clone()
corrupted = clean.clone()
corrupted[0, 0] += 1.0  # simulate flip
healed = engine.heal(corrupted, clean)
```

## Debugging

```bash
utahvidia zeo -v          # verbose logging
pytest tests/test_zeo_shield.py -v
```

Common issues:

| Symptom | Fix |
|---------|-----|
| Native extension fails to compile | Install CUDA toolkit, ensure `nvcc` in PATH |
| Triton missing | `pip install triton` (Linux); use PyTorch fallback |
| Slower than `torch.matmul` | ZEO tile op is element-wise demo kernel, not GEMM |

## Next steps

- [Migration guide](migration-guide.md) — phased CUDA → Utah-Vid-ia
- [Technical reference](technical.md) — full module list

[Back to index](index.md)
