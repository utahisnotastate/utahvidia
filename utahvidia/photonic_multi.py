"""
Photonic Multi-Silicon Bridge — peer-to-peer multi-GPU split-frame orchestration.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import torch

logger = logging.getLogger("utahvidia.photonic_multi")


@dataclass
class PhotonicMultiBridge:
    """
    Enables P2P peer access and split-frame dispatch across heterogeneous GPUs.
    """

    device_primary: int = 0
    device_secondary: int = 1
    peer_access_enabled: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if not torch.cuda.is_available() or torch.cuda.device_count() < 2:
            logger.info("[PHOTONIC BRIDGE] Single die detected. Monolithic mode.")
            return

        can_01 = torch.cuda.can_device_access_peer(self.device_primary, self.device_secondary)
        can_10 = torch.cuda.can_device_access_peer(self.device_secondary, self.device_primary)
        if can_01 and can_10:
            self.peer_access_enabled = True
            logger.info("[PHOTONIC BRIDGE] P2P interconnect available.")
        else:
            logger.warning("[PHOTONIC BRIDGE] P2P unavailable between devices.")

    def split_frame_matmul(
        self,
        a: torch.Tensor,
        b: torch.Tensor,
    ) -> torch.Tensor:
        """Split matrix work across two GPUs when P2P is available."""
        if not self.peer_access_enabled or a.device.type != "cuda":
            return torch.matmul(a, b)

        mid = a.size(0) // 2
        stream0 = torch.cuda.Stream(device=self.device_primary)
        stream1 = torch.cuda.Stream(device=self.device_secondary)

        a0, a1 = a[:mid].cuda(self.device_primary), a[mid:].cuda(self.device_secondary)
        b0, b1 = b[:mid].cuda(self.device_primary), b[mid:].cuda(self.device_secondary)

        with torch.cuda.device(self.device_primary), torch.cuda.stream(stream0):
            out0 = torch.matmul(a0, b0)
        with torch.cuda.device(self.device_secondary), torch.cuda.stream(stream1):
            out1 = torch.matmul(a1, b1)

        stream0.synchronize()
        stream1.synchronize()
        return torch.cat([out0.to(a.device), out1.to(a.device)], dim=0)
