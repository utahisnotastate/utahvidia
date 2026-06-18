# レイテンシーシールド — ドライバーレス フレーム再構成

## 問題

ゲームエンジンとベンダードライバはフレームディスパッチを **直列化** する。CPU キューが GPU 作業をブロック → マイクロスタッターと入力レイテンシ。

## 解決策

**Utah-Vid-ia レイテンシーシールド** はフレームストリームをインターセプトし、以下から中間フレームを合成する:

- 現在フレーム（RGBA）
- 履歴フレーム
- ピクセル単位のモーションベクトル

ディスプレイパイプラインがドライバ完了を待つ前に。

## アーキテクチャ

```
Render engine → current/history/motion tensors
        ↓
LatencyShieldIntercept (dedicated CUDA stream)
        ↓
utahvidia_reconstruction_kernel (or PyTorch fallback)
        ↓
Display-ready frame
```

## カーネルパラメータ

| パラメータ | デフォルト | 役割 |
|-------|---------|------|
| `BLOCK_DIM_X` | 32 | ワープ幅 |
| `BLOCK_DIM_Y` | 8 | 占有率チューニング |
| `alpha` | 0.65 | 現在と履歴のブレンド |
| `SHARED_PADDING` | 1 | バンクコンフリクト回避 |

## JIT 温度プロファイル

`JitProfiler` はシミュレートされたコア温度が 82°C を超えると `alpha` と占有率ターゲットを切り替える —— 完全 Driver API 展開では `UtahvidiaJitProfiler` による PTX ホットスワップのスタンドイン。

## API

```python
from utahvidia.latency_shield import LatencyShieldIntercept, reconstruct_frames

shield = LatencyShieldIntercept(1920, 1080)
out = shield.dispatch(current, history, motion, core_temp_c=75.0)
```

## 本番メモ

- Alpha v0.3: テンソルレベルのインターセプト、カーネルモードディスプレイフックではない
- ネイティブ CUDA JIT は `torch.utils.cpp_extension.load` 経由
- 真の OS バイパスは `microvisor.py` を参照（**シミュレーションのみ**）

## 他の言語

[English](../en/latency-shield.md) · [中文](../zh/latency-shield.md)

[ゲームドキュメントに戻る](gaming-index.md)
