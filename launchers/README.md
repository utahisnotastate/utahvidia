# Download Utah-Vid-ia Gaming (no Git required)

Three ways to run the **full gaming unlock** without cloning the repository.

## Option 1 — Download the `.exe` (easiest)

1. Open [GitHub Releases](https://github.com/utahisnotastate/utahvidia/releases)
2. Download **`UtahVidia-Gaming.exe`** (Windows)
3. Double-click to run — full stack, all profiles enabled

The exe is large (~200MB+) because it bundles Python and PyTorch. No install steps.

> Releases are built automatically when a version tag is pushed (e.g. `v0.4.0`), or from **Actions → Build UtahVidia-Gaming.exe → Run workflow**.

## Option 2 — Double-click `.bat` (needs Python)

1. Download the repo as [ZIP](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip) and extract
2. Run **`launchers/UtahVidia-Gaming.bat`**
3. Installs Utah-Vid-ia from the folder and runs the gaming unlock

Requires [Python 3.10+](https://python.org) — **no Git**.

## Option 3 — One command (needs Python + pip)

```bash
pip install git+https://github.com/utahisnotastate/utahvidia.git
utahvidia-gaming
```

Or from a downloaded ZIP:

```bash
cd utahvidia-main
pip install -e .
utahvidia-gaming
```

---

## Build the exe yourself

```powershell
cd launchers
.\build_gaming_exe.ps1
# Output: ..\dist\UtahVidia-Gaming.exe
```

Requires `pip install pyinstaller`.

---

## Optional donations

Utah-Vid-ia is **free (MIT)**. Everything is unlocked.

Support development: [utah@utahcreates.com via PayPal](https://www.paypal.com/donate/?business=utah%40utahcreates.com)
