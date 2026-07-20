# Interactive onboarding

Use this reference only when onboarding or revision requires several compact choices. The interaction must reduce effort, not turn profiling into a survey.

## Conversation state

Track only the minimum current-session state:

```yaml
route: "fresh-start|revise-existing|unsure|unresolved"
posture: "preserve|consolidate|rebuild|none"
surfaces: []
privacy_choice: "none|metadata|targeted|unresolved"
confirmed_groups: []
skipped_fields: []
next_step: ""
```

Do not persist this state outside the conversation without explicit consent. Never include raw configuration bodies, file contents, credentials, identity inferences, or private scan findings in a visual interaction.

## Interaction rules

1. Start with the route only when it is unresolved. If it is already known, acknowledge it and move to the next material decision.
2. Ask one decision group at a time. Avoid a long all-at-once form.
3. Provide a recommended choice with one plain-language reason when evidence supports it.
4. Accept `back`, `skip`, and `pause` at every conversational step:
   - `back`: restore the prior decision group and keep later answers only when they remain valid.
   - `skip`: record the field as skipped and continue, except for write authority, privacy consent, or destructive/high-impact confirmation.
   - `pause`: return the compact state, what is already decided, and one copy-ready resume sentence.
5. Keep open-ended descriptions in ordinary chat: recurring jobs, desired outputs, friction, must-preserve behavior, and nuanced wording.
6. Show an early useful result, such as the selected route, likely configuration layers, or a provisional recommendation, before asking for additional detail.

## Interaction layers

Use `visualize` only when it is installed and the host supports it. Load and obey its full `SKILL.md` before creating or updating any interaction.

For low-impact choices, a visual surface is optional and should be used only when it materially lowers effort.

Good visual groups are:

- setup route: fresh start, revise existing, unsure;
- retention posture: preserve, consolidate, rebuild;
- grouped recommendations: keep, consolidate, replace, retire, user decision;
- provisional scope: the local and account surfaces under consideration.

Use native radio buttons or checkboxes and one clearly labeled submit action. Send only explicit selections to the current conversation with `window.openai.sendFollowUpMessage({ prompt, title })`. The prompt must identify the Skill, current mode, selected values, and requested next step so the conversation can resume without interpreting hidden UI state.

Implement `back` and `skip` as local controls only when they can be represented safely. Implement `pause` by sending the current compact state back to the conversation; browser-local state is not durable.

Do not use the visual for free-form profiling, configuration diff review, secrets, full Custom Instructions, `AGENTS.md` bodies, or scan results. Do not require the user to use it. If it cannot load or the host does not support `window.openai`, immediately present the same choices as numbered text and retain the same conversation state.

## Mandatory confirmation gates

The following actions require a separate confirmation gate:

- metadata or targeted-content privacy scans;
- local or account writes and high-impact configuration activation;
- migration export, import, and rollback.

When `visualize` is available and the host supports it, render a distinct confirmation surface. This is not optional UI polish. It is the authority boundary.

The surface must:

1. Put `Waiting for authorization — no action has run` at the top.
2. Name one concrete action and show its exact paths or account surfaces, mode, file and byte caps, exclusions, destination or report path, conflict policy, and backup or rollback behavior as applicable.
3. Provide one primary action whose label names the operation, such as `Approve and start metadata scan`.
4. Provide `Adjust scope` and `Cancel`. `Back` or `Pause` may also be offered when useful. Never offer `Skip`.
5. Explain that opening the surface, continuing to it, or accepting a preselected value is not consent.
6. Send only the explicit decision and non-sensitive scope fields back with `window.openai.sendFollowUpMessage({ prompt, title })`.

The follow-up prompt must be self-contained and machine-readable enough to preserve the boundary. Include at least:

```text
skill=supbewhy-p13n
authorization=approved|adjust|cancelled
action=metadata-scan|targeted-scan|apply|export|import|rollback
scope=<exact approved paths or account surfaces>
limits=<mode, file cap, byte cap, and exclusions when applicable>
destination=<report, bundle, target, or none>
next_step=<execute approved action or return to scope editing>
```

Do not execute from hidden browser state. Execute only after the conversation receives `authorization=approved` with a concrete action and matching scope. Changing the action, mode, path, cap, destination, conflict policy, or replacement set invalidates the earlier approval and requires a new confirmation gate.

`Adjust scope` returns to scope editing without reading or writing anything. `Cancel` records a no-action result. A missing, ambiguous, defaulted, or skipped response is not approval.

## Plain-text fallback

Use this compact pattern:

```text
Recommended: 2 — Consolidate, because it keeps useful intent while removing duplication.

1. Preserve
2. Consolidate
3. Rebuild

Reply with 1/2/3, or say back, skip, or pause.
```

Do not re-ask answers already supplied. After a selection, state what changed and ask only the next outcome-changing question.

For a mandatory confirmation gate, do not reuse the ordinary numbered-choice pattern. Use a prominent blocking message:

```text
STATUS: Waiting for authorization — no data has been read or changed.

Action: <one concrete operation>
Scope: <exact paths or account surfaces>
Mode and limits: <mode, file cap, byte cap>
Always excluded: <credentials, history, caches, and other denied roots>
Output / backup: <report, bundle, backup, rollback effect, or none>

To approve this exact action and scope, reply:
Approve <action> for the scope above.

Reply `adjust scope` or `cancel` to continue without executing it.
```

The approval sentence must be visible as a required action, not buried in surrounding prose or shown merely as a copy example. Do not call inspection or mutation tools until the exact affirmative reply is received.
