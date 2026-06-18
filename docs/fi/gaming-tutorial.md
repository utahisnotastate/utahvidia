# Pelaajan opas — nollasta GPU-avaamiseen

Täydellinen walkthrough: asenna Utah-Vid-ia, aja pelipino, vertaa GPU:ta ja valinnaisesti **avaa Pro-profiilit pysyvästi** [Patron-ohjelman](gpu-unlock-patron.md) kautta.

**Aika:** ~30 minuuttia · **Hinta:** 0 € (Pro-avaus valinnainen lahjoituksella)

---

## Mitä saavutat

1. Asennat Utah-Vid-ian Windowsille, Linuxille tai macOS:lle  
2. Ajat **Asymptotic Reality Engine** -pelidemoa  
3. Ymmärrät latency shield + perceptual upscale **omalla** GPU:llasi  
4. Vertailet ennen/jälkeen -tuntumaa  
5. Valinnaisesti **avaat Pro Gaming Profiles -profiilit pysyvästi** PayPal-lahjoituksella  

---

## Edellytykset

| Vaatimus | Huomiot |
|----------|---------|
| Python 3.10+ | `py --version` tai `python3 --version` |
| pip | Paketinasennin |
| Git | Kloonaa GitHubista |
| GPU (valinnainen) | NVIDIA CUDA = paras; AMD/Intel PyTorchin kautta; CPU = demotila |

---

## Vaihe 1 — Kloonaa ja asenna

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

Tarkista:

```bash
utahvidia --help
# or: py -m utahvidia.cli
```

---

## Vaihe 2 — Ensimmäinen pelidemosi

```bash
utahvidia gaming
```

Odotettu tuloste (lyhennetty):

```
UTAH-VIDIA // Universal Compute Bridge v0.3.0
microvisor: [MICROVISOR SIM] ...
Latency shield: (180, 320, 4) in X.XX ms
Perceptual upscale: (360, 640, 3)
Speculative frame: (180, 320, 4)
```

**Mitä tapahtui:**

- **Latency shield** sekoitti nykyisen ja historian kehykset liikevektorien avulla (sujuvampi liike).  
- **Perceptual upscale** kaksinkertaisti resoluution matalaresoluutioisesta pohjasta (AI-tyylinen demo).  
- **Speculative intent** esirenderöi fantomikehyksiä hiiren kaltaisista deltoista.  

---

## Vaihe 3 — Koko pinon kierros

```bash
utahvidia all
```

Ajaa ghost kernel, compiler, osmotic router, photonic sim, ZEO-Shield, orchestrator **ja** pelipinon.

---

## Vaihe 4 — Vertaa GPU:ta

```bash
utahvidia bench
```

Tallenna tuloste — hyödyllinen GitHub-issueissa ja Patron-profiilien vertailussa.

CUDA-järjestelmissä NVCC:n kanssa natiivit kernelit voivat JIT-kääntyä ensimmäisellä ajolla (kertaluonteinen lisäsekuntien kulu).

---

## Vaihe 5 — Python: säädä kehyksiä koneellasi

Luo `my_gaming_test.py`:

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

Aja:

```bash
python my_gaming_test.py
```

---

## Vaihe 6 — Kilpailu- vs elokuvaprofiilit (ilmaiset oletukset)

```python
from utahvidia.patron import apply_gaming_profile, list_profiles

print(list_profiles())  # competitive, cinematic, vr, patron_* if unlocked

engine = UtahRealityEngine()
apply_gaming_profile(engine, "competitive")  # lower alpha = snappier
# apply_gaming_profile(engine, "cinematic")  # smoother interpolation
```

| Profiili | Parhaiten | Latency shield alpha |
|----------|-----------|----------------------|
| `competitive` | e-urheilu, nopea hiiri | 0.75 (terävämpi) |
| `cinematic` | yksinpeli, tarina | 0.55 (sujuvampi) |
| `vr` | VR-lasit | 0.60 + pienempi spekulatiivinen horisontti |

Vain Patron-profiilit (avaamisen jälkeen): `patron_max`, `patron_vram`, `patron_legend`.

---

## Vaihe 7 — Avaa Pro Gaming Profiles

1. Lahjoita PayPalin kautta: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  
2. Muistio: **`GPU-UNLOCK`**  
3. Luo patron-tiedosto tai aseta ympäristömuuttuja — [täydet ohjeet](gpu-unlock-patron.md#activate-your-unlock)  
4. Tarkista:

```bash
utahvidia patron
```

5. Käytä max-profiilia:

```python
from utahvidia import UtahRealityEngine
from utahvidia.patron import apply_gaming_profile, patron_status

print(patron_status())
engine = UtahRealityEngine()
apply_gaming_profile(engine, "patron_max")
```

**Olet avannut Pro-esiasetukset pysyvästi tällä koneella** (tiedosto tai env säilyy uudelleenkäynnistyksissä).

---

## Vaihe 8 — Vianmääritys

| Ongelma | Korjaus |
|---------|---------|
| `python` ei löydy (Windows) | Käytä `py` |
| CUDA ei tunnistu | Asenna [PyTorch + CUDA](https://pytorch.org); CPU-tila toimii silti |
| Natiivin kernelin kääntö epäonnistuu | Käytä PyTorch-polku; aseta API:ssa `use_native=False` |
| Patron ei aktiivinen | Tarkista `~/.utahvidia/patron.unlock` tai `UTAHVIDIA_PATRON=1` |
| FPS ei muutu muissa peleissä | Utah-Vid-ia on väliohjelmisto — integroi ensin oppaan skripteillä; täysi peli-hook on roadmapilla |

---

## Vaihe 9 — Jaa ja tue

- Tähti repolle: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)  
- Kerro ystäville: lahjoita **GPU-UNLOCK** → Pro-profiilit  
- Striimaajat: linkki [gpu-unlock-patron.md](gpu-unlock-patron.md) bioon  

---

## Seuraavaa luettavaa

- [GPU Unlock Patron -ohjelma](gpu-unlock-patron.md)  
- [Pelaamisen UKK](gaming-faq.md)  
- [Latency Shield -syväluotaus](latency-shield.md)  
- [Lapsille — miksi GPU:t merkitsevät](gaming-children.md)  

[Takaisin pelikeskukseen](gaming-index.md)

**Muut kielet:** [English](../en/gaming-tutorial.md) · [Eesti](../et/gaming-tutorial.md) · [Русский](../ru/gaming-tutorial.md) · [Suomi](../fi/gaming-tutorial.md)
