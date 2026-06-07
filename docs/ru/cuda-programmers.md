# Utah-Vid-ia для CUDA-программистов

Вы уже мыслите ядрами, потоками и occupancy. Это руководство сопоставляет концепции CUDA с модулями Utah-Vid-ia и показывает минимальные пути интеграции.

## Карта ментальной модели

| Мир CUDA | Эквивалент Utah-Vid-ia |
|----------|------------------------|
| `nvcc` / PTX | `UtahVectorCompiler` + Triton BRTR |
| CUDA runtime API | PyTorch + опционально `zeo_shield_kernel.cu` |
| `cudaMemcpyAsync` prefetch | `NeuralStatePrefetcher` dual streams |
| Multi-GPU `cudaSetDevice` | `UtahOsmoticRouter.route_sync` |
| ECC / восстановление после ошибок | `entropy_shield` / `engine.heal()` |
| Кастомное `__global__` ядро | Расширить `zeo_shield_kernel.cu` или Triton kernel |

## Когда использовать Utah-Vid-ia vs чистый CUDA

**Используйте Utah-Vid-ia, когда:**

- PyTorch (или ATen) уже в стеке
- Нужны оркестрация + хуки переносимости без переписки каждого ядра
- Прототипируете жидкое планирование на нескольких GPU

**Оставайтесь на чистом CUDA, когда:**

- Нужны вручную настроенные warp-level ядра с нулевым Python overhead
- Зависите от CUDA-специфичных библиотек без PyTorch-пути (cuDNN custom ops и т.д.)
- Продакшен требует сертифицированные toolchain'ы сегодня

## Быстрая интеграция

### 1. Drop-in оркестратор (тензоры PyTorch)

```python
import torch
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
a = torch.randn(1024, 1024, device="cuda")
b = torch.randn(1024, 1024, device="cuda")
c = orch.execute_shielded_matmul(a, b)
```

### 2. Ghost layer на существующих torch ops

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

### 3. Нативное ZEO-ядро (CUDA C++)

Источники:

- `zeo_shield_kernel.cu` — `launch_zeo_kernel`, shared-memory tile, `entropy_shield`
- `native/zeo_shield_bindings.cpp` — расширение PyTorch

Python автозагружает при первом вызове:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul

out = zeo_prefetched_matmul(a, b, use_native=True)
```

Требования: NVCC в `PATH`, PyTorch с CUDA.

### 4. Точка расширения кастомного ядра

Добавьте device-функции в `zeo_shield_kernel.cu`, экспортируйте через bindings, вызывайте из `ZeoShieldEngine`.

Паттерн:

```cpp
extern "C" void launch_zeo_kernel(..., cudaStream_t stream);
```

Используйте `at::cuda::getCurrentCUDAStream()` в bindings для соблюдения семантики потоков PyTorch.

## Потоки и prefetch

`NeuralStatePrefetcher` отражает **перекрытие compute / prefetch потоков**:

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

Сравните с ручным:

```cpp
cudaStream_t compute, prefetch;
kernel_compute<<<..., compute>>>(...);
cudaMemcpyAsync(..., prefetch);
```

## Entropy shield vs ECC

CUDA ECC **обнаруживает и исправляет** на уровне контроллера памяти.

Utah-Vid-ia Entropy-Shield **смешивает значения к эталонной решётке паритета** в софте — полезно для демо graceful degradation и исследований, **не** замена политике датацентрового ECC.

```python
from utahvidia import ZeoShieldEngine

engine = ZeoShieldEngine()
clean = kernel_output.clone()
corrupted = clean.clone()
corrupted[0, 0] += 1.0  # simulate flip
healed = engine.heal(corrupted, clean)
```

## Отладка

```bash
utahvidia zeo -v          # verbose logging
pytest tests/test_zeo_shield.py -v
```

Типичные проблемы:

| Симптом | Решение |
|---------|---------|
| Нативное расширение не компилируется | Установите CUDA toolkit, убедитесь что `nvcc` в PATH |
| Triton отсутствует | `pip install triton` (Linux); используйте PyTorch fallback |
| Медленнее `torch.matmul` | ZEO tile op — поэлементное демо-ядро, не GEMM |

## Следующие шаги

- [Руководство по миграции](migration-guide.md) — поэтапный CUDA → Utah-Vid-ia
- [Техническая справка](technical.md) — полный список модулей

[Назад к индексу](index.md)
