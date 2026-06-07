"""
[SYSTEM: UTAH-VIDIA // VECTOR COMPILER]
[AUTHOR: GENERAL 23 // UTAH-1]
[PHYSICS: Binary Real-Time Rewriting (BRTR) of compute kernels]

Top-level entry point — delegates to the integrated package.
"""

from utahvidia.compiler import UtahVectorCompiler, trigger_compiler, utah_vector_kernel

__all__ = ["UtahVectorCompiler", "trigger_compiler", "utah_vector_kernel"]

if __name__ == "__main__":
    import torch

    data = torch.randn(1_048_576)
    if torch.cuda.is_available():
        data = data.cuda()

    out = trigger_compiler(data)
    print(f"[UTAH-VIDIA] Vector compile OK — in={data.shape}, out={out.shape}")
