#include <torch/extension.h>
#include <cuda_runtime.h>

extern "C" void launch_zeo_kernel(
    float* d_A,
    float* d_B,
    float* d_C,
    float* d_parity,
    int N,
    cudaStream_t stream
);

torch::Tensor zeo_shield_matmul_cuda(
    torch::Tensor A,
    torch::Tensor B,
    c10::optional<torch::Tensor> parity
) {
    TORCH_CHECK(A.is_cuda(), "A must be a CUDA tensor");
    TORCH_CHECK(B.is_cuda(), "B must be a CUDA tensor");
    TORCH_CHECK(A.dtype() == torch::kFloat32, "only float32 supported");
    TORCH_CHECK(B.dtype() == torch::kFloat32, "only float32 supported");
    TORCH_CHECK(A.dim() == 2 && B.dim() == 2, "inputs must be 2D");
    TORCH_CHECK(A.size(0) == A.size(1), "matrix must be square");
    TORCH_CHECK(A.sizes() == B.sizes(), "A and B must match shape");

    const int N = static_cast<int>(A.size(0));
    auto C = torch::empty_like(A);
    float* d_parity = nullptr;
    if (parity.has_value()) {
        TORCH_CHECK(parity->is_cuda(), "parity must be CUDA");
        d_parity = parity->data_ptr<float>();
    }

    cudaStream_t stream = at::cuda::getCurrentCUDAStream();
    launch_zeo_kernel(
        A.data_ptr<float>(),
        B.data_ptr<float>(),
        C.data_ptr<float>(),
        d_parity,
        N,
        stream
    );
    return C;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("zeo_shield_matmul_cuda", &zeo_shield_matmul_cuda, "ZEO-Shield prefetched matmul");
}
