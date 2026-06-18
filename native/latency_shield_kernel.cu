/*
[SYSTEM: UTAH-VIDIA // LATENCY SHIELD RECONSTRUCTION KERNEL]
[PHYSICS: Driverless Asynchronous Frame Reconstruction]
*/

#include <cuda_runtime.h>

#define BLOCK_DIM_X 32
#define BLOCK_DIM_Y 8
#define SHARED_PADDING 1

__global__ void __launch_bounds__(256, 4)
utahvidia_reconstruction_kernel(
    const float4* __restrict__ g_current_frame,
    const float4* __restrict__ g_history_frame,
    const float2* __restrict__ g_motion_vectors,
    float4* __restrict__ g_output_frame,
    const int width,
    const int height,
    const float alpha)
{
    __shared__ float4 s_current[BLOCK_DIM_Y][BLOCK_DIM_X + SHARED_PADDING];
    __shared__ float4 s_history[BLOCK_DIM_Y][BLOCK_DIM_X + SHARED_PADDING];
    __shared__ float2 s_motion[BLOCK_DIM_Y][BLOCK_DIM_X + SHARED_PADDING];

    const int tx = threadIdx.x;
    const int ty = threadIdx.y;

    for (int global_y = blockIdx.y * blockDim.y + ty; global_y < height; global_y += gridDim.y * blockDim.y) {
        for (int global_x = blockIdx.x * blockDim.x + tx; global_x < width; global_x += gridDim.x * blockDim.x) {
            const int global_index = global_y * width + global_x;

            s_current[ty][tx] = g_current_frame[global_index];
            s_history[ty][tx] = g_history_frame[global_index];
            s_motion[ty][tx] = g_motion_vectors[global_index];
            __syncthreads();

            const float4 current_pixel = s_current[ty][tx];
            const float4 history_pixel = s_history[ty][tx];
            const float2 motion = s_motion[ty][tx];

            const float target_x = (float)global_x + motion.x;
            const float target_y = (float)global_y + motion.y;

            float4 synthesized_pixel;
            if (target_x >= 0.0f && target_x < (float)width && target_y >= 0.0f && target_y < (float)height) {
                synthesized_pixel.x = current_pixel.x * alpha + history_pixel.x * (1.0f - alpha);
                synthesized_pixel.y = current_pixel.y * alpha + history_pixel.y * (1.0f - alpha);
                synthesized_pixel.z = current_pixel.z * alpha + history_pixel.z * (1.0f - alpha);
                synthesized_pixel.w = 1.0f;
            } else {
                synthesized_pixel = current_pixel;
                synthesized_pixel.w = 1.0f;
            }

            g_output_frame[global_index] = synthesized_pixel;
            __syncthreads();
        }
    }
}

extern "C" void launch_utahvidia_shield(
    const float4* d_current_frame,
    const float4* d_history_frame,
    const float2* d_motion_vectors,
    float4* d_output_frame,
    const int width,
    const int height,
    const float alpha,
    cudaStream_t stream)
{
    dim3 block_layout(BLOCK_DIM_X, BLOCK_DIM_Y);
    dim3 grid_layout(
        (width + BLOCK_DIM_X - 1) / BLOCK_DIM_X,
        (height + BLOCK_DIM_Y - 1) / BLOCK_DIM_Y);
    utahvidia_reconstruction_kernel<<<grid_layout, block_layout, 0, stream>>>(
        d_current_frame, d_history_frame, d_motion_vectors, d_output_frame,
        width, height, alpha);
}
