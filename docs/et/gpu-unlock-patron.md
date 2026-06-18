# GPU Unlock Patron Programm

**Ava oma GPU täispotentsiaal — toeta Utah-Vid-ia ja hoia riistvara kauem asjakohasena.**

Utah-Vid-ia tuum on **tasuta ja avatud lähtekoodiga (MIT)**. **GPU Unlock Patron Programm** võimaldab mängijatel, kes annetavad, juurdepääsu **Pro Gaming Profiles** eelseadetele: häälestatud profiilid, mis eraldavad maksimaalse sujuvuse, VRAM-i efektiivsuse ja kaadrite tempimise juba olemasolevast silikonist.

## PayPal (jäädav avamine)

**Anneta:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

Lisa PayPal märkusesse/memo-sse: **`GPU-UNLOCK`** ja oma GitHub või e-post (valikuline, tänu jaoks).

Pärast annetust aktiveeri avamine (vaata [Õpetuse samm 7](gaming-tutorial.md#step-7-unlock-pro-gaming-profiles)).

---

## Mida „jäädav avamine" tähendab

| Tasuta (kõigile) | Patron avamine |
|------------------|----------------|
| Täielik avatud lähtekoodiga virn | Kõik tasuta tasemel |
| Latency shield demo | **Pro latency profiilid** (competitive / cinematic / VR) |
| Põhiline mängude CLI | **Patron bänner + avamise olek** |
| Kogukonna tugi | Prioriteetne issue silt GitHubis (lisa PayPal kviitung issue-sse) |
| — | **VRAM osmotic agressiivne eelseade** (suurem virtuaalne arena) |
| — | **Speculative intent horisont ×2** (sujuvam tunne kiire hiirega) |
| — | **Varajane juurdepääs** uutele mängude tuumadele |

**Oluline:** Patron avamine on **tarkvara konfiguratsioon + eelseaded** — mitte maagiline silikon. Sinu GPU-l on endiselt füüsilised piirid. Aitame sul lõpetada tsüklite raiskamise draiveri paisumisele ja nähtamatule detailile.

---

## Soovitatud tasemed (auusüsteem)

| Tase | Soovitatud summa | Saad |
|------|------------------|------|
| **Supporter** | 5 $+ | Pro profiilid + patron olek |
| **Enthusiast** | 15 $+ | Eelnev + nimi [PATRONS.md](../../PATRONS.md) failis (opt-in PayPal märkuses) |
| **Legend** | 50 $+ | Eelnev + varajased beeta buildid `@patron` sildiga väljalaskes |

Mis tahes summa avab Pro profiilid, kui lisad annetuse märkusesse **`GPU-UNLOCK`**.

---

## Aktiveeri avamine

### Valik A — Keskkonnamuutuja (kiire)

```powershell
# Windows PowerShell (current session)
$env:UTAHVIDIA_PATRON = "1"

# Permanent (user)
[System.Environment]::SetEnvironmentVariable("UTAHVIDIA_PATRON", "1", "User")
```

```bash
# Linux / macOS
export UTAHVIDIA_PATRON=1
echo 'export UTAHVIDIA_PATRON=1' >> ~/.bashrc
```

### Valik B — Patron fail (soovitatud)

Pärast annetust loo:

**Windows:** `%USERPROFILE%\.utahvidia\patron.unlock`  
**Linux/macOS:** `~/.utahvidia/patron.unlock`

```powershell
mkdir $env:USERPROFILE\.utahvidia -Force
"GPU-UNLOCK" | Out-File $env:USERPROFILE\.utahvidia\patron.unlock -Encoding utf8
```

```bash
mkdir -p ~/.utahvidia
echo "GPU-UNLOCK" > ~/.utahvidia/patron.unlock
```

Valikuline: lisa teisele reale PayPal tehingu ID toe kontrolliks.

### Kontrolli

```bash
utahvidia patron
```

Peaksid nägema: `Patron unlock: ACTIVE` ja saadaolevaid Pro profiile.

---

## Loojatele ja striimijatele

Võid oma publikule öelda:

> „Anneta Utah-Vid-ia-le PayPali kaudu (**utah@utahcreates.com**, memo **GPU-UNLOCK**), et avada jäädavalt Pro Gaming Profiles, mis häälestavad Utah-Vid-ia sinu täpse GPU jaoks — rohkem FPS-tunnet ilma uut riistvara ostmata."

Link: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)

Partnerlusstiilis: ametlikku partnerprogrammi veel pole. Kasuta annetuse linki + õpetust oma kirjelduse; opt-in PATRONS.md krediidi jaoks.

---

## Tagasimaksed ja ausus

- Annetused on vabatahtlikud ja PayPal standardpoliitika järgi tagastamatud.
- Kui Pro profiilid ei aita sinu süsteemis, [ava issue](https://github.com/utahisnotastate/utahvidia/issues) koos `utahvidia bench` väljundiga — parandame eelseadeid kõigile.

[Täielik mängija õpetus](gaming-tutorial.md) · [Üldine annetamine](donate.md) · [Tagasi mängude keskusesse](gaming-index.md)

**Teised keeled:** [English](../en/gpu-unlock-patron.md) · [Eesti](../et/gpu-unlock-patron.md) · [Русский](../ru/gpu-unlock-patron.md) · [Suomi](../fi/gpu-unlock-patron.md)
