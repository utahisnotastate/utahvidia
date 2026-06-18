# GPU Unlock Patron Program

**Unlock your GPU's full potential — support Utah-Vid-ia, keep your hardware relevant longer.**

Utah-Vid-ia core is **free and open source (MIT)**. The **GPU Unlock Patron Program** lets gamers who donate access **Pro Gaming Profiles**: tuned presets that squeeze maximum smoothness, VRAM efficiency, and frame pacing from the silicon you already own.

## PayPal (permanent unlock)

**Donate:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

In the PayPal note/memo, include: **`GPU-UNLOCK`** and your GitHub or email (optional, for thank-you).

After donating, activate your unlock (see [Tutorial step 7](gaming-tutorial.md#step-7-unlock-pro-gaming-profiles)).

---

## What "permanently unlock" means

| Free (everyone) | Patron unlock |
|-----------------|---------------|
| Full open-source stack | Everything in free tier |
| Latency shield demo | **Pro latency profiles** (competitive / cinematic / VR) |
| Basic gaming CLI | **Patron banner + unlock status** |
| Community support | Priority issue tag on GitHub (include PayPal receipt in issue) |
| — | **VRAM osmotic aggressive preset** (larger virtual arena) |
| — | **Speculative intent horizon ×2** (smoother feel on fast mice) |
| — | **Early access** to new gaming kernels |

**Important:** Patron unlock is **software configuration + presets** — not magic silicon. Your GPU still has physical limits. We help you stop wasting cycles on driver bloat and invisible detail.

---

## Suggested tiers (honor system)

| Tier | Suggested amount | You get |
|------|------------------|---------|
| **Supporter** | $5+ | Pro profiles + patron status |
| **Enthusiast** | $15+ | Above + name in [PATRONS.md](../../PATRONS.md) (opt-in via PayPal note) |
| **Legend** | $50+ | Above + early beta builds tagged `@patron` on releases |

Any amount unlocks Pro profiles if you include **`GPU-UNLOCK`** in your donation note.

---

## Activate your unlock

### Option A — Environment variable (quick)

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

### Option B — Patron file (recommended)

After donating, create:

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

Optional: add your PayPal transaction ID on the second line for support verification.

### Verify

```bash
utahvidia patron
```

You should see: `Patron unlock: ACTIVE` and available Pro profiles.

---

## For creators & streamers

You may tell your audience:

> "Donate to Utah-Vid-ia via PayPal (**utah@utahcreates.com**, memo **GPU-UNLOCK**) to permanently unlock Pro Gaming Profiles that tune Utah-Vid-ia for your exact GPU — more FPS feel without buying new hardware."

Link: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)

Affiliate-style: we do not run a formal affiliate program yet. Use donate link + tutorial in your description; opt into PATRONS.md for credit.

---

## Refunds & honesty

- Donations are voluntary and non-refundable via PayPal standard policy.
- If Pro profiles do not help on your system, [file an issue](https://github.com/utahisnotastate/utahvidia/issues) with `utahvidia bench` output — we improve presets for everyone.

[Full gamer tutorial](gaming-tutorial.md) · [Donate general info](donate.md) · [Back to gaming hub](gaming-index.md)
