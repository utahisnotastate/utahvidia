# Utah-Vid-ia lapsille (ja uteliaille aikuisille)

Kuvittele, että tietokoneessasi on **GPU** — supernopea laskuapuri. Se tekee miljoonia laskuja kerralla — loistava peleihin ja tekoälyyn.

## Ongelma: yksi yksityinen tie

Monet ohjelmat voivat tällä hetkellä käyttää helposti vain yhden yrityksen GPU:ta (usein NVIDIA). Se on kuin kaupunki, jossa jokaisen auton **täytyy** ajaa yhden yrityksen yksityisellä tiellä. Jos ostat eri auton (eri GPU-merkin), tie sanoo *"anteeksi, ei sallittu."*

Se ei ole reilua, ja se maksaa perheille ja kouluille enemmän.

## Mitä Utah-Vid-ia tekee: moottoritie kaikille

**Utah-Vid-ia** rakentaa **jaetun moottoritien** yksityisten teiden päälle.

Ohjelmasi sanoo edelleen "laske nämä yhteen" tai "kerro tämä matriisi". Utah-Vid-ia:

1. **Kuuntelee** laskupyynnön (Ghost Kernel)
2. **Kääntää** sen niin, että useammat GPU:t ymmärtävät (Vector Compiler)
3. **Valitsee** klusterin vähiten kuormitetun GPU:n (Osmotic Router)
4. **Valmistelee** seuraavan työn etukäteen, jotta kukaan ei odota (ZEO Pre-Sight)
5. **Korjaa** pienet muistivirheet lempeästi kaatumisen sijaan (Entropy Shield)

## Hauskoja vertauksia

| Utah-Vid-ia -osa | Arjen vertaus |
|------------------|----------------|
| Ghost Kernel | Tulkki ovella |
| Vector Compiler | Räätäli, joka säätää vaatteita kävellessäsi |
| Osmotic Router | Valmentaja, joka passaa vähiten väsyneelle pelaajalle |
| ZEO Pre-Sight | Seuraavan sivun lukeminen samalla kun lopetat nykyisen |
| Photonic Bridge | Taskulamput välittävät viestejä huoneen huutamisen sijaan |

## Kokeile (aikuisen kanssa)

```bash
pip install -e ".[dev]"
utahvidia
```

Näet kuusi demoa. Jokainen tulostaa, mitä Utah-Vid-ia tekee.

## Iso ajatus muistettavaksi

**Laitteisto on laatikko. Utah-Vid-ia on valo, joka kulkee sen läpi.**

Et aina tarvitse hienompaa laatikkoa. Joskus tarvitset älykkäämpää ohjelmistoa, jotta jokainen laatikko toimii hyvin.

[Takaisin indeksiin](index.md) · [Lahjoita](donate.md)
