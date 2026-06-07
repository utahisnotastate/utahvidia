# ZEO-Shield Architecture

Visual reference for the Utah-Vid-ia Batch 4 stack: **Neural-State Pre-fetching** and **Entropy-Shield**.

## System overview

```mermaid
flowchart TB
    subgraph Client["Application / LLM Runtime"]
        SV[Semantic Vector]
        OPS[Tensor Op Graph]
    end

    subgraph UtahVidia["Utah-Vid-ia Stack"]
        CORE[Ghost Kernel Layer]
        COMP[Vector Compiler BRTR]
        OTR[Osmotic Tensor Router]
        ZEO[ZEO-Shield Engine]
    end

    subgraph ZEOInternal["ZEO-Shield Internals"]
        PRE[NeuralStatePrefetcher]
        ENT[Entropy Lattice Shield]
        NAT[zeo_shield_kernel.cu]
    end

    subgraph Silicon["Hardware"]
        GPU[(GPU VRAM)]
    end

    SV --> PRE
    OPS --> CORE
    CORE --> COMP
    COMP --> OTR
    OTR --> ZEO
    PRE --> ZEO
    ZEO --> ENT
    ENT --> NAT
    NAT --> GPU
    ENT --> GPU
```

## Pre-Sight execution flow

Predictive prefetch uses dual CUDA streams: compute runs the current op while prefetch stages the next.

```mermaid
sequenceDiagram
    participant App
    participant Prefetcher as NeuralStatePrefetcher
    participant SCompute as stream_compute
    participant SPrefetch as stream_prefetch
    participant GPU

    App->>Prefetcher: predict_from_embedding(semantic_vector, ops)
    Prefetcher->>Prefetcher: queue depth from stress norm

    loop Each pipeline stage
        App->>Prefetcher: execute_current(job)
        par Prefetch next
            Prefetcher->>SPrefetch: run next op
            SPrefetch->>GPU: async prefetch
        and Compute current
            Prefetcher->>SCompute: run current op
            SCompute->>GPU: async compute
        end
        Prefetcher->>Prefetcher: synchronize streams
        App->>App: entropy_shield_tensor(output)
    end
```

## Entropy-Shield manifold correction

Instead of hard ECC abort, divergent values blend toward local parity.

```mermaid
flowchart LR
    A[Tensor value] --> D{abs val - parity > tol?}
    P[Parity lattice] --> D
    D -->|no| R[Return value]
    D -->|yes| M["Manifold correction: (val + parity) / 2"]
    M --> R
```

## CUDA kernel tile flow

`zeo_shield_kernel.cu` stages a 32×32 tile of `A` in shared memory, multiplies against `B`, then applies `entropy_shield`.

```mermaid
flowchart TB
    H[Host: launch_zeo_kernel] --> G[Grid of 32x32 blocks]
    G --> SM[Shared memory sA 32x32]
    SM --> LD[Load tile from global A]
    LD --> SYNC[__syncthreads]
    SYNC --> MUL[val = sA * B]
    MUL --> ES[entropy_shield val parity]
    ES --> ST[Store to C]
```

## Integration map

| Layer | Module | Role |
|-------|--------|------|
| Ghost translation | `utahvidia/core.py` | IR intercept, vendor abstraction |
| BRTR compiler | `utahvidia/compiler.py` | Triton JIT / PyTorch fallback |
| Fluid routing | `utahvidia/osmotic.py` | Multi-GPU load balance |
| Pre-Sight | `utahvidia/zeo_shield.py` | `NeuralStatePrefetcher` |
| Entropy lattice | `utahvidia/zeo_shield.py` | `entropy_shield_tensor` |
| Native kernel | `zeo_shield_kernel.cu` | CUDA prefetch + shield |

## Running benchmarks

```bash
py -m benchmarks.benchmark_zeo_shield --sizes 128 256 512 --iters 20
```

Native CUDA extension JIT-compiles on first use when `torch.cuda.is_available()` and NVCC is on `PATH`.
