# Mängude KKK

## Üldine

### Kas Utah-Vid-ia asendab mu GPU?

**Ei.** See paneb sinu GPU targemalt tööle — parem kaadrite tempimine, valikulised upscale teed, multi-GPU jagamine, VRAM virtualiseerimise demod. Füüsika piirab endiselt tipptulemust.

### Kas see on ohutu?

Jah. Avatud lähtekood (MIT), pip paketis pole kernel-režiimi rootkit'e. Microvisor on **ainult simulatsioon**. Patron avamine on kohalik konfiguratsioonifail — mitte nuhkvara.

### Kas see töötab mu mänguga?

v0.3 on **vahevara + demod**. Integreeri täna Python/skriptide kaudu. Otsene süst AAA mängudesse on teekonnal (Driver API / platvormipartnerid).

---

## Patron / annetused

### Mida ma annetuse eest saan?

[Pro Gaming Profiles](gpu-unlock-patron.md): `patron_max`, `patron_vram`, `patron_legend` — häälestatud eelseaded latency shield, speculative intent ja osmotic VRAM jaoks.

### Minimaalne annetus?

Mis tahes summa memo-ga **`GPU-UNLOCK`**. Soovitus: 5 $ Supporter, 15 $ Enthusiast, 50 $ Legend.

### Kas avamine on tõesti jäädav?

Jah — salvestatud `~/.utahvidia/patron.unlock` või `UTAHVIDIA_PATRON=1`. Pole tellimust. Ühekordne annetus, igaveseks sinu arvutites (auusüsteem).

### Kas saan tagasimakse?

Kehtib PayPal standardne tagasimaksepoliitika. Võta ühendust GitHub issue kaudu, kui eelseaded sinu riistvaral ebaõnnestuvad.

---

## Tehniline

### NVIDIA vs AMD vs Intel?

PyTorch tee töötab kõikjal. Natiivsed CUDA tuumad (latency shield, ZEO) vajavad NVIDIA + valikulist NVCC-d.

### Miks ma ei näe Cyberpunk / Fortnite'is kõrgemat FPS-i?

Need mängud ei kutsu Utah-Vid-ia automaatselt. Käivita esmalt `utahvidia gaming` ja kohandatud skriptid. Patron profiilid kehtivad, kui **sina** suunad kaadreid mootori kaudu.

### Mis on „perceptual upscale"?

Renderda madal resolutsioon sisemiselt, sünteesi detail holographic/tensor teel — sama idee nagu DLSS/FSR, Utah-Vid-ia stiilis demo `UtahRealityEngine.perceptual_upscale_path`-is.

---

## Tugi

- GitHub Issues: [utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia/issues)  
- Anneta: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  

[Täielik õpetus](gaming-tutorial.md) · [Mängude keskus](gaming-index.md)

**Teised keeled:** [English](../en/gaming-faq.md) · [Eesti](../et/gaming-faq.md) · [Русский](../ru/gaming-faq.md) · [Suomi](../fi/gaming-faq.md)
