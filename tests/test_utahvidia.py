import torch

from utahvidia import UtahOsmoticRouter, UtahVectorCompiler, UtahVidIaEngine, activate_ghost_layer
from utahvidia.compiler import trigger_compiler
from utahvidia.photonic_sim import PhotonicBridge, route_swarm_data


def test_engine_matmul():
    engine = UtahVidIaEngine(verbose=False)
    out = engine.matmul_demo(32, 32, 32)
    assert out.shape == (32, 32)


def test_ghost_layer_records_translation():
    with activate_ghost_layer(verbose=False) as ghost:
        x = torch.ones(4)
        y = torch.ones(4)
        ghost.wrap("add", torch.add)(x, y)
    assert len(ghost.history) >= 1
    assert "utah.mlir.add" in ghost.history[0].target_ir


def test_compiler_fallback_cpu():
    data = torch.randn(1024)
    out = trigger_compiler(data)
    assert torch.allclose(out, data * 2.0)


def test_osmotic_route_matmul():
    router = UtahOsmoticRouter()
    a = torch.randn(16, 16)
    b = torch.randn(16, 16)
    result = router.route_sync(torch.matmul, a, b)
    assert result.shape == (16, 16)


def test_photonic_sim():
    bridge = PhotonicBridge(tx_pin=1, rx_pin=2)
    route_swarm_data(bridge, 0x55)
    assert bridge._rx_buffer == [0x55]
