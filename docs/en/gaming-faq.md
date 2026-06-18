# Gaming FAQ

## General

### Will Utah-Vid-ia replace my GPU?

**No.** It makes the GPU you have work smarter — better frame pacing, optional upscale paths, multi-GPU split, VRAM virtualization demos. Physics still limits peak performance.

### Is it safe?

Yes. Open source (MIT), no kernel-mode rootkits in the pip package. Microvisor is **simulation only**. Patron unlock is a local config file — no spyware.

### Does it work with my game?

v0.3 is **middleware + demos**. Integrate via Python/scripts today. Direct injection into AAA games is on the roadmap (Driver API / platform partners).

---

## Patron / donations

### What do I get if I donate?

[Pro Gaming Profiles](gpu-unlock-patron.md): `patron_max`, `patron_vram`, `patron_legend` — tuned presets for latency shield, speculative intent, and osmotic VRAM.

### Minimum donation?

Any amount with memo **`GPU-UNLOCK`**. Suggested: $5 Supporter, $15 Enthusiast, $50 Legend.

### Is unlock really permanent?

Yes — stored in `~/.utahvidia/patron.unlock` or `UTAHVIDIA_PATRON=1`. No subscription. One-time donate, keep forever on your PCs (honor system).

### Can I get a refund?

PayPal standard refund policy applies. Contact support via GitHub issue if presets fail on your hardware.

---

## Technical

### NVIDIA vs AMD vs Intel?

PyTorch path works everywhere. Native CUDA kernels (latency shield, ZEO) need NVIDIA + optional NVCC.

### Why don't I see higher FPS in Cyberpunk / Fortnite yet?

Those games don't call Utah-Vid-ia automatically. Run `utahvidia gaming` and custom scripts first. Patron profiles apply when **you** route frames through the engine.

### What is "perceptual upscale"?

Render low-res internally, synthesize detail via holographic/tensor path — same idea as DLSS/FSR, Utah-Vid-ia style demo in `UtahRealityEngine.perceptual_upscale_path`.

---

## Support

- GitHub Issues: [utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia/issues)  
- Donate: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  

[Full tutorial](gaming-tutorial.md) · [Gaming hub](gaming-index.md)
