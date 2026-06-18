# Mängija õpetus — nullist GPU avamiseni

Täielik juhend: paigalda Utah-Vid-ia, käivita mängude virn, võrdle oma GPU-d ja valikuliselt **ava Pro profiilid jäädavalt** [Patron Programmi](gpu-unlock-patron.md) kaudu.

**Aeg:** ~30 minutit · **Maksumus:** 0 € (Pro avamine valikuline annetuse kaudu)

---

## Mida sa saavutad

1. Paigaldad Utah-Vid-ia Windowsile, Linuxile või macOS-ile  
2. Käivitad **Asymptotic Reality Engine** mängude demo  
3. Mõistad latency shield + perceptual upscale **oma** GPU-l  
4. Võrdled enne/pärast tunnet  
5. Valikuliselt **avaad Pro Gaming Profiles jäädavalt** PayPal annetusega  

---

## Eeltingimused

| Nõue | Märkused |
|------|----------|
| Python 3.10+ | `py --version` või `python3 --version` |
| pip | Paketihaldur |
| Git | Klooni GitHubist |
| GPU (valikuline) | NVIDIA CUDA = parim; AMD/Intel PyTorchi kaudu; CPU = demo režiim |

---

## Samm 1 — Klooni ja paigalda

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

Kontrolli:

```bash
utahvidia --help
# või: py -m utahvidia.cli
```

---

## Samm 2 — Käivita esimene mängude demo

```bash
utahvidia gaming
```

Oodatav väljund (lühendatud):

```
UTAH-VIDIA // Universal Compute Bridge v0.3.0
microvisor: [MICROVISOR SIM] ...
Latency shield: (180, 320, 4) in X.XX ms
Perceptual upscale: (360, 640, 3)
Speculative frame: (180, 320, 4)
```

**Mis juhtus:**

- **Latency shield** segas praeguse + ajaloo kaadreid liikumisvektorite abil (sujuvam liikumistunne).  
- **Perceptual upscale** kahekordistas eraldusvõime madala resolutsiooni baasist (AI-stiilis demo).  
- **Speculative intent** eel-renderdas fantoomkaadreid hiire-sarnaste deltade põhjal.  

---

## Samm 3 — Täielik virna tuur

```bash
utahvidia all
```

Käivitab ghost kernel, compiler, osmotic router, photonic sim, ZEO-Shield, orchestrator **ja** mängude virna.

---

## Samm 4 — Võrdle oma GPU-d

```bash
utahvidia bench
```

Salvesta väljund — kasulik GitHub issue'de ja Patron profiilide võrdlemise jaoks.

CUDA süsteemidel NVCC-ga võivad natiivsed tuumad esimesel käivitusel JIT-kompileeruda (ühekordne lisasekundite kulu).

---

## Samm 5 — Python: häälesta kaadreid oma masinal

Loo `my_gaming_test.py`:

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

Käivita:

```bash
python my_gaming_test.py
```

---

## Samm 6 — Võistlus- vs kinoprofiilid (tasuta vaikimisi)

```python
from utahvidia.patron import apply_gaming_profile, list_profiles

print(list_profiles())  # competitive, cinematic, vr, patron_* if unlocked

engine = UtahRealityEngine()
apply_gaming_profile(engine, "competitive")  # lower alpha = snappier
# apply_gaming_profile(engine, "cinematic")  # smoother interpolation
```

| Profiil | Sobib | Latency shield alpha |
|---------|-------|----------------------|
| `competitive` | e-spord, kiire hiir | 0.75 (teravam) |
| `cinematic` | ühe mängija, lugu | 0.55 (sujuvam) |
| `vr` | peakomplektid | 0.60 + vähendatud spekulatiivne horisont |

Ainult Patron profiilid (pärast avamist): `patron_max`, `patron_vram`, `patron_legend`.

---

## Samm 7 — Ava Pro Gaming Profiles

1. Anneta PayPali kaudu: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  
2. Märkus/memo: **`GPU-UNLOCK`**  
3. Loo patron fail või sea keskkonnamuutuja — [täielikud juhised](gpu-unlock-patron.md#activate-your-unlock)  
4. Kontrolli:

```bash
utahvidia patron
```

5. Rakenda max profiil:

```python
from utahvidia import UtahRealityEngine
from utahvidia.patron import apply_gaming_profile, patron_status

print(patron_status())
engine = UtahRealityEngine()
apply_gaming_profile(engine, "patron_max")
```

**Oled selles masinas Pro eelseaded jäädavalt avanud** (fail või env püsib taaskäivituste üle).

---

## Samm 8 — Tõrkeotsing

| Probleem | Lahendus |
|----------|----------|
| `python` ei leitud (Windows) | Kasuta `py` |
| CUDA ei tuvastatud | Paigalda [PyTorch + CUDA](https://pytorch.org); CPU režiim töötab ikka |
| Natiivse tuuma kompileerimine ebaõnnestub | Kasuta PyTorch teed; sea API-s `use_native=False` |
| Patron pole aktiivne | Kontrolli `~/.utahvidia/patron.unlock` või `UTAHVIDIA_PATRON=1` |
| FPS ei muutu teistes mängudes | Utah-Vid-ia on vahevara — integreeri esmalt õpetuse skriptide kaudu; täielik mängu hook on teekonnal |

---

## Samm 9 — Jaga ja toeta

- Tähe repo: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)  
- Räägi sõpradele: anneta **GPU-UNLOCK** → Pro profiilid  
- Striimijad: lisa link [gpu-unlock-patron.md](gpu-unlock-patron.md) oma bio-sse  

---

## Järgmised lugemised

- [GPU Unlock Patron Programm](gpu-unlock-patron.md)  
- [Mängude KKK](gaming-faq.md)  
- [Latency Shield süvauuring](latency-shield.md)  
- [Lastele — miks GPU-d loevad](gaming-children.md)  

[Tagasi mängude keskusesse](gaming-index.md)

**Teised keeled:** [English](../en/gaming-tutorial.md) · [Eesti](../et/gaming-tutorial.md) · [Русский](../ru/gaming-tutorial.md) · [Suomi](../fi/gaming-tutorial.md)
