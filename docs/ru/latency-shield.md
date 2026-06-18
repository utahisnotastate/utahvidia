# Latency Shield — реконструкция кадров без драйвера

## Проблема

Игровые движки и драйверы вендоров **сериализуют** отправку кадров. Очереди CPU блокируют работу GPU → микро-стutter и input latency.

## Решение

**Utah-Vid-ia Latency Shield** перехватывает поток кадров и синтезирует промежуточные кадры из:

- Текущего кадра (RGBA)
- Кадра истории
- Пиксельных векторов движения

До того, как display pipeline дождётся завершения драйвера.

## Архитектура

```
Render engine → current/history/motion tensors
        ↓
LatencyShieldIntercept (dedicated CUDA stream)
        ↓
utahvidia_reconstruction_kernel (or PyTorch fallback)
        ↓
Display-ready frame
```

## Параметры ядра

| Параметр | По умолчанию | Роль |
|----------|--------------|------|
| `BLOCK_DIM_X` | 32 | Ширина warp |
| `BLOCK_DIM_Y` | 8 | Настройка occupancy |
| `alpha` | 0.65 | Смешивание current vs history |
| `SHARED_PADDING` | 1 | Избежание bank conflict |

## JIT thermal profiles

`JitProfiler` переключает `alpha` и цели occupancy, когда симулированная температура ядра превышает 82°C — замена PTX hot-swap через `UtahvidiaJitProfiler` в полном развёртывании Driver API.

## API

```python
from utahvidia.latency_shield import LatencyShieldIntercept, reconstruct_frames

shield = LatencyShieldIntercept(1920, 1080)
out = shield.dispatch(current, history, motion, core_temp_c=75.0)
```

## Production notes

- Alpha v0.3: intercept на уровне tensor, не kernel-mode display hook
- Native CUDA JIT через `torch.utils.cpp_extension.load`
- Для настоящего OS bypass см. `microvisor.py` (**только симуляция**)

[Назад к игровой документации](gaming-index.md)

**Другие языки:** [English](../en/latency-shield.md) · [Eesti](../et/latency-shield.md) · [Русский](../ru/latency-shield.md) · [Suomi](../fi/latency-shield.md)
