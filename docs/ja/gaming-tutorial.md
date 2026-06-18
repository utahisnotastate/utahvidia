# ゲーマー向けチュートリアル — ゼロから GPU アンロックまで

完全ウォークスルー: Utah-Vid-ia のインストール、ゲーミングスタックの実行、GPU のベンチマーク、そして任意で[パトロン・プログラム](gpu-unlock-patron.md)経由の **Pro プロファイルアンロック**。

**所要時間:** 約 30 分 · **費用:** $0（Pro アンロックは寄付で任意）

---

## 達成すること

1. Windows、Linux、macOS に Utah-Vid-ia をインストール  
2. **漸近リアリティエンジン** ゲームデモを実行  
3. **あなたの** GPU 上でのレイテンシーシールド + 知覚アップスケールを理解  
4. 前後の体感をベンチマーク  
5. 任意で PayPal 寄付により **Pro ゲーミングプロファイルを永久アンロック**  

---

## 前提条件

| 要件 | メモ |
|-------------|-------|
| Python 3.10+ | `py --version` または `python3 --version` |
| pip | パッケージインストーラ |
| Git | GitHub からクローン |
| GPU（任意） | NVIDIA CUDA が最良; AMD/Intel は PyTorch 経由; CPU = デモモード |

---

## ステップ 1 — クローンとインストール

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
```

Windows PowerShell:

```powershell
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
py -m pip install -e ".[dev]"
```

確認:

```bash
utahvidia --help
# or: py -m utahvidia.cli
```

---

## ステップ 2 — 最初のゲームデモを実行

```bash
utahvidia gaming
```

想定出力（抜粋）:

```
UTAH-VIDIA // Universal Compute Bridge v0.3.0
microvisor: [MICROVISOR SIM] ...
Latency shield: (180, 320, 4) in X.XX ms
Perceptual upscale: (360, 640, 3)
Speculative frame: (180, 320, 4)
```

**何が起きたか:**

- **レイテンシーシールド** がモーションベクトルで現在フレームと履歴をブレンド（より滑らかな動き）。  
- **知覚アップスケール** が低解像度ベースラインから解像度を 2 倍（AI スタイル経路デモ）。  
- **推測インテント** がマウス風デルタからファントムフレームを事前レンダリング。  

---

## ステップ 3 — フルスタックツアー

```bash
utahvidia all
```

ghost kernel、コンパイラ、オスモティックルーター、フォトニックシム、ZEO-Shield、オーケストレータ、**および** ゲーミングスタックを実行。

---

## ステップ 4 — GPU をベンチマーク

```bash
utahvidia bench
```

出力を保存 —— GitHub issue やパトロンプロファイル比較に有用。

NVCC 付き CUDA システムでは、ネイティブカーネルが初回実行時に JIT コンパイルされる場合あり（一度だけ数秒追加）。

---

## ステップ 5 — Python: マシン上でフレームを調整

`my_gaming_test.py` を作成:

```python
import torch
from utahvidia import UtahRealityEngine
from utahvidia.latency_shield import DisplayHookConfig

# Match your monitor or game resolution
W, H = 1920, 1080
engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=W, height=H))

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")
print(engine.bootstrap_gaming_enclave())

current = torch.rand(H, W, 4, device=device)
history = torch.rand(H, W, 4, device=device)
motion = torch.randn(H, W, 2, device=device) * 0.3

frame = engine.reconstruct_frame(current, history, motion)
upscaled = engine.perceptual_upscale_path(current[..., :3])

print("Frame:", frame.shape, "Upscaled:", upscaled.shape)
```

実行:

```bash
python my_gaming_test.py
```

---

## ステップ 6 — 競技 vs シネマティックプロファイル（無料デフォルト）

```python
from utahvidia.patron import apply_gaming_profile, list_profiles

print(list_profiles())  # competitive, cinematic, vr, patron_* if unlocked

engine = UtahRealityEngine()
apply_gaming_profile(engine, "competitive")  # lower alpha = snappier
# apply_gaming_profile(engine, "cinematic")  # smoother interpolation
```

| プロファイル | おすすめ | レイテンシーシールド alpha |
|---------|----------|----------------------|
| `competitive` | eスポーツ、速いマウス | 0.75（よりキビキビ） |
| `cinematic` | シングルプレイ、ストーリー | 0.55（より滑らか） |
| `vr` | ヘッドセット | 0.60 + 推測ホライズン短縮 |

アンロック後のパトロン専用: `patron_max`、`patron_vram`、`patron_legend`。

---

## ステップ 7 — Pro ゲーミングプロファイルをアンロック

1. PayPal で寄付: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  
2. メモ/備考: **`GPU-UNLOCK`**  
3. パトロンファイル作成または環境変数設定 —— [完全手順](gpu-unlock-patron.md#アンロックを有効化する)  
4. 確認:

```bash
utahvidia patron
```

5. max プロファイルを適用:

```python
from utahvidia import UtahRealityEngine
from utahvidia.patron import apply_gaming_profile, patron_status

print(patron_status())
engine = UtahRealityEngine()
apply_gaming_profile(engine, "patron_max")
```

**このマシンで Pro プリセットを永久アンロックしました**（ファイルまたは環境変数は再起動後も保持）。

---

## ステップ 8 — トラブルシューティング

| 問題 | 対処 |
|---------|-----|
| `python` が見つからない（Windows） | `py` を使う |
| CUDA が検出されない | [PyTorch + CUDA](https://pytorch.org) をインストール; CPU モードも動作 |
| ネイティブカーネルコンパイル失敗 | PyTorch 経路を使用; API で `use_native=False` |
| パトロンが有効でない | `~/.utahvidia/patron.unlock` または `UTAHVIDIA_PATRON=1` を確認 |
| 他ゲームで FPS 変化なし | Utah-Vid-ia はミドルウェア —— まずチュートリアルスクリプトで統合; フルゲームフックはロードマップ |

---

## ステップ 9 — 共有と支援

- リポジトリにスター: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)  
- 友達に伝える: **GPU-UNLOCK** 寄付 → Pro プロファイル  
- 配信者: プロフィールに [gpu-unlock-patron.md](gpu-unlock-patron.md) をリンク  

---

## 次に読む

- [GPU アンロック パトロン・プログラム](gpu-unlock-patron.md)  
- [ゲーム FAQ](gaming-faq.md)  
- [レイテンシーシールド詳細](latency-shield.md)  
- [子ども向け —— GPU がなぜ重要か](gaming-children.md)  

## 他の言語

[English](../en/gaming-tutorial.md) · [中文](../zh/gaming-tutorial.md)

[ゲームハブに戻る](gaming-index.md)
