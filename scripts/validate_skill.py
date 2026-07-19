#!/usr/bin/env python3
"""Validate the public Skill tree and release archive without third-party packages."""

import re
import sys
from pathlib import Path
from zipfile import BadZipFile, ZipFile


ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
SKILL = ROOT / "supbewhy-p13n"
ZIP = ROOT / "dist" / "supbewhy-p13n.zip"
ERRORS: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def runtime_files() -> set[str]:
    return {
        path.relative_to(ROOT).as_posix()
        for path in SKILL.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.name != ".DS_Store"
        and path.suffix not in {".pyc", ".pyo"}
    }


require((ROOT / "README.md").is_file(), "Missing README.md")
require((SKILL / "SKILL.md").is_file(), "Missing installable SKILL.md")
require((SKILL / "agents" / "openai.yaml").is_file(), "Missing agents/openai.yaml")
require((ROOT / "docs" / "images" / "fresh-start.png").is_file(), "Missing fresh-start screenshot")
require((ROOT / "docs" / "images" / "revise-existing.png").is_file(), "Missing revise-existing screenshot")
require(ZIP.is_file(), "Missing dist/supbewhy-p13n.zip")

skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8") if (SKILL / "SKILL.md").is_file() else ""
frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill_text, re.DOTALL)
require(frontmatter is not None, "Invalid YAML frontmatter boundary")
if frontmatter:
    metadata = frontmatter.group(1)
    require(re.search(r"^name:\s*supbewhy-p13n\s*$", metadata, re.MULTILINE) is not None, "Wrong Skill name")
    require(re.search(r"^description:\s*.+$", metadata, re.MULTILINE) is not None, "Missing Skill description")

for reference in sorted(set(re.findall(r"`(references/[^`]+\.md)`", skill_text))):
    require((SKILL / reference).is_file(), f"Missing referenced file: {reference}")

for script in sorted((SKILL / "scripts").glob("*.py")):
    try:
        compile(script.read_text(encoding="utf-8"), str(script), "exec")
    except SyntaxError as error:
        ERRORS.append(f"Python syntax error in {script.relative_to(ROOT)}: {error}")

public_text_files = [ROOT / "README.md", *SKILL.rglob("*.md"), *SKILL.rglob("*.yaml"), *SKILL.rglob("*.py")]
secret_patterns = {
    "macOS user path": re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    "Windows user path": re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\\\s]+"),
    "private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    "GitHub token": re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}"),
}
for path in public_text_files:
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    for label, pattern in secret_patterns.items():
        require(pattern.search(text) is None, f"Found {label} in {path.relative_to(ROOT)}")

if ZIP.is_file():
    try:
        with ZipFile(ZIP) as archive:
            names = set(archive.namelist())
            require(names == runtime_files(), "Release ZIP does not exactly match the runtime Skill tree")
            require(all(name.startswith("supbewhy-p13n/") for name in names), "Release ZIP contains an unexpected root")
    except BadZipFile:
        ERRORS.append("Release ZIP is invalid")

if ERRORS:
    for error in ERRORS:
        print(f"ERROR: {error}")
    raise SystemExit(1)

print(f"Skill release is valid: {len(runtime_files())} runtime files")
