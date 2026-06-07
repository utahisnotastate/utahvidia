# Utah-Vid-ia — техническая справка

## Обзор стека

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

Полные диаграммы: [../ARCHITECTURE.md](../ARCHITECTURE.md)

## Модули

| Модуль | Файл | Ответственность |
|--------|------|-----------------|
| Core | `utahvidia/core.py` | `GhostKernelLayer`, `UtahVidIaEngine`, `activate_ghost_layer()` |
| Compiler | `utahvidia/compiler.py` | `UtahVectorCompiler`, Triton JIT, CPU fallback |
| Osmotic | `utahvidia/osmotic.py` | `UtahOsmoticRouter`, async + sync routing |
| ZEO | `utahvidia/zeo_shield.py` | Prefetch streams, entropy heal, native loader |
| Orchestrator | `utahvidia/orchestrator.py` | `UtahSiliconOrchestrator` |
| Native | `zeo_shield_kernel.cu` | Tile prefetch + `entropy_shield` device fn |

## Требования

- Python ≥ 3.10
- PyTorch ≥ 2.0
- Опционально: Triton (Linux CUDA), NVCC (native ZEO JIT)

## Установка

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
pip install -e ".[compiler]"   # Linux + Triton when available
```

## API

### Оркестратор (рекомендуется)

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

### Осмотическая маршрутизация

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
result = router.route_sync(torch.matmul, a, b)
```

## Нативное CUDA-расширение

Загружается лениво через `torch.utils.cpp_extension.load`, когда:

- CUDA доступна
- NVCC в `PATH`
- Источники: `zeo_shield_kernel.cu`, `native/zeo_shield_bindings.cpp`

Принудительный Python-путь: `zeo_prefetched_matmul(A, B, use_native=False)`

## Бенчмарки

```bash
utahvidia bench
utahvidia-bench --sizes 128 256 512 1024 --iters 20
```

Примечание: ядро ZEO tile — поэлементное `A * B` с shield-метаданными; сравнивайте паттерны латентности, а не FLOPs GEMM.

## Тестирование

```bash
pytest -q
```

## Точки расширения

1. **Настоящий экспорт MLIR** — заменить строковый IR в `GhostKernelLayer.translate()`
2. **Бэкенд SPIR-V / ROCm** — подключить к пути компиляции
3. **Кастомные источники паритета** — корпоративное хранилище контрольных сумм для Entropy-Shield
4. **Интеграция планировщика** — K8s device plugin, вызывающий `UtahOsmoticRouter`

## Версия

Текущая: **v0.2.0** (альфа)

[Назад к индексу](index.md) · [CUDA-программистам](cuda-programmers.md) · [Миграция](migration-guide.md)
