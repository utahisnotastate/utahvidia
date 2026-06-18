# Mängija õpetus — paigalduseta mängude avamine

Käivita **täielik Utah-Vid-ia mängude virn** ilma Gitita, avamisfailideta ja maksmata.

**Valikulised annetused:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## Kiireim tee: laadi `.exe`

1. Mine [GitHub Releases](https://github.com/utahisnotastate/utahvidia/releases)
2. Laadi alla **`UtahVidia-Gaming.exe`**
3. Topeltklõps

Näed:

```
UTAH-VIDIA GAMING UNLOCK
Full stack enabled — no install, no unlock file needed
[1/4] Boot gaming enclave...
[2/4] Latency shield frame reconstruction...
[3/4] Perceptual upscale + speculative intent...
[4/4] Fractal + holographic paths...
GAMING UNLOCK COMPLETE — all profiles active
```

Vajuta Enter sulgemiseks (pakitud exe puhul).

Release'i veel pole? Kasuta allpool valikut 2 või 3, või palu hooldajal käivitada [Build workflow](https://github.com/utahisnotastate/utahvidia/actions).

---

## Valik 2 — ZIP + `.bat` (Python vajalik, Git pole vaja)

1. Laadi [Source ZIP](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip)
2. Paki lahti suvalisse kohta (nt `Desktop\utahvidia-main`)
3. Topeltklõpsa **`launchers\UtahVidia-Gaming.bat`**

Paigaldab kaustast ja käivitab täieliku avamise.

---

## Valik 3 — Python üherea käsk

Kui sul on Python 3.10+:

```bash
pip install git+https://github.com/utahisnotastate/utahvidia.git
utahvidia-gaming
```

---

## Mis avatakse (kõik tasuta)

| Funktsioon | Mida teeb |
|------------|-----------|
| Latency shield | Sujuvamad kaadrid liikumisteadliku taastamise kaudu |
| Profile `max` | Parim vaikimisi häälestus (rakendatakse automaatselt) |
| Perceptual upscale | Madala resolutsiooni baasist kõrgema resolutsiooni demoteele |
| Speculative intent | Eel-renderdus ennustatud sisendi liikumise põhjal |
| Osmotic VRAM | Suur virtuaalse mälu ala (simulatsioon) |
| Photonic / fractal / holographic | Täielik Reality Engine demo |

Saadaolevad profiilid: `competitive`, `cinematic`, `vr`, `max`, `vram`, `legend`

---

## Samm-sammult: häälesta GPU (valikuline)

Pärast avamise ühekordset käivitamist loo `my_game.py`:

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

## Tõrkeotsing

| Probleem | Lahendus |
|----------|----------|
| Releases lehel pole `.exe` | Kasuta `.bat` või `utahvidia-gaming`; hooldaja saab käivitada Actions workflow |
| Python ei leitud | Paigalda [python.org](https://python.org) või kasuta `.exe` |
| exe blokeeritud Windowsis | Klõpsa „Rohkem teavet" → „Käivita ikkagi" (allkirjastamata avatud lähtekoodi build) |
| Suur allalaadimine | Exe sisaldab PyTorchi (~200MB+) — väiksemaks kasuta `.bat` teed |
| AAA mängudes FPS ei muutu | Utah-Vid-ia on vahevara — integreeri skriptide kaudu; otsene mängu hook on teekonnal |

---

## Toeta projekti (valikuline)

Igavesti tasuta. Annetused aitavad riistvara testimist ja tõlkeid:

**PayPal:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## Järgmised lugemised

- [Mängude keskus](gaming-index.md)
- [Mängude KKK](gaming-faq.md)
- [Allalaadimisjuhend](../../launchers/README.md)

## Teised keeled

[English](../en/gaming-tutorial.md) · [中文](../zh/gaming-tutorial.md) · [Eesti](../et/gaming-tutorial.md) · [Русский](../ru/gaming-tutorial.md) · [Suomi](../fi/gaming-tutorial.md) · [日本語](../ja/gaming-tutorial.md)

[Tagasi dokumentatsiooni indeksisse](index.md)
