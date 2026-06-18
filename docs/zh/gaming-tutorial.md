# 玩家教程 — 免安装游戏解锁

**无需 Git、无需解锁文件、无需付费**即可运行完整的 Utah-Vid-ia 游戏技术栈。

**可选捐赠：** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## 最快路径：下载 `.exe`

1. 前往 [GitHub Releases](https://github.com/utahisnotastate/utahvidia/releases)
2. 下载 **`UtahVidia-Gaming.exe`**
3. 双击运行

你将看到：

```
UTAH-VIDIA GAMING UNLOCK
Full stack enabled — no install, no unlock file needed
[1/4] Boot gaming enclave...
[2/4] Latency shield frame reconstruction...
[3/4] Perceptual upscale + speculative intent...
[4/4] Fractal + holographic paths...
GAMING UNLOCK COMPLETE — all profiles active
```

按 Enter 关闭（运行打包 exe 时）。

还没有 Release？使用下方选项 2 或 3，或请维护者运行 [Build workflow](https://github.com/utahisnotastate/utahvidia/actions)。

---

## 选项 2 — ZIP + `.bat`（需要 Python，无需 Git）

1. 下载 [Source ZIP](https://github.com/utahisnotastate/utahvidia/archive/refs/heads/main.zip)
2. 解压到任意位置（例如 `Desktop\utahvidia-main`）
3. 双击 **`launchers\UtahVidia-Gaming.bat`**

从文件夹安装并运行完整解锁。

---

## 选项 3 — Python 一行命令

若已安装 Python 3.10+：

```bash
pip install git+https://github.com/utahisnotastate/utahvidia.git
utahvidia-gaming
```

---

## 解锁内容（全部免费）

| 功能 | 作用 |
|------|------|
| Latency shield | 通过运动感知重建实现更流畅的帧 |
| Profile `max` | 最佳默认调优（自动应用） |
| Perceptual upscale | 低分辨率基线到高分辨率演示路径 |
| Speculative intent | 根据预测输入运动预渲染 |
| Osmotic VRAM | 大型虚拟内存区域（模拟） |
| Photonic / fractal / holographic | 完整 Reality Engine 演示 |

可用配置文件：`competitive`、`cinematic`、`vr`、`max`、`vram`、`legend`

---

## 分步：调优 GPU（可选）

运行解锁一次后，创建 `my_game.py`：

```python
from utahvidia import UtahRealityEngine
from utahvidia.gaming_profiles import apply_gaming_profile
from utahvidia.latency_shield import DisplayHookConfig
import torch

W, H = 1920, 1080
engine = UtahRealityEngine(display_hook=DisplayHookConfig(width=W, height=H))
apply_gaming_profile(engine, "competitive")  # or cinematic, max, legend

device = "cuda" if torch.cuda.is_available() else "cpu"
current = torch.rand(H, W, 4, device=device)
history = torch.rand(H, W, 4, device=device)
motion = torch.randn(H, W, 2, device=device) * 0.3

frame = engine.reconstruct_frame(current, history, motion)
print("OK", frame.shape)
```

---

## 故障排除

| 问题 | 解决办法 |
|------|----------|
| Releases 页没有 `.exe` | 使用 `.bat` 或 `utahvidia-gaming`；维护者可触发 Actions workflow |
| 找不到 Python | 从 [python.org](https://python.org) 安装，或使用 `.exe` |
| exe 被 Windows 拦截 | 点击「更多信息」→「仍要运行」（未签名的开源构建） |
| 下载体积大 | exe 捆绑 PyTorch（约 200MB+）— 使用 `.bat` 路径下载更小 |
| AAA 游戏 FPS 无变化 | Utah-Vid-ia 是中间件 — 通过脚本集成；直接游戏钩子在路线图中 |

---

## 支持项目（可选）

永久免费。捐赠有助于硬件测试和翻译：

**PayPal：** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

---

## 延伸阅读

- [游戏中心](gaming-index.md)
- [游戏 FAQ](gaming-faq.md)
- [下载指南](../../launchers/README.md)

## 其他语言

[English](../en/gaming-tutorial.md) · [Eesti](../et/gaming-tutorial.md) · [Русский](../ru/gaming-tutorial.md) · [Suomi](../fi/gaming-tutorial.md) · [日本語](../ja/gaming-tutorial.md)

[返回文档索引](index.md)
