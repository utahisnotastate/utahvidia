# Программа GPU Unlock Patron

**Раскройте полный потенциал GPU — поддержите Utah-Vid-ia и продлите срок службы вашего железа.**

Ядро Utah-Vid-ia **бесплатно и с открытым исходным кодом (MIT)**. **Программа GPU Unlock Patron** даёт геймерам, которые жертвуют, доступ к **Pro Gaming Profiles**: настроенным пресетам, которые выжимают максимум плавности, эффективности VRAM и стабильности кадров из уже имеющегося кремния.

## PayPal (постоянная разблокировка)

**Пожертвование:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

В примечании PayPal укажите: **`GPU-UNLOCK`** и ваш GitHub или email (опционально, для благодарности).

После пожертвования активируйте разблокировку (см. [Шаг 7 учебника](gaming-tutorial.md#step-7-unlock-pro-gaming-profiles)).

---

## Что значит «постоянная разблокировка»

| Бесплатно (всем) | Patron unlock |
|------------------|---------------|
| Полный open-source стек | Всё из бесплатного уровня |
| Демо latency shield | **Pro latency profiles** (competitive / cinematic / VR) |
| Базовый игровой CLI | **Patron banner + статус разблокировки** |
| Поддержка сообщества | Приоритетный тег issue на GitHub (приложите квитанцию PayPal) |
| — | **Агрессивный пресет VRAM osmotic** (большая виртуальная арена) |
| — | **Speculative intent horizon ×2** (плавнее при быстрой мыши) |
| — | **Ранний доступ** к новым игровым ядрам |

**Важно:** Patron unlock — это **конфигурация ПО + пресеты**, а не магия кремния. У GPU остаются физические пределы. Мы помогаем перестать тратить циклы на раздувание драйверов и невидимые детали.

---

## Рекомендуемые уровни (на доверии)

| Уровень | Рекомендуемая сумма | Вы получаете |
|---------|---------------------|--------------|
| **Supporter** | $5+ | Pro-профили + статус patron |
| **Enthusiast** | $15+ | Выше + имя в [PATRONS.md](../../PATRONS.md) (opt-in в примечании PayPal) |
| **Legend** | $50+ | Выше + ранние beta-сборки с тегом `@patron` в релизах |

Любая сумма разблокирует Pro-профили при **`GPU-UNLOCK`** в примечании к пожертвованию.

---

## Активация разблокировки

### Вариант A — Переменная окружения (быстро)

```powershell
# Windows PowerShell (current session)
$env:UTAHVIDIA_PATRON = "1"

# Permanent (user)
[System.Environment]::SetEnvironmentVariable("UTAHVIDIA_PATRON", "1", "User")
```

```bash
# Linux / macOS
export UTAHVIDIA_PATRON=1
echo 'export UTAHVIDIA_PATRON=1' >> ~/.bashrc
```

### Вариант B — Patron-файл (рекомендуется)

После пожертвования создайте:

**Windows:** `%USERPROFILE%\.utahvidia\patron.unlock`  
**Linux/macOS:** `~/.utahvidia/patron.unlock`

```powershell
mkdir $env:USERPROFILE\.utahvidia -Force
"GPU-UNLOCK" | Out-File $env:USERPROFILE\.utahvidia\patron.unlock -Encoding utf8
```

```bash
mkdir -p ~/.utahvidia
echo "GPU-UNLOCK" > ~/.utahvidia/patron.unlock
```

Опционально: добавьте ID транзакции PayPal на второй строке для проверки поддержкой.

### Проверка

```bash
utahvidia patron
```

Должно быть: `Patron unlock: ACTIVE` и доступные Pro-профили.

---

## Для создателей и стримеров

Вы можете сказать аудитории:

> «Пожертвуйте Utah-Vid-ia через PayPal (**utah@utahcreates.com**, memo **GPU-UNLOCK**), чтобы навсегда разблокировать Pro Gaming Profiles, настроенные под ваш GPU — больше ощущения FPS без покупки нового железа.»

Ссылка: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)

Партнёрская программа формально пока не запущена. Используйте ссылку на пожертвование + учебник в описании; opt-in в PATRONS.md для упоминания.

---

## Возвраты и честность

- Пожертвования добровольны и невозвратны по стандартной политике PayPal.
- Если Pro-профили не помогают на вашей системе, [создайте issue](https://github.com/utahisnotastate/utahvidia/issues) с выводом `utahvidia bench` — мы улучшаем пресеты для всех.

[Полный учебник для геймеров](gaming-tutorial.md) · [Общая информация о пожертвованиях](donate.md) · [Назад к игровому хабу](gaming-index.md)

**Другие языки:** [English](../en/gpu-unlock-patron.md) · [Eesti](../et/gpu-unlock-patron.md) · [Русский](../ru/gpu-unlock-patron.md) · [Suomi](../fi/gpu-unlock-patron.md)
