# Siirtymäopas — CUDA / PyTorch → Utah-Vid-ia

Tämä opas auttaa tiimejä ottamaan Utah-Vid-ian käyttöön vaiheittain pysäyttämättä tuotannon koulutusta tai päättelyä.

## Siirtymän periaatteet

1. **Varjo ensin** — aja Utah-Vid-ia rinnakkain olemassa olevien ajojen kanssa; vertaa tuloksia ja viivettä.
2. **Yksi kerros kerrallaan** — orkestroija → osmotic-reititys → ZEO → natiivikernelit.
3. **Pidä palautusmahdollisuus** — feature flag importille; ei big bang -uudelleenkirjoitusta.

## Vaihe 0 — Inventaario (1 viikko)

Dokumentoi:

- [ ] PyTorch vs raaka CUDA vs Triton -käyttö
- [ ] GPU-mallit ja ajurit jokaisessa ympäristössä
- [ ] Moni-GPU-topologia (NVLink, PCIe)
- [ ] Kriittiset viive-SLO:t ja virhebudjetit

Asenna Utah-Vid-ia kehityskoneelle:

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
utahvidia all
pytest -q
```

## Vaihe 1 — Ghost layer -havaittavuus (1–2 viikkoa)

**Tavoite:** IR-auditointijälki muuttamatta numeriikkaa.

```python
from utahvidia import activate_ghost_layer
import torch

with activate_ghost_layer(verbose=True) as ghost:
    # wrap your existing torch calls
    result = ghost.wrap("matmul", torch.matmul)(a, b)

for record in ghost.history:
    print(record.op_name, record.target_ir)
```

**Poistumiskriteeri:** Kaikki hot path -op:t kirjattu; ei mitattavaa p99-viiveen heikkenemistä.

## Vaihe 2 — Osmotic-reititys (2–4 viikkoa)

**Tavoite:** Jaa eräajot GPU:ille paineen, ei kovakoodattujen laitetunnusten mukaan.

Ennen:

```python
with torch.cuda.device(0):
    out = model(batch)
```

Jälkeen:

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
out = router.route_sync(forward_fn, batch)
```

**Poistumiskriteeri:** Parantunut hyödyntäminen moni-GPU-solmuissa; ei oikeellisuuspoikkeamaa kultatestissä.

## Vaihe 3 — Orkestroijan yhdistäminen (2–4 viikkoa)

**Tavoite:** Yksi API ghostille + reititykselle + ZEO-koukuille.

```python
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
out = orch.execute_shielded_matmul(a, b)
pipeline_out = orch.run_llm_stress_demo(hidden=4096, layers=your_layer_count)
```

Korvaa ad hoc -laitelogiikka orkestroijakutsuilla konfiguraatiolipun takana:

```python
USE_UTAH = os.getenv("UTAHVIDIA", "0") == "1"

if USE_UTAH:
    out = orch.execute_shielded_matmul(a, b)
else:
    out = torch.matmul(a, b)
```

## Vaihe 4 — Vektorikääntäjä / Triton (valinnainen, Linux CUDA)

```bash
pip install -e ".[compiler]"
```

```python
from utahvidia.compiler import trigger_compiler
out = trigger_compiler(data_tensor)
```

Käytä elementtikohtaisiin mukautettuihin op:eihin ennen koko GEMM:n siirtoa Tritoniin.

## Vaihe 5 — Natiivi ZEO-kernel (valinnainen)

Vaatii NVCC:n. Vertaa ennen tuotantoon ottamista:

```bash
utahvidia bench
```

Ota käyttöön työkuormittain:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul
out = zeo_prefetched_matmul(a, b, use_native=True)
```

## Vaihe 6 — Entropy-paraneminen (tutkimus / erä vain)

**Älä** ota paranemista käyttöön live-koulutuksen häviöpoluilla ilman validointia.

```python
from utahvidia import ZeoShieldEngine
engine = ZeoShieldEngine()
restored = engine.heal(corrupted, reference_clean)
```

## Palautuslista

- Aseta `UTAHVIDIA=0`
- Poista orkestroijakääreen importit
- Pidä ghost-lokit pois päältä (`verbose=False`)

## Validointimatriisi

| Testi | Läpäisyehdot |
|------|----------------|
| Numeerinen pariteetti | `torch.allclose(baseline, utah, rtol=..., atol=...)` |
| Viive | p99 sovitun budjetin sisällä |
| Moni-GPU | Hyödyntämisen σ laski |
| Soak-testi | 24 h eräajo, nolla uutta OOM-luokkaa |

## Muista pinoista

| Lähdepino | Huomiot |
|--------------|-------|
| **Puhdas CUDA C++** | Kääri ensin PyTorch-rajalla tai sido mukautettu laajennus kuten `zeo_shield_bindings.cpp` |
| **JAX** | Ei suoraa tukea; vie PyTorchiin tai kutsu Python-orkestroijaa aliprosessin kautta |
| **TensorFlow** | Sama — käytä TFX/PyTorch-siltaa tai siirrä hot path |
| **ROCm PyTorch** | Osmotic + ghost toimivat; natiivi ZEO CUDA -kernel on tänään vain NVIDIA |

## Tuki

Ongelmat: [GitHub Issues](https://github.com/utahisnotastate/utahvidia/issues)  
Lahjoita: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

[Takaisin indeksiin](index.md) · [CUDA-ohjelmoijille](cuda-programmers.md)
