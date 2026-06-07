# 移行ガイド — CUDA / PyTorch → Utah-Vid-ia

本番の学習や推論を止めずに、Utah-Vid-ia を段階的に導入するためのガイドです。

## 移行の原則

1. **まずシャドー** — 既存ジョブと並行して Utah-Vid-ia を実行し、出力とレイテンシを比較する。
2. **一度に一層** — オーケストレータ → osmotic ルーティング → ZEO → ネイティブカーネル。
3. **ロールバックを維持** — import をフィーチャーフラグ化し、一括書き換えはしない。

## フェーズ 0 — 棚卸し（1週間）

記録すること:

- [ ] PyTorch vs 生 CUDA vs Triton の使用状況
- [ ] 各環境の GPU モデルとドライバ
- [ ] マルチ GPU トポロジ（NVLink、PCIe）
- [ ] 重要なレイテンシ SLO とエラーバジェット

開発マシンに Utah-Vid-ia をインストール:

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
utahvidia all
pytest -q
```

## フェーズ 1 — Ghost layer 可観測性（1〜2週間）

**目標:** 数値を変えずに IR 監査証跡を得る。

```python
from utahvidia import activate_ghost_layer
import torch

with activate_ghost_layer(verbose=True) as ghost:
    # wrap your existing torch calls
    result = ghost.wrap("matmul", torch.matmul)(a, b)

for record in ghost.history:
    print(record.op_name, record.target_ir)
```

**完了条件:** ホットパス op がすべてログされる。p99 レイテンシに測定可能な悪化がない。

## フェーズ 2 — Osmotic ルーティング（2〜4週間）

**目標:** ハードコードされたデバイス ID ではなく、負荷に応じてバッチジョブを GPU に分散する。

変更前:

```python
with torch.cuda.device(0):
    out = model(batch)
```

変更後:

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
out = router.route_sync(forward_fn, batch)
```

**完了条件:** マルチ GPU ノードの利用率が向上。ゴールデンテストで正確性のずれがない。

## フェーズ 3 — オーケストレータ統合（2〜4週間）

**目標:** ghost + ルーティング + ZEO フックの単一 API。

```python
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
out = orch.execute_shielded_matmul(a, b)
pipeline_out = orch.run_llm_stress_demo(hidden=4096, layers=your_layer_count)
```

アドホックなデバイスロジックを、設定フラグの背後にあるオーケストレータ呼び出しに置き換える:

```python
USE_UTAH = os.getenv("UTAHVIDIA", "0") == "1"

if USE_UTAH:
    out = orch.execute_shielded_matmul(a, b)
else:
    out = torch.matmul(a, b)
```

## フェーズ 4 — ベクトルコンパイラ / Triton（任意、Linux CUDA）

```bash
pip install -e ".[compiler]"
```

```python
from utahvidia.compiler import trigger_compiler
out = trigger_compiler(data_tensor)
```

GEMM 全体を Triton に移植する前に、要素ごとのカスタム op に使用する。

## フェーズ 5 — ネイティブ ZEO カーネル（任意）

NVCC が必要。本番で有効化する前にベンチマークする:

```bash
utahvidia bench
```

ワークロードごとに有効化:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul
out = zeo_prefetched_matmul(a, b, use_native=True)
```

## フェーズ 6 — Entropy 修復（研究 / バッチのみ）

検証なしにライブ学習の損失パスで修復を有効化 **しない** こと。

```python
from utahvidia import ZeoShieldEngine
engine = ZeoShieldEngine()
restored = engine.heal(corrupted, reference_clean)
```

## ロールバックチェックリスト

- `UTAHVIDIA=0` を設定
- オーケストレータラッパーの import を削除
- ghost ログを無効化（`verbose=False`）

## 検証マトリクス

| テスト | 合格条件 |
|------|----------------|
| 数値パリティ | `torch.allclose(baseline, utah, rtol=..., atol=...)` |
| レイテンシ | p99 が合意した予算内 |
| マルチ GPU | 利用率の σ が低下 |
| ソークテスト | 24時間バッチジョブ、新しい OOM クラスゼロ |

## 他スタックからの移行

| 元スタック | 備考 |
|--------------|-------|
| **純 CUDA C++** | まず PyTorch 境界でラップするか、`zeo_shield_bindings.cpp` のようなカスタム拡張をバインド |
| **JAX** | 直接サポートなし; PyTorch にエクスポートするか、サブプロセス経由で Python オーケストレータを呼ぶ |
| **TensorFlow** | 同様 — TFX/PyTorch ブリッジを使うかホットパスを移植 |
| **ROCm PyTorch** | Osmotic + ghost は動作; ネイティブ ZEO CUDA カーネルは現時点 NVIDIA のみ |

## サポート

Issue: [GitHub Issues](https://github.com/utahisnotastate/utahvidia/issues)  
寄付: [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

[索引に戻る](index.md) · [CUDA プログラマー向け](cuda-programmers.md)
