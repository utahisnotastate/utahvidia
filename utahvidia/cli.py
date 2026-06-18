"""Utah-Vid-ia CLI — run stack demos and quick benchmarks."""

from __future__ import annotations

import argparse
import logging
import time

import torch

from utahvidia.compiler import trigger_compiler
from utahvidia.core import UtahVidIaEngine, activate_ghost_layer
from utahvidia.orchestrator import UtahSiliconOrchestrator
from utahvidia.reality_engine import UtahRealityEngine
from utahvidia.latency_shield import DisplayHookConfig
from utahvidia.osmotic import UtahOsmoticRouter
from utahvidia.photonic_sim import PhotonicBridge, route_swarm_data
from utahvidia.zeo_shield import (
    ZeoShieldEngine,
    build_parity_lattice,
    entropy_shield_tensor,
    zeo_prefetched_matmul,
)


def _banner() -> None:
    print("=" * 60)
    print("  UTAH-VIDIA // Universal Compute Bridge v0.3.0")
    print("  Ghost | Compiler | Osmotic | ZEO | Reality Engine")
    print("=" * 60)


def demo_ghost() -> None:
    engine = UtahVidIaEngine()
    device = engine.device
    x = torch.randn(512, 512, device=device)
    y = torch.randn(512, 512, device=device)

    with activate_ghost_layer() as ghost:
        add_fn = ghost.wrap("add", torch.add)
        t0 = time.perf_counter()
        result = engine.execute_optimized(add_fn, x, y)
        torch.cuda.synchronize() if device == "cuda" else None
        elapsed = (time.perf_counter() - t0) * 1000

    print(f"  Ghost layer: add {x.shape} + {y.shape} -> {result.shape}")
    print(f"  Device: {device} | {elapsed:.2f} ms | {len(ghost.history)} IR records")


def demo_compiler() -> None:
    n = 1 << 20
    data = torch.randn(n)
    if torch.cuda.is_available():
        data = data.cuda()

    t0 = time.perf_counter()
    out = trigger_compiler(data)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    elapsed = (time.perf_counter() - t0) * 1000

    ok = torch.allclose(out, data * 2.0, rtol=1e-4, atol=1e-4)
    print(f"  Vector compiler: {n} elements | {elapsed:.2f} ms | correct={ok}")


def demo_osmotic() -> None:
    router = UtahOsmoticRouter()
    print(f"  Fluid pool: {router.compute_nodes}")

    jobs = []
    for _ in range(4):
        a = torch.randn(128, 128)
        b = torch.randn(128, 128)
        jobs.append((torch.matmul, (a, b), {}))

    t0 = time.perf_counter()
    results = router.route_tensors_parallel(jobs)
    elapsed = (time.perf_counter() - t0) * 1000

    print(f"  Osmotic parallel: {len(results)} matmuls in {elapsed:.2f} ms")
    for node in router.pressures():
        print(f"    {node.device}: pressure={node.pressure:.2f}")


def demo_photonic() -> None:
    bridge = PhotonicBridge(tx_pin=26, rx_pin=32)
    for byte in (0x55, 0xAA, 0x23):
        route_swarm_data(bridge, byte)
    print(f"  Photonic sim: {len(bridge._rx_buffer)} packets buffered")


def demo_zeo() -> None:
    engine = ZeoShieldEngine(verbose=False)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    n = 128
    A = torch.randn(n, n, device=device)
    B = torch.randn(n, n, device=device)

    t0 = time.perf_counter()
    out = engine.matmul_shielded(A, B)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    elapsed = (time.perf_counter() - t0) * 1000

    corrupted = engine.inject_bit_flip(out, 10, delta=1.0)
    healed = engine.heal(corrupted, out)
    corruption = (corrupted - out).abs().max().item()
    residual = (healed - out).abs().max().item()

    print(f"  ZEO matmul: {n}x{n} | {elapsed:.2f} ms")
    print(f"  Entropy shield: corruption={corruption:.4f} -> residual={residual:.4f}")


def demo_orchestrator() -> None:
    orch = UtahSiliconOrchestrator()
    layers = orch.run_llm_stress_demo(hidden=64, layers=3)
    print(f"  Silicon orchestrator: {len(layers)} pre-sighted layers")
    print(f"  Final activation shape: {layers[-1].shape}")


def demo_gaming() -> None:
    engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=320, height=180))
    boot = engine.bootstrap_gaming_enclave()
    for k, v in boot.items():
        print(f"  {k}: {v}")

    device = engine.device if engine.device != "cpu" else "cpu"
    h, w = 180, 320
    current = torch.rand(h, w, 4, device=device)
    history = torch.rand(h, w, 4, device=device)
    motion = torch.randn(h, w, 2, device=device) * 0.5

    t0 = time.perf_counter()
    frame = engine.reconstruct_frame(current, history, motion)
    elapsed = (time.perf_counter() - t0) * 1000

    latent = torch.randn(engine.holographic.latent_dim, device=device)
    upscaled = engine.perceptual_upscale_path(current[..., :3], latent)
    speculative = engine.speculative_render_cycle(current, (1.5, -0.5))

    weights = torch.randn(64, device=device)
    grad = torch.randn(64, device=device)
    engine.fractal.ring.push(1, grad)
    new_w = engine.distributed_weight_step(weights, grad, step=1)

    print(f"  Latency shield: {tuple(frame.shape)} in {elapsed:.2f} ms")
    print(f"  Perceptual upscale: {tuple(upscaled.shape)}")
    print(f"  Speculative frame: {tuple(speculative.shape)}")
    print(f"  Fractal step: weights {tuple(new_w.shape)}")


def demo_latency() -> None:
    demo_gaming()


def demo_all() -> None:
    _banner()
    print("\n[1/6] Kernel Ghosting Layer")
    demo_ghost()
    print("\n[2/6] Vector Compiler (BRTR)")
    demo_compiler()
    print("\n[3/6] Osmotic Tensor Router")
    demo_osmotic()
    print("\n[4/6] Photonic Matrix Bridge (sim)")
    demo_photonic()
    print("\n[5/6] ZEO-Shield Engine")
    demo_zeo()
    print("\n[6/6] Silicon-Transparency Orchestrator")
    demo_orchestrator()
    print("\n[BONUS] Asymptotic Reality Engine (Gaming)")
    demo_gaming()
    print("\n[UTAH-VIDIA] All subsystems nominal.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Utah-Vid-ia Universal Compute Bridge")
    parser.add_argument(
        "command",
        nargs="?",
        default="all",
        choices=["all", "ghost", "compiler", "osmotic", "photonic", "zeo", "orchestrator", "gaming", "latency", "bench"],
        help="Which subsystem demo to run",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(message)s",
    )

    if args.command == "bench":
        from benchmarks.benchmark_zeo_shield import run_benchmark

        _banner()
        run_benchmark([128, 256, 512], 10)
        return

    commands = {
        "all": demo_all,
        "ghost": lambda: (_banner(), demo_ghost()),
        "compiler": lambda: (_banner(), demo_compiler()),
        "osmotic": lambda: (_banner(), demo_osmotic()),
        "photonic": lambda: (_banner(), demo_photonic()),
        "zeo": lambda: (_banner(), demo_zeo()),
        "orchestrator": lambda: (_banner(), demo_orchestrator()),
        "gaming": lambda: (_banner(), demo_gaming()),
        "latency": lambda: (_banner(), demo_latency()),
    }
    commands[args.command]()


if __name__ == "__main__":
    main()
