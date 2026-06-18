# Игровой FAQ

## Общее

### Заменит ли Utah-Vid-ia мой GPU?

**Нет.** Он заставляет ваш GPU работать умнее — лучший frame pacing, опциональные upscale-пути, multi-GPU split, демо виртуализации VRAM. Физика по-прежнему ограничивает пиковую производительность.

### Это безопасно?

Да. Open source (MIT), в pip-пакете нет kernel-mode rootkit'ов. Microvisor — **только симуляция**. Patron unlock — локальный конфиг-файл, без шпионского ПО.

### Работает ли с моей игрой?

v0.3 — **middleware + демо**. Интеграция через Python/скрипты сегодня. Прямая инъекция в AAA-игры в roadmap (Driver API / партнёры платформ).

---

## Patron / пожертвования

### Что я получу за пожертвование?

[Pro Gaming Profiles](gpu-unlock-patron.md): `patron_max`, `patron_vram`, `patron_legend` — настроенные пресеты для latency shield, speculative intent и osmotic VRAM.

### Минимальное пожертвование?

Любая сумма с memo **`GPU-UNLOCK`**. Рекомендуется: $5 Supporter, $15 Enthusiast, $50 Legend.

### Разблокировка действительно постоянная?

Да — хранится в `~/.utahvidia/patron.unlock` или `UTAHVIDIA_PATRON=1`. Без подписки. Разовое пожертвование, навсегда на ваших ПК (на доверии).

### Можно ли вернуть деньги?

Действует стандартная политика возвратов PayPal. Обратитесь через GitHub issue, если пресеты не работают на вашем железе.

---

## Техническое

### NVIDIA vs AMD vs Intel?

PyTorch-путь работает везде. Нативные CUDA-ядра (latency shield, ZEO) требуют NVIDIA + опциональный NVCC.

### Почему я не вижу больший FPS в Cyberpunk / Fortnite?

Эти игры не вызывают Utah-Vid-ia автоматически. Сначала запустите `utahvidia gaming` и свои скрипты. Patron-профили применяются, когда **вы** направляете кадры через движок.

### Что такое «perceptual upscale»?

Рендер низкого разрешения внутри, синтез деталей через holographic/tensor path — та же идея, что DLSS/FSR, демо в стиле Utah-Vid-ia в `UtahRealityEngine.perceptual_upscale_path`.

---

## Поддержка

- GitHub Issues: [utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia/issues)  
- Пожертвование: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  

[Полный учебник](gaming-tutorial.md) · [Игровой хаб](gaming-index.md)

**Другие языки:** [English](../en/gaming-faq.md) · [Eesti](../et/gaming-faq.md) · [Русский](../ru/gaming-faq.md) · [Suomi](../fi/gaming-faq.md)
