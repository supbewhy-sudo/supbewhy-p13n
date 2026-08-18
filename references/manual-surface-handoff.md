# Manual surface handoff

Use this reference when account UI, authentication, or OS permissions cannot be completed automatically.

## Output format

For each manual action, provide:

1. surface and purpose;
2. shortest current navigation path;
3. exact copy-ready content or value when safe;
4. what must not be pasted, especially secrets;
5. how the user verifies success.

Verify changing UI paths with current official OpenAI documentation. Do not rely on stale screenshots.

## Backup handoff

Do not turn backup into a repeated manual ritual.

| Current state | Required behavior |
|---|---|
| No write will occur | Do not create or request a backup |
| Existing local target is readable and in the approved write scope | Back it up automatically immediately before writing and report the backup path |
| A new local file will be created | Journal the new path for rollback; no old copy exists |
| Existing ChatGPT text was pasted or otherwise supplied and replacement is approved | Generate one dated rollback snapshot before handoff; save it only to an approved local destination |
| Existing ChatGPT text is unavailable to Codex | Explain the access boundary once, then offer account export or one-time copy before replacement |

Ask the user to verify that supplied ChatGPT content covers the intended surfaces once, not once per field or step. Never say an account setting was backed up automatically unless a durable snapshot was actually created and its location can be reported.

## Typical handoffs

- ChatGPT Personalization: prepare the rollback snapshot, paste approved Custom Instructions, and verify in a new ordinary chat.
- ChatGPT Projects: verify project presence, instructions, files, and memory mode; do not recreate cloud projects unless missing.
- Codex login: authenticate on the target device instead of copying auth files.
- Plugins and connectors: reinstall or enable, then repeat OAuth when requested.
- MCP: import server definitions only, then authenticate with the provider.
- Computer Use: grant the target operating system's Accessibility or Screen Recording permissions.

Never report an account or OS action as complete until the user confirms it or the state can be read back safely.
