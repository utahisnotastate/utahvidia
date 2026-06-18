# Latency Shield — ajuriton kehyksen rekonstruktio

## Ongelma

Pelimoottorit ja valmistajan ajurit **serialisoivat** kehysten lähetyksen. CPU-jonot estävät GPU-työn → mikronykinät ja syötelatenssi.

## Ratkaisu

**Utah-Vid-ia Latency Shield** sieppaa kehysvirran ja syntetisoi välikehyksiä:

- Nykyisestä kehyksestä (RGBA)
- Historiakehyksestä
- Pikselikohtaisista liikevektoreista

Ennen kuin näyttöputki odottaa ajurin valmistumista.

## Arkkitehtuuri

```
Render engine → current/history/motion tensors
        ↓
LatencyShieldIntercept (dedicated CUDA stream)
        ↓
utahvidia_reconstruction_kernel (or PyTorch fallback)
        ↓
Display-ready frame
```

## Kernel-parametrit

| Parametri | Oletus | Rooli |
|-----------|--------|-------|
| `BLOCK_DIM_X` | 32 | Warp-leveys |
| `BLOCK_DIM_Y` | 8 | Occupancy-säätö |
| `alpha` | 0.65 | Nykyisen vs historian sekoitus |
| `SHARED_PADDING` | 1 | Bank conflict -välttäminen |

## JIT-lämpöprofiilit

`JitProfiler` vaihtaa `alpha` ja occupancy-tavoitteet, kun simuloitu ytimen lämpö ylittää 82°C — PTX hot-swapin sija `UtahvidiaJitProfiler` kautta täydessä Driver API -käyttöönotossa.

## API

```python
from utahvidia.latency_shield import LatencyShieldIntercept, reconstruct_frames

shield = LatencyShieldIntercept(1920, 1080)
out = shield.dispatch(current, history, motion, core_temp_c=75.0)
```

## Tuotantohuomiot

- Alpha v0.3: tensor-tason intercept, ei kernel-tilan display hook
- Natiivi CUDA JIT `torch.utils.cpp_extension.load` kautta
- Todelliseen OS bypass -ratkaisuun katso `microvisor.py` (**vain simulaatio**)

[Takaisin pelidokumentaatioon](gaming-index.md)

**Muut kielet:** [English](../en/latency-shield.md) · [Eesti](../et/latency-shield.md) · [Русский](../ru/latency-shield.md) · [Suomi](../fi/latency-shield.md)
