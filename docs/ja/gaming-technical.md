# ゲーミングスタック — 技術リファレンス

## UtahRealityEngine

`UtahSiliconOrchestrator` を拡張した統合オーケストレータ:

```python
from utahvidia import UtahRealityEngine
import torch

engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=1920, height=1080))
print(engine.bootstrap_gaming_enclave())

h, w = 1080, 1920
current = torch.rand(h, w, 4, device=engine.device)
history = torch.rand(h, w, 4, device=current.device)
motion = torch.zeros(h, w, 2, device=current.device)

frame = engine.reconstruct_frame(current, history, motion)
upscaled = engine.perceptual_upscale_path(current[..., :3])
phantom = engine.speculative_render_cycle(current, mouse_delta=(2.0, -1.0))
```

## モジュールマップ

| 拡張 | モジュール | ネイティブ CUDA |
|-----------|--------|-------------|
| レイテンシーシールド | `utahvidia/latency_shield.py` | `native/latency_shield_kernel.cu` |
| オスモティック VRAM | `utahvidia/vram_osmotic.py` | VMM スタブ（本番は Driver API） |
| フォトニック マルチ GPU | `utahvidia/photonic_multi.py` | PyTorch マルチデバイス |
| ホログラフィックウェイト | `utahvidia/holographic.py` | PyTorch 手続き的 |
| フラクタル ハイパーグラフ | `utahvidia/fractal_graph.py` | PyTorch |
| 推測インテント | `utahvidia/speculative_intent.py` | PyTorch |
| Microvisor | `utahvidia/microvisor.py` | **シミュレーションのみ** |

## レイテンシーシールド カーネル

- ブロック: `32 x 8`（256 スレッド、ワープ整列）
- 共有メモリパディング `[BLOCK_DIM_X + 1]` でバンクコンフリクト緩和
- 任意解像度向けグリッドストライドループ
- ホスト: 専用 `torch.cuda.Stream(priority=-1)`

## フック層戦略

| 経路 | 利点 | 欠点 |
|------|------|------|
| **PyTorch ストリームインターセプト**（デフォルト） | ポータブル、pip インストール | 真のディスプレイドライバーフックではない |
| **CUDA Driver API**（`cuModuleLoad` PTX） | ランタイムの肥大を迂回 | PTX ビルドとプラットフォーム統合が必要 |
| **Vulkan/DX12 レイヤー** | エンジンネイティブ | API スケジューラを再導入 |

推奨ロールアウト: PyTorch シャドウ経路 → Driver API beta → プラットフォームパートナーシップ。

## ベンチマーク

```bash
utahvidia gaming
utahvidia latency
```

## 他の言語

[English](../en/gaming-technical.md) · [中文](../zh/gaming-technical.md)

[レイテンシーシールド詳細](latency-shield.md) · [アーキテクチャ Mermaid](../ARCHITECTURE.md)
