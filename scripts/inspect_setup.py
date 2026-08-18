#!/usr/bin/env python3
"""Bounded, read-only inventory for ChatGPT/Codex personalization files."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import re
import sys
from pathlib import Path


DENIED_NAMES = {
    "auth.json",
    "history.jsonl",
    "session_index.jsonl",
    ".env",
    "credentials",
    "credentials.json",
    "cookies",
    "cookies.json",
}

DENIED_PARTS = {
    ".git",
    ".system",
    "attachments",
    "backups",
    "cache",
    "caches",
    "ipc",
    "keychain",
    "log",
    "logs",
    "node_modules",
    "plugins",
    "sessions",
    "shell_snapshots",
    "sqlite",
    ".tmp",
    "vendor",
    "vendor_imports",
    "worktrees",
}

DENIED_SUFFIXES = {".sqlite", ".db", ".db-wal", ".db-shm", ".sock"}

TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".rules",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "openai-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "github-token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    "bearer-token": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{16,}", re.I),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    "assigned-secret": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b\s*[=:]\s*[\"']?(?!\$\{|env:)[A-Za-z0-9._~+/-]{16,}"
    ),
}

ABSOLUTE_PATH_PATTERNS = {
    "posix-home": re.compile(r"(?<![A-Za-z0-9_])/(?:Users|home)/[^\s\"']+"),
    "windows-drive": re.compile(r"\b[A-Za-z]:\\[^\r\n\"']+"),
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def slug(value: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "item"
    return base[:48]


def is_denied(path: Path) -> bool:
    name = path.name.lower()
    if name in DENIED_NAMES or name.startswith(".env"):
        return True
    if any(part.lower() in DENIED_PARTS for part in path.parts):
        return True
    return any(name.endswith(suffix) for suffix in DENIED_SUFFIXES)


def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {"AGENTS.md", "MEMORY.md"}


def safe_stat(path: Path):
    try:
        return path.lstat()
    except OSError:
        return None


def iter_files(root: Path):
    if root.is_symlink():
        return
    if root.is_file():
        if not is_denied(root):
            yield root
        return
    if not root.is_dir():
        return
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if not is_denied(current_path / name) and not (current_path / name).is_symlink()
        ]
        for name in files:
            candidate = current_path / name
            if not is_denied(candidate) and not candidate.is_symlink():
                yield candidate


def summarize_path(path: Path, content_audit: bool, budget: dict) -> dict:
    total_bytes = 0
    file_count = 0
    latest_mtime = 0.0
    findings: dict[str, int] = {}
    truncated = False

    if path.is_symlink():
        return {
            "file_count": 0,
            "bytes": 0,
            "modified_at": None,
            "content_audited": False,
            "findings": {"symlink": 1},
            "truncated": False,
        }

    for file_path in iter_files(path):
        if budget["files"] >= budget["max_files"]:
            truncated = True
            break
        stat = safe_stat(file_path)
        if stat is None:
            findings["unreadable"] = findings.get("unreadable", 0) + 1
            continue
        if budget["bytes"] + stat.st_size > budget["max_bytes"]:
            truncated = True
            break
        budget["files"] += 1
        budget["bytes"] += stat.st_size
        file_count += 1
        total_bytes += stat.st_size
        latest_mtime = max(latest_mtime, stat.st_mtime)

        if not content_audit or not is_text(file_path):
            continue
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            findings["unreadable"] = findings.get("unreadable", 0) + 1
            continue
        for category, pattern in SECRET_PATTERNS.items():
            count = len(pattern.findall(text))
            if count:
                findings[category] = findings.get(category, 0) + count
        for category, pattern in ABSOLUTE_PATH_PATTERNS.items():
            count = len(pattern.findall(text))
            if count:
                findings[category] = findings.get(category, 0) + count
        placeholders = len(re.findall(r"\{\{[A-Z0-9_:-]+\}\}", text))
        if placeholders:
            findings["template-placeholders"] = findings.get("template-placeholders", 0) + placeholders

    return {
        "file_count": file_count,
        "bytes": total_bytes,
        "modified_at": (
            dt.datetime.fromtimestamp(latest_mtime, dt.timezone.utc).isoformat(timespec="seconds")
            if latest_mtime
            else None
        ),
        "content_audited": content_audit,
        "findings": findings,
        "truncated": truncated,
    }


def candidate(item_id: str, path: Path, kind: str, scope: str, portability: str, target: str) -> dict:
    return {
        "id": item_id,
        "path": str(path),
        "kind": kind,
        "scope": scope,
        "portability": portability,
        "target_template": target,
    }


def collect_candidates(home: Path, codex_home: Path, projects: list[Path]) -> tuple[list[dict], list[str]]:
    items: list[dict] = []
    warnings: list[str] = []

    fixed = [
        candidate("global-agents", codex_home / "AGENTS.md", "agents", "global", "portable", "${CODEX_HOME}/AGENTS.md"),
        candidate("global-config", codex_home / "config.toml", "config", "global", "review-required", "${CODEX_HOME}/config.toml"),
        candidate("templates", codex_home / "templates", "templates", "global", "portable", "${CODEX_HOME}/templates"),
        candidate("prompts", codex_home / "prompts", "prompts", "global", "portable", "${CODEX_HOME}/prompts"),
        candidate("hooks-json", codex_home / "hooks.json", "hooks", "global", "review-required", "${CODEX_HOME}/hooks.json"),
        candidate("hooks", codex_home / "hooks", "hooks", "global", "review-required", "${CODEX_HOME}/hooks"),
        candidate("rules", codex_home / "rules", "rules", "global", "review-required", "${CODEX_HOME}/rules"),
    ]
    items.extend(item for item in fixed if item["path"] and Path(item["path"]).exists())

    for profile_path in sorted(codex_home.glob("*.config.toml")):
        items.append(
            candidate(
                f"profile-{slug(profile_path.stem)}",
                profile_path,
                "config-profile",
                "global",
                "review-required",
                f"${{CODEX_HOME}}/{profile_path.name}",
            )
        )

    skill_roots = [
        (codex_home / "skills", "${CODEX_HOME}/skills", "codex"),
        (home / ".agents" / "skills", "${HOME}/.agents/skills", "agents"),
    ]
    for root, target_root, label in skill_roots:
        if not root.is_dir():
            continue
        for skill_path in sorted(root.iterdir()):
            if not skill_path.is_dir() or skill_path.is_symlink() or skill_path.name.startswith("."):
                continue
            items.append(
                candidate(
                    f"skill-{label}-{slug(skill_path.name)}",
                    skill_path,
                    "skill",
                    "global",
                    "select-required",
                    f"{target_root}/{skill_path.name}",
                )
            )

    for index, project in enumerate(projects, start=1):
        project = project.expanduser().resolve()
        project_key = f"p{index}-{hashlib.sha256(str(project).encode()).hexdigest()[:8]}"
        if not project.is_dir():
            warnings.append(f"Project root does not exist: {project}")
            continue
        project_fixed = [
            ("agents", project / "AGENTS.md", "agents", "portable"),
            ("memory", project / "MEMORY.md", "memory", "portable"),
            ("config", project / ".codex" / "config.toml", "config", "review-required"),
            ("hooks", project / ".codex" / "hooks.json", "hooks", "review-required"),
            ("rules", project / ".codex" / "rules", "rules", "review-required"),
            ("skills", project / ".agents" / "skills", "skills", "select-required"),
        ]
        for suffix, path, kind, portability in project_fixed:
            if path.exists():
                relative = path.relative_to(project).as_posix()
                items.append(
                    candidate(
                        f"project-{project_key}-{suffix}",
                        path,
                        kind,
                        "project",
                        "project-bound" if portability == "portable" else portability,
                        f"${{PROJECT_ROOT:{project_key}}}/{relative}",
                    )
                )

    return items, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, help="Codex home; defaults to CODEX_HOME or ~/.codex")
    parser.add_argument("--project", action="append", default=[], type=Path, help="Approved project root; repeatable")
    parser.add_argument("--content-audit", action="store_true", help="Read approved text files for risk categories")
    parser.add_argument("--max-files", type=int, default=500)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    parser.add_argument("--output", type=Path, help="Write JSON report; stdout when omitted")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_files < 1 or args.max_bytes < 1:
        raise SystemExit("--max-files and --max-bytes must be positive")

    home_input = Path.home().expanduser()
    home = home_input.resolve()
    codex_home_input = (args.codex_home or Path(os.environ.get("CODEX_HOME", home_input / ".codex"))).expanduser()
    codex_home = codex_home_input.resolve()
    candidates, warnings = collect_candidates(home, codex_home, args.project)
    budget = {"files": 0, "bytes": 0, "max_files": args.max_files, "max_bytes": args.max_bytes}
    items: list[dict] = []

    for item in candidates:
        path = Path(item["path"])
        if is_denied(path):
            warnings.append(f"Denied candidate excluded: {path}")
            continue
        details = summarize_path(path, args.content_audit, budget)
        items.append({**item, **details})
        if details["truncated"]:
            warnings.append(f"Budget reached while inspecting: {path}")
            break

    report = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "scan_mode": "targeted-content" if args.content_audit else "metadata",
        "platform": {"system": platform.system(), "release": platform.release()},
        "home": str(home),
        "codex_home": str(codex_home),
        "path_aliases": {
            "home": sorted({str(home_input), str(home)}),
            "codex_home": sorted({str(codex_home_input), str(codex_home)}),
        },
        "scan_roots": [str(codex_home), str(home / ".agents" / "skills")]
        + [str(path.expanduser().resolve()) for path in args.project],
        "limits": {"max_files": args.max_files, "max_bytes": args.max_bytes},
        "observed": {"files": budget["files"], "bytes": budget["bytes"]},
        "items": items,
        "warnings": warnings,
        "denied_categories": sorted(DENIED_PARTS | DENIED_NAMES),
    }
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
