# Latency Shield — draiverita kaadri taastamine

## Probleem

Mängumootorid ja tootja draiverid **serialiseerivad** kaadrite saatmise. CPU järjekorrad blokeerivad GPU töö → mikro-tõkked ja sisendlatentsus.

## Lahendus

**Utah-Vid-ia Latency Shield** püüab kinni kaadrivoo ja sünteesib vahekaadreid:

- Praegusest kaadrist (RGBA)
- Ajaloo kaadrist
- Pikslipõhistest liikumisvektoritest

Enne kui ekraanipipeline ootab draiveri lõpetamist.

## Arhitektuur

```
Render engine → current/history/motion tensors
        ↓
LatencyShieldIntercept (dedicated CUDA stream)
        ↓
utahvidia_reconstruction_kernel (or PyTorch fallback)
        ↓
Display-ready frame
```

## Tuuma parameetrid

| Parameeter | Vaikimisi | Roll |
|------------|-----------|------|
| `BLOCK_DIM_X` | 32 | Warp laius |
| `BLOCK_DIM_Y` | 8 | Occupancy häälestus |
| `alpha` | 0.65 | Praeguse vs ajaloo segu |
| `SHARED_PADDING` | 1 | Bank conflict vältimine |

## JIT soojusprofiilid

`JitProfiler` vahetab `alpha` ja occupancy sihte, kui simuleeritud tuuma temp ületab 82°C — asendus PTX hot-swap'ile `UtahvidiaJitProfiler` kaudu täielikus Driver API juurutuses.

## API

```python
from utahvidia.latency_shield import LatencyShieldIntercept, reconstruct_frames

shield = LatencyShieldIntercept(1920, 1080)
out = shield.dispatch(current, history, motion, core_temp_c=75.0)
```

## Tootmis märkused

- Alpha v0.3: tensor-taseme intercept, mitte kernel-režiimi display hook
- Natiivne CUDA JIT `torch.utils.cpp_extension.load` kaudu
- Tõelise OS bypass jaoks vaata `microvisor.py` (**ainult simulatsioon**)

[Tagasi mängude dokumentatsiooni](gaming-index.md)

**Teised keeled:** [English](../en/latency-shield.md) · [Eesti](../et/latency-shield.md) · [Русский](../ru/latency-shield.md) · [Suomi](../fi/latency-shield.md)
