"""Benchmark ZEO-Shield vs standard PyTorch CUDA paths."""

from __future__ import annotations

import argparse
import statistics
import time

import torch

from utahvidia.zeo_shield import ZeoShieldEngine, zeo_prefetched_matmul


def _sync() -> None:
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def _bench(fn, warmup: int = 3, iters: int = 20) -> dict[str, float]:
    for _ in range(warmup):
        fn()
    _sync()
    samples = []
    for _ in range(iters):
        t0 = time.perf_counter()
        fn()
        _sync()
        samples.append((time.perf_counter() - t0) * 1000)
    return {
        "mean_ms": statistics.mean(samples),
        "stdev_ms": statistics.pstdev(samples) if len(samples) > 1 else 0.0,
        "min_ms": min(samples),
    }


def run_benchmark(sizes: list[int], iters: int) -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("=" * 68)
    print("  UTAH-VIDIA // ZEO-Shield Benchmark")
    print(f"  Device: {device}" + (f" ({torch.cuda.get_device_name(0)})" if device == "cuda" else ""))
    print("=" * 68)

    engine = ZeoShieldEngine(verbose=False)

    for n in sizes:
        A = torch.randn(n, n, device=device)
        B = torch.randn(n, n, device=device)

        baseline = _bench(lambda: torch.matmul(A, B), iters=iters)
        zeo = _bench(lambda: zeo_prefetched_matmul(A, B, use_native=False), iters=iters)
        shielded = _bench(lambda: engine.matmul_shielded(A, B), iters=iters)

        print(f"\n  N={n}")
        print(f"    torch.matmul       {baseline['mean_ms']:8.3f} ms  (min {baseline['min_ms']:.3f})")
        print(f"    zeo_prefetch (py)  {zeo['mean_ms']:8.3f} ms  (min {zeo['min_ms']:.3f})")
        print(f"    zeo_shield engine  {shielded['mean_ms']:8.3f} ms  (min {shielded['min_ms']:.3f})")

        if device == "cuda":
            try:
                native = _bench(lambda: zeo_prefetched_matmul(A, B, use_native=True), iters=iters)
                print(f"    zeo_native (CUDA)  {native['mean_ms']:8.3f} ms  (min {native['min_ms']:.3f})")
            except Exception as exc:
                print(f"    zeo_native (CUDA)  skipped ({exc})")

    print("\n  Note: ZEO tile kernel is element-wise (A*B) with prefetch+shield;")
    print("  torch.matmul is full GEMM — compare latency patterns, not FLOPs.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark ZEO-Shield kernels")
    parser.add_argument("--sizes", type=int, nargs="+", default=[128, 256, 512])
    parser.add_argument("--iters", type=int, default=20)
    args = parser.parse_args()
    run_benchmark(args.sizes, args.iters)


if __name__ == "__main__":
    main()
