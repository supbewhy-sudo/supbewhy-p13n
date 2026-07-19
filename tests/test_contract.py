import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "supbewhy-p13n" / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_setup_routes_are_present(self) -> None:
        for route in ("fresh-start", "revise-existing", "unsure"):
            self.assertIn(route, self.text)

    def test_retention_postures_are_present(self) -> None:
        for posture in ("Preserve", "Consolidate", "Rebuild"):
            self.assertIn(posture, self.text)

    def test_interaction_fallback_is_required(self) -> None:
        self.assertIn("numbered text equivalent", self.text)
        self.assertIn("`back`, `skip`, `pause`", self.text)

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
