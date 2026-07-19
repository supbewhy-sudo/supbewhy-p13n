import subprocess
import sys
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]


class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_release.py")], check=True, cwd=ROOT)

    def test_readme_images_exist(self) -> None:
        for image in ("fresh-start.png", "revise-existing.png"):
            self.assertTrue((ROOT / "docs" / "images" / image).is_file())

    def test_zip_has_installable_root(self) -> None:
        with ZipFile(ROOT / "dist" / "supbewhy-p13n.zip") as archive:
            names = archive.namelist()
        self.assertIn("supbewhy-p13n/SKILL.md", names)
        self.assertTrue(all(name.startswith("supbewhy-p13n/") for name in names))

    def test_zip_excludes_runtime_noise(self) -> None:
        with ZipFile(ROOT / "dist" / "supbewhy-p13n.zip") as archive:
            names = archive.namelist()
        self.assertFalse(any("__pycache__" in name or name.endswith((".pyc", ".pyo")) for name in names))

    def test_public_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_skill.py"), str(ROOT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
