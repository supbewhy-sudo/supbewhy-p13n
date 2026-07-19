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

## Optional Visualize layer

Use `visualize` only when it is installed and a compact selection surface materially lowers effort. Load and obey its full `SKILL.md` before creating or updating any interaction.

Good visual groups are:

- setup route: fresh start, revise existing, unsure;
- retention posture: preserve, consolidate, rebuild;
- scan consent: questionnaire only, metadata inventory, targeted audit;
- grouped recommendations: keep, consolidate, replace, retire, user decision;
- final scope: the exact local and account surfaces to apply.

Use native radio buttons or checkboxes and one clearly labeled submit action. Send only explicit selections to the current conversation with `window.openai.sendFollowUpMessage({ prompt, title })`. The prompt must identify the Skill, current mode, selected values, and requested next step so the conversation can resume without interpreting hidden UI state.

Implement `back` and `skip` as local controls only when they can be represented safely. Implement `pause` by sending the current compact state back to the conversation; browser-local state is not durable.

Do not use the visual for free-form profiling, configuration diff review, secrets, full Custom Instructions, `AGENTS.md` bodies, or scan results. Do not require the user to use it. If it cannot load or the host does not support `window.openai`, immediately present the same choices as numbered text and retain the same conversation state.

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
