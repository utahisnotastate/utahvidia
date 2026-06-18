# 游戏 FAQ

## 一般问题

### Utah-Vid-ia 会取代我的 GPU 吗？

**不会。** 它让你现有的 GPU 更聪明地工作 —— 更好的帧节奏、可选的上采样路径、多 GPU 分帧、VRAM 虚拟化演示。物理仍然限制峰值性能。

### 安全吗？

安全。开源（MIT），pip 包中没有内核级 rootkit。Microvisor **仅为模拟**。赞助者解锁是本地配置文件 —— 无间谍软件。

### 能和我的游戏一起用吗？

v0.3 是 **中间件 + 演示**。今天可通过 Python/脚本集成。直接注入 AAA 游戏在路线图中（Driver API / 平台合作）。

---

## 赞助者 / 捐赠

### 捐赠后我能得到什么？

[Pro 游戏配置文件](gpu-unlock-patron.md)：`patron_max`、`patron_vram`、`patron_legend` —— 针对延迟护盾、推测意图与渗透式 VRAM 调优的预设。

### 最低捐赠金额？

任意金额，备注 **`GPU-UNLOCK`**。建议：$5 支持者、$15 爱好者、$50 传奇。

### 解锁真的是永久的吗？

是的 —— 保存在 `~/.utahvidia/patron.unlock` 或 `UTAHVIDIA_PATRON=1`。无订阅。一次捐赠，在你的电脑上永久保留（荣誉制度）。

### 可以退款吗？

适用 PayPal 标准退款政策。若预设对你的硬件无效，请通过 GitHub Issue 联系支持。

---

## 技术问题

### NVIDIA 还是 AMD 还是 Intel？

PyTorch 路径处处可用。原生 CUDA 内核（延迟护盾、ZEO）需要 NVIDIA + 可选 NVCC。

### 为什么在赛博朋克 / 堡垒之夜里还看不到更高 FPS？

这些游戏不会自动调用 Utah-Vid-ia。请先运行 `utahvidia gaming` 和自定义脚本。赞助者配置文件在你 **主动** 把帧送入引擎时生效。

### 什么是「感知上采样」？

内部低分辨率渲染，通过全息/张量路径合成细节 —— 与 DLSS/FSR 同类思路，Utah-Vid-ia 风格演示在 `UtahRealityEngine.perceptual_upscale_path`。

---

## 支持

- GitHub Issues：[utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia/issues)  
- 捐赠：[utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)  

## 其他语言

[English](../en/gaming-faq.md) · [日本語](../ja/gaming-faq.md)

[完整教程](gaming-tutorial.md) · [游戏中心](gaming-index.md)
