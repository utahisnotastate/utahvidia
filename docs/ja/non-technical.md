# Utah-Vid-ia — 非技術者向け概要

## ひとことで

**Utah-Vid-ia は、AI や計算ソフトウェアをさまざまな GPU 上でもっと柔軟に動かし、クラスター利用率を高め、メモリの不具合によるクラッシュを減らすミドルウェアです。**

## なぜ重要か

GPU ベンダーはチップ **と** ソフトウェアのエコシステムをセットで売ります。NVIDIA の CUDA ロックインが最も有名な例です。チームは何年も CUDA 専用コードに投資し、AMD や Intel、より安いハードウェアを使おうとすると、すべて書き直すのに苦労します。

Utah-Vid-ia は **アプリケーションとハードウェアのあいだ** に位置します。PyTorch や AI モデルを置き換えるものではありません — 移植性とオーケストレーションの層を追加します。

## 解決を目指す課題

| 課題 | Utah-Vid-ia のアプローチ |
|---------|----------------------|
| ベンダーロックイン | Ghost kernel + ポータブル IR メタデータ |
| 静的で画一的なドライバ | ランタイムのベクトル再コンパイル（BRTR） |
| GPU クラスターの負荷の偏り | Osmotic マルチ GPU ルーティング |
| CPU 待ちで GPU がアイドル | Neural-State Pre-fetching（ZEO） |
| ECC オーバーヘッド / サイレント破損 | Entropy-Shield マニフォールド修復 |
| エアギャップ / RF なしリンク | Photonic bridge（組み込み試作） |

## 恩恵を受ける人

- **AI スタートアップ** — 混在 GPU 群でハードウェア予算を有効活用
- **レンダーファームと研究所** — ベンダーごとの独自スケジューラなしで負荷分散
- **企業** — 単一ベンダー交渉リスクの低減
- **主権型 / オフライン展開** — フォトニックメッシュオプション（実験的）

## 現時点で *ない* もの

- あらゆるワークロードで「10倍速くなる」魔法のボタンではない
- 初日から CUDA を完全に置き換えるものではない（alpha v0.2.0）
- 自社検証なしに規制対象の本番環境向けに認証済みではない

## 評価方法（30分）

1. [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia) をクローン
2. `utahvidia` を実行してライブデモを確認
3. お使いの GPU で `utahvidia bench` を実行
4. 予算やベンダー戦略を決める場合は [CTO ガイド](cto.md) を読む

## 支援

寄付: [PayPal 経由 utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

[索引に戻る](index.md)
