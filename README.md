# supɃewhY-P13N

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/supbewhy-sudo/supbewhy-p13n/releases)
[![Tests](https://img.shields.io/badge/tests-16%20passing-brightgreen.svg)](#验证状态)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **别再每次都重教 AI 了** — P13N 让 ChatGPT 和 Codex 永久记住你的工作习惯。

[English](README_EN.md) | [中文](README.md)

**P13N** 是智能个性化配置 Skill，根据你的真实工作推荐配置位置，任何修改都先预览。

🎯 **核心差异**：不是把所有规则塞进一段 Prompt，而是帮你放到合适的配置层。

---

## 目录

- [一句话](#一句话)
- [为什么需要 P13N](#为什么需要-p13n)
- [核心特性](#核心特性)
- [快速开始](#快速开始)
- [使用场景](#使用场景)
- [配置位置说明](#配置位置说明)
- [安装](#安装)
- [权限与迁移](#权限与迁移)
- [验证状态](#验证状态)
- [FAQ](#faq)
- [贡献指南](#贡献指南)
- [许可证](#许可证)
- [关于作者](#关于作者)

---

## 一句话

P13N 是智能个性化配置 Skill。它根据你的真实工作推荐配置位置（Custom Instructions、Projects、AGENTS.md、MEMORY.md、Skill），任何修改都先预览，确认后才执行。

**关键特性**：
- ✅ 不用学配置语法 — 问你 3-5 个问题就能配好
- ✅ 不会搞乱旧配置 — 先预览，确认后才修改
- ✅ 换设备能迁移 — 导出脱敏包，新设备导入
- ✅ 根据工作推荐 — 只配当前用得到的，不硬塞

**与手动配置的差异**：

| 手动配置 | 使用 P13N |
|---------|----------|
| 需要学 Custom Instructions、AGENTS.md 语法 | 回答问题就能配好 |
| 不知道该放哪个配置位置 | 根据工作类型自动推荐 |
| 修改前心里没底 | 先预览，看清楚再确认 |
| 换设备重来一遍 | 导出迁移包，一键导入 |

`P13N` 是 Personalization（个性化）的缩写。

> 这是个人维护的公开项目，与 OpenAI 官方无关。

---

## 为什么需要 P13N

### 你可能遇到这些问题

| 痛点 | P13N 的解决方式 |
|------|---------------|
| 每次开新对话都要重新解释背景和输出要求 | 把长期习惯放到 Custom Instructions 或全局 AGENTS.md |
| AI 该直接做的时候一直追问，该谨慎的时候却自作主张 | 配置明确的授权边界和确认规则 |
| 个性化规则越写越多，最后互相打架 | 检查冲突、重复和错位，先预览再整理 |
| 项目做了很久，之前确认过的决策还是会被忘掉 | 用项目 MEMORY.md 记录决策、踩坑和纠正 |
| 同一套 Prompt 复制了很多遍，却没变成稳定流程 | 识别重复工作，建议做成 Skill |

### 核心理念

P13N 不是把所有规则塞进一段 Prompt，而是：

1. **按工作类型分层**：长期习惯 → 全局；项目规则 → 项目；重复流程 → Skill
2. **只配当前用得到的**：不用 Projects 就不配；不做本地项目就不需要 AGENTS.md
3. **先预览后修改**：任何写入都先给预览，确认后才执行
4. **可迁移**：换设备时导出脱敏包，新设备一键导入

---

## 核心特性

### ✅ 不用学配置语法

**你不需要先学习**：
- Custom Instructions 怎么写
- AGENTS.md 的格式
- MEMORY.md 的规则

**P13N 会从你的真实工作开始问**：
- 你主要用 AI 做什么？
- 最常重复的工作有哪些？
- 目前哪些 AI 行为最浪费时间？
- 你希望它怎么处理模糊需求？

问完后给出配置预览，确认后自动写入。

---

### ✅ 不会搞乱旧配置

**放心，旧配置不会被直接清空。**

P13N 会：
- 找出重复规则
- 检测互相冲突的要求
- 识别放错位置的项目内容
- 标记已经不用的旧流程

**任何修改都先给预览**，确认后才会执行。

替换本地配置前会自动备份。

---

### ✅ 换设备能迁移

**分两步操作**：

1. **在旧设备导出脱敏包**：删除密码、Token、聊天记录
2. **在新设备导入**：预览并确认后恢复配置

**迁移包包含**：
- Custom Instructions 内容
- 全局和项目 AGENTS.md
- 项目 MEMORY.md
- 自定义 Skill

**不包含**：
- 聊天记录
- 密码、Token、登录状态
- 日志、缓存、数据库

---

### ✅ 根据工作推荐

P13N 会根据你的工作类型推荐配置位置。

**只配当前用得到的**，不会硬塞所有选项。

| 你的工作方式 | P13N 会推荐 |
|------------|-----------|
| 只用 ChatGPT 写文章 | Custom Instructions |
| 用 ChatGPT 做某个领域工作 | Custom Instructions + Projects |
| 用 Codex 改本地项目 | 全局 AGENTS.md + 项目 AGENTS.md |
| 长期项目需要记决策 | + MEMORY.md |
| 有固定重复工作 | + Skill |

---

## 快速开始

> 5 分钟完成首次配置

### 前置要求

- Codex 已安装（需要 Codex Skills 支持）
- 基础使用过 ChatGPT 或 Codex

### 3 步开始

**1. 安装 P13N**

```bash
git clone https://github.com/supbewhy-sudo/supbewhy-p13n.git
cd supbewhy-p13n
cp -R ./supbewhy-p13n "${CODEX_HOME:-$HOME/.codex}/skills/"
```

**2. 重启 Codex**

**3. 发送配置指令**

```text
使用 $supbewhy-p13n 帮我配置 ChatGPT 和 Codex 个性化。
我没有配置过，请从最小问诊开始，先不要扫描电脑。
```

P13N 会问你 3-5 个问题，然后给出配置预览。确认后自动写入。

**🎉 完成！** 现在 AI 会记住你的工作习惯了。

---

**已经有配置？** 跳到 [整理已有配置](#场景-2已有配置需要整理)

---

## 使用场景

### 场景 1：从未配置过（推荐新用户）

**不用先学这些名词**：
- Custom Instructions
- AGENTS.md
- MEMORY.md

**P13N 会从你的真实工作开始问**：

<details>
<summary>📋 点击查看完整问题清单</summary>

- 你主要使用 ChatGPT、Work、Codex，还是本地项目？
- 最常重复的工作有哪些，最后想拿到什么成品？
- 目前哪些 AI 行为最让你浪费时间？
- 你希望它怎么处理语言、篇幅、分歧和模糊需求？
- 什么操作可以直接执行，什么操作必须先确认？
- 有没有需要长期保留背景和决策的项目？

</details>

**问完后给出配置预览**，确认后自动写入。

**示例交互**：

![新用户交互界面](docs/images/fresh-start.png)

**开始指令**：

```text
使用 $supbewhy-p13n 帮我配置 ChatGPT 和 Codex 个性化。
我没有配置过，请从最小问诊开始，先不要扫描电脑。
```

---

### 场景 2：已有配置，需要整理

**放心，旧配置不会被直接清空。**

P13N 会：
- ✅ 找出重复规则
- ✅ 检测互相冲突的要求
- ✅ 识别放错位置的项目内容
- ✅ 标记已经不用的旧流程

**你可以选择**：
- 尽量保留有用习惯
- 整理并优化
- 从头重新设计

**必须修改的内容先给预览**，确认后才会执行。

**示例交互**：

![已有配置用户交互界面](docs/images/revise-existing.png)

**开始指令**：

```text
使用 $supbewhy-p13n 审查我现有的 Custom Instructions 和 AGENTS.md。
保留有用习惯并整理，先给我预览，不要直接修改。
```

---

### 场景 3：换新设备，迁移配置

**分两步操作**：

**步骤 1：在旧设备导出**

```text
使用 $supbewhy-p13n 盘点这台电脑上可以安全迁移的 Codex 个性化。
先给我看迁移预览，等我确认后再导出脱敏迁移包。
不要复制凭据、聊天记录和缓存。
```

**步骤 2：在新设备导入**

把导出的 ZIP 通过可信方式带到新设备，安装 P13N 后：

```text
使用 $supbewhy-p13n 预览这个迁移包：<文件路径>。
先检查文件校验、目标位置和配置冲突，等我确认后再导入。
```

**迁移范围**：
- ✅ Custom Instructions 内容
- ✅ 全局和项目 AGENTS.md
- ✅ 项目 MEMORY.md
- ✅ 自定义 Skill
- ❌ 聊天记录
- ❌ 密码、Token、登录状态
- ❌ 日志、缓存、数据库

---

## 配置位置说明

P13N 会根据你的工作类型推荐配置位置。**只配当前用得到的**，不会硬塞所有选项。

### 配置映射表

| 配置位置 | 适用场景 | 放什么内容 |
|---------|---------|-----------|
| **Custom Instructions** | 所有 ChatGPT 用户 | 语言、篇幅、语气、长期沟通习惯 |
| **ChatGPT Projects** | 有长期领域工作的 ChatGPT 用户 | 某个领域的背景、文件、项目要求 |
| **全局 AGENTS.md** | 使用 Codex 的所有本地项目 | 跨项目的协作方式、通用规范 |
| **项目 AGENTS.md** | 单个本地项目 | 当前项目的命令、目录规范、验证方法 |
| **项目 MEMORY.md** | 需要记录决策的长期项目 | 已确认的决策、踩坑记录、用户纠正 |
| **Skill** | 有固定重复工作的用户 | 输入、输出、步骤都稳定的流程 |
| **Hook / Rule** | 需要自动检查的场景 | 必须检查或禁止的操作 |

### 重要说明

- **`MEMORY.md` 不是自动记忆**：需要在项目 `AGENTS.md` 中明确要求读取和维护
- **ChatGPT 账号设置**：如果不能自动完成，P13N 会整理好内容并告诉你去哪里粘贴
- **不是所有人都需要全部配置**：只用 ChatGPT 写文章的人，可能只需要 Custom Instructions 和一个 Project

### 配置后的区别

**配置前**：
```
你：帮我优化这段代码
AI：好的，我需要了解...
你：（每次都要重新解释背景、风格、输出要求）
```

**配置后**：
```
你：帮我优化这段代码
AI：（自动按你的习惯输出：简洁、带注释、保持现有风格）
```

---

## 安装

### 方式 1：Git Clone（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/supbewhy-sudo/supbewhy-p13n.git
cd supbewhy-p13n

# 2. 复制到 Codex Skills 目录
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$CODEX_SKILLS_DIR"
cp -R ./supbewhy-p13n "$CODEX_SKILLS_DIR/"

# 3. 验证安装
ls "$CODEX_SKILLS_DIR/supbewhy-p13n/SKILL.md"
```

### 方式 2：下载 ZIP

1. 下载 [`dist/supbewhy-p13n.zip`](dist/supbewhy-p13n.zip)
2. 解压后把 `supbewhy-p13n/` 目录复制到 `${CODEX_HOME:-$HOME/.codex}/skills/`

### 重要说明

- ⚠️ **安装包不包含你的个人配置**
- ⚠️ 安装完成后需要**重启 Codex** 或打开新任务
- ✅ 支持多用户：每个用户的配置独立存储

### 卸载

```bash
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/supbewhy-p13n"
```

**注意**：卸载 P13N 不会删除已经配置好的 Custom Instructions 或 AGENTS.md。

---

## 权限与迁移

### 权限模式

P13N 把不同操作分成不同权限层级：

| 操作 | 需要授权 | 说明 |
|------|---------|------|
| **询问能力** | ❌ 不需要 | "你能帮我配置吗？" 不会触发文件操作 |
| **只读检查** | ✅ 需要 | 扫描现有配置，但不修改 |
| **预览** | ❌ 不需要 | 展示将要修改的内容 |
| **写入** | ✅ 需要确认 | 修改 Custom Instructions、AGENTS.md 等 |
| **导出** | ✅ 需要确认 | 创建迁移包 |
| **导入** | ✅ 需要确认 | 从迁移包恢复配置 |

**安全机制**：
- ✅ 替换本地配置前自动备份
- ✅ 任何修改都先预览，确认后才执行
- ✅ 导出的迁移包会自动脱敏（删除密码、Token）

### 迁移边界

**普通迁移包含**：
- ✅ Custom Instructions 内容
- ✅ 全局和项目 AGENTS.md
- ✅ 项目 MEMORY.md（如果启用）
- ✅ 自定义 Skill 定义
- ✅ Hook 和 Rule 配置

**普通迁移不包含**：
- ❌ 聊天记录
- ❌ 密码、Token、API Key
- ❌ 登录状态、Session
- ❌ 日志文件
- ❌ 缓存目录
- ❌ SQLite 数据库

**重要说明**：
- ⚠️ **P13N 不会自动同步设备**
- ⚠️ 如果旧设备无法使用且没有备份，本地配置无法还原
- ✅ 云端设置（ChatGPT 账号）和 Git 项目配置可按原方式恢复

### 账号设置

**ChatGPT 账号设置**（Custom Instructions、Projects）：
- 如果 API 支持：P13N 自动完成
- 如果不支持：P13N 整理好内容，告诉你去哪里粘贴

**需要在对应界面完成的操作**：
- ChatGPT 账号登录
- OAuth 授权
- 系统权限授予

---

## 验证状态

### 当前版本

**v0.1.0** (2024-08-13)

### 测试覆盖

- ✅ **16 项自动测试**
  - Skill 结构完整性
  - 发行包格式验证
  - 问诊路线逻辑
  - 授权流程检查
  - 备份机制验证
  - 迁移规则合规性

### 运行测试

```bash
# 构建发行包
python3 scripts/build_release.py

# 验证 Skill 结构
python3 scripts/validate_skill.py .

# 运行所有测试
python3 -m unittest discover -s tests -v
```

### 兼容性

| 平台 | 状态 | 说明 |
|------|------|------|
| **Codex CLI** | ✅ 测试通过 | |
| **Codex IDE Plugin** | ⚠️ 部分支持 | 表单可能降级为对话 |
| **ChatGPT** | ⚠️ 仅配置建议 | 不能直接修改账号设置 |
| **macOS** | ✅ 测试通过 | |
| **Linux** | ✅ 测试通过 | |
| **Windows** | ⚠️ 未充分测试 | 路径可能需要调整 |

### 已知限制

- 自动测试只验证结构和流程约束
- 不同客户端、账号和操作系统需要实际验证
- ChatGPT 账号设置可能需要手动完成

---

## FAQ

### Q: P13N 会不会搞乱我现有的配置？

**A:** 不会。任何修改都先给预览，确认后才执行。替换本地配置前会自动备份。

---

### Q: 我不懂 Custom Instructions 和 AGENTS.md，能用吗？

**A:** 能。P13N 从你的真实工作开始问，不需要先学这些名词。

---

### Q: 换新电脑，配置能带走吗？

**A:** 能。在旧设备导出脱敏迁移包，新设备导入即可。但聊天记录、密码、Token 不在迁移范围。

---

### Q: P13N 会自动同步我的多台设备吗？

**A:** 不会。P13N 只提供手动导出/导入功能，不会自动同步。

---

### Q: 安装包里包含我的个人配置吗？

**A:** 不包含。`dist/supbewhy-p13n.zip` 只是 Skill 本身，不含你的个人配置。

---

### Q: 为什么 P13N 要询问那么多问题？

**A:** 因为每个人的工作方式不同。只用 ChatGPT 写文章的人，可能只需要 Custom Instructions；经常用 Codex 改本地项目的人，才需要 AGENTS.md。P13N 根据你的回答推荐合适的配置，不会硬塞用不到的东西。

---

### Q: 配置后，AI 的回答会有什么不同？

**A:**
- **配置前**：每次都要重新解释背景、风格、输出要求
- **配置后**：AI 自动按你的习惯输出，简单的模糊问题带着假设继续，可能导致返工的才停下来确认

---

### Q: 这个项目和 OpenAI 官方有关系吗？

**A:** 无关。这是个人维护的开源项目。

---

### Q: 发现 Bug 或有功能建议怎么办？

**A:** 欢迎提 [Issue](https://github.com/supbewhy-sudo/supbewhy-p13n/issues) 或 [Pull Request](https://github.com/supbewhy-sudo/supbewhy-p13n/pulls)。

---

## 贡献指南

欢迎贡献代码、文档或建议！

### 如何贡献

1. Fork 这个仓库
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. Push 到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 贡献类型

- 🐛 **Bug 修复**
- ✨ **新功能**
- 📝 **文档改进**
- 🎨 **界面优化**
- ✅ **测试补充**
- 🌐 **多语言支持**

### 代码规范

- 遵循现有代码风格
- 补充必要的测试
- 更新相关文档

---

## 许可证

本项目采用 [MIT License](LICENSE) 开源。

---

## 关于作者

我是 BewhY，一名设计师。我一直在研究一件很具体的事：**怎么让 AI 真正顺手，而不是给自己多添一套需要维护的规则。**

📕 [小红书：supBewhY](https://www.xiaohongshu.com/user/profile/5a04413511be1005cafea0f9)

---

**如果 P13N 帮到了你，欢迎给个 ⭐️ Star！**
