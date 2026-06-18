"""Shared native extension loader for Utah-Vid-ia CUDA modules."""

from __future__ import annotations

import threading
from pathlib import Path

import torch

_CACHE: dict[str, object] = {}
_LOCK = threading.Lock()


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_cuda_extension(name: str, sources: list[str]):
    with _LOCK:
        if name in _CACHE:
            return _CACHE[name]
        if not torch.cuda.is_available():
            return None
        try:
            from torch.utils.cpp_extension import load

            root = project_root()
            mod = load(
                name=name,
                sources=[str(root / s) for s in sources],
                extra_cuda_cflags=["-O3"],
                verbose=False,
            )
            _CACHE[name] = mod
            return mod
        except Exception:
            return None
