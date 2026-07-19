# Configuration map

Use the smallest durable surface that matches the scope. Verify current OpenAI behavior from official sources before making claims about sync, availability, limits, or UI paths.

| Need | Surface | Default handling |
|---|---|---|
| Stable response language, tone, density | ChatGPT Custom Instructions | Generate copy-ready text; verify account UI after application |
| Repeated domain context, files, project instructions | ChatGPT Project | Create only when recurring context justifies maintenance |
| Personal Codex defaults across repositories | Global `AGENTS.md` | Keep short; explain authority and verification preferences |
| Repository facts and commands | Project `AGENTS.md` | Keep with the repository; closest scope wins |
| Project decisions and corrections | Project `MEMORY.md` custom protocol | Require `AGENTS.md` to read and update it |
| Repeatable task workflow | Skill | Use only for stable inputs, outputs, and procedure |
| Command or lifecycle enforcement | Hook or Rule | Add only when deterministic enforcement is needed |
| Model, sandbox, approvals, MCP, feature flags | `config.toml` | Treat as high impact; preview and confirm separately |

## Layer rules

- Avoid copying the same instruction into every layer.
- Project instructions may override global account instructions; include only project-specific differences where possible.
- Do not create ChatGPT Projects for one-off topics.
- Do not require `AGENTS.md` or `MEMORY.md` for pure chat, temporary snippets, or projectless work.
- Keep code-discoverable facts out of memory files.
- Keep credentials out of every instruction and memory surface.

When revising an existing setup, preserve useful intent but move each rule to the smallest correct surface. Do not keep duplication merely because it already exists. Do not remove the old version until the grouped recommendation, focused diffs, backup method, and concrete scope are confirmed.

## Codex paths

Detect paths at runtime instead of assuming them:

- `CODEX_HOME`, defaulting to `~/.codex`.
- global `AGENTS.md` under `CODEX_HOME`.
- user Skills under discoverable user locations such as `$HOME/.agents/skills` and environment-supported legacy locations.
- repo Skills under `.agents/skills`.
- project config under `.codex/config.toml` in trusted repositories.

Do not copy caches, system Skills, plugin caches, sessions, logs, or databases as configuration.
