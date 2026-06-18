# GPU アンロック パトロン・プログラム

**GPU の潜在能力を解放 —— Utah-Vid-ia を支援し、今あるハードウェアを長く活かす。**

Utah-Vid-ia コアは **無料のオープンソース（MIT）** です。**GPU アンロック パトロン・プログラム** は寄付したゲーマーに **Pro ゲーミングプロファイル** へのアクセスを提供します: すでに持っているシリコンから最大の滑らかさ、VRAM 効率、フレームペーシングを引き出す調整済みプリセットです。

## PayPal（永久アンロック）

**寄付:** [utah@utahcreates.com](https://www.paypal.com/donate/?business=utah%40utahcreates.com)

PayPal のメモ/備考に **`GPU-UNLOCK`** と GitHub またはメール（任意、お礼用）を記載してください。

寄付後、アンロックを有効化 —— [チュートリアル ステップ 7](gaming-tutorial.md#ステップ-7--pro-ゲーミングプロファイルをアンロック) を参照。

---

## 「永久アンロック」の意味

| 無料（全員） | パトロンアンロック |
|-----------------|---------------|
| 完全なオープンソーススタック | 無料枠のすべて |
| レイテンシーシールドデモ | **Pro レイテンシープロファイル**（競技 / シネマティック / VR） |
| 基本ゲーム CLI | **パトロンバナー + アンロック状態** |
| コミュニティサポート | GitHub 優先 issue タグ（PayPal 領収書を issue に添付） |
| — | **VRAM オスモティック アグレッシブプリセット**（より大きな仮想アリーナ） |
| — | **推測インテント ホライズン ×2**（速いマウスでより滑らかな感覚） |
| — | **新ゲーミングカーネルへの早期アクセス** |

**重要:** パトロンアンロックは **ソフトウェア設定 + プリセット** —— 魔法のシリコンではありません。GPU には物理的な限界があります。ドライバの肥大と見えないディテールへの無駄なサイクルを止めるお手伝いをします。

---

## 推奨ティア（名誉制度）

| ティア | 推奨金額 | 得られるもの |
|------|------------------|---------|
| **サポーター** | $5+ | Pro プロファイル + パトロン状態 |
| **エンスージアスト** | $15+ | 上記 + [PATRONS.md](../../PATRONS.md) への名前（PayPal メモでオプトイン） |
| **レジェンド** | $50+ | 上記 + リリース `@patron` タグ付き早期 beta ビルド |

寄付メモに **`GPU-UNLOCK`** を含めれば、金額は問わず Pro プロファイルがアンロックされます。

---

## アンロックを有効化する

### オプション A — 環境変数（クイック）

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

### オプション B — パトロンファイル（推奨）

寄付後、以下を作成:

**Windows:** `%USERPROFILE%\.utahvidia\patron.unlock`  
**Linux/macOS:** `~/.utahvidia/patron.unlock`

```powershell
mkdir $env:USERPROFILE\.utahvidia -Force
"GPU-UNLOCK" | Out-File $env:USERPROFILE\.utahvidia\patron.unlock -Encoding utf8
```

```bash
mkdir -p ~/.utahvidia
echo "GPU-UNLOCK" > ~/.utahvidia/patron.unlock
```

任意: 2 行目に PayPal 取引 ID を追加してサポート検証に使えます。

### 確認

```bash
utahvidia patron
```

`Patron unlock: ACTIVE` と利用可能な Pro プロファイルが表示されるはずです。

---

## クリエイター & 配信者向け

視聴者に伝えてよい内容:

> 「PayPal で Utah-Vid-ia に寄付（**utah@utahcreates.com**、メモ **GPU-UNLOCK**）すると、あなたの GPU 向けに Utah-Vid-ia を調整した Pro ゲーミングプロファイルが永久アンロック —— 新しいハードウェアを買わずにより FPS を感じられます。」

リンク: [github.com/utahisnotastate/utahvidia](https://github.com/utahisnotastate/utahvidia)

アフィリエイト: 正式なアフィリエイトプログラムはまだありません。説明欄に寄付リンク + チュートリアルを使い、PATRONS.md にオプトインしてクレジットを得てください。

---

## 返金と誠実さ

- 寄付は任意で、PayPal 標準ポリシーにより返金不可。
- Pro プロファイルがシステムで役立たない場合は `utahvidia bench` 出力付きで [issue を報告](https://github.com/utahisnotastate/utahvidia/issues) —— 全員向けにプリセットを改善します。

## 他の言語

[English](../en/gpu-unlock-patron.md) · [中文](../zh/gpu-unlock-patron.md)

[完全ゲーマーチュートリアル](gaming-tutorial.md) · [寄付の一般情報](donate.md) · [ゲームハブに戻る](gaming-index.md)
