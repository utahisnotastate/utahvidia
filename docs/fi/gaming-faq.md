# Pelaamisen UKK

## Yleistä

### Korvaako Utah-Vid-ia GPU:ni?

**Ei.** Se saa GPU:si toimimaan älykkäämmin — parempi kehysten tahdistus, valinnaiset upscale-polut, multi-GPU-jako, VRAM-virtualisointidemot. Fysiikka rajoittaa silti huipputehoa.

### Onko se turvallinen?

Kyllä. Avoin lähdekoodi (MIT), pip-paketissa ei kernel-tilassa rootkittejä. Microvisor on **vain simulaatio**. Patron-avaus on paikallinen konfiguraatiotiedosto — ei vakoiluohjelmistoa.

### Toimiiko se pelini kanssa?

v0.3 on **väliohjelmisto + demot**. Integroi tänään Python/skripteillä. Suora injektio AAA-peleihin on roadmapilla (Driver API / alustakumppanit).

---

## Patron / lahjoitukset

### Mitä saan lahjoittaessani?

[Pro Gaming Profiles](gpu-unlock-patron.md): `patron_max`, `patron_vram`, `patron_legend` — viritetyt esiasetukset latency shieldille, speculative intentille ja osmotic VRAM:lle.

### Minimilahjoitus?

Mikä tahansa summa muistiolla **`GPU-UNLOCK`**. Ehdotus: 5 $ Supporter, 15 $ Enthusiast, 50 $ Legend.

### Onko avaus todella pysyvä?

Kyllä — tallennettu `~/.utahvidia/patron.unlock` tai `UTAHVIDIA_PATRON=1`. Ei tilausta. Kertalahjoitus, ikuisesti koneillasi (kunniajärjestelmä).

### Saanko palautuksen?

PayPalin standardipalautuskäytäntö. Ota yhteyttä GitHub-issuen kautta, jos esiasetukset eivät toimi laitteessasi.

---

## Tekninen

### NVIDIA vs AMD vs Intel?

PyTorch-polku toimii kaikkialla. Natiivit CUDA-kernelit (latency shield, ZEO) vaativat NVIDIA:n + valinnaisen NVCC:n.

### Miksi en näe korkeampaa FPS:ää Cyberpunkissa / Fortnitessa?

Nuo pelit eivät kutsu Utah-Vid-iaa automaattisesti. Aja ensin `utahvidia gaming` ja omat skriptit. Patron-profiilit pätevät, kun **sinä** ohjaat kehykset mootorin kautta.

### Mikä on „perceptual upscale"?

Renderöi matala resoluutio sisäisesti, syntetisoi yksityiskohdat holographic/tensor-polulla — sama idea kuin DLSS/FSR, Utah-Vid-ia-tyylinen demo `UtahRealityEngine.perceptual_upscale_path`:ssa.

---

## Tuki

- GitHub Issues: [utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia/issues)  
- Lahjoita: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  

[Täysi opas](gaming-tutorial.md) · [Pelikeskus](gaming-index.md)

**Muut kielet:** [English](../en/gaming-faq.md) · [Eesti](../et/gaming-faq.md) · [Русский](../ru/gaming-faq.md) · [Suomi](../fi/gaming-faq.md)
