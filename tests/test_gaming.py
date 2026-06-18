import torch

from utahvidia import UtahRealityEngine
from utahvidia.latency_shield import reconstruct_frames
from utahvidia.fractal_graph import FractalHyperGraph
from utahvidia.holographic import HolographicTensorCore
from utahvidia.speculative_intent import IntentTelemetry, SpeculativeIntentEngine


def test_reconstruct_frames_cpu():
    h, w = 64, 64
    cur = torch.rand(h, w, 4)
    hist = torch.rand(h, w, 4)
    motion = torch.zeros(h, w, 2)
    out = reconstruct_frames(cur, hist, motion, use_native=False)
    assert out.shape == (h, w, 4)


def test_reality_engine_bootstrap():
    engine = UtahRealityEngine()
    boot = engine.bootstrap_gaming_enclave()
    assert "microvisor" in boot


def test_holographic_footprint():
    core = HolographicTensorCore(latent_dim=64)
    assert core.memory_footprint_bytes() == 256


def test_fractal_assimilate():
    graph = FractalHyperGraph()
    w = torch.ones(8)
    g = torch.full((8,), 0.2)
    out = graph.assimilate(w, g, global_step=0)
    assert out.shape == (8,)


def test_speculative_intent():
    engine = SpeculativeIntentEngine()
    frame = torch.rand(32, 32, 4)
    intent = IntentTelemetry(delta_x=1.0, delta_y=0.5)
    phantoms = engine.render_phantoms(frame, intent)
    assert len(phantoms) == 3
    collapsed = engine.collapse(intent, intent)
    assert collapsed is not None


def test_gaming_profiles_free():
    from utahvidia.gaming_profiles import apply_gaming_profile, list_profiles

    assert "legend" in list_profiles()
    engine = UtahRealityEngine()
    cfg = apply_gaming_profile(engine, "legend")
    assert cfg["virtual_gigabytes"] == 512


def test_gaming_launcher_runs():
    from utahvidia.gaming_launcher import run_gaming_unlock

    assert run_gaming_unlock(width=32, height=32) == 0
