"""
Utah-Vid-ia: Universal Compute Bridge.

Hardware-agnostic GPU middleware — kernel ghosting, vector compilation,
osmotic multi-GPU routing, ZEO-Shield, and Asymptotic Reality Engine.
"""

from utahvidia.core import GhostKernelLayer, UtahVidIaEngine, activate_ghost_layer
from utahvidia.compiler import UtahVectorCompiler, trigger_compiler
from utahvidia.osmotic import UtahOsmoticRouter
from utahvidia.orchestrator import UtahSiliconOrchestrator
from utahvidia.reality_engine import UtahRealityEngine
from utahvidia.latency_shield import LatencyShieldIntercept, reconstruct_frames
from utahvidia.zeo_shield import NeuralStatePrefetcher, ZeoShieldEngine, zeo_prefetched_matmul

from utahvidia.patron import apply_gaming_profile, is_patron_unlocked, patron_status

__all__ = [
    "GhostKernelLayer",
    "UtahVidIaEngine",
    "activate_ghost_layer",
    "UtahVectorCompiler",
    "trigger_compiler",
    "UtahOsmoticRouter",
    "NeuralStatePrefetcher",
    "ZeoShieldEngine",
    "zeo_prefetched_matmul",
    "UtahSiliconOrchestrator",
    "UtahRealityEngine",
    "LatencyShieldIntercept",
    "reconstruct_frames",
    "apply_gaming_profile",
    "is_patron_unlocked",
    "patron_status",
]
__version__ = "0.3.1"
