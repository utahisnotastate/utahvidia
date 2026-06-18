# Учебник для геймеров — игровой unlock без установки

Запустите **полный игровой стек Utah-Vid-ia** без Git, без unlock-файлов и без оплаты.

**Опциональные пожертвования:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## Самый быстрый путь: скачать `.exe`

1. Перейдите на [GitHub Releases](https://github.com/utahisnotastate/utahvidia/releases)
2. Скачайте **`UtahVidia-Gaming.exe`**
3. Дважды щёлкните

Вы увидите:

```
UTAH-VIDIA GAMING UNLOCK
Full stack enabled — no install, no unlock file needed
[1/4] Boot gaming enclave...
[2/4] Latency shield frame reconstruction...
[3/4] Perceptual upscale + speculative intent...
[4/4] Fractal + holographic paths...
GAMING UNLOCK COMPLETE — all profiles active
```

Нажмите Enter для закрытия (при запуске упакованного exe).

Ещё нет Release? Используйте вариант 2 или 3 ниже, или попросите maintainer запустить [Build workflow](https://github.com/utahisnotastate/utahvidia/actions).

---

## Вариант 2 — ZIP + `.bat` (нужен Python, Git не нужен)

1. Скачайте [Source ZIP](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip)
2. Распакуйте куда угодно (например `Desktop\utahvidia-main`)
3. Дважды щёлкните **`launchers\UtahVidia-Gaming.bat`**

Устанавливает из папки и запускает полный unlock.

---

## Вариант 3 — Python одной строкой

Если установлен Python 3.10+:

```bash
pip install git+https://github.com/utahisnotastate/utahvidia.git
utahvidia-gaming
```

---

## Что разблокируется (всё бесплатно)

| Функция | Что делает |
|---------|------------|
| Latency shield | Более плавные кадры через реконструкцию с учётом движения |
| Profile `max` | Лучшая настройка по умолчанию (применяется автоматически) |
| Perceptual upscale | Путь от низкого разрешения к демо высокого |
| Speculative intent | Предварительный рендер по предсказанному движению ввода |
| Osmotic VRAM | Большая арена виртуальной памяти (симуляция) |
| Photonic / fractal / holographic | Полное демо Reality Engine |

Доступные профили: `competitive`, `cinematic`, `vr`, `max`, `vram`, `legend`

---

## Пошагово: настройка GPU (опционально)

После однократного запуска unlock создайте `my_game.py`:

```python
from utahvidia import UtahRealityEngine
from utahvidia.gaming_profiles import apply_gaming_profile
from utahvidia.latency_shield import DisplayHookConfig
import torch

W, H = 1920, 1080
engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=W, height=H))
apply_gaming_profile(engine, "competitive")  # or cinematic, max, legend

device = "cuda" if torch.cuda.is_available() else "cpu"
current = torch.rand(H, W, 4, device=device)
history = torch.rand(H, W, 4, device=device)
motion = torch.randn(H, W, 2, device=device) * 0.3

frame = engine.reconstruct_frame(current, history, motion)
print("OK", frame.shape)
```

---

## Устранение неполадок

| Проблема | Решение |
|----------|---------|
| Нет `.exe` на странице Releases | Используйте `.bat` или `utahvidia-gaming`; maintainer может запустить Actions workflow |
| Python не найден | Установите с [python.org](https://python.org) или используйте `.exe` |
| exe заблокирован Windows | «Подробнее» → «Выполнить в любом случае» (неподписанная OSS-сборка) |
| Большой размер загрузки | exe включает PyTorch (~200MB+) — для меньшей загрузки используйте `.bat` |
| Нет изменения FPS в AAA-играх | Utah-Vid-ia — middleware; интегрируйте через скрипты; прямой game hook в roadmap |

---

## Поддержать проект (опционально)

Бесплатно навсегда. Пожертвования помогают тестированию железа и переводам:

**PayPal:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## Дальнейшее чтение

- [Игровой хаб](gaming-index.md)
- [Игровой FAQ](gaming-faq.md)
- [Руководство по загрузке](../../launchers/README.md)

## Другие языки

[English](../en/gaming-tutorial.md) · [中文](../zh/gaming-tutorial.md) · [Eesti](../et/gaming-tutorial.md) · [Русский](../ru/gaming-tutorial.md) · [Suomi](../fi/gaming-tutorial.md) · [日本語](../ja/gaming-tutorial.md)

[Назад к индексу документации](index.md)
