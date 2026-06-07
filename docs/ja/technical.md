# Utah-Vid-ia — 技術リファレンス

## スタック概要

```
Application (PyTorch / custom)
        ↓
UtahSiliconOrchestrator  ← unified entry
        ↓
┌───────────────────────────────────────────┐
│ GhostKernelLayer   (IR intercept)         │
│ UtahVectorCompiler (Triton BRTR / fallback)│
│ UtahOsmoticRouter  (multi-GPU pressure)   │
│ ZeoShieldEngine    (prefetch + heal)      │
│ zeo_shield_kernel.cu (optional native)    │
└───────────────────────────────────────────┘
        ↓
CUDA / ROCm / CPU (via PyTorch)
```

詳細図: [../ARCHITECTURE.md](../ARCHITECTURE.md)

## モジュール

| モジュール | ファイル | 役割 |
|--------|------|----------------|
| Core | `utahvidia/core.py` | `GhostKernelLayer`, `UtahVidIaEngine`, `activate_ghost_layer()` |
| Compiler | `utahvidia/compiler.py` | `UtahVectorCompiler`, Triton JIT, CPU fallback |
| Osmotic | `utahvidia/osmotic.py` | `UtahOsmoticRouter`, async + sync routing |
| ZEO | `utahvidia/zeo_shield.py` | Prefetch streams, entropy heal, native loader |
| Orchestrator | `utahvidia/orchestrator.py` | `UtahSiliconOrchestrator` |
| Native | `zeo_shield_kernel.cu` | Tile prefetch + `entropy_shield` device fn |

## 要件

- Python ≥ 3.10
- PyTorch ≥ 2.0
- 任意: Triton（Linux CUDA）、NVCC（ネイティブ ZEO JIT）

## インストール

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
pip install -e ".[compiler]"   # Linux + Triton when available
```

## API 概要

### Orchestrator（推奨）

```python
from utahvidia import UtahSiliconOrchestrator
import torch

orch = UtahSiliconOrchestrator()
A, B = torch.randn(512, 512), torch.randn(512, 512)
out = orch.execute_shielded_matmul(A, B)
layers = orch.run_llm_stress_demo(hidden=256, layers=8)
```

### Ghost layer

```python
from utahvidia import UtahVidIaEngine, activate_ghost_layer
import torch

engine = UtahVidIaEngine()
with activate_ghost_layer() as ghost:
    fn = ghost.wrap("add", torch.add)
    result = engine.execute_optimized(fn, x, y)
# ghost.history contains IR audit records
```

### ZEO-Shield

```python
from utahvidia import ZeoShieldEngine

engine = ZeoShieldEngine()
out = engine.matmul_shielded(A, B)
healed = engine.heal(corrupted_tensor, clean_reference)
```

### Osmotic routing

```python
from utahvidia import UtahOsmoticRouter

router = UtahOsmoticRouter()
result = router.route_sync(torch.matmul, a, b)
```

## ネイティブ CUDA 拡張

次の条件を満たすとき、`torch.utils.cpp_extension.load` 経由で遅延ロードされます:

- CUDA が利用可能
- `PATH` に NVCC がある
- ソース: `zeo_shield_kernel.cu`, `native/zeo_shield_bindings.cpp`

Python パスを強制: `zeo_prefetched_matmul(A, B, use_native=False)`

## ベンチマーク

```bash
utahvidia bench
utahvidia-bench --sizes 128 256 512 1024 --iters 20
```

注: ZEO タイルカーネルは要素ごとの `A * B` とシールドメタデータです。GEMM FLOPs ではなくレイテンシパターンを比較してください。

## テスト

```bash
pytest -q
```

## 拡張ポイント

1. **実際の MLIR エクスポート** — `GhostKernelLayer.translate()` の文字列 IR を置き換え
2. **SPIR-V / ROCm バックエンド** — コンパイラのコンパイルパスに接続
3. **カスタムパリティソース** — Entropy-Shield 向けエンタープライズチェックサムストア
4. **スケジューラ統合** — `UtahOsmoticRouter` を呼ぶ K8s デバイスプラグイン

## バージョン

現在: **v0.2.0**（alpha）

[索引に戻る](index.md) · [CUDA プログラマー向け](cuda-programmers.md) · [移行ガイド](migration-guide.md)
