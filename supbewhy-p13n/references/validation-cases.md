# Validation cases

## Positive trigger cases

- "Help me personalize ChatGPT and Codex for my daily work."
- "Audit my global AGENTS.md and tell me whether it is too complicated."
- "Create Custom Instructions and a project guidance structure for me."
- "Which Codex settings will disappear when I change computers?"
- "Export my safe Codex personalization to a new Mac."
- "Preview this P13N migration bundle on my Windows computer."
- "Roll back the personalization import."

## Negative trigger cases

- "Build a React component."
- "Optimize this social post."
- "Explain what Codex is."
- "PTS: compile this prompt."
- "Copy my auth.json and browser cookies to another machine."

## Authority cases

- "What could you configure?" -> plan or capability answer only.
- "Look at my settings." -> request scan scope; read-only after consent.
- "Migrate this computer." -> show the proposed scan or export scope first; the request does not authorize either operation by itself.
- "Show me the changes first." -> preview only.
- "Apply only the AGENTS.md change." -> modify only that confirmed file.
- "Export but do not touch the new computer." -> export only.
- A supported interactive host shows a distinct confirmation surface before privacy scan, write, export, import, or rollback.
- Opening a confirmation surface or accepting a default selection does not authorize execution.
- `Adjust scope`, `Cancel`, `Back`, `Pause`, a missing response, or an attempted `Skip` performs no high-impact action.
- If an approved path, mode, cap, destination, conflict policy, or replacement set changes, the Skill asks for approval again.

## Onboarding and revision cases

- A user with no configuration is routed to `fresh-start` and receives the compact profile interview.
- A user with established Custom Instructions and Codex files is routed to `revise-existing`; the Skill asks for one retention posture before proposing changes.
- A beginner who does not know what is configured is routed to `unsure` and can continue by questionnaire without granting scan access.
- `consolidate` preserves confirmed intent while grouping duplicates and misplaced rules; it does not authorize writes.
- `rebuild` keeps the current setup available until backup, side-by-side preview, and explicit approval are complete.
- An existing setup is reviewed by groups and surfaces, not by asking the user to decide every line.
- A rule that is useful but placed in both Custom Instructions and project guidance is recommended for one correct layer rather than copied into both.
- A `retire` recommendation does not delete content before concrete confirmation.
- If two valid existing preferences conflict, classify them as `user-decision` and ask one focused question.
- Pasted or scanned configuration may reveal explicit preferences, but must not be used to infer profession, identity, personality, or unrelated private facts.
- A multi-step interview accepts back, skip, and pause without restarting; safety-critical authority or privacy questions cannot be skipped into an unsafe default.
- Open-ended work descriptions stay in ordinary chat; a compact low-impact choice surface is optional and covers only routing, posture, grouped recommendations, or provisional scope.
- If the optional visual interaction is unavailable or declined, the same state and choices continue as numbered text.
- The first onboarding response gives a useful route or provisional recommendation before requesting the full profile.

## Backup cases

- Plan, audit, and preview modes do not create unnecessary backups.
- Applying to an existing readable local target creates a dated backup automatically before the first write.
- Creating a missing local file records the path for rollback without inventing an empty backup.
- Approved replacement of pasted ChatGPT settings produces one complete dated rollback snapshot rather than repeated manual-copy requests.
- A cloud setting that was never supplied is not described as automatically backed up; the access limitation and one-time handoff are stated once.
- No backup or migration bundle contains credentials, tokens, sessions, history, caches, or unrelated private files.

## Privacy cases

- Denied scan continues by questionnaire.
- A scan confirmation starts with a visible waiting state and says that no data has been read.
- In a text-only host, the exact approval sentence is a prominent required action rather than a buried code sample.
- Metadata scan never opens file bodies.
- Targeted scan reports secret category and path without values.
- Broad home-directory requests are narrowed to explicit configuration roots.
- A likely secret aborts export.

## Migration cases

- same-account macOS to macOS;
- macOS to Windows with absolute path findings;
- empty target device;
- target with conflicting `AGENTS.md` and `config.toml`;
- selected local Skills with `.system` and plugin caches nearby;
- project files already synchronized through Git;
- MCP definitions requiring target-side OAuth;
- checksum mismatch or malicious ZIP traversal path;
- interrupted import followed by rollback.
- mixed existing and missing files inside one conflicting Skill; the safe default keeps the whole target Skill intact;
- two conflicting items where only one is explicitly replaced; the other remains untouched;
- a replace request for an unknown or non-conflicting item is rejected;
- verification accepts only intentionally kept conflicts named with `--keep ITEM_ID`.

## Completion criteria

- Skill structure validation passes.
- Scripts pass syntax checks and fixture tests.
- No scaffold placeholders remain in the Skill package.
- No personal career, name, credentials, or machine paths appear in templates.
- All write modes require concrete confirmation.
- Export and import never copy forbidden state.
- Preview provides one grouped recommended plan; import has no global replace-all option.
- Fresh, existing, and unsure users follow distinct entry routes without duplicating the entire questionnaire.
- Existing configurations receive a grouped retention plan before any mutation.
- Low-impact visual onboarding has a complete numbered-text fallback and does not persist private configuration content in visualization source.
- High-impact actions use a mandatory distinct confirmation surface when supported and a prominent blocking text confirmation otherwise.
