#include <torch/extension.h>
#include <cuda_runtime.h>

extern "C" void launch_utahvidia_shield(
    const float4* d_current_frame,
    const float4* d_history_frame,
    const float2* d_motion_vectors,
    float4* d_output_frame,
    const int width,
    const int height,
    const float alpha,
    cudaStream_t stream);

torch::Tensor utahvidia_reconstruct_frames_cuda(
    torch::Tensor current,
    torch::Tensor history,
    torch::Tensor motion,
    double alpha)
{
    TORCH_CHECK(current.is_cuda(), "current must be CUDA");
    TORCH_CHECK(history.sizes() == current.sizes(), "history shape mismatch");
    TORCH_CHECK(motion.dim() == 3 && motion.size(2) == 2, "motion must be HxWx2");

    const int height = static_cast<int>(current.size(0));
    const int width = static_cast<int>(current.size(1));

    auto current_f = current.contiguous().to(torch::kFloat32);
    auto history_f = history.contiguous().to(torch::kFloat32);
    auto motion_f = motion.contiguous().to(torch::kFloat32);
    auto output = torch::empty_like(current_f);

    cudaStream_t stream = at::cuda::getCurrentCUDAStream();
    launch_utahvidia_shield(
        reinterpret_cast<const float4*>(current_f.data_ptr<float>()),
        reinterpret_cast<const float4*>(history_f.data_ptr<float>()),
        reinterpret_cast<const float2*>(motion_f.data_ptr<float>()),
        reinterpret_cast<float4*>(output.data_ptr<float>()),
        width,
        height,
        static_cast<float>(alpha),
        stream);
    return output;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("reconstruct_frames_cuda", &utahvidia_reconstruct_frames_cuda, "Latency shield frame reconstruction");
}
