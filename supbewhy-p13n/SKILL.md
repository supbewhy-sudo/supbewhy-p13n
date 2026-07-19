---
name: supbewhy-p13n
description: Audit, design, preview, safely apply, export, migrate, import, verify, and roll back personalized ChatGPT and Codex guidance and local configuration. Use when a user asks to personalize, configure, optimize, audit, back up, transfer, restore, or migrate ChatGPT or Codex behavior between devices, including Custom Instructions, Project guidance, AGENTS.md, project MEMORY.md protocols, templates, user-created skills, hooks, rules, prompts, MCP definitions, and portable Codex settings. Do not use for ordinary task execution, one-off prompt writing, unrelated coding, PTS prompt compilation, chat-history migration, credential copying, or broad device scanning without explicit consent.
---

# supɃewhY-P13N

Personalize ChatGPT and Codex from a user's real work patterns, then safely move the local Codex portion between devices. Treat advice, inspection, preview, and mutation as separate authority levels.

## Resolve the mode

Choose one mode from the user's request. When intent is ambiguous, default to the least mutating mode.

- `plan-only`: recommend a configuration without reading or changing local files.
- `audit-only`: inspect an approved scope and report; do not modify.
- `preview`: generate proposed content and exact diffs; do not apply.
- `apply`: apply only the explicitly confirmed local changes.
- `migration-audit`: classify what is cloud, local, project-bound, machine-specific, sensitive, or unknown.
- `migration-export`: create a sanitized, portable migration bundle from confirmed items.
- `migration-import-preview`: verify a bundle and show target conflicts without writing.
- `migration-import`: back up confirmed targets, import, and verify.
- `migration-verify`: verify a completed setup or migration.
- `migration-rollback`: restore a backup created by this workflow after explicit confirmation.

Capability questions and conditional wording such as "if you configured this" never authorize `apply`, export, import, or rollback.

## Route setup before profiling

Read `references/profile-schema.md` when onboarding or revising a profile.

Use an explicit route when the user's state is not already clear:

- `fresh-start`: the user has no meaningful personalization or wants to start from a blank slate.
- `revise-existing`: the user has used Custom Instructions, Projects, `AGENTS.md`, Skills, Hooks, Rules, templates, prompts, or Codex settings and wants to improve them.
- `unsure`: the user does not know what is configured or which surface owns it.

Do not ask this routing question when the request already answers it. For `unsure`, offer questionnaire-only discovery or a consented metadata inventory; do not assume access.

For `revise-existing`, ask for one starting posture instead of making the user review every rule:

1. Preserve: keep current wording and structure where possible; fix only clear conflicts, risks, or broken behavior.
2. Consolidate (recommended): preserve useful intent, but allow deduplication, regrouping, and focused rewriting after preview.
3. Rebuild: design a replacement from first principles, while retaining a backup and side-by-side preview until explicit approval.

Apply the posture as a default, not an irreversible bulk decision. If different surfaces genuinely need different treatment, recommend the exceptions rather than asking the user to configure each surface up front.

Inspect or accept pasted existing configuration only after the relevant authority is clear. Extract explicit preferences and workflow intent from it, but do not infer profession, identity, personality, or private facts. Ask only for gaps that materially change the proposed result.

Group existing content by surface and purpose. Recommend one of `keep`, `consolidate`, `replace`, `retire`, or `user-decision` for each group, with the reason and user impact. Never delete or overwrite because a group was classified; classification produces a preview, not authority.

For `fresh-start`, start with the smallest useful interview:

1. Ask which surfaces the user actually uses: Chat, Work, Codex app, CLI, IDE, local projects.
2. Ask for up to three recurring jobs and their expected deliverables.
3. Ask what currently wastes time or produces poor results.
4. Ask how the user wants the assistant to handle language, density, disagreement, ambiguity, and execution authority.
5. Ask whether persistent project context is needed.
6. Offer the scan levels from `references/privacy-scan-policy.md`; do not assume consent.

Treat profession as optional context. Prefer jobs-to-be-done, outputs, and recurring friction because they map more directly to configuration.

Ask follow-up questions only when the answer changes a configuration layer, permission boundary, privacy decision, or migration result. Keep the profile ephemeral unless the user explicitly approves saving it.

## Keep onboarding low-friction

Read `references/interactive-onboarding.md` when onboarding spans multiple choices or the user asks for a conversational form.

- Ask one decision group at a time and make the first response useful before requesting a full profile.
- Always accept `back`, `skip`, `pause`, or their language-equivalent. Allow `skip` unless the missing answer controls write authority, privacy consent, or a destructive/high-impact action.
- On `back`, revise the prior answer without restarting. On `pause`, return a compact resumable state and do not persist it outside the conversation unless the user approves.
- Prefer ordinary chat for open-ended work descriptions and nuanced preferences.
- When the `visualize` Skill is available and a compact choice surface would materially reduce effort, use it as an optional interaction layer for routing, retention posture, consent, grouped decisions, or final scope confirmation. Load and follow the full `visualize` Skill before creating the interaction.
- Keep all decisions valid without the visual. If the visual is unavailable, unsupported, or declined, use a numbered text equivalent and continue from the same state.
- Never put discovered configuration bodies, secrets, private file contents, or durable profile data inside visualization source. Send only the user's explicit selections back to the conversation.

## Inspect safely

Read `references/privacy-scan-policy.md` before inspecting local configuration.

- Show the proposed paths, scan mode, file and byte caps, exclusions, and approximate context cost before reading file contents.
- Use `scripts/inspect_setup.py` for bounded inventory and optional content-risk scanning.
- Never scan the whole home directory, chat history, browser profiles, credentials, caches, logs, sessions, SQLite state, `.env`, or keychains.
- Never infer a user's profession, identity, or personality from unrelated private files.
- If consent is denied, continue with the questionnaire.

## Map needs to the smallest surface

Read `references/configuration-map.md` when choosing where guidance belongs.

- Put stable cross-chat response preferences in ChatGPT Custom Instructions.
- Use ChatGPT Projects only for repeated domain context, project files, or project-specific guidance.
- Put personal Codex defaults in the global `AGENTS.md`.
- Put repo facts, commands, conventions, and verification in project `AGENTS.md` files.
- Use project `MEMORY.md` only as an explicit custom protocol referenced by `AGENTS.md`; do not call it native Codex discovery.
- Use a Skill for a repeatable workflow with stable inputs and outputs.
- Use Hooks or Rules only for deterministic enforcement.
- Change models, sandboxing, approval policy, MCP permissions, or other high-impact `config.toml` settings only as a separately explained and confirmed action.

Verify current OpenAI product behavior with official sources when sync, availability, limits, or UI paths could have changed.

## Preview before applying

Return a preview containing:

1. Findings, assumptions, and unresolved uncertainties.
2. The chosen setup route and, for existing setups, the retention posture.
3. A grouped `keep`, `consolidate`, `replace`, `retire`, or `user-decision` recommendation for existing content.
4. Current-to-proposed layer map.
5. Exact files and account surfaces affected.
6. Proposed content or focused diffs.
7. Security and maintenance impact.
8. Automatic actions versus manual UI, login, or OS-permission steps.
9. Validation and rollback plan.

Lead with one recommended plan and allow optional group-level adjustment. Do not ask the user to decide line by line unless a specific unresolved conflict changes meaning. Do not write until the user confirms the concrete scope. Back up every existing target before replacement. Create only missing files and make surgical edits to existing files. Do not delete unrelated content.

Apply backups according to the surface instead of asking the user to repeat work:

- `plan-only`, `audit-only`, and `preview`: do not create a backup because nothing is being replaced.
- Existing local targets in an approved `apply` or `migration-import`: create the dated backup and transaction record automatically immediately before the first write. Do not ask the user to manually copy files Codex can already read.
- Missing local targets: record the created path in the transaction journal; there is no prior file to back up.
- ChatGPT account surfaces whose current text was supplied in the conversation: after replacement is approved, generate one complete dated rollback snapshot before the handoff. Save it automatically only when the user has approved a local backup destination; otherwise keep it as a copy-ready rollback block and state that it is not a durable local backup.
- ChatGPT account surfaces whose current text is unavailable: state the limitation once and offer the shortest account export or one-time copy path before replacement. Do not repeat the same backup request at every step and do not claim an automatic cloud backup.
- Never include credentials, tokens, sessions, history, caches, or unrelated private data in a backup or migration bundle.

Use the templates in `assets/` only as starting points. Remove unused sections and placeholders before delivery.

## Migrate between devices

Read `references/migration-policy.md` before any migration mode.

### Audit the source

Classify every candidate as:

- cloud/account: verify on the target account; do not duplicate locally.
- portable local: safe to bundle after inspection.
- review required: contains paths, commands, permissions, dependencies, or machine assumptions.
- project-bound: prefer the project's Git or approved file-sync channel.
- reauthorize: move definitions only; repeat login, OAuth, plugin installation, or OS permissions.
- forbidden: credentials, tokens, sessions, logs, caches, history, sockets, databases, keychains, or unrelated private data.
- unknown: exclude until verified.

Do not copy all of `CODEX_HOME`. Do not copy system or plugin caches. Prefer reinstalling third-party Skills and Plugins from their known source; bundle only user-created or intentionally modified local Skills.

### Export

1. Run a metadata inventory first.
2. Show the selected item IDs and destination.
3. Obtain explicit export approval.
4. Use `scripts/migrate_setup.py export` to scan for likely secrets, replace known home roots with portable placeholders, create checksums, and generate a ZIP bundle.
5. Stop if a possible secret is found; never add a bypass that exports secret values.

### Import

1. Use `scripts/migrate_setup.py preview` first.
2. Present `recommended_plan` first: one safe default action, grouped attention items, then optional item-level adjustment. Treat an entire Skill as one item; do not ask about each file.
3. The safe default creates missing items, skips identical items, and keeps every conflicting item intact. Never use a global replace-all decision.
4. For high-impact `AGENTS.md`, config, Hook, or Rule conflicts, recommend keeping the target and show a focused diff for optional semantic merge. Do not let the script guess the merge.
5. Obtain one explicit approval for the concrete plan. Only when the user expands an item, pass repeatable `--replace ITEM_ID` or `--keep ITEM_ID`; replacement is allowed only for named conflicting items.
6. Use `scripts/migrate_setup.py import --confirm APPLY` after approval. The importer backs up every existing file it replaces and records item decisions in the transaction journal.
7. Reauthorize OAuth, credentials, Plugins, MCP connections, and OS permissions manually.
8. Run `verify`, passing each intentionally kept conflicting item as `--keep ITEM_ID`; retain the generated rollback directory.

### Roll back

Preview the rollback journal. Use `rollback --confirm ROLLBACK` only after explicit approval. Restore only paths recorded by the import transaction.

## Validate the result

Read `references/validation-cases.md` for acceptance and trigger cases.

Check, as applicable:

- Custom Instructions and Project guidance are not duplicated.
- Global and project `AGENTS.md` scopes are correct.
- A project `MEMORY.md` protocol is explicitly referenced and works.
- selected Skills are discoverable and trigger correctly.
- templates contain no unresolved placeholders.
- imported files contain no old user-home paths or likely secrets.
- Hooks and Rules are reviewed before activation.
- MCP definitions exist but credentials are reauthorized.
- the target can be restored from the transaction backup.

If account UI, authentication, or OS permission work cannot be automated safely, use `references/manual-surface-handoff.md` and give the shortest current manual path. Never claim completion without verification.

## Output contract

For planning and audits, lead with the recommended configuration and the user impact. For previews, show the proposed scope and diffs. For applied work, report changed paths, backups, checks run, manual steps, and remaining risks.

Do not expose raw file contents discovered during a privacy scan unless the user explicitly asked for those contents and they contain no sensitive values.
