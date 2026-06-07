# Руководство по миграции — CUDA / PyTorch → Utah-Vid-ia

Это руководство помогает командам внедрять Utah-Vid-ia постепенно, не останавливая продакшен-обучение или инференс.

## Принципы миграции

1. **Сначала тень** — запускайте Utah-Vid-ia параллельно существующим задачам; сравнивайте выходы и латентность.
2. **Один слой за раз** — оркестратор → осмотическая маршрутизация → ZEO → нативные ядра.
3. **Сохраняйте откат** — feature flag на импорт; без big-bang переписки.

## Фаза 0 — Инвентаризация (1 неделя)

Задокументируйте:

- [ ] Использование PyTorch vs чистый CUDA vs Triton
- [ ] Модели GPU и драйверы в каждой среде
- [ ] Топология multi-GPU (NVLink, PCIe)
- [ ] Критичные SLO латентности и error budget

Установите Utah-Vid-ia на dev-машине:

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
utahvidia all
pytest -q
```

## Фаза 1 — Наблюдаемость Ghost layer (1–2 недели)

**Цель:** аудит IR без изменения численных результатов.

```python
from utahvidia import activate_ghost_layer
import torch

with activate_ghost_layer(verbose=True) as ghost:
    # wrap your existing torch calls
    result = ghost.wrap("matmul", torch.matmul)(a, b)

for record in ghost.history:
    print(record.op_name, record.target_ir)
```

**Критерий выхода:** Все hot-path ops залогированы; измеримой регрессии p99 латентности нет.

## Фаза 2 — Осмотическая маршрутизация (2–4 недели)

**Цель:** Распределять batch-задачи по GPU по давлению, а не по жёстко заданным device ID.

До:

```python
with torch.cuda.device(0):
    out = model(batch)
```

После:

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
out = router.route_sync(forward_fn, batch)
```

**Критерий выхода:** Улучшенная утилизация на multi-GPU узлах; нет дрейфа корректности на golden tests.

## Фаза 3 — Унификация оркестратора (2–4 недели)

**Цель:** Единый API для ghost + маршрутизации + ZEO хуков.

```python
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
out = orch.execute_shielded_matmul(a, b)
pipeline_out = orch.run_llm_stress_demo(hidden=4096, layers=your_layer_count)
```

Замените ad-hoc логику устройств вызовами оркестратора за feature flag:

```python
USE_UTAH = os.getenv("UTAHVIDIA", "0") == "1"

if USE_UTAH:
    out = orch.execute_shielded_matmul(a, b)
else:
    out = torch.matmul(a, b)
```

## Фаза 4 — Векторный компилятор / Triton (опционально, Linux CUDA)

```bash
pip install -e ".[compiler]"
```

```python
from utahvidia.compiler import trigger_compiler
out = trigger_compiler(data_tensor)
```

Используйте для поэлементных кастомных ops перед портированием полного GEMM в Triton.

## Фаза 5 — Нативное ZEO-ядро (опционально)

Требует NVCC. Забенчмаркируйте перед включением в продакшен:

```bash
utahvidia bench
```

Включайте по нагрузке:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul
out = zeo_prefetched_matmul(a, b, use_native=True)
```

## Фаза 6 — Entropy healing (только research / batch)

**Не** включайте healing на live training loss paths без валидации.

```python
from utahvidia import ZeoShieldEngine
engine = ZeoShieldEngine()
restored = engine.heal(corrupted, reference_clean)
```

## Чеклист отката

- Установите `UTAHVIDIA=0`
- Удалите импорты обёртки оркестратора
- Держите ghost logs выключенными (`verbose=False`)

## Матрица валидации

| Тест | Условие прохождения |
|------|---------------------|
| Численный паритет | `torch.allclose(baseline, utah, rtol=..., atol=...)` |
| Латентность | p99 в согласованном бюджете |
| Multi-GPU | σ утилизации уменьшилась |
| Soak test | 24ч batch-задача, ноль новых классов OOM |

## Из других стеков

| Исходный стек | Примечания |
|---------------|------------|
| **Чистый CUDA C++** | Оборачивайте на границе PyTorch сначала, или биндите кастомное расширение как `zeo_shield_bindings.cpp` |
| **JAX** | Не поддерживается напрямую; экспортируйте в PyTorch или вызывайте Python-оркестратор через subprocess |
| **TensorFlow** | То же — используйте TFX/PyTorch bridge или портируйте hot path |
| **ROCm PyTorch** | Osmotic + ghost работают; нативное ZEO CUDA-ядро сегодня только для NVIDIA |

## Поддержка

Issues: [GitHub Issues](https://github.com/utahisnotastate/utahvidia/issues)  
Пожертвовать: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

[Назад к индексу](index.md) · [CUDA-программистам](cuda-programmers.md)
