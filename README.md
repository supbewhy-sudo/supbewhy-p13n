# supɃewhY-P13N

> 让 ChatGPT 和 Codex 适应你的工作习惯，少一点反复磨合。

P13N 是一个个性化配置 Skill。它会先问清楚你平时用 AI 做什么、希望拿到什么结果、讨厌哪些回答方式，然后把这些要求放到合适的位置。

可能是 Custom Instructions，也可能是 Projects、`AGENTS.md`、项目记忆或某个 Skill。用不到的配置，它不会硬塞给你。

`P13N` 是 Personalization（个性化）的缩写。

> 这是个人维护的公开项目，与 OpenAI 官方无关。

## 它能解决什么

你可能遇到过这些情况：

- 每次开新对话，都要重新解释背景和输出要求。
- AI 该直接做的时候一直追问，该谨慎的时候却自作主张。
- 个性化规则越写越多，最后互相打架。
- 项目做了很久，之前确认过的决策和踩过的坑还是会被忘掉。
- 同一套 Prompt 复制了很多遍，却始终没有变成稳定流程。

P13N 会把这些问题拆开处理。长期沟通习惯放在全局，项目内容留在项目里，重复工作足够稳定时再做成 Skill。

## 两种配置方式

### 1️⃣ 从来没有配置过

不用先学 Custom Instructions、`AGENTS.md` 这些名词。

P13N 会从你真实在做的事开始问：

- 你主要使用 ChatGPT、Work、Codex，还是本地项目？
- 最常重复的工作有哪些，最后想拿到什么成品？
- 目前哪些 AI 行为最让你浪费时间？
- 你希望它怎么处理语言、篇幅、分歧和模糊需求？
- 什么操作可以直接执行，什么操作必须先确认？
- 有没有需要长期保留背景和决策的项目？

问完以后，它会给出一套够用的配置。

比如，只用 ChatGPT 写运营内容的人，也许只需要一份 Custom Instructions 和一个长期 Project。经常让 Codex 修改本地项目的人，才需要考虑全局和项目级 `AGENTS.md`。

![fresh-start 新用户交互界面](docs/images/fresh-start.png)

### 2️⃣ 已经配过，但有点乱

旧配置不会被直接清空。

你可以选择尽量保留，也可以让 P13N 帮你整理。整理时，它会找出重复规则、互相冲突的要求、放错位置的项目内容，以及已经不用的旧路径和旧流程。

必须保留的习惯会留下。需要调整的内容先给预览，确认后才会修改。

![revise-existing 已有配置用户交互界面](docs/images/revise-existing.png)

不知道自己配过什么也没关系。你可以只回答问卷，也可以在看清检查范围后，允许它做一次只读盘点。

界面表单只是为了让选择更轻松。宿主不支持表单时，用普通对话也能走完整个流程。

## 最后会配置哪些内容

每个人拿到的结果不一样。P13N 只选当前有用的部分。

| 配置位置 | 放什么 |
|---|---|
| Custom Instructions | 语言、篇幅、语气和长期沟通习惯 |
| ChatGPT Projects | 某个长期领域的背景、文件和项目要求 |
| 全局 `AGENTS.md` | Codex 在不同项目里都要遵守的协作方式 |
| 项目 `AGENTS.md` | 当前项目的命令、目录规范和验证方法 |
| 项目 `MEMORY.md` | 已确认的决策、踩坑和用户纠正 |
| Skill | 输入、输出和步骤都比较固定的重复工作 |
| Hook / Rule | 必须自动检查或禁止的操作 |

`MEMORY.md` 需要由项目 `AGENTS.md` 明确要求读取和维护，它不是 Codex 自带的自动记忆入口。

ChatGPT 账号里的设置如果不能自动完成，P13N 会把内容整理好，再告诉你去哪里粘贴、怎么检查是否生效。

## 用起来有什么变化

配置之前，你可能每次都在教 AI 怎么跟你合作。

配置之后，稳定的习惯会留在正确的位置。简单的模糊问题可以带着假设继续，可能导致返工或风险的问题才停下来确认。项目里的构建命令、修改边界和历史决策，也不用一次次重讲。

如果某件事已经重复很多次，P13N 还会提醒你：这可能不该继续靠复制 Prompt 解决了。

## 安装

### 安装到个人 Codex

```bash
git clone https://github.com/supbewhy-sudo/supbewhy-p13n.git
cd supbewhy-p13n

CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$CODEX_SKILLS_DIR"
cp -R ./supbewhy-p13n "$CODEX_SKILLS_DIR/"
```

也可以下载 [`dist/supbewhy-p13n.zip`](dist/supbewhy-p13n.zip)，解压后把 `supbewhy-p13n/` 放进 Codex Skills 目录。

安装完成后，重启 Codex 或打开一个新任务。

## 开始使用

第一次配置：

```text
使用 $supbewhy-p13n 帮我配置 ChatGPT 和 Codex 个性化。我没有配置过，请从最小问诊开始，先不要扫描电脑。
```

整理已有配置：

```text
使用 $supbewhy-p13n 审查我现有的 Custom Instructions 和 AGENTS.md。保留有用习惯并整理，先给我预览，不要直接修改。
```

迁移到新设备：

```text
使用 $supbewhy-p13n 盘点这台电脑上可以安全迁移的 Codex 个性化。先给我迁移预览，不要复制凭据、聊天记录和缓存。
```

## 关于权限和迁移

询问、只读检查、预览、写入、导出和导入是不同的权限。你问“能不能帮我配置”，不会触发文件修改。

需要替换本地配置时，P13N 会先备份。ChatGPT 账号设置、登录、OAuth 和系统权限，则要在对应界面完成。

跨设备迁移只带走确认过的便携配置，不会复制整个 `CODEX_HOME`。聊天记录、密码、Token、登录状态、日志、缓存和 SQLite 数据库都不在普通迁移范围里。

到了新设备，先从 GitHub 安装 P13N，再用它检查和导入其他配置。

## 验证状态

当前版本：`0.1.0`

仓库有 16 项自动测试，覆盖 Skill 结构、发行包、问诊路线、授权、备份和迁移规则。

```bash
python3 scripts/build_release.py
python3 scripts/validate_skill.py .
python3 -m unittest discover -s tests -v
```

这些测试用于检查结构和流程约束。不同客户端、账号和操作系统，仍需要实际验证。

## 关于作者

我是 BewhY，一名设计师。我一直在研究一件很具体的事：怎么让 AI 真正顺手，而不是给自己多添一套需要维护的规则。

📕 [小红书：supBewhY](https://www.xiaohongshu.com/user/profile/5a04313511be1005cafea0f9)
