# Учебник для геймеров — от нуля до GPU unlock

Полное руководство: установите Utah-Vid-ia, запустите игровой стек, проведите бенчмарк GPU и при желании **навсегда разблокируйте Pro-профили** через [программу Patron](gpu-unlock-patron.md).

**Время:** ~30 минут · **Стоимость:** $0 (разблокировка Pro опциональна через пожертвование)

---

## Что вы получите

1. Установите Utah-Vid-ia на Windows, Linux или macOS  
2. Запустите игровое демо **Asymptotic Reality Engine**  
3. Поймёте latency shield + perceptual upscale на **вашем** GPU  
4. Сравните ощущения до/после  
5. При желании **навсегда разблокируете Pro Gaming Profiles** через пожертвование PayPal  

---

## Требования

| Требование | Примечания |
|------------|------------|
| Python 3.10+ | `py --version` или `python3 --version` |
| pip | Установщик пакетов |
| Git | Клонирование с GitHub |
| GPU (опционально) | NVIDIA CUDA = лучший; AMD/Intel через PyTorch; CPU = демо-режим |

---

## Шаг 1 — Клонирование и установка

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
```

Windows PowerShell:

```powershell
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
py -m pip install -e ".[dev]"
```

Проверка:

```bash
utahvidia --help
# or: py -m utahvidia.cli
```

---

## Шаг 2 — Первое игровое демо

```bash
utahvidia gaming
```

Ожидаемый вывод (сокращённо):

```
UTAH-VIDIA // Universal Compute Bridge v0.3.0
microvisor: [MICROVISOR SIM] ...
Latency shield: (180, 320, 4) in X.XX ms
Perceptual upscale: (360, 640, 3)
Speculative frame: (180, 320, 4)
```

**Что произошло:**

- **Latency shield** смешал текущий и исторический кадры с помощью векторов движения (более плавное движение).  
- **Perceptual upscale** удвоил разрешение из низкого базового (демо AI-пути).  
- **Speculative intent** предварительно отрисовал фантомные кадры по дельтам, похожим на движение мыши.  

---

## Шаг 3 — Полный тур по стеку

```bash
utahvidia all
```

Запускает ghost kernel, compiler, osmotic router, photonic sim, ZEO-Shield, orchestrator **и** игровой стек.

---

## Шаг 4 — Бенчмарк GPU

```bash
utahvidia bench
```

Сохраните вывод — полезно для GitHub issues и сравнения Patron-профилей.

На системах с CUDA и NVCC нативные ядра могут JIT-компилироваться при первом запуске (дополнительные секунды один раз).

---

## Шаг 5 — Python: настройка кадров на вашей машине

Создайте `my_gaming_test.py`:

```python
import torch
from utahvidia import UtahRealityEngine
from utahvidia.latency_shield import DisplayHookConfig

# Match your monitor or game resolution
W, H = 1920, 1080
engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=W, height=H))

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")
print(engine.bootstrap_gaming_enclave())

current = torch.rand(H, W, 4, device=device)
history = torch.rand(H, W, 4, device=device)
motion = torch.randn(H, W, 2, device=device) * 0.3

frame = engine.reconstruct_frame(current, history, motion)
upscaled = engine.perceptual_upscale_path(current[..., :3])

print("Frame:", frame.shape, "Upscaled:", upscaled.shape)
```

Запуск:

```bash
python my_gaming_test.py
```

---

## Шаг 6 — Соревновательные vs кинематографические профили (бесплатно)

```python
from utahvidia.patron import apply_gaming_profile, list_profiles

print(list_profiles())  # competitive, cinematic, vr, patron_* if unlocked

engine = UtahRealityEngine()
apply_gaming_profile(engine, "competitive")  # lower alpha = snappier
# apply_gaming_profile(engine, "cinematic")  # smoother interpolation
```

| Профиль | Лучше для | Latency shield alpha |
|---------|-----------|----------------------|
| `competitive` | киберспорт, быстрая мышь | 0.75 (отзывчивее) |
| `cinematic` | одиночная игра, сюжет | 0.55 (плавнее) |
| `vr` | шлемы VR | 0.60 + уменьшенный speculative horizon |

Только для Patron (после разблокировки): `patron_max`, `patron_vram`, `patron_legend`.

---

## Шаг 7 — Разблокировка Pro Gaming Profiles

1. Пожертвуйте через PayPal: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  
2. Примечание/memo: **`GPU-UNLOCK`**  
3. Создайте patron-файл или задайте переменную окружения — [полные инструкции](gpu-unlock-patron.md#activate-your-unlock)  
4. Проверка:

```bash
utahvidia patron
```

5. Примените max-профиль:

```python
from utahvidia import UtahRealityEngine
from utahvidia.patron import apply_gaming_profile, patron_status

print(patron_status())
engine = UtahRealityEngine()
apply_gaming_profile(engine, "patron_max")
```

**Вы навсегда разблокировали Pro-пресеты на этой машине** (файл или env сохраняется после перезагрузки).

---

## Шаг 8 — Устранение неполадок

| Проблема | Решение |
|----------|---------|
| `python` не найден (Windows) | Используйте `py` |
| CUDA не обнаружена | Установите [PyTorch + CUDA](https://pytorch.org); CPU-режим тоже работает |
| Сбой компиляции нативного ядра | Используйте PyTorch-путь; задайте `use_native=False` в API |
| Patron не активен | Проверьте `~/.utahvidia/patron.unlock` или `UTAHVIDIA_PATRON=1` |
| Нет изменения FPS в других играх | Utah-Vid-ia — middleware; сначала интегрируйте через скрипты учебника; полный game hook в roadmap |

---

## Шаг 9 — Поделитесь и поддержите

- Звезда репозиторию: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)  
- Расскажите друзьям: пожертвование **GPU-UNLOCK** → Pro-профили  
- Стримерам: ссылка [gpu-unlock-patron.md](gpu-unlock-patron.md) в описании канала  

---

## Дальнейшее чтение

- [Программа GPU Unlock Patron](gpu-unlock-patron.md)  
- [Игровой FAQ](gaming-faq.md)  
- [Latency Shield — подробно](latency-shield.md)  
- [Для детей — зачем нужны GPU](gaming-children.md)  

[Назад к игровому хабу](gaming-index.md)

**Другие языки:** [English](../en/gaming-tutorial.md) · [Eesti](../et/gaming-tutorial.md) · [Русский](../ru/gaming-tutorial.md) · [Suomi](../fi/gaming-tutorial.md)
