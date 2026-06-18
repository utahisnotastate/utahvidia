# 玩家教程 — 从零到 GPU 解锁

完整 walkthrough：安装 Utah-Vid-ia、运行游戏技术栈、基准测试你的 GPU，并可选通过[赞助者计划](gpu-unlock-patron.md) **解锁 Pro 配置文件**。

**时间：** 约 30 分钟 · **费用：** $0（Pro 解锁可通过捐赠可选）

---

## 你将完成什么

1. 在 Windows、Linux 或 macOS 上安装 Utah-Vid-ia  
2. 运行 **渐近现实引擎** 游戏演示  
3. 理解延迟护盾 + 感知上采样在 **你的** GPU 上的作用  
4. 基准测试前后体感对比  
5. 可选通过 PayPal 捐赠 **永久解锁 Pro 游戏配置文件**  

---

## 前置条件

| 要求 | 说明 |
|-------------|-------|
| Python 3.10+ | `py --version` 或 `python3 --version` |
| pip | 包安装器 |
| Git | 从 GitHub 克隆 |
| GPU（可选） | NVIDIA CUDA 最佳；AMD/Intel 经 PyTorch；CPU = 演示模式 |

---

## 第 1 步 — 克隆与安装

```bash
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
pip install -e ".[dev]"
```

Windows PowerShell：

```powershell
git clone https://github.com/utahisnotastate/utahvidia.git
cd utahvidia
py -m pip install -e ".[dev]"
```

验证：

```bash
utahvidia --help
# or: py -m utahvidia.cli
```

---

## 第 2 步 — 运行第一个游戏演示

```bash
utahvidia gaming
```

预期输出（节选）：

```
UTAH-VIDIA // Universal Compute Bridge v0.3.0
microvisor: [MICROVISOR SIM] ...
Latency shield: (180, 320, 4) in X.XX ms
Perceptual upscale: (360, 640, 3)
Speculative frame: (180, 320, 4)
```

**发生了什么：**

- **延迟护盾** 用运动向量混合当前帧与历史帧（运动更顺滑）。  
- **感知上采样** 从低分辨率基线加倍分辨率（AI 风格路径演示）。  
- **推测意图** 根据类鼠标增量预渲染幻影帧。  

---

## 第 3 步 — 完整技术栈导览

```bash
utahvidia all
```

运行 ghost kernel、编译器、渗透路由器、光子模拟、ZEO-Shield、编排器，**以及** 游戏技术栈。

---

## 第 4 步 — 基准测试你的 GPU

```bash
utahvidia bench
```

保存输出 —— 对 GitHub Issue 和对比赞助者配置文件很有用。

带 NVCC 的 CUDA 系统上，原生内核可能在首次运行时 JIT 编译（多等几秒，仅一次）。

---

## 第 5 步 — Python：在本机调优帧

创建 `my_gaming_test.py`：

```python
import torch
from utahvidia import UtahRealityEngine
from utahvidia.latency_shield import DisplayHookConfig

# Match your monitor or game resolution
W, H = 1920, 1080
engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=W, height=H))

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")
print(engine.bootstrap_gaming_enclave())

current = torch.rand(H, W, 4, device=device)
history = torch.rand(H, W, 4, device=device)
motion = torch.randn(H, W, 2, device=device) * 0.3

frame = engine.reconstruct_frame(current, history, motion)
upscaled = engine.perceptual_upscale_path(current[..., :3])

print("Frame:", frame.shape, "Upscaled:", upscaled.shape)
```

运行：

```bash
python my_gaming_test.py
```

---

## 第 6 步 — 竞技 vs 电影配置文件（免费默认）

```python
from utahvidia.patron import apply_gaming_profile, list_profiles

print(list_profiles())  # competitive, cinematic, vr, patron_* if unlocked

engine = UtahRealityEngine()
apply_gaming_profile(engine, "competitive")  # lower alpha = snappier
# apply_gaming_profile(engine, "cinematic")  # smoother interpolation
```

| 配置文件 | 适合 | 延迟护盾 alpha |
|---------|----------|----------------------|
| `competitive` | 电竞、快鼠标 | 0.75（更灵敏） |
| `cinematic` | 单机、剧情 | 0.55（更顺滑） |
| `vr` | 头显 | 0.60 + 缩短推测视野 |

解锁后赞助者专属：`patron_max`、`patron_vram`、`patron_legend`。

---

## 第 7 步 — 解锁 Pro 游戏配置文件

1. 通过 PayPal 捐赠：[utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  
2. 备注/附言：**`GPU-UNLOCK`**  
3. 创建赞助者文件或设置环境变量 —— [完整说明](gpu-unlock-patron.md#激活你的解锁)  
4. 验证：

```bash
utahvidia patron
```

5. 应用 max 配置文件：

```python
from utahvidia import UtahRealityEngine
from utahvidia.patron import apply_gaming_profile, patron_status

print(patron_status())
engine = UtahRealityEngine()
apply_gaming_profile(engine, "patron_max")
```

**你已在该机器上永久解锁 Pro 预设**（文件或环境变量重启后仍有效）。

---

## 第 8 步 — 故障排除

| 问题 | 解决办法 |
|---------|-----|
| 找不到 `python`（Windows） | 改用 `py` |
| 未检测到 CUDA | 安装 [PyTorch + CUDA](https://pytorch.org)；CPU 模式仍可用 |
| 原生内核编译失败 | 使用 PyTorch 路径；API 中设 `use_native=False` |
| 赞助者未激活 | 检查 `~/.utahvidia/patron.unlock` 或 `UTAHVIDIA_PATRON=1` |
| 其他游戏 FPS 无变化 | Utah-Vid-ia 是中间件 —— 先通过教程脚本集成；完整游戏钩子在路线图中 |

---

## 第 9 步 — 分享与支持

- 为仓库点 Star：[github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)  
- 告诉朋友：捐赠 **GPU-UNLOCK** → Pro 配置文件  
- 主播：在简介中链接 [gpu-unlock-patron.md](gpu-unlock-patron.md)  

---

## 延伸阅读

- [GPU 解锁赞助者计划](gpu-unlock-patron.md)  
- [游戏 FAQ](gaming-faq.md)  
- [延迟护盾深入](latency-shield.md)  
- [儿童版 —— 为什么 GPU 重要](gaming-children.md)  

## 其他语言

[English](../en/gaming-tutorial.md) · [日本語](../ja/gaming-tutorial.md)

[返回游戏中心](gaming-index.md)
