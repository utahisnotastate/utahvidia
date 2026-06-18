# Gamer Tutorial — Install-Free Gaming Unlock

Run the **full Utah-Vid-ia gaming stack** without Git, without unlock files, without paying.

**Optional donations:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## Fastest path: download the `.exe`

1. Go to [GitHub Releases](https://github.com/utahisnotastate/utahvidia/releases)
2. Download **`UtahVidia-Gaming.exe`**
3. Double-click

You will see:

```
UTAH-VIDIA GAMING UNLOCK
Full stack enabled — no install, no unlock file needed
[1/4] Boot gaming enclave...
[2/4] Latency shield frame reconstruction...
[3/4] Perceptual upscale + speculative intent...
[4/4] Fractal + holographic paths...
GAMING UNLOCK COMPLETE — all profiles active
```

Press Enter to close (when running the packaged exe).

No release yet? Use Option 2 or 3 below, or ask the maintainer to run the [Build workflow](https://github.com/utahisnotastate/utahvidia/actions).

---

## Option 2 — ZIP + `.bat` (Python required, no Git)

1. Download [Source ZIP](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip)
2. Extract anywhere (e.g. `Desktop\utahvidia-main`)
3. Double-click **`launchers\UtahVidia-Gaming.bat`**

Installs from the folder and runs the full unlock.

---

## Option 3 — Python one-liner

If you have Python 3.10+:

```bash
pip install git+https://github.com/utahisnotastate/utahvidia.git
utahvidia-gaming
```

---

## What gets unlocked (everything, free)

| Feature | What it does |
|---------|----------------|
| Latency shield | Smoother frames via motion-aware reconstruction |
| Profile `max` | Best default tuning (applied automatically) |
| Perceptual upscale | Low-res baseline to higher-res demo path |
| Speculative intent | Pre-render from predicted input motion |
| Osmotic VRAM | Large virtual memory arena (simulation) |
| Photonic / fractal / holographic | Full Reality Engine demo |

Profiles available: `competitive`, `cinematic`, `vr`, `max`, `vram`, `legend`

---

## Step-by-step: tune your GPU (optional)

After running the unlock once, create `my_game.py`:

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

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No `.exe` on Releases page | Use `.bat` or `utahvidia-gaming`; maintainer can trigger Actions workflow |
| Python not found | Install from [python.org](https://python.org) or use the `.exe` |
| exe blocked by Windows | Click "More info" → "Run anyway" (unsigned open-source build) |
| Large download | Exe bundles PyTorch (~200MB+) — use `.bat` path for smaller download |
| No FPS change in AAA games | Utah-Vid-ia is middleware — integrate via scripts; direct game hook is roadmap |

---

## Support the project (optional)

Free forever. Donations help hardware testing and translations:

**PayPal:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## Next reads

- [Gaming hub](gaming-index.md)
- [Gaming FAQ](gaming-faq.md)
- [Download guide](../../launchers/README.md)

[Back to documentation index](index.md)
