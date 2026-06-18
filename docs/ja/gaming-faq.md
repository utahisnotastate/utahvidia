# ゲーム FAQ

## ダウンロードと実行

### Git なしで実行するには？

[Releases](https://github.com/utahisnotastate/utahvidia/releases) から **`UtahVidia-Gaming.exe`** をダウンロードするか、[ZIP ダウンロード](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip) から `launchers/UtahVidia-Gaming.bat` を使用してください。

[gaming-tutorial.md](gaming-tutorial.md) を参照。

### 支払いでロックされた機能はある？

**いいえ。** すべてのゲーミングプロファイルと機能は無料です。寄付は [PayPal](https://www.paypal.com/donate/?business=utah%40utahcreates.com) で任意です。

### exe が大きいのはなぜ？

Python と PyTorch を同梱しています（~200MB+）。Python がある場合は `.bat` ランチャーを使用してください。

---

## 一般

### Utah-Vid-ia は GPU の代わりになる？

いいえ — 既存の GPU をより賢く動かします。物理が上限を決めます。

### 安全？

はい。オープンソース（MIT）。ペイウォールファイルなし。pip パッケージの Microvisor はシミュレーションのみ。

### ゲーム内で自動動作する？

v0.4 はミドルウェア + ワンクリックアンロックデモ。直接 AAA ゲーム統合はロードマップ上。

---

## 寄付

### 寄付は必要？

いいえ。Utah-Vid-ia は無料です。

### 寄付方法は？

[PayPal で utah@utahcreates.com に寄付](https://www.paypal.com/donate/?business=utah%40utahcreates.com) — 金額は問いません。ベンチマークとドキュメントに役立ちます。

---

## 技術

### NVIDIA vs AMD？

PyTorch はすべてで動作。ネイティブ CUDA カーネルは NVIDIA + オプションの NVCC が必要。

## 他の言語

[English](../en/gaming-faq.md) · [中文](../zh/gaming-faq.md) · [Eesti](../et/gaming-faq.md) · [Русский](../ru/gaming-faq.md) · [Suomi](../fi/gaming-faq.md)

[完全チュートリアル](gaming-tutorial.md) · [ゲームハブ](gaming-index.md)
