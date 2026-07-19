#!/usr/bin/env python3
"""Build a deterministic release ZIP containing the installable Skill directory."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "supbewhy-p13n"
OUTPUT = ROOT / "dist" / "supbewhy-p13n.zip"
FIXED_TIME = (2026, 7, 20, 0, 0, 0)


def runtime_files() -> list[Path]:
    return sorted(
        path
        for path in SKILL.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.name != ".DS_Store"
        and path.suffix not in {".pyc", ".pyo"}
    )


def build() -> Path:
    if not (SKILL / "SKILL.md").is_file():
        raise SystemExit("Missing supbewhy-p13n/SKILL.md")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for path in runtime_files():
            relative = path.relative_to(ROOT).as_posix()
            info = ZipInfo(relative, FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = (path.stat().st_mode & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes())
    return OUTPUT


if __name__ == "__main__":
    print(build())
