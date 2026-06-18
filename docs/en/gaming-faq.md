# Gaming FAQ

## Download & run

### How do I run this without Git?

Download **`UtahVidia-Gaming.exe`** from [Releases](https://github.com/utahisnotastate/utahvidia/releases), or use `launchers/UtahVidia-Gaming.bat` from a [ZIP download](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip).

See [gaming-tutorial.md](gaming-tutorial.md).

### Is anything locked behind payment?

**No.** All gaming profiles and features are free. Donations are optional via [PayPal](https://www.paypal.com/donate/?business=utah%40utahcreates.com).

### Why is the exe so large?

It bundles Python and PyTorch (~200MB+). Use the `.bat` launcher if you already have Python.

---

## General

### Will Utah-Vid-ia replace my GPU?

No — it helps your existing GPU run smarter. Physics still sets the ceiling.

### Is it safe?

Yes. Open source (MIT). No paywall files. Microvisor is simulation-only in the pip package.

### Does it work inside my game automatically?

v0.4 is middleware + one-click unlock demo. Direct AAA game integration is on the roadmap.

---

## Donations

### Do I need to donate?

No. Utah-Vid-ia is free.

### How do I donate?

[utah@utahcreates.com via PayPal](https://www.paypal.com/donate/?business=utah%40utahcreates.com) — any amount helps benchmarks and docs.

---

## Technical

### NVIDIA vs AMD?

PyTorch works on all. Native CUDA kernels need NVIDIA + optional NVCC.

[Full tutorial](gaming-tutorial.md) · [Gaming hub](gaming-index.md)
