# Migratsioonijuhend — CUDA / PyTorch → Utah-Vid-ia

See juhend aitab meeskondadel Utah-Vid-ia järkjärgult kasutusele võtta ilma tootmise treenimist või järeldust peatamata.

## Migratsiooni põhimõtted

1. **Varjurežiim esmalt** — käivita Utah-Vid-ia paralleelselt olemasolevate töödega; võrdle väljundeid ja latentsust.
2. **Üks kiht korraga** — orkestreerija → osmootiline marsruutimine → ZEO → natiivsed tuumad.
3. **Hoia tagasipööramine** — funktsioonilipp importile; mitte suur ühekorraga ümberkirjutus.

## Faas 0 — Inventuur (1 nädal)

Dokumenteeri:

- [ ] PyTorch vs toor CUDA vs Triton kasutus
- [ ] GPU mudelid ja draiverid igas keskkonnas
- [ ] Mitme GPU topoloogia (NVLink, PCIe)
- [ ] Kriitilised latentsuse SLO-d ja veaeelarved

Paigalda Utah-Vid-ia arendusmasinasse:

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
utahvidia all
pytest -q
```

## Faas 1 — Ghost layer jälgitavus (1–2 nädalat)

**Eesmärk:** IR auditi jälg ilma numbrilisi tulemusi muutmata.

```python
from utahvidia import activate_ghost_layer
import torch

with activate_ghost_layer(verbose=True) as ghost:
    # wrap your existing torch calls
    result = ghost.wrap("matmul", torch.matmul)(a, b)

for record in ghost.history:
    print(record.op_name, record.target_ir)
```

**Väljumiskriteerium:** Kõik kuumad teed logitud; mõõdetav regressioon p99 latentsuses puudub.

## Faas 2 — Osmootiline marsruutimine (2–4 nädalat)

**Eesmärk:** Jaota partiitööd GPU-de vahel surve järgi, mitte kõvakodeeritud seadme ID-de järgi.

Enne:

```python
with torch.cuda.device(0):
    out = model(batch)
```

Pärast:

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
out = router.route_sync(forward_fn, batch)
```

**Väljumiskriteerium:** Parem kasutus mitme GPU sõlmedel; õigsuse kõrvalekalle puudub kuldtestidel.

## Faas 3 — Orkestreerija ühtlustamine (2–4 nädalat)

**Eesmärk:** Üks API ghost + marsruutimise + ZEO konksude jaoks.

```python
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
out = orch.execute_shielded_matmul(a, b)
pipeline_out = orch.run_llm_stress_demo(hidden=4096, layers=your_layer_count)
```

Asenda ad-hoc seadme loogika orkestreerija kutsetega konfiguratsioonilipu taga:

```python
USE_UTAH = os.getenv("UTAHVIDIA", "0") == "1"

if USE_UTAH:
    out = orch.execute_shielded_matmul(a, b)
else:
    out = torch.matmul(a, b)
```

## Faas 4 — Vektorkompilaator / Triton (valikuline, Linux CUDA)

```bash
pip install -e ".[compiler]"
```

```python
from utahvidia.compiler import trigger_compiler
out = trigger_compiler(data_tensor)
```

Kasuta elementide kaupa kohandatud ops-ide jaoks enne täieliku GEMM portimist Tritonisse.

## Faas 5 — Natiivne ZEO tuum (valikuline)

Nõuab NVCC-d. Võrdlesta enne tootmises lubamist:

```bash
utahvidia bench
```

Luba töökoormuse kaupa:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul
out = zeo_prefetched_matmul(a, b, use_native=True)
```

## Faas 6 — Entropy parandamine (uurimus / parti ainult)

**Ära** luba parandamist reaalajas treenimise kaotuste teedel ilma valideerimiseta.

```python
from utahvidia import ZeoShieldEngine
engine = ZeoShieldEngine()
restored = engine.heal(corrupted, reference_clean)
```

## Tagasipööramise kontrollnimekiri

- Sea `UTAHVIDIA=0`
- Eemalda orkestreerija ümbrisimportid
- Hoia ghost logid keelatud (`verbose=False`)

## Valideerimise maatriks

| Test | Läbimise tingimus |
|------|-------------------|
| Numbriline pariteet | `torch.allclose(baseline, utah, rtol=..., atol=...)` |
| Latentsus | p99 kokkulepitud eelarve piires |
| Mitme GPU | Kasutuse σ vähenes |
| Leotustest | 24h partiitöö, null uut OOM klassi |

## Teistest virnadest

| Lähtevirn | Märkused |
|-----------|----------|
| **Puhas CUDA C++** | Ümbrise PyTorch piiril esmalt või seo kohandatud laiendus nagu `zeo_shield_bindings.cpp` |
| **JAX** | Otse ei toetata; ekspordi PyTorchi või kutsu Python orkestreerijat alamprotsessi kaudu |
| **TensorFlow** | Sama — kasuta TFX/PyTorch silda või pordi kuum tee |
| **ROCm PyTorch** | Osmootiline + ghost töötavad; natiivne ZEO CUDA tuum on täna ainult NVIDIA |

## Toetus

Probleemid: [GitHub Issues](https://github.com/utahisnotastate/utahvidia/issues)  
Anneta: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

[Tagasi indeksisse](index.md) · [CUDA programmeerijatele](cuda-programmers.md)
