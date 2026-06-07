# Utah-Vid-ia CUDA programmeerijatele

Sa mõtled juba tuumades, voogudes ja hõivatuses. See juhend kaardistab CUDA mõisted Utah-Vid-ia moodulitele ja näitab minimaalseid integratsiooniteid.

## Mõttemudeli kaart

| CUDA maailm | Utah-Vid-ia ekvivalent |
|-------------|------------------------|
| `nvcc` / PTX | `UtahVectorCompiler` + Triton BRTR |
| CUDA runtime API | PyTorch + valikuline `zeo_shield_kernel.cu` |
| `cudaMemcpyAsync` prefetch | `NeuralStatePrefetcher` dual streams |
| Mitme GPU `cudaSetDevice` | `UtahOsmoticRouter.route_sync` |
| ECC / vea taastamine | `entropy_shield` / `engine.heal()` |
| Kohandatud `__global__` tuum | Laienda `zeo_shield_kernel.cu` või Triton tuuma |

## Millal kasutada Utah-Vid-ia vs toor CUDA

**Kasuta Utah-Vid-ia, kui:**

- PyTorch (või ATen) on juba virnas
- Soovid orkestreerimist + portatiivsuse konksusid ilma iga tuuma ümber kirjutamata
- Prototypeerid mitme GPU vedelat ajastamist

**Jää toor CUDA juurde, kui:**

- Vajad käsitsi häälestatud warp-taseme tuumasid null Python ülekoormusega
- Sõltud CUDA-spetsiifilistest teekidest ilma PyTorch teeta (cuDNN kohandatud ops jne)
- Tootmine nõuab sertifitseeritud tööriistaahelaid täna

## Kiire integratsioon

### 1. Otse asendatav orkestreerija (PyTorch tensorid)

```python
import torch
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
a = torch.randn(1024, 1024, device="cuda")
b = torch.randn(1024, 1024, device="cuda")
c = orch.execute_shielded_matmul(a, b)
```

### 2. Ghost layer olemasolevatel torch ops-il

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

### 3. Natiivne ZEO tuum (CUDA C++)

Allikad:

- `zeo_shield_kernel.cu` — `launch_zeo_kernel`, shared-memory tile, `entropy_shield`
- `native/zeo_shield_bindings.cpp` — PyTorch laiendus

Python laadib automaatselt esimesel kutsel:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul

out = zeo_prefetched_matmul(a, b, use_native=True)
```

Nõuded: NVCC `PATH`-is, PyTorch CUDA-ga.

### 4. Kohandatud tuuma laienduspunkt

Lisa seadme funktsioonid `zeo_shield_kernel.cu`-sse, avalda bindings kaudu, kutsu `ZeoShieldEngine`-ist.

Muster:

```cpp
extern "C" void launch_zeo_kernel(..., cudaStream_t stream);
```

Kasuta `at::cuda::getCurrentCUDAStream()` bindings-is, et austada PyTorch voo semantikat.

## Vood ja prefetch

`NeuralStatePrefetcher` peegeldab **arvutus / prefetch voo kattumist**:

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

Võrdle käsitsi:

```cpp
cudaStream_t compute, prefetch;
kernel_compute<<<..., compute>>>(...);
cudaMemcpyAsync(..., prefetch);
```

## Entropy shield vs ECC

CUDA ECC **tuvastab ja parandab** mälukontrolleri tasemel.

Utah-Vid-ia Entropy-Shield **segmab väärtusi viitepariteedi võre poole** tarkvaras — kasulik graatsilise degradeerumise demode ja uurimistöö jaoks, **mitte** andmekeskuse ECC poliitika asendajana.

```python
from utahvidia import ZeoShieldEngine

engine = ZeoShieldEngine()
clean = kernel_output.clone()
corrupted = clean.clone()
corrupted[0, 0] += 1.0  # simulate flip
healed = engine.heal(corrupted, clean)
```

## Silumine

```bash
utahvidia zeo -v          # verbose logging
pytest tests/test_zeo_shield.py -v
```

Levinud probleemid:

| Sümptom | Lahendus |
|---------|----------|
| Natiivne laiendus ei kompileeru | Paigalda CUDA tööriistakomplekt, veendu et `nvcc` on PATH-is |
| Triton puudub | `pip install triton` (Linux); kasuta PyTorch fallback |
| Aeglasem kui `torch.matmul` | ZEO plaadi op on elementide kaupa demo tuum, mitte GEMM |

## Järgmised sammud

- [Migratsioonijuhend](migration-guide.md) — faasiline CUDA → Utah-Vid-ia
- [Tehniline viide](technical.md) — täielik moodulite nimekiri

[Tagasi indeksisse](index.md)
