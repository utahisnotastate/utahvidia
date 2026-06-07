# CUDA プログラマー向け Utah-Vid-ia

カーネル、ストリーム、オキュパンシーで考えるあなたへ。このガイドは CUDA の概念を Utah-Vid-ia モジュールに対応づけ、最小限の統合パスを示します。

## 概念マップ

| CUDA の世界 | Utah-Vid-ia の対応 |
|------------|------------------------|
| `nvcc` / PTX | `UtahVectorCompiler` + Triton BRTR |
| CUDA ランタイム API | PyTorch + 任意の `zeo_shield_kernel.cu` |
| `cudaMemcpyAsync` プリフェッチ | `NeuralStatePrefetcher` デュアルストリーム |
| マルチ GPU `cudaSetDevice` | `UtahOsmoticRouter.route_sync` |
| ECC / エラー回復 | `entropy_shield` / `engine.heal()` |
| カスタム `__global__` カーネル | `zeo_shield_kernel.cu` または Triton カーネルを拡張 |

## Utah-Vid-ia と生 CUDA の使い分け

**Utah-Vid-ia を使うとき:**

- PyTorch（または ATen）がすでにスタックにある
- すべてのカーネルを書き直さずにオーケストレーション + 移植性フックが欲しい
- マルチ GPU の流動的スケジューリングを試作している

**生 CUDA のままにするとき:**

- Python オーバーヘッドゼロで手チューニングしたワープレベルカーネルが必要
- PyTorch パスのない CUDA 専用ライブラリに依存（cuDNN カスタム op など）
- 本番が今日時点で認証済みツールチェーンを要求する

## クイック統合

### 1. ドロップインオーケストレータ（PyTorch テンソル）

```python
import torch
from utahvidia import UtahSiliconOrchestrator

orch = UtahSiliconOrchestrator()
a = torch.randn(1024, 1024, device="cuda")
b = torch.randn(1024, 1024, device="cuda")
c = orch.execute_shielded_matmul(a, b)
```

### 2. 既存 torch op への Ghost layer

```python
from utahvidia import activate_ghost_layer, UtahVidIaEngine
import torch

engine = UtahVidIaEngine()
x = torch.randn(4096, 4096, device="cuda")

with activate_ghost_layer() as ghost:
    matmul = ghost.wrap("matmul", torch.matmul)
    y = engine.execute_optimized(matmul, x, x)

print(ghost.history[-1].target_ir)  # utah.mlir.matmul @ device(cuda) -> spirv
```

### 3. ネイティブ ZEO カーネル（CUDA C++）

ソース:

- `zeo_shield_kernel.cu` — `launch_zeo_kernel`, 共有メモリタイル, `entropy_shield`
- `native/zeo_shield_bindings.cpp` — PyTorch 拡張

初回呼び出しで Python が自動ロード:

```python
from utahvidia.zeo_shield import zeo_prefetched_matmul

out = zeo_prefetched_matmul(a, b, use_native=True)
```

要件: `PATH` に NVCC、CUDA 付き PyTorch。

### 4. カスタムカーネル拡張ポイント

`zeo_shield_kernel.cu` にデバイス関数を追加し、バインディング経由で公開、`ZeoShieldEngine` から呼び出す。

パターン:

```cpp
extern "C" void launch_zeo_kernel(..., cudaStream_t stream);
```

バインディングでは `at::cuda::getCurrentCUDAStream()` を使い、PyTorch のストリームセマンティクスを尊重する。

## ストリームとプリフェッチ

`NeuralStatePrefetcher` は **計算 / プリフェッチストリームのオーバーラップ** を再現します:

```python
from utahvidia.zeo_shield import NeuralStatePrefetcher, PrefetchJob
import torch

prefetcher = NeuralStatePrefetcher()
semantic = torch.randn(768, device="cuda")  # prompt embedding proxy

jobs = [
    PrefetchJob("layer0", torch.matmul, (a, w0), {}),
    PrefetchJob("layer1", torch.matmul, (a, w1), {}),
]
prefetcher.predict_from_embedding(semantic, jobs)
out = prefetcher.execute_current(jobs[0])
```

手動実装との比較:

```cpp
cudaStream_t compute, prefetch;
kernel_compute<<<..., compute>>>(...);
cudaMemcpyAsync(..., prefetch);
```

## Entropy shield と ECC

CUDA ECC はメモリコントローラレベルで **検出と訂正** を行います。

Utah-Vid-ia Entropy-Shield はソフトウェアで値を参照パリティ格子に向けて **ブレンド** します — 優雅な劣化デモや研究に有用ですが、データセンター ECC ポリシーの **代替ではありません**。

```python
from utahvidia import ZeoShieldEngine

engine = ZeoShieldEngine()
clean = kernel_output.clone()
corrupted = clean.clone()
corrupted[0, 0] += 1.0  # simulate flip
healed = engine.heal(corrupted, clean)
```

## デバッグ

```bash
utahvidia zeo -v          # verbose logging
pytest tests/test_zeo_shield.py -v
```

よくある問題:

| 症状 | 対処 |
|---------|-----|
| ネイティブ拡張のコンパイル失敗 | CUDA ツールキットをインストール、`nvcc` が PATH にあることを確認 |
| Triton がない | `pip install triton`（Linux）; PyTorch フォールバックを使用 |
| `torch.matmul` より遅い | ZEO タイル op は要素ごとのデモカーネルで、GEMM ではない |

## 次のステップ

- [移行ガイド](migration-guide.md) — CUDA → Utah-Vid-ia の段階的移行
- [技術リファレンス](technical.md) — 全モジュール一覧

[索引に戻る](index.md)
