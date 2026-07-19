# Privacy and scan policy

## Consent levels

### None

Use questionnaire answers only. Do not inspect local files.

### Metadata

List approved configuration paths, file types, sizes, modification times, and classifications. Do not read file bodies. This is the recommended first scan.

### Targeted content audit

Read only approved configuration files to detect likely secrets, absolute paths, unresolved placeholders, and portability risks. Do not return raw content unless requested and safe.

## Before scanning

Show:

- exact roots and candidate paths;
- metadata or content mode;
- maximum file count and total bytes;
- denied files and directories;
- approximate context cost: small under 100 KB, medium 100 KB to 1 MB, large above 1 MB;
- where any report will be written.

These size bands are operational estimates, not exact token counts. Recommend narrowing any large scan.

## Always deny

- `auth.json`, tokens, credentials, cookies, keychains, `.env*`;
- chat history, session indexes, shell snapshots, logs, attachments;
- SQLite databases and journals;
- caches, temporary directories, IPC sockets, worktrees, backups;
- browser profiles and unrelated personal folders;
- `.git`, `node_modules`, vendor trees, system or bundled Skill caches.

Never broaden the scan because an expected file was missing. Report the missing path and ask before inspecting another root.

## Sensitive findings

Report only the file path, finding category, and count. Do not echo matched values. A likely secret blocks migration export until the source is removed or converted to an environment-variable reference.
