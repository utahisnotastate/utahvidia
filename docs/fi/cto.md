# Utah-Vid-ia — Opas CTO:lle

## Johtoyhteenveto

Utah-Vid-ia on **alfa-vaiheen laskentaväliohjelmisto**, joka vähentää riippuvuutta yhden toimittajan GPU-ohjelmistopinoista. Se käsittelee klusterin tehottomuutta, siirrettävyysriskejä ja luotettavuusaukkoja, jotka ilmenevät **sen jälkeen**, kun laitteisto on jo ostettu.

Strateginen arvo ei ole "korvaa NVIDIA huomenna". Se on **valinnanvapaus**: sekalaitteistot, neuvotteluvalta ja polku laitteistosta riippumattomaan tekoälyinfrastruktuuriin.

## Liiketoimintaongelmat kartoitettuna

| CTO:n huoli | Utah-Vid-ia -vastaus | Kypsyys |
|-------------|----------------------|----------|
| CUDA-riippuvuuden kustannus | Ghost kernel + siirrettävät IR-koukut | Alpha — metatieto tänään, taustat liitettävissä |
| H100-klusterin alihyödyntäminen | Osmotic fluid routing | Alpha — demo-tasoa, vaatii työkuormaprofiloinnin |
| Ajurin viive uudella piirillä | BRTR-vektorikääntäjä (Triton) | Alpha — CUDA ensin |
| Hiljainen VRAM-korruptio / uudelleenyritykset | Entropy-Shield -paraneminen | Alpha — monikkokorjaus, ei datakeskuksen ECC |
| Toimittajakeskittymisriski | Monitoimittaja-abstraktio | Tiekartta — validoi omalla piirilläsi |

## Kokonaisomistuskustannus (TCO) -kehys

**Ilman väliohjelmistoa:** uudelleenkirjoituskustannukset toimittajan vaihdossa, päällekkäinen suunnittelu aikatauluttajille, joutokäynnissä olevat GPU:t heterogeenisissa telineissä, incident-aika epäselvissä ajurivioissa.

**Väliohjelmiston kanssa (tavoitetila):** yksi orkestrointi-API (`UtahSiliconOrchestrator`), jaetut vertailumittaukset toimittajien välillä, vaiheittainen siirtymä jo käytössä olevista PyTorch-poluista.

**Nykytila:** v0.2.0 on **uskottava prototyyppi** tekniseen due diligenceen — ei suora nvcc-korvaaja kaikelle tuotanto-CUDA:lle.

## Riskirekisteri (rehellinen)

| Riski | Lieventäminen |
|------|------------|
| Alfa-laatu | Pilotti ensin ei-kriittisillä eräajoilla |
| Suorituskyvyn vaihtelu | Vaadi `utahvidia bench` kalustollasi ennen ostoa |
| Oikeudellinen / IP | MIT-lisenssi; tarkista patenttimaisema neuvonantajan kanssa |
| Toimittajan reaktio | Käsittele neuvotteluvarana, ei vihamielisenä lanseerauksena |
| Tukimalli | Sisäinen champion + yhteisö/GitHub-issue:t tänään |

## Suositeltu pilotti (90 päivää)

**Vaihe 1 — Perustaso (2 viikkoa)**  
Vertaa olemassa olevia PyTorch/CUDA-ajoja. Kirjaa $/päättely ja GPU-hyödyntäminen.

**Vaihe 2 — Varjotila (4 viikkoa)**  
Aja Utah-Vid-ia -orkestroijaa rinnakkaisliikenteessä. Vertaa viiveen p50/p99 ja virheprosentteja.

**Vaihe 3 — Osittainen reititys (4 viikkoa)**  
Reititä 10–20 % eräpäättelystä osmotic + ZEO -polkujen kautta.

**Vaihe 4 — Päätös**  
Laajenna, forkkaa sisäisesti, kumppanoidu tai arkistoi — mitattujen säästöjen, ei diojen perusteella.

## Keskustelu GPU-toimittajien kanssa

Kehystä Utah-Vid-ia **Silicon-Transparency -väliohjelmistoksi**:

> "Parannamme hyödyntämistä ja luotettavuutta *teidän* laitteistollanne ilman, että vaadimme ajurien avaamista. Voimme integroitua hankinnan, OEM-paketin tai lisensoidun taustapaikan kautta."

Sama asenne, joka saa suuret toimittajat mukaan: ratkaiset **heidän yritysskaalausongelmansa**, et vain hyökkää katetta vastaan.

## Rakenna vs osta vs rahoita

| Vaihtoehto | Milloin |
|--------|------|
| **Rahoita / lahjoita** | Pieni tiimi, haluaa vaikutusta tiekarttaan |
| **Pilotti sisäisesti** | ML-alustatiimi ≥ 2 insinööriä |
| **Hanki** | Toimittaja tai kilpailija, joka etsii siirrettävyys-IP:tä |

Lahjoita: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

## Materiaalit hallituksen esitykseen

1. Live-demo: `utahvidia orchestrator`
2. Vertailumittauksen tuloste: `utahvidia bench`
3. Arkkitehtuuri: [../ARCHITECTURE.md](../ARCHITECTURE.md)
4. Siirtymäsuunnitelma: [migration-guide.md](migration-guide.md)

[Takaisin indeksiin](index.md) · [Ei-tekninen yleiskatsaus](non-technical.md)
