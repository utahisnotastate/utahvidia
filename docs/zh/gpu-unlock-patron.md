# GPU 解锁赞助者计划

**解锁 GPU 全部潜力 —— 支持 Utah-Vid-ia，让现有硬件更长久地有用。**

Utah-Vid-ia 核心是 **免费开源（MIT）**。**GPU 解锁赞助者计划** 让捐赠的玩家获得 **Pro 游戏配置文件**：调优预设，从你已有的硅片中榨出最大流畅度、VRAM 效率与帧节奏。

## PayPal（永久解锁）

**捐赠：** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

在 PayPal 备注/附言中写上：**`GPU-UNLOCK`** 以及你的 GitHub 或邮箱（可选，用于致谢）。

捐赠后激活解锁 —— 见[教程第 7 步](gaming-tutorial.md#step-7--unlock-pro-gaming-profiles)。

---

## 「永久解锁」是什么意思

| 免费（所有人） | 赞助者解锁 |
|-----------------|---------------|
| 完整开源技术栈 | 免费档全部内容 |
| 延迟护盾演示 | **Pro 延迟配置**（竞技 / 电影 / VR） |
| 基础游戏 CLI | **赞助者横幅 + 解锁状态** |
| 社区支持 | GitHub 优先 Issue 标签（附上 PayPal 收据） |
| — | **VRAM 渗透激进预设**（更大虚拟竞技场） |
| — | **推测意图视野 ×2**（快鼠标更顺滑） |
| — | **新游戏内核抢先体验** |

**重要：** 赞助者解锁是 **软件配置 + 预设** —— 不是魔法硅片。你的 GPU 仍有物理极限。我们帮你停止在驱动臃肿和看不见的细节上浪费周期。

---

## 建议档位（荣誉制度）

| 档位 | 建议金额 | 你得到 |
|------|------------------|---------|
| **支持者** | $5+ | Pro 配置文件 + 赞助者状态 |
| **爱好者** | $15+ | 以上 + [PATRONS.md](../../PATRONS.md) 署名（PayPal 备注选择加入） |
| **传奇** | $50+ | 以上 + 发布版 `@patron` 抢先 beta 构建 |

任意金额均可解锁 Pro 配置文件，只要在捐赠备注中包含 **`GPU-UNLOCK`**。

---

## 激活你的解锁

### 方案 A — 环境变量（快速）

```powershell
# Windows PowerShell (current session)
$env:UTAHVIDIA_PATRON = "1"

# Permanent (user)
[System.Environment]::SetEnvironmentVariable("UTAHVIDIA_PATRON", "1", "User")
```

```bash
# Linux / macOS
export UTAHVIDIA_PATRON=1
echo 'export UTAHVIDIA_PATRON=1' >> ~/.bashrc
```

### 方案 B — 赞助者文件（推荐）

捐赠后创建：

**Windows：** `%USERPROFILE%\.utahvidia\patron.unlock`  
**Linux/macOS：** `~/.utahvidia/patron.unlock`

```powershell
mkdir $env:USERPROFILE\.utahvidia -Force
"GPU-UNLOCK" | Out-File $env:USERPROFILE\.utahvidia\patron.unlock -Encoding utf8
```

```bash
mkdir -p ~/.utahvidia
echo "GPU-UNLOCK" > ~/.utahvidia/patron.unlock
```

可选：第二行写上 PayPal 交易 ID，便于支持验证。

### 验证

```bash
utahvidia patron
```

应看到：`Patron unlock: ACTIVE` 以及可用的 Pro 配置文件。

---

## 面向创作者与主播

你可以告诉观众：

> 「通过 PayPal 捐赠 Utah-Vid-ia（**utah@utahcreates.com**，备注 **GPU-UNLOCK**），永久解锁 Pro 游戏配置文件，针对你的 GPU 调优 Utah-Vid-ia —— 不买新硬件也能更有 FPS 感。」

链接：[github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)

联盟说明：我们尚未运行正式联盟计划。在简介中使用捐赠链接 + 教程；选择加入 PATRONS.md 获得署名。

---

## 退款与诚信

- 捐赠为自愿，按 PayPal 标准政策不可退款。
- 若 Pro 配置文件对你的系统无效，请[提交 Issue](https://github.com/utahisnotastate/utahvidia/issues) 并附上 `utahvidia bench` 输出 —— 我们会为所有人改进预设。

## 其他语言

[English](../en/gpu-unlock-patron.md) · [日本語](../ja/gpu-unlock-patron.md)

[完整玩家教程](gaming-tutorial.md) · [捐赠总览](donate.md) · [返回游戏中心](gaming-index.md)
