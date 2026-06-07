import torch

from utahvidia import UtahSiliconOrchestrator, ZeoShieldEngine, zeo_prefetched_matmul
from utahvidia.zeo_shield import (
    NeuralStatePrefetcher,
    PrefetchJob,
    build_parity_lattice,
    entropy_shield_tensor,
)


def test_entropy_shield_heals_flip():
    base = torch.ones(8, 8)
    parity = build_parity_lattice(base)
    corrupted = base.clone()
    corrupted[2, 2] = 99.0
    healed = entropy_shield_tensor(corrupted, parity)
    assert healed[2, 2].item() != 99.0
    assert abs(healed[2, 2].item() - 1.0) < 50.0  # manifold blend toward parity


def test_zeo_prefetched_matmul_shape():
    A = torch.randn(32, 32)
    B = torch.randn(32, 32)
    out = zeo_prefetched_matmul(A, B, use_native=False)
    assert out.shape == (32, 32)
    assert torch.allclose(out, A * B, rtol=1e-5, atol=1e-5)


def test_zeo_heal_bit_flip():
    engine = ZeoShieldEngine(verbose=False)
    clean = torch.ones(16, 16)
    corrupted = engine.inject_bit_flip(clean, 5, delta=10.0)
    healed = engine.heal(corrupted, clean)
    assert (healed - clean).abs().max().item() < (corrupted - clean).abs().max().item()


def test_neural_prefetcher_queue():
    prefetcher = NeuralStatePrefetcher(max_queue=4)
    semantic = torch.randn(128)
    jobs = [
        PrefetchJob("a", torch.mul, (torch.ones(4), torch.ones(4)), {}),
        PrefetchJob("b", torch.add, (torch.ones(4), torch.ones(4)), {}),
    ]
    prefetcher.predict_from_embedding(semantic, jobs)
    assert len(prefetcher._queue) >= 1


def test_zeo_engine_pipeline():
    engine = ZeoShieldEngine(verbose=False)
    semantic = torch.randn(32)
    stages = [
        ("s0", torch.matmul, (torch.randn(16, 16), torch.randn(16, 16)), {}),
        ("s1", torch.matmul, (torch.randn(16, 16), torch.randn(16, 16)), {}),
    ]
    outputs = engine.run_pipeline(semantic, stages)
    assert len(outputs) == 2


def test_silicon_orchestrator():
    orch = UtahSiliconOrchestrator()
    A = torch.randn(16, 16)
    B = torch.randn(16, 16)
    out = orch.execute_shielded_matmul(A, B)
    assert out.shape == (16, 16)
