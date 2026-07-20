import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "supbewhy-p13n" / "SKILL.md"
INTERACTION = ROOT / "supbewhy-p13n" / "references" / "interactive-onboarding.md"
PRIVACY = ROOT / "supbewhy-p13n" / "references" / "privacy-scan-policy.md"
MIGRATION = ROOT / "supbewhy-p13n" / "references" / "migration-policy.md"


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SKILL.read_text(encoding="utf-8")
        cls.interaction = INTERACTION.read_text(encoding="utf-8")
        cls.privacy = PRIVACY.read_text(encoding="utf-8")
        cls.migration = MIGRATION.read_text(encoding="utf-8")

    def test_setup_routes_are_present(self) -> None:
        for route in ("fresh-start", "revise-existing", "unsure"):
            self.assertIn(route, self.text)

    def test_retention_postures_are_present(self) -> None:
        for posture in ("Preserve", "Consolidate", "Rebuild"):
            self.assertIn(posture, self.text)

    def test_interaction_fallback_is_required(self) -> None:
        self.assertIn("numbered text equivalent", self.text)
        self.assertIn("`back`, `skip`, `pause`", self.text)

    def test_high_impact_actions_use_confirmation_gates(self) -> None:
        self.assertIn("localized equivalent of `Waiting for authorization — no action has run`", self.text)
        self.assertIn("Never offer `skip` or its localized equivalent", self.text)
        self.assertIn("Any action, mode, path, cap, destination, or conflict-policy change requires new approval", self.text)

    def test_visible_interactions_follow_codex_language(self) -> None:
        self.assertIn("Resolve `interaction_language`", self.text)
        self.assertIn("Do not use the language of this Skill file or its examples as the user's language", self.text)
        self.assertIn("Localize every visible status, heading, field label", self.text)
        self.assertIn("current Codex response language or the dominant language of the conversation", self.interaction)
        self.assertIn("Keep paths, commands, code, item IDs, enum values, and structured follow-up keys unchanged", self.interaction)
        self.assertIn("For Simplified Chinese", self.interaction)

    def test_confirmation_followup_preserves_explicit_authority(self) -> None:
        self.assertIn("authorization=approved|adjust|cancelled", self.interaction)
        self.assertIn("Do not execute from hidden browser state", self.interaction)
        self.assertIn("A missing, ambiguous, defaulted, or skipped response is not approval", self.interaction)

    def test_privacy_scope_changes_require_reapproval(self) -> None:
        self.assertIn("A default selection, an opened surface", self.privacy)
        self.assertIn("invalidates the earlier approval and requires a new confirmation", self.privacy)

    def test_migration_uses_the_same_confirmation_boundary(self) -> None:
        self.assertIn("Export, import, and rollback approvals use the mandatory confirmation gate", self.migration)
        self.assertIn("A changed destination, item set, target root, conflict decision, or replacement set invalidates the earlier approval", self.migration)

    def test_advice_does_not_authorize_writes(self) -> None:
        self.assertIn("never authorize `apply`", self.text)
        self.assertIn("Do not write until the user confirms", self.text)

    def test_backup_boundaries_are_explicit(self) -> None:
        self.assertIn("do not create a backup because nothing is being replaced", self.text)
        self.assertIn("create the dated backup and transaction record automatically", self.text)
        self.assertIn("do not claim an automatic cloud backup", self.text)

    def test_migration_has_preview_verify_and_rollback(self) -> None:
        for mode in ("migration-import-preview", "migration-verify", "migration-rollback"):
            self.assertIn(mode, self.text)

    def test_forbidden_state_is_excluded(self) -> None:
        for term in ("tokens", "sessions", "logs", "caches", "history", "keychains"):
            self.assertIn(term, self.text)


if __name__ == "__main__":
    unittest.main()
