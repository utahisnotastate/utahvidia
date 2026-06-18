# 游戏 FAQ

## 下载与运行

### 如何在不使用 Git 的情况下运行？

从 [Releases](https://github.com/utahisnotastate/utahvidia/releases) 下载 **`UtahVidia-Gaming.exe`**，或从 [ZIP 下载](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip) 使用 `launchers/UtahVidia-Gaming.bat`。

参见 [gaming-tutorial.md](gaming-tutorial.md)。

### 是否有功能需要付费解锁？

**没有。** 所有游戏配置文件和功能均免费。可通过 [PayPal](https://www.paypal.com/donate/?business=utah%40utahcreates.com) 可选捐赠。

### 为什么 exe 这么大？

它捆绑了 Python 和 PyTorch（约 200MB+）。若已安装 Python，可使用 `.bat` 启动器。

---

## 一般问题

### Utah-Vid-ia 会取代我的 GPU 吗？

不会 — 它帮助现有 GPU 更智能地运行。物理仍然限制性能上限。

### 安全吗？

安全。开源（MIT）。无付费墙文件。pip 包中的 Microvisor 仅为模拟。

### 能否自动在我的游戏中运行？

v0.4 是中间件 + 一键解锁演示。直接 AAA 游戏集成在路线图中。

---

## 捐赠

### 需要捐赠吗？

不需要。Utah-Vid-ia 免费。

### 如何捐赠？

[通过 PayPal 捐赠 utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com) — 任意金额都有助于基准测试和文档。

---

## 技术问题

### NVIDIA 还是 AMD？

PyTorch 通用。原生 CUDA 内核需要 NVIDIA + 可选 NVCC。

## 其他语言

[English](../en/gaming-faq.md) · [Eesti](../et/gaming-faq.md) · [Русский](../ru/gaming-faq.md) · [Suomi](../fi/gaming-faq.md) · [日本語](../ja/gaming-faq.md)

[完整教程](gaming-tutorial.md) · [游戏中心](gaming-index.md)
