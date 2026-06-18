# Utah-Vid-ia

**Universal Compute Bridge** — free GPU middleware (MIT). Gaming unlock included, no paywall.

> Repository: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)

## Gamers — download and run (no Git)

| Method | How |
|--------|-----|
| **Windows `.exe`** | [Releases](https://github.com/utahisnotastate/utahvidia/releases) → `UtahVidia-Gaming.exe` |
| **ZIP + `.bat`** | [Download ZIP](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip) → run `launchers/UtahVidia-Gaming.bat` |
| **Python** | `pip install git+https://github.com/utahisnotastate/utahvidia.git` then `utahvidia-gaming` |

Full guide: [launchers/README.md](launchers/README.md) · [Gamer tutorial](docs/en/gaming-tutorial.md)

**Optional donations:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

## Documentation

**[docs/README.md](docs/README.md)** — guides in English, 中文, Eesti, Русский, Suomi, 日本語

## Install (developers)

```bash
pip install -e ".[dev]"
utahvidia-gaming   # full gaming unlock
utahvidia gaming   # same via main CLI
```

## Architecture

```
Ghost Kernel → Vector Compiler → Osmotic Router → ZEO-Shield → Reality Engine
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## License

MIT — free forever.
