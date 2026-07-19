# Profile schema

Use this reference only for onboarding, revision, or migration discovery. Do not persist the profile without explicit consent.

## Setup route

Resolve one state before asking for a full profile:

- `fresh-start`: no meaningful configuration exists, or the user explicitly wants a blank-slate design.
- `revise-existing`: personalization already exists on one or more ChatGPT or Codex surfaces.
- `unsure`: the user cannot reliably identify what is configured.

If the user already described the state, route directly. Otherwise ask one compact question with these three choices.

For `unsure`, offer:

1. questionnaire-only discovery; or
2. a metadata inventory of approved Codex configuration roots.

ChatGPT account settings may require pasted text, screenshots, or an account-side export because local inspection cannot be assumed. Follow the privacy policy before any local inventory.

## Fresh-start questions

Ask these in one compact message:

1. Which surfaces do you use: Chat, Work, Codex app, CLI, IDE, local repositories?
2. What are the three most repeated tasks, and what finished output do you expect from each?
3. What behavior currently wastes time, causes rework, or feels wrong?
4. What language, response density, and level of technical explanation do you prefer?
5. When should the assistant advise, preview, or execute directly?
6. Do you want questionnaire-only setup, metadata inventory, or targeted content audit?

Ask profession or industry only when it changes terminology, risk, compliance, or deliverable expectations.

## Existing-setup questions

Do not repeat the full fresh-start interview. Ask only:

1. Which surfaces already contain personalization?
2. Which starting posture should guide the review?
   - `preserve`: keep wording and structure; fix only clear problems.
   - `consolidate`: preserve useful intent; allow deduplication, regrouping, and rewriting. Recommend this by default because it balances continuity with cleanup.
   - `rebuild`: design a replacement, but retain the old setup until the user approves the final preview.
3. How may the current configuration be supplied: pasted content, screenshots, approved metadata inventory, or approved targeted audit?
4. What behavior must remain unchanged?

Treat the posture as a default across surfaces. Ask for a surface-specific exception only when the evidence shows that one surface needs materially different handling.

Classify existing content in groups, not line by line:

| Decision | Meaning | Default authority |
|---|---|---|
| `keep` | Correctly scoped, useful, and non-duplicative | Preserve |
| `consolidate` | Useful intent with duplication, conflict, poor placement, or excessive wording | Preview merged or rewritten form |
| `replace` | Existing content cannot meet the confirmed goal safely or clearly | Preview replacement; require confirmation |
| `retire` | Obsolete, harmful, or fully superseded content | Keep until deletion is explicitly confirmed |
| `user-decision` | Two valid intents conflict and cannot be resolved from evidence | Ask one focused question |

For each group, show the surface, current intent, issue, recommendation, reason, user impact, and focused diff when content is available. Preserve intent rather than blindly preserving wording. Never infer permission to mutate from the selected posture.

## Follow-up fields

Collect only fields that affect the result:

```yaml
profile_version: 1
setup:
  state: "fresh-start|revise-existing|unsure"
  existing_posture: "none|preserve|consolidate|rebuild"
  existing_surfaces: []
  must_preserve: []
surfaces: []
recurring_jobs:
  - job: ""
    inputs: []
    deliverable: ""
    frequency: ""
friction: []
communication:
  language: ""
  density: "concise|balanced|detailed"
  terminology_help: true
  disagreement_style: "direct|neutral|gentle"
decision_behavior:
  low_risk_ambiguity: "assume-and-state|ask"
  write_authority: "explicit-only|scoped-autonomy"
  high_impact_confirmation: true
technical_context:
  level: "nontechnical|light|practitioner|expert"
  local_projects: false
  operating_systems: []
persistence:
  account_preferences: false
  chatgpt_projects: false
  global_codex_guidance: false
  project_guidance: false
  project_memory_protocol: false
privacy:
  scan_level: "none|metadata|targeted"
  approved_paths: []
  persist_profile: false
```

Do not treat empty fields as permission to infer private facts. State low-risk assumptions and ask one consolidated question for outcome-changing gaps.
