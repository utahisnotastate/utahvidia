# GPU Unlock Patron -ohjelma

**Avaa GPU:si täyden potentiaalin — tue Utah-Vid-iaa ja pidä laitteesi relevanttina pidempään.**

Utah-Vid-ian ydin on **ilmainen avoimen lähdekoodin (MIT)**. **GPU Unlock Patron -ohjelma** antaa lahjoittaville pelaajille pääsyn **Pro Gaming Profiles** -esiasetuksiin: viritettyihin profiileihin, jotka puristavat maksimaalisen sujuvuuden, VRAM-tehokkuuden ja kehysten tahdistuksen jo omistamastasi piistä.

## PayPal (pysyvä avaus)

**Lahjoita:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

PayPal-muistioon: **`GPU-UNLOCK`** ja GitHub tai sähköposti (valinnainen, kiitokseen).

Lahjoituksen jälkeen aktivoi avaus (katso [Opas vaihe 7](gaming-tutorial.md#step-7-unlock-pro-gaming-profiles)).

---

## Mitä „pysyvä avaus" tarkoittaa

| Ilmainen (kaikille) | Patron-avaus |
|---------------------|--------------|
| Täysi avoimen lähdekoodin pino | Kaikki ilmaisella tasolla |
| Latency shield -demo | **Pro latency -profiilit** (competitive / cinematic / VR) |
| Perus peli-CLI | **Patron-banneri + avauksen tila** |
| Yhteisötuki | Prioriteettitagi GitHub-issueissa (liitä PayPal-kuitti) |
| — | **VRAM osmotic aggressiivinen esiasetus** (suurempi virtuaaliareena) |
| — | **Speculative intent horizon ×2** (sujuvampi tunne nopealla hiirellä) |
| — | **Varhainen pääsy** uusiin pelikerneliin |

**Tärkeää:** Patron-avaus on **ohjelmistokonfiguraatio + esiasetukset** — ei taikaa piissä. GPU:llasi on edelleen fyysiset rajat. Autamme lopettamaan syklien tuhlaamisen ajurin pullistumiseen ja näkymättömään yksityiskohtaan.

---

## Ehdotetut tasot (kunniajärjestelmä)

| Taso | Ehdotettu summa | Saat |
|------|-----------------|------|
| **Supporter** | 5 $+ | Pro-profiilit + patron-tila |
| **Enthusiast** | 15 $+ | Edellinen + nimi [PATRONS.md](../../PATRONS.md) -tiedostossa (opt-in PayPal-muistiosta) |
| **Legend** | 50 $+ | Edellinen + varhaiset beta-buildit `@patron`-tagilla julkaisuissa |

Mikä tahansa summa avaa Pro-profiilit, jos lahjoitusmuistiossa on **`GPU-UNLOCK`**.

---

## Aktivoi avaus

### Vaihtoehto A — Ympäristömuuttuja (nopea)

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

### Vaihtoehto B — Patron-tiedosto (suositeltu)

Lahjoituksen jälkeen luo:

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

Valinnainen: lisää PayPal-tapahtuman ID toiselle riville tuen varmistukseen.

### Tarkista

```bash
utahvidia patron
```

Pitäisi näkyä: `Patron unlock: ACTIVE` ja saatavilla olevat Pro-profiilit.

---

## Sisällöntuottajille ja striimaajille

Voit kertoa yleisöllesi:

> „Lahjoita Utah-Vid-ialle PayPalin kautta (**utah@utahcreates.com**, muistio **GPU-UNLOCK**), avataksesi pysyvästi Pro Gaming Profiles -profiilit, jotka virittävät Utah-Vid-ian juuri sinun GPU:llesi — enemmän FPS-tuntumaa ilman uutta laitetta."

Linkki: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)

Kumppanuusohjelmaa ei vielä ole. Käytä lahjoituslinkkiä + opasta kuvauksessasi; opt-in PATRONS.md-krediittiin.

---

## Palautukset ja rehellisyys

- Lahjoitukset ovat vapaaehtoisia ja palauttamattomia PayPalin standardikäytännön mukaan.
- Jos Pro-profiilit eivät auta järjestelmässäsi, [avaa issue](https://github.com/utahisnotastate/utahvidia/issues) `utahvidia bench` -tulosteella — parannamme esiasetuksia kaikille.

[Täysi pelaajan opas](gaming-tutorial.md) · [Yleiset lahjoitustiedot](donate.md) · [Takaisin pelikeskukseen](gaming-index.md)

**Muut kielet:** [English](../en/gpu-unlock-patron.md) · [Eesti](../et/gpu-unlock-patron.md) · [Русский](../ru/gpu-unlock-patron.md) · [Suomi](../fi/gpu-unlock-patron.md)
