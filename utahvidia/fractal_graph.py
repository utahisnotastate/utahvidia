"""
Fractal Hyper-Graph — predictive distributed gradient assimilation (PyTorch).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import torch

logger = logging.getLogger("utahvidia.fractal_graph")

RING_BUFFER_SLOTS = 8


@dataclass
class GradientRingBuffer:
    """Lock-free ring buffer simulation for WAN gradient staging."""

    slots: int = RING_BUFFER_SLOTS
    gradients: list[torch.Tensor | None] = field(default_factory=list)
    momentum: list[torch.Tensor | None] = field(default_factory=list)
    sequence_ids: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.gradients = [None] * self.slots
        self.momentum = [None] * self.slots
        self.sequence_ids = [0] * self.slots

    def push(self, step: int, grad: torch.Tensor, mom: torch.Tensor | None = None) -> None:
        idx = step % self.slots
        self.gradients[idx] = grad.detach().clone()
        self.momentum[idx] = mom.detach().clone() if mom is not None else torch.zeros_like(grad)
        self.sequence_ids[idx] = step

    def get(self, step: int) -> tuple[torch.Tensor | None, torch.Tensor | None, bool]:
        idx = step % self.slots
        ready = self.sequence_ids[idx] == step
        return self.gradients[idx], self.momentum[idx], ready


@dataclass
class FractalHyperGraph:
    """
    Decentralized training step with predictive gradient branch when WAN lags.
    """

    learning_rate: float = 1e-3
    ring: GradientRingBuffer = field(default_factory=GradientRingBuffer)

    def local_step(
        self,
        weights: torch.Tensor,
        predicted_grad: torch.Tensor,
        global_step: int,
        *,
        remote_arrived: bool = False,
        remote_grad: torch.Tensor | None = None,
        remote_momentum: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if remote_arrived and remote_grad is not None:
            mom = remote_momentum if remote_momentum is not None else torch.zeros_like(remote_grad)
            delta = (remote_grad * 0.9) + (mom * 0.1)
        else:
            delta = predicted_grad * 0.5
        return weights - (self.learning_rate * delta)

    def assimilate(
        self,
        weights: torch.Tensor,
        predicted_grad: torch.Tensor,
        global_step: int,
    ) -> torch.Tensor:
        remote_grad, remote_mom, ready = self.ring.get(global_step)
        if ready and remote_grad is not None:
            return self.local_step(
                weights, predicted_grad, global_step,
                remote_arrived=True, remote_grad=remote_grad, remote_momentum=remote_mom,
            )
        return self.local_step(weights, predicted_grad, global_step, remote_arrived=False)
