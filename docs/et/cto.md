# Utah-Vid-ia — juhend CTO-dele

## Juhtkonna kokkuvõte

Utah-Vid-ia on **alfa staadiumis arvutuslik vahevara**, mis vähendab sõltuvust ühe tarnija GPU tarkvaravirnadest. See lahendab klastri ebaefektiivsust, portatiivsuse riski ja töökindluse lünki, mis ilmnevad **pärast** riistvara ostmist.

Strateegiline väärtus pole „asenda NVIDIA homme.” See on **valikuvõimalus**: segatud laevastikud, läbirääkimiste hoob ja tee riistvaratransparentse tehisintellekti infrastruktuuri poole.

## Äriprobleemide kaardistus

| CTO mure | Utah-Vid-ia vastus | Küpsus |
|----------|-------------------|--------|
| CUDA lukustuse maks | Ghost kernel + portatiivsed IR konksud | Alfa — metaandmed täna, backendid pistikprogrammitavad |
| H100 klastri alakasutus | Osmootiline vedel marsruutimine | Alfa — demo tasemel, vajab sinu töökoormuse profiilimist |
| Draiveri viivitus uuel sillamisel | BRTR vektorkompilaator (Triton) | Alfa — CUDA-esmalt |
| Vaikne VRAM korruptsioon / korduskatsed | Entropy-Shield parandamine | Alfa — manifoldi korrektsioon, mitte andmekeskuse ECC |
| Tarnija kontsentratsiooni risk | Mitme tarnija abstraktsiooni narratiiv | Teekaart — valideeri oma sillamisel |

## Kogumaksumuse (TCO) raamistik

**Ilma vahevärata:** ümberkirjutamise kulu tarnija vahetamisel, dubleeritud inseneritöö ajastajate jaoks, tühikäik heterogeensetes riiulites, intsidentide aeg läbipaistmatute draiverivigade tõttu.

**Vaheväraga (sihtolek):** üks orkestreerimise API (`UtahSiliconOrchestrator`), jagatud võrdlustestid tarnijate vahel, järkjärguline migratsioon PyTorch teedelt, mida juba käitad.

**Praegune reaalsus:** v0.2.0 on **usutav prototüüp** tehniliseks due diligence'iks — mitte otse asendus nvcc-le kogu tootmise CUDA jaoks.

## Riskiregister (aus)

| Risk | Leevendus |
|------|-----------|
| Alfa kvaliteet | Piloot mitte-kriitilistel partiitöödel esmalt |
| Jõudluse varieeruvus | Nõua `utahvidia bench` oma laevastikul enne ostutellimust |
| Õigus / IP | MIT litsents; vaata patendimaastikku koos nõustajaga |
| Tarnija reaktsioon | Kohtle läbirääkimiste varana, mitte vaenuliku käivitamisena |
| Toe mudel | Sisemine eestvedaja + kogukond/GitHub probleemid täna |

## Soovitatav piloot (90 päeva)

**Faas 1 — Baasjoon (2 nädalat)**  
Võrdlesta olemasolevad PyTorch/CUDA tööd. Salvesta $/järeldus ja GPU kasutus.

**Faas 2 — Varjurežiim (4 nädalat)**  
Käivita Utah-Vid-ia orkestreerija duplikaatliikluses. Võrdle latentsust p50/p99 ja veamäärasid.

**Faas 3 — Osaline marsruut (4 nädalat)**  
Marsruudi 10–20% partiijäreldustest osmootilise + ZEO teede kaudu.

**Faas 4 — Otsus**  
Laienda, hargne sisemiselt, partner või arhiveeri — mõõdetud säästude, mitte slaidide põhjal.

## Vestlus GPU tarnijatega

Raamista Utah-Vid-ia kui **Silicon-Transparency vahevara**:

> „Parandame kasutust ja töökindlust *teie* riistvaral ilma, et nõuaksime draiverite avatud lähtekoodi. Saame integreeruda omandamise, OEM paketi või litsentseeritud backend-pesa kaudu.”

See on sama hoiak, mis paneb suuri tarnijaid kaasa töötama: lahendad **nende ettevõtte skaleerimise valu**, mitte ainult ei ründa marginaali.

## Ehita vs osta vs rahasta

| Valik | Millal |
|-------|--------|
| **Rahasta / anneta** | Väike meeskond, soov mõjutada teekaarti |
| **Piloot sisemiselt** | ML-platvormi meeskond ≥ 2 inseneri |
| **Omandamine** | Tarnija või konkurent, kes otsib portatiivsuse IP-d |

Anneta: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

## Artefaktid sinu juhatuse slaidide jaoks

1. Reaalajas demo: `utahvidia orchestrator`
2. Võrdlustesti väljund: `utahvidia bench`
3. Arhitektuur: [../ARCHITECTURE.md](../ARCHITECTURE.md)
4. Migratsiooniplaan: [migration-guide.md](migration-guide.md)

[Tagasi indeksisse](index.md) · [Mitte-tehniline ülevaade](non-technical.md)
