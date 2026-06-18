# Pelaajan opas — asennusvapaa peliavaus

Aja **koko Utah-Vid-ia -pelipino** ilman Gitiä, avaustiedostoja ja maksua.

**Valinnaiset lahjoitukset:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## Nopein reitti: lataa `.exe`

1. Siirry [GitHub Releases](https://github.com/utahisnotastate/utahvidia/releases)
2. Lataa **`UtahVidia-Gaming.exe`**
3. Kaksoisklikkaa

Näet:

```
UTAH-VIDIA GAMING UNLOCK
Full stack enabled — no install, no unlock file needed
[1/4] Boot gaming enclave...
[2/4] Latency shield frame reconstruction...
[3/4] Perceptual upscale + speculative intent...
[4/4] Fractal + holographic paths...
GAMING UNLOCK COMPLETE — all profiles active
```

Paina Enter sulkeaksesi (pakattu exe).

Ei vielä Releaseä? Käytä alla olevaa vaihtoehtoa 2 tai 3, tai pyydä ylläpitäjää ajamaan [Build workflow](https://github.com/utahisnotastate/utahvidia/actions).

---

## Vaihtoehto 2 — ZIP + `.bat` (Python tarvitaan, Git ei)

1. Lataa [Source ZIP](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip)
2. Pura minne tahansa (esim. `Desktop\utahvidia-main`)
3. Kaksoisklikkaa **`launchers\UtahVidia-Gaming.bat`**

Asentaa kansiosta ja ajaa täyden avauksen.

---

## Vaihtoehto 3 — Python-yksirivi

Jos Python 3.10+ on asennettu:

```bash
pip install git+https://github.com/utahisnotastate/utahvidia.git
utahvidia-gaming
```

---

## Mitä avataan (kaikki ilmaiseksi)

| Ominaisuus | Mitä tekee |
|------------|------------|
| Latency shield | Sujuvammat kehykset liiketietoisen rekonstruktion kautta |
| Profile `max` | Paras oletusviritys (käytetään automaattisesti) |
| Perceptual upscale | Matalaresoluutioisesta pohjasta korkeampaan demopolkuun |
| Speculative intent | Esirenderöinti ennustetun syötteen liikkeen perusteella |
| Osmotic VRAM | Suuri virtuaalimuistialue (simulaatio) |
| Photonic / fractal / holographic | Täysi Reality Engine -demo |

Saatavilla olevat profiilit: `competitive`, `cinematic`, `vr`, `max`, `vram`, `legend`

---

## Vaiheittain: säädä GPU (valinnainen)

Kun olet ajanut avauksen kerran, luo `my_game.py`:

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

## Vianmääritys

| Ongelma | Korjaus |
|---------|---------|
| Ei `.exe`:tä Releases-sivulla | Käytä `.bat` tai `utahvidia-gaming`; ylläpitäjä voi käynnistää Actions workflow |
| Pythonia ei löydy | Asenna [python.org](https://python.org) tai käytä `.exe` |
| exe estetty Windowsissa | Klikkaa „Lisätietoja" → „Suorita silti" (allekirjoittamaton avoimen lähdekoodin build) |
| Suuri lataus | exe sisältää PyTorchin (~200MB+) — pienempään lataukseen käytä `.bat`-polkua |
| Ei FPS-muutosta AAA-peleissä | Utah-Vid-ia on väliohjelmisto — integroi skripteillä; suora peli-hook on roadmapilla |

---

## Tue projektia (valinnainen)

Ilmainen ikuisesti. Lahjoitukset auttavat laitetestauksessa ja käännöksissä:

**PayPal:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## Seuraavaa luettavaa

- [Pelikeskus](gaming-index.md)
- [Pelaamisen UKK](gaming-faq.md)
- [Latausopas](../../launchers/README.md)

## Muut kielet

[English](../en/gaming-tutorial.md) · [中文](../zh/gaming-tutorial.md) · [Eesti](../et/gaming-tutorial.md) · [Русский](../ru/gaming-tutorial.md) · [Suomi](../fi/gaming-tutorial.md) · [日本語](../ja/gaming-tutorial.md)

[Takaisin dokumentaatioindeksiin](index.md)
