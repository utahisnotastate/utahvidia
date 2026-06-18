# Gamer Tutorial — From Zero to GPU Unlock

Complete walkthrough: install Utah-Vid-ia, run the gaming stack, benchmark your GPU, and optionally **unlock Pro profiles** via the [Patron Program](gpu-unlock-patron.md).

**Time:** ~30 minutes · **Cost:** $0 (Pro unlock optional via donation)

---

## What you will achieve

1. Install Utah-Vid-ia on Windows, Linux, or macOS  
2. Run the **Asymptotic Reality Engine** gaming demo  
3. Understand latency shield + perceptual upscale on **your** GPU  
4. Benchmark before/after feel  
5. Optionally **permanently unlock Pro Gaming Profiles** with a PayPal donation  

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.10+ | `py --version` or `python3 --version` |
| pip | Package installer |
| Git | Clone from GitHub |
| GPU (optional) | NVIDIA CUDA = best; AMD/Intel via PyTorch; CPU = demo mode |

---

## Step 1 — Clone and install

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

Verify:

```bash
utahvidia --help
# or: py -m utahvidia.cli
```

---

## Step 2 — Run your first gaming demo

```bash
utahvidia gaming
```

Expected output (abbreviated):

```
UTAH-VIDIA // Universal Compute Bridge v0.3.0
microvisor: [MICROVISOR SIM] ...
Latency shield: (180, 320, 4) in X.XX ms
Perceptual upscale: (360, 640, 3)
Speculative frame: (180, 320, 4)
```

**What happened:**

- **Latency shield** blended current + history frames using motion vectors (smoother motion feel).  
- **Perceptual upscale** doubled resolution from a low-res baseline (AI-style path demo).  
- **Speculative intent** pre-rendered phantom frames from mouse-like deltas.  

---

## Step 3 — Full stack tour

```bash
utahvidia all
```

Runs ghost kernel, compiler, osmotic router, photonic sim, ZEO-Shield, orchestrator, **and** gaming stack.

---

## Step 4 — Benchmark your GPU

```bash
utahvidia bench
```

Save the output — useful for GitHub issues and comparing Patron profiles.

On CUDA systems with NVCC, native kernels may JIT-compile on first run (extra seconds once).

---

## Step 5 — Python: tune frames on your machine

Create `my_gaming_test.py`:

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

Run:

```bash
python my_gaming_test.py
```

---

## Step 6 — Competitive vs cinematic profiles (free defaults)

```python
from utahvidia.patron import apply_gaming_profile, list_profiles

print(list_profiles())  # competitive, cinematic, vr, patron_* if unlocked

engine = UtahRealityEngine()
apply_gaming_profile(engine, "competitive")  # lower alpha = snappier
# apply_gaming_profile(engine, "cinematic")  # smoother interpolation
```

| Profile | Best for | Latency shield alpha |
|---------|----------|----------------------|
| `competitive` | esports, fast mouse | 0.75 (snappier) |
| `cinematic` | single-player, story | 0.55 (smoother) |
| `vr` | headsets | 0.60 + reduced speculative horizon |

Patron-only profiles (after unlock): `patron_max`, `patron_vram`, `patron_legend`.

---

## Step 7 — Unlock Pro Gaming Profiles

1. Donate via PayPal: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  
2. Memo/note: **`GPU-UNLOCK`**  
3. Create patron file or set env var — [full instructions](gpu-unlock-patron.md#activate-your-unlock)  
4. Verify:

```bash
utahvidia patron
```

5. Apply max profile:

```python
from utahvidia import UtahRealityEngine
from utahvidia.patron import apply_gaming_profile, patron_status

print(patron_status())
engine = UtahRealityEngine()
apply_gaming_profile(engine, "patron_max")
```

**You have permanently unlocked Pro presets on this machine** (file or env persists across reboots).

---

## Step 8 — Troubleshooting

| Problem | Fix |
|---------|-----|
| `python` not found (Windows) | Use `py` instead |
| CUDA not detected | Install [PyTorch + CUDA](https://pytorch.org); CPU mode still works |
| Native kernel compile fails | Use PyTorch path; set `use_native=False` in API |
| Patron not active | Check `~/.utahvidia/patron.unlock` or `UTAHVIDIA_PATRON=1` |
| No FPS change in other games | Utah-Vid-ia is middleware — integrate via tutorial scripts first; full game hook is roadmap |

---

## Step 9 — Share and support

- Star the repo: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)  
- Tell friends: donate **GPU-UNLOCK** → Pro profiles  
- Streamers: link [gpu-unlock-patron.md](gpu-unlock-patron.md) in your bio  

---

## Next reads

- [GPU Unlock Patron Program](gpu-unlock-patron.md)  
- [Gaming FAQ](gaming-faq.md)  
- [Latency Shield deep dive](latency-shield.md)  
- [For kids — why GPUs matter](gaming-children.md)  

[Back to gaming hub](gaming-index.md)
