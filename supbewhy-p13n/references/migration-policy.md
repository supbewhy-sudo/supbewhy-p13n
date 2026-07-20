# Migration policy

## Default recommendation

Use a sanitized ZIP bundle for a one-time device move. Recommend a private version-controlled dotfiles repository only after a successful one-time migration and only for users who want ongoing multi-device maintenance.

Never copy the complete `CODEX_HOME` directory.

## Classification

| Class | Examples | Action |
|---|---|---|
| Cloud/account | Custom Instructions, Projects, account memory | Log in and verify; do not duplicate |
| Portable local | global `AGENTS.md`, generic templates, selected user Skills | Bundle after inspection |
| Review required | `config.toml`, Hooks, Rules, MCP definitions, absolute paths | Preview and adapt |
| Project-bound | repo `AGENTS.md`, `.codex/config.toml`, project `MEMORY.md` | Prefer Git; otherwise require explicit project mapping |
| Reauthorize | OAuth, Plugins, connectors, OS permissions | Reinstall or log in on target |
| Forbidden | auth, tokens, history, sessions, logs, caches, databases | Exclude |
| Unknown | undocumented state | Exclude until verified |

## Bundle rules

- Use format versioning and SHA-256 checksums.
- Replace the known source `CODEX_HOME` and home directory in text with `${CODEX_HOME}` and `${HOME}`.
- Flag other absolute paths for manual mapping.
- Preserve file permissions only when meaningful and safe; never restore setuid or executable status blindly.
- Include only user-selected Skills. Exclude `.system`, plugin cache, marketplace cache, generated runtime Skills, and unknown third-party copies by default.
- Export MCP definitions without credentials. Require target-side login.
- Export `config.toml` only after a targeted audit and explicit selection.

## Conflict rules

- `create`: target is missing; safe after confirmation.
- `identical`: skip.
- `conflict`: group by item, default to keep the target item intact, and produce a focused diff when useful.
- `blocked`: secret, unsafe path, checksum failure, unsupported target, or missing project mapping.

Present one recommended plan instead of asking about every file. The user may approve that plan once or expand only the items they want to adjust. A Skill directory is one item, so a conflict never creates a partial mixed Skill by default.

The deterministic importer has no replace-all mode. It may replace only item IDs explicitly named with `--replace ITEM_ID`, after backup. `--keep ITEM_ID` records an explicit keep decision; unlisted conflicts also use the safe keep default. Semantic merge remains an agent task performed with a focused diff and separate confirmation.

## Transaction rules

Before import:

1. verify ZIP paths and checksums;
2. resolve target placeholders;
3. block paths outside approved roots;
4. scan rendered content for likely secrets;
5. generate a dry-run report;
6. show the grouped recommended plan and any high-attention items;
7. obtain one explicit confirmation for the final item plan.

Export, import, and rollback approvals use the mandatory confirmation gate in `interactive-onboarding.md`. When the host supports `visualize`, show the action, exact selected item IDs, source or target roots, destination, conflict decisions, and backup or rollback effect in a distinct authorization surface. Provide one operation-specific approval action plus `Adjust scope` and `Cancel`; never offer `Skip`. A changed destination, item set, target root, conflict decision, or replacement set invalidates the earlier approval. In a text-only host, use the prominent blocking confirmation fallback.

During import, create a timestamped backup and journal every target. On failure, stop and preserve the journal. Rollback may restore only journaled paths.

## Manual work after import

- sign in to ChatGPT/Codex;
- verify cloud Projects and Custom Instructions;
- reinstall Plugins or third-party Skills from trusted sources;
- repeat MCP OAuth and connector authorization;
- grant Computer Use or OS permissions;
- install missing commands and runtimes;
- validate old absolute paths and shell differences.
