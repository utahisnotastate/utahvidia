"""
[SYSTEM: UTAH-VIDIA // OSMOTIC TENSOR ROUTER]
[PHYSICS: Asynchronous Load-Balancing & Constraint-Based Execution]
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable

import torch

logger = logging.getLogger("utahvidia.osmotic")


@dataclass
class ExecutionConstraints:
    """Constraint envelope for autonomic silicon routing."""

    max_latency_ms: float | None = None
    max_power_watts: float | None = None


@dataclass
class NodePressure:
    """Per-device load snapshot."""

    device: str
    pressure: float
    last_used: float = field(default_factory=time.monotonic)


class UtahOsmoticRouter:
    """
    Dynamic batching middleware: routes tensor ops to the lowest-pressure node.

    Makes a rack of GPUs behave like a single fluid compute pool.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self.compute_nodes = self._discover_nodes()
        self.node_load: dict[str, float] = {node: 0.0 for node in self.compute_nodes}
        self._history: list[tuple[str, str]] = []

    @staticmethod
    def _discover_nodes() -> list[str]:
        if torch.cuda.is_available():
            return [f"cuda:{i}" for i in range(torch.cuda.device_count())]
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return ["mps"]
        return ["cpu"]

    def pressures(self) -> list[NodePressure]:
        with self._lock:
            return [
                NodePressure(device=node, pressure=load)
                for node, load in self.node_load.items()
            ]

    def _select_node(self) -> str:
        with self._lock:
            return min(self.node_load, key=self.node_load.get)

    def _bump_load(self, node: str, delta: float) -> None:
        with self._lock:
            self.node_load[node] = max(0.0, self.node_load[node] + delta)

    def route_sync(
        self,
        tensor_op: Callable[..., Any],
        *args: Any,
        load_weight: float = 0.1,
        constraints: ExecutionConstraints | None = None,
        **kwargs: Any,
    ) -> Any:
        """Synchronously route *tensor_op* to the lowest-pressure compute node."""
        target = self._select_node()
        logger.info("[UTAH-VIDIA] Osmotic Routing: Flowing task to %s", target)
        self._history.append((tensor_op.__name__, target))

        started = time.perf_counter()
        self._bump_load(target, load_weight)
        try:
            if target.startswith("cuda"):
                device_index = int(target.split(":")[1])
                with torch.cuda.device(device_index):
                    result = tensor_op(*args, **kwargs)
            elif target == "mps":
                result = tensor_op(*args, **kwargs)
            else:
                result = tensor_op(*args, **kwargs)
        finally:
            self._bump_load(target, -load_weight)

        elapsed_ms = (time.perf_counter() - started) * 1000
        if constraints and constraints.max_latency_ms is not None:
            if elapsed_ms > constraints.max_latency_ms:
                logger.warning(
                    "[UTAH-VIDIA] Constraint breach: %.2f ms > %.2f ms on %s",
                    elapsed_ms,
                    constraints.max_latency_ms,
                    target,
                )
        return result

    async def route_tensor(
        self,
        tensor_op: Callable[..., Any],
        *args: Any,
        load_weight: float = 0.1,
        **kwargs: Any,
    ) -> Any:
        """Async wrapper around :meth:`route_sync` for asyncio orchestrators."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.route_sync(tensor_op, *args, load_weight=load_weight, **kwargs),
        )

    def route_tensors_parallel(
        self,
        jobs: list[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]],
    ) -> list[Any]:
        """Route a batch of independent tensor jobs across the fluid pool."""

        async def _run_all() -> list[Any]:
            tasks = [
                self.route_tensor(op, *args, **kwargs)
                for op, args, kwargs in jobs
            ]
            return list(await asyncio.gather(*tasks))

        return asyncio.run(_run_all())
