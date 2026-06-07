# Utah-Vid-ia CUDA-ohjelmoijille

Ajattelet jo kernelien, streamien ja okkuupanssin termein. Tämä opas kartoittaa CUDA-käsitteet Utah-Vid-ia -moduuleihin ja näyttää minimaaliset integraatiopolut.

## Käsitteiden kartta

| CUDA-maailma | Utah-Vid-ia -vastine |
|------------|------------------------|
| `nvcc` / PTX | `UtahVectorCompiler` + Triton BRTR |
| CUDA runtime API | PyTorch + valinnainen `zeo_shield_kernel.cu` |
| `cudaMemcpyAsync` -esihaku | `NeuralStatePrefetcher` -kaksoisstreamit |
| Moni-GPU `cudaSetDevice` | `UtahOsmoticRouter.route_sync` |
| ECC / virheenpalautus | `entropy_shield` / `engine.heal()` |
| Mukautettu `__global__` -kernel | Laajenna `zeo_shield_kernel.cu` tai Triton-kernel |

## Milloin Utah-Vid-ia vs raaka CUDA

**Käytä Utah-Vid-iaa, kun:**

- PyTorch (tai ATen) on jo pinossa
- Haluat orkestroinnin ja siirrettävyyskoukut ilman jokaisen kernelin uudelleenkirjoitusta
- Prototyypität moni-GPU-virtaavaa aikataulutusta

**Pysy raaassa CUDA:ssa, kun:**

- Tarvitset käsin viritettyjä warp-tason kerneleitä ilman Python-ylijäämää
- Riippuvat CUDA-spesifisistä kirjastoista ilman PyTorch-polkuja (cuDNN-mukautetut op:t jne.)
- Tuotanto vaatii sertifioidut työkaluketjut tänään

## Nopea integraatio

### 1. Pudotusorkestroija (PyTorch-tensorit)

```python
import torch
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
a = torch.randn(1024, 1024, device="cuda")
b = torch.randn(1024, 1024, device="cuda")
c = orch.execute_shielded_matmul(a, b)
```

### 2. Ghost layer olemassa oleville torch-op:ille

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

### 3. Natiivi ZEO-kernel (CUDA C++)

Lähteet:

- `zeo_shield_kernel.cu` — `launch_zeo_kernel`, jaettu muistilaatta, `entropy_shield`
- `native/zeo_shield_bindings.cpp` — PyTorch-laajennus

Python lataa automaattisesti ensimmäisellä kutsulla:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul

out = zeo_prefetched_matmul(a, b, use_native=True)
```

Vaatimukset: NVCC `PATH`:ssa, PyTorch CUDA:lla.

### 4. Mukautetun kernelin laajennuspiste

Lisää laitefunktioita `zeo_shield_kernel.cu`:hun, julkaise sidonnusten kautta, kutsu `ZeoShieldEngine`:stä.

Kuvio:

```cpp
extern "C" void launch_zeo_kernel(..., cudaStream_t stream);
```

Käytä sidonnusten `at::cuda::getCurrentCUDAStream()` kunnioittaaksesi PyTorchin stream-semantiikkaa.

## Streamit ja esihaku

`NeuralStatePrefetcher` heijastaa **laskenta- / esihakustreamin päällekkäisyyttä**:

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

Vertaa manuaaliseen:

```cpp
cudaStream_t compute, prefetch;
kernel_compute<<<..., compute>>>(...);
cudaMemcpyAsync(..., prefetch);
```

## Entropy shield vs ECC

CUDA ECC **havaitsee ja korjaa** muistinhallintatasolla.

Utah-Vid-ia Entropy-Shield **sekoittaa arvoja kohti viitepariteettihilaa** ohjelmistossa — hyödyllinen arvokkaan heikentymisen demoihin ja tutkimukseen, **ei** korvike datakeskuksen ECC-politiikalle.

```python
from utahvidia import ZeoShieldEngine

engine = ZeoShieldEngine()
clean = kernel_output.clone()
corrupted = clean.clone()
corrupted[0, 0] += 1.0  # simulate flip
healed = engine.heal(corrupted, clean)
```

## Vianetsintä

```bash
utahvidia zeo -v          # verbose logging
pytest tests/test_zeo_shield.py -v
```

Yleisiä ongelmia:

| Oire | Korjaus |
|---------|-----|
| Natiivin laajennuksen kääntö epäonnistuu | Asenna CUDA-työkalupaketti, varmista `nvcc` PATH:ssa |
| Triton puuttuu | `pip install triton` (Linux); käytä PyTorch-varavaihtoehtoa |
| Hitaampi kuin `torch.matmul` | ZEO-laattaop on elementtikohtainen demokernel, ei GEMM |

## Seuraavat askeleet

- [Siirtymäopas](migration-guide.md) — vaiheittainen CUDA → Utah-Vid-ia
- [Tekninen viite](technical.md) — täydellinen moduulilista

[Takaisin indeksiin](index.md)
