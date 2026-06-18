# ゲーム FAQ

## 一般

### Utah-Vid-ia は GPU の代わりになる？

**いいえ。** 持っている GPU をより賢く動かします —— より良いフレームペーシング、オプションのアップスケール経路、マルチ GPU 分割、VRAM 仮想化デモ。物理がピーク性能の限界を決めます。

### 安全？

はい。オープンソース（MIT）、pip パッケージにカーネルモード rootkit はありません。Microvisor は **シミュレーションのみ**。パトロンアンロックはローカル設定ファイル —— スパイウェアなし。

### 自分のゲームで動く？

v0.3 は **ミドルウェア + デモ**。今日は Python/スクリプトで統合。AAA ゲームへの直接注入はロードマップ上（Driver API / プラットフォームパートナー）。

---

## パトロン / 寄付

### 寄付すると何がもらえる？

[Pro ゲーミングプロファイル](gpu-unlock-patron.md): `patron_max`、`patron_vram`、`patron_legend` —— レイテンシーシールド、推測インテント、オスモティック VRAM 向けに調整されたプリセット。

### 最低寄付額は？

メモ **`GPU-UNLOCK`** 付きなら金額は問いません。目安: $5 サポーター、$15 エンスージアスト、$50 レジェンド。

### アンロックは本当に永久？

はい —— `~/.utahvidia/patron.unlock` または `UTAHVIDIA_PATRON=1` に保存。サブスクなし。一度寄付すれば PC 上で永久（名誉制度）。

### 返金はできる？

PayPal の標準返金ポリシーが適用されます。プリセットがハードウェアで機能しない場合は GitHub issue でサポートに連絡してください。

---

## 技術

### NVIDIA vs AMD vs Intel？

PyTorch 経路はどこでも動作。ネイティブ CUDA カーネル（レイテンシーシールド、ZEO）は NVIDIA + オプションの NVCC が必要。

### サイバーパンク / フォートナイトで FPS が上がらないのはなぜ？

それらのゲームは Utah-Vid-ia を自動では呼びません。まず `utahvidia gaming` とカスタムスクリプトを実行。パトロンプロファイルは **あなたが** フレームをエンジンに通したときに適用されます。

### 「知覚アップスケール」とは？

内部で低解像度レンダリングし、ホログラフィック/テンソル経路でディテールを合成 —— DLSS/FSR と同じ発想、Utah-Vid-ia スタイルのデモは `UtahRealityEngine.perceptual_upscale_path`。

---

## サポート

- GitHub Issues: [utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia/issues)  
- 寄付: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  

## 他の言語

[English](../en/gaming-faq.md) · [中文](../zh/gaming-faq.md)

[完全チュートリアル](gaming-tutorial.md) · [ゲームハブ](gaming-index.md)
