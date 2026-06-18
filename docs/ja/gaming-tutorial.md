# ゲーマー向けチュートリアル — インストール不要のゲーミングアンロック

Git 不要、アンロックファイル不要、**支払い不要**で **Utah-Vid-ia ゲーミングスタック全体**を実行できます。

**任意の寄付:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## 最速ルート: `.exe` をダウンロード

1. [GitHub Releases](https://github.com/utahisnotastate/utahvidia/releases) にアクセス
2. **`UtahVidia-Gaming.exe`** をダウンロード
3. ダブルクリック

次の表示が出ます:

```
UTAH-VIDIA GAMING UNLOCK
Full stack enabled — no install, no unlock file needed
[1/4] Boot gaming enclave...
[2/4] Latency shield frame reconstruction...
[3/4] Perceptual upscale + speculative intent...
[4/4] Fractal + holographic paths...
GAMING UNLOCK COMPLETE — all profiles active
```

Enter で閉じます（パッケージ exe 実行時）。

まだ Release がない？下のオプション 2 または 3 を使うか、メンテナーに [Build workflow](https://github.com/utahisnotastate/utahvidia/actions) の実行を依頼してください。

---

## オプション 2 — ZIP + `.bat`（Python 必要、Git 不要）

1. [Source ZIP](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip) をダウンロード
2. 任意の場所に展開（例: `Desktop\utahvidia-main`）
3. **`launchers\UtahVidia-Gaming.bat`** をダブルクリック

フォルダからインストールしてフルアンロックを実行します。

---

## オプション 3 — Python ワンライナー

Python 3.10+ がある場合:

```bash
pip install git+https://github.com/utahisnotastate/utahvidia.git
utahvidia-gaming
```

---

## アンロック内容（すべて無料）

| 機能 | 説明 |
|------|------|
| Latency shield | モーション認識再構成でより滑らかなフレーム |
| Profile `max` | 最適なデフォルトチューニング（自動適用） |
| Perceptual upscale | 低解像度ベースラインから高解像度デモパス |
| Speculative intent | 予測入力モーションからの事前レンダリング |
| Osmotic VRAM | 大規模仮想メモリアリーナ（シミュレーション） |
| Photonic / fractal / holographic | フル Reality Engine デモ |

利用可能なプロファイル: `competitive`, `cinematic`, `vr`, `max`, `vram`, `legend`

---

## ステップバイステップ: GPU を調整（任意）

アンロックを一度実行した後、`my_game.py` を作成:

```python
from utahvidia import UtahRealityEngine
from utahvidia.gaming_profiles import apply_gaming_profile
from utahvidia.latency_shield import DisplayHookConfig
import torch

W, H = 1920, 1080
engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=W, height=H))
apply_gaming_profile(engine, "competitive")  # or cinematic, max, legend

device = "cuda" if torch.cuda.is_available() else "cpu"
current = torch.rand(H, W, 4, device=device)
history = torch.rand(H, W, 4, device=device)
motion = torch.randn(H, W, 2, device=device) * 0.3

frame = engine.reconstruct_frame(current, history, motion)
print("OK", frame.shape)
```

---

## トラブルシューティング

| 問題 | 対処 |
|------|------|
| Releases に `.exe` がない | `.bat` または `utahvidia-gaming` を使用; メンテナーが Actions workflow を起動可能 |
| Python が見つからない | [python.org](https://python.org) からインストール、または `.exe` を使用 |
| exe が Windows にブロックされる | 「詳細情報」→「実行する」（未署名の OSS ビルド） |
| ダウンロードが大きい | exe は PyTorch を同梱（~200MB+）— 小さいダウンロードには `.bat` パス |
| AAA ゲームで FPS 変化なし | Utah-Vid-ia はミドルウェア — スクリプトで統合; 直接ゲームフックはロードマップ |

---

## プロジェクトを支援（任意）

永久無料。寄付はハードウェアテストと翻訳に役立ちます:

**PayPal:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## 次に読む

- [ゲームハブ](gaming-index.md)
- [ゲーム FAQ](gaming-faq.md)
- [ダウンロードガイド](../../launchers/README.md)

## 他の言語

[English](../en/gaming-tutorial.md) · [中文](../zh/gaming-tutorial.md) · [Eesti](../et/gaming-tutorial.md) · [Русский](../ru/gaming-tutorial.md) · [Suomi](../fi/gaming-tutorial.md)

[ドキュメント索引に戻る](index.md)
