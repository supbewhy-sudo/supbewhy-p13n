#!/usr/bin/env python3
"""Create, preview, import, verify, and roll back sanitized Codex personalization bundles."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import zipfile
from pathlib import Path

from inspect_setup import ABSOLUTE_PATH_PATTERNS, SECRET_PATTERNS, is_denied, is_text, iter_files


FORMAT_VERSION = 1
MAX_DEFAULT_FILE_BYTES = 10_000_000
MAX_DEFAULT_TOTAL_BYTES = 50_000_000
PLACEHOLDER_PATTERN = re.compile(r"\$\{(?:HOME|CODEX_HOME|PROJECT_ROOT:[A-Za-z0-9_-]+)\}")
HIGH_RISK_KINDS = {"agents", "config", "config-profile", "hooks", "rules"}


class MigrationError(RuntimeError):
    pass


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json_text(value), encoding="utf-8")
    temporary.replace(path)


def within(path: Path, roots: list[Path]) -> bool:
    resolved = path.resolve(strict=False)
    for root in roots:
        try:
            resolved.relative_to(root.resolve(strict=False))
            return True
        except ValueError:
            continue
    return False


def ensure_safe_zip_name(name: str) -> None:
    pure = Path(name)
    if pure.is_absolute() or ".." in pure.parts or name.startswith(("/", "\\")):
        raise MigrationError(f"Unsafe archive path: {name}")


def secret_categories(text: str) -> list[str]:
    return sorted(category for category, pattern in SECRET_PATTERNS.items() if pattern.search(text))


def absolute_path_counts(text: str) -> dict[str, int]:
    findings = {}
    for category, pattern in ABSOLUTE_PATH_PATTERNS.items():
        count = len(pattern.findall(text))
        if count:
            findings[category] = count
    return findings


def replace_source_roots(text: str, source_homes: list[str], source_codex_homes: list[str]) -> tuple[str, list[str]]:
    changes = []
    replacements = [(value, "${CODEX_HOME}") for value in source_codex_homes]
    replacements.extend((value, "${HOME}") for value in source_homes)
    ordered = sorted(set(replacements), key=lambda item: len(item[0]), reverse=True)
    for source, placeholder in ordered:
        if source and source in text:
            text = text.replace(source, placeholder)
            changes.append(f"replaced-with:{placeholder}")
    return text, changes


def parse_project_maps(values: list[str]) -> dict[str, Path]:
    result = {}
    for value in values:
        if "=" not in value:
            raise MigrationError(f"Invalid project map, expected ID=PATH: {value}")
        key, raw_path = value.split("=", 1)
        if not key or not raw_path:
            raise MigrationError(f"Invalid project map: {value}")
        result[key] = Path(raw_path).expanduser().resolve()
    return result


def resolve_target(template: str, home: Path, codex_home: Path, project_maps: dict[str, Path]) -> tuple[Path | None, str | None]:
    rendered = template.replace("${CODEX_HOME}", str(codex_home)).replace("${HOME}", str(home))
    for key, path in project_maps.items():
        rendered = rendered.replace(f"${{PROJECT_ROOT:{key}}}", str(path))
    unresolved = PLACEHOLDER_PATTERN.search(rendered)
    if unresolved:
        return None, f"Missing mapping for {unresolved.group(0)}"
    return Path(rendered).expanduser(), None


def render_payload(data: bytes, text_file: bool, home: Path, codex_home: Path, project_maps: dict[str, Path]) -> bytes:
    if not text_file:
        return data
    text = data.decode("utf-8")
    text = text.replace("${CODEX_HOME}", str(codex_home)).replace("${HOME}", str(home))
    for key, path in project_maps.items():
        text = text.replace(f"${{PROJECT_ROOT:{key}}}", str(path))
    return text.encode("utf-8")


def load_inventory(path: Path) -> dict:
    try:
        inventory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MigrationError(f"Cannot read inventory: {exc}") from exc
    if inventory.get("schema_version") != 1 or not isinstance(inventory.get("items"), list):
        raise MigrationError("Unsupported or malformed inventory")
    return inventory


def selected_items(inventory: dict, include: list[str]) -> list[dict]:
    by_id = {item.get("id"): item for item in inventory["items"]}
    if include:
        missing = [item_id for item_id in include if item_id not in by_id]
        if missing:
            raise MigrationError(f"Unknown inventory item IDs: {', '.join(missing)}")
        return [by_id[item_id] for item_id in include]
    return [
        item
        for item in inventory["items"]
        if item.get("portability") == "portable" and item.get("scope") == "global"
    ]


def command_audit(args: argparse.Namespace) -> int:
    inventory = load_inventory(args.inventory)
    summary: dict[str, int] = {}
    for item in inventory["items"]:
        key = item.get("portability", "unknown")
        summary[key] = summary.get(key, 0) + 1
    result = {
        "inventory": str(args.inventory),
        "scan_mode": inventory.get("scan_mode"),
        "items": len(inventory["items"]),
        "classifications": summary,
        "warnings": inventory.get("warnings", []),
    }
    sys.stdout.write(json_text(result))
    return 0


def command_export(args: argparse.Namespace) -> int:
    if args.confirm != "EXPORT":
        raise MigrationError("Export requires --confirm EXPORT after the user approves the selected item IDs")
    inventory = load_inventory(args.inventory)
    items = selected_items(inventory, args.include)
    if not items:
        raise MigrationError("No exportable items selected")

    roots = [Path(value).expanduser().resolve() for value in inventory.get("scan_roots", [])]
    aliases = inventory.get("path_aliases", {})
    source_homes = aliases.get("home") or [inventory["home"]]
    source_codex_homes = aliases.get("codex_home") or [inventory["codex_home"]]
    payloads: list[tuple[str, bytes]] = []
    manifest_files = []
    total_bytes = 0
    seen_archives = set()
    seen_targets = set()

    for item in items:
        root = Path(item["path"]).expanduser()
        if not within(root, roots):
            raise MigrationError(f"Inventory item is outside approved scan roots: {item['id']}")
        if not root.exists():
            raise MigrationError(f"Selected item no longer exists: {item['id']}")
        if root.is_symlink() or is_denied(root):
            raise MigrationError(f"Selected item is denied or a symlink: {item['id']}")

        files = list(iter_files(root))
        if not files:
            continue
        for file_path in files:
            if file_path.is_symlink() or is_denied(file_path):
                continue
            raw = file_path.read_bytes()
            if len(raw) > args.max_file_bytes:
                raise MigrationError(f"File exceeds size cap: {item['id']}/{file_path.name}")
            total_bytes += len(raw)
            if total_bytes > args.max_total_bytes:
                raise MigrationError("Selected files exceed total export size cap")

            relative = Path(file_path.name) if root.is_file() else file_path.relative_to(root)
            archive_name = f"payload/{item['id']}/{relative.as_posix()}"
            ensure_safe_zip_name(archive_name)
            target = item["target_template"] if root.is_file() else f"{item['target_template'].rstrip('/')}/{relative.as_posix()}"
            if archive_name in seen_archives or target in seen_targets:
                raise MigrationError(f"Duplicate archive or target path: {item['id']}/{relative}")
            seen_archives.add(archive_name)
            seen_targets.add(target)

            text_file = is_text(file_path)
            transformations = []
            path_findings = {}
            data = raw
            if text_file:
                try:
                    text = raw.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise MigrationError(f"Text file is not valid UTF-8: {item['id']}/{relative}") from exc
                secrets = secret_categories(text)
                if secrets:
                    raise MigrationError(
                        f"Possible secret blocks export in {item['id']}/{relative}: {', '.join(secrets)}"
                    )
                text, transformations = replace_source_roots(text, source_homes, source_codex_homes)
                path_findings = absolute_path_counts(text)
                data = text.encode("utf-8")

            stat_result = file_path.stat()
            executable = bool(stat_result.st_mode & stat.S_IXUSR)
            payloads.append((archive_name, data))
            manifest_files.append(
                {
                    "item_id": item["id"],
                    "kind": item.get("kind", "unknown"),
                    "scope": item.get("scope", "unknown"),
                    "portability": item.get("portability", "unknown"),
                    "archive": archive_name,
                    "target_template": target,
                    "sha256": sha256(data),
                    "bytes": len(data),
                    "text": text_file,
                    "executable": executable,
                    "transformations": transformations,
                    "remaining_absolute_paths": path_findings,
                }
            )

    if not manifest_files:
        raise MigrationError("Selected items contain no eligible files")

    manifest = {
        "format_version": FORMAT_VERSION,
        "created_at": iso_now(),
        "source": {
            "platform": inventory.get("platform", {}),
            "scan_mode": inventory.get("scan_mode"),
        },
        "selected_item_ids": [item["id"] for item in items],
        "files": manifest_files,
        "manual_actions": [
            "Sign in to ChatGPT/Codex on the target device.",
            "Verify cloud Custom Instructions and Projects instead of recreating them.",
            "Reinstall Plugins and unknown third-party Skills from trusted sources.",
            "Repeat MCP OAuth, connector authorization, and operating-system permissions.",
        ],
    }
    export_report = "\n".join(
        [
            "# Export report",
            "",
            f"- Created: {manifest['created_at']}",
            f"- Selected items: {', '.join(manifest['selected_item_ids'])}",
            f"- Files: {len(manifest_files)}",
            f"- Payload bytes: {sum(entry['bytes'] for entry in manifest_files)}",
            "- Credentials, history, sessions, caches, logs, and databases are excluded.",
            "- Files with remaining absolute paths require manual review before import.",
            "",
        ]
    )
    manual_report = "# Manual reconfiguration\n\n" + "\n".join(
        f"- {action}" for action in manifest["manual_actions"]
    ) + "\n"
    checksums = "".join(f"{entry['sha256']}  {entry['archive']}\n" for entry in manifest_files)

    output = args.output.expanduser()
    if output.suffix.lower() != ".zip":
        raise MigrationError("Export output must end with .zip")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json_text(manifest))
        archive.writestr("checksums.sha256", checksums)
        archive.writestr("reports/export-report.md", export_report)
        archive.writestr("reports/manual-reconfiguration.md", manual_report)
        for name, data in payloads:
            archive.writestr(name, data)
    temporary.replace(output)
    sys.stdout.write(json_text({"bundle": str(output), "files": len(manifest_files), "bytes": output.stat().st_size}))
    return 0


def open_bundle(path: Path) -> tuple[zipfile.ZipFile, dict]:
    try:
        archive = zipfile.ZipFile(path, "r")
    except (OSError, zipfile.BadZipFile) as exc:
        raise MigrationError(f"Cannot open migration bundle: {exc}") from exc
    names = archive.namelist()
    if len(names) != len(set(names)):
        archive.close()
        raise MigrationError("Migration bundle contains duplicate archive paths")
    total_size = 0
    for info in archive.infolist():
        name = info.filename
        ensure_safe_zip_name(name)
        if info.file_size > MAX_DEFAULT_FILE_BYTES:
            archive.close()
            raise MigrationError(f"Archive entry exceeds size cap: {name}")
        total_size += info.file_size
        if total_size > MAX_DEFAULT_TOTAL_BYTES + 1_000_000:
            archive.close()
            raise MigrationError("Migration bundle exceeds uncompressed size cap")
    try:
        manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        archive.close()
        raise MigrationError(f"Invalid manifest: {exc}") from exc
    if manifest.get("format_version") != FORMAT_VERSION or not isinstance(manifest.get("files"), list):
        archive.close()
        raise MigrationError("Unsupported migration bundle version")
    return archive, manifest


def evaluate_bundle(args: argparse.Namespace) -> tuple[dict, dict[str, bytes]]:
    home = args.target_home.expanduser().resolve() if args.target_home else Path.home().resolve()
    codex_home = (
        args.target_codex_home.expanduser().resolve()
        if args.target_codex_home
        else Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser().resolve()
    )
    project_maps = parse_project_maps(args.project_map)
    approved_review = set(args.approve_review)
    allowed_roots = [codex_home, home / ".agents" / "skills", *project_maps.values()]
    archive, manifest = open_bundle(args.bundle)
    results = []
    rendered_payloads: dict[str, bytes] = {}
    try:
        for entry in manifest["files"]:
            archive_name = entry.get("archive", "")
            item_id = entry.get("item_id") or f"unknown:{archive_name}"
            kind = entry.get("kind", "unknown")
            base_result = {"archive": archive_name, "item_id": item_id, "kind": kind}
            ensure_safe_zip_name(archive_name)
            try:
                source_data = archive.read(archive_name)
            except KeyError:
                results.append({**base_result, "status": "blocked", "reason": "Missing payload"})
                continue
            if sha256(source_data) != entry.get("sha256"):
                results.append({**base_result, "status": "blocked", "reason": "Checksum mismatch"})
                continue

            target, error = resolve_target(entry.get("target_template", ""), home, codex_home, project_maps)
            if error or target is None:
                results.append({**base_result, "status": "blocked", "reason": error})
                continue
            target = target.resolve(strict=False)
            if not within(target, allowed_roots):
                results.append(
                    {**base_result, "target": str(target), "status": "blocked", "reason": "Target outside approved roots"}
                )
                continue
            if is_denied(target):
                results.append(
                    {**base_result, "target": str(target), "status": "blocked", "reason": "Target is a denied state path"}
                )
                continue
            if target.is_symlink():
                results.append(
                    {**base_result, "target": str(target), "status": "blocked", "reason": "Target is a symlink"}
                )
                continue

            try:
                rendered = render_payload(source_data, bool(entry.get("text")), home, codex_home, project_maps)
            except UnicodeDecodeError:
                results.append(
                    {**base_result, "target": str(target), "status": "blocked", "reason": "Invalid UTF-8 text payload"}
                )
                continue
            if entry.get("text"):
                text = rendered.decode("utf-8")
                secrets = secret_categories(text)
                if secrets:
                    results.append(
                        {
                            **base_result,
                            "target": str(target),
                            "status": "blocked",
                            "reason": f"Possible secret: {', '.join(secrets)}",
                        }
                    )
                    continue
                unresolved = PLACEHOLDER_PATTERN.search(text)
                if unresolved:
                    results.append(
                        {
                            **base_result,
                            "target": str(target),
                            "status": "blocked",
                            "reason": f"Unresolved placeholder: {unresolved.group(0)}",
                        }
                    )
                    continue

            review_reasons = []
            if entry.get("portability") in {"review-required", "select-required"}:
                review_reasons.append(entry.get("portability"))
            if entry.get("remaining_absolute_paths"):
                review_reasons.append("remaining absolute paths")
            if not entry.get("text"):
                review_reasons.append("binary payload")
            if entry.get("executable"):
                review_reasons.append("executable payload")
            if review_reasons and entry.get("item_id") not in approved_review:
                results.append(
                    {
                        **base_result,
                        "target": str(target),
                        "status": "review-required",
                        "reason": ", ".join(review_reasons),
                    }
                )
                rendered_payloads[archive_name] = rendered
                continue

            rendered_payloads[archive_name] = rendered
            if not target.exists():
                status_value = "create"
            elif not target.is_file():
                status_value = "blocked"
                error = "Target exists and is not a regular file"
            else:
                try:
                    status_value = "identical" if target.read_bytes() == rendered else "conflict"
                except OSError as exc:
                    status_value = "blocked"
                    error = f"Cannot read target: {exc}"
            result = {
                **base_result,
                "target": str(target),
                "status": status_value,
            }
            if status_value == "blocked":
                result["reason"] = error
            results.append(result)
    finally:
        archive.close()

    report = {
        "bundle": str(args.bundle),
        "target_home": str(home),
        "target_codex_home": str(codex_home),
        "approved_roots": [str(path) for path in allowed_roots],
        "results": results,
        "summary": {},
    }
    for result in results:
        status_value = result["status"]
        report["summary"][status_value] = report["summary"].get(status_value, 0) + 1
    report["recommended_plan"] = build_recommended_plan(results)
    return report, rendered_payloads


def build_recommended_plan(results: list[dict]) -> dict:
    grouped: dict[str, dict] = {}
    for result in results:
        item_id = result["item_id"]
        group = grouped.setdefault(
            item_id,
            {
                "item_id": item_id,
                "kind": result.get("kind", "unknown"),
                "files": 0,
                "statuses": {},
            },
        )
        group["files"] += 1
        status_value = result["status"]
        group["statuses"][status_value] = group["statuses"].get(status_value, 0) + 1

    action_summary: dict[str, int] = {}
    groups = []
    for group in grouped.values():
        statuses = group["statuses"]
        kind = group["kind"]
        if statuses.get("blocked"):
            action = "stop"
            attention = "high"
            reason = "包含被阻止的文件，必须先解决安全或映射问题。"
            alternatives = []
        elif statuses.get("review-required"):
            action = "review-first"
            attention = "high"
            reason = "包含路径、权限、二进制、可执行内容或需选择的 Skill，审核前不导入。"
            alternatives = ["approve-review", "keep-target"]
        elif statuses.get("conflict"):
            action = "manual-merge" if kind in HIGH_RISK_KINDS else "keep-target"
            attention = "high" if kind in HIGH_RISK_KINDS else "normal"
            reason = (
                "高影响配置发生冲突，推荐保留目标并由 Codex 展示差异后合并。"
                if kind in HIGH_RISK_KINDS
                else "目标已有同名项目，推荐完整保留目标版本。"
            )
            alternatives = ["keep-target", "replace-from-bundle", "manual-merge"]
        elif statuses.get("create"):
            action = "create"
            attention = "normal"
            reason = "目标缺失，确认总方案后创建。"
            alternatives = ["create", "skip"]
        else:
            action = "skip-identical"
            attention = "none"
            reason = "目标内容相同，无需操作。"
            alternatives = ["skip"]
        action_summary[action] = action_summary.get(action, 0) + 1
        groups.append(
            {
                **group,
                "recommended_action": action,
                "attention": attention,
                "reason": reason,
                "alternatives": alternatives,
            }
        )

    return {
        "mode": "safe-default",
        "one_click_action": "确认后创建缺失项目；相同项目跳过；冲突项目按 item 完整保留。",
        "customization": "仅在用户展开调整时，对指定 item 使用 --replace ITEM_ID 或 --keep ITEM_ID。",
        "action_summary": action_summary,
        "groups": groups,
    }


def validate_item_decisions(report: dict, keep_items: set[str], replace_items: set[str]) -> set[str]:
    known_items = {group["item_id"] for group in report["recommended_plan"]["groups"]}
    unknown = sorted((keep_items | replace_items) - known_items)
    if unknown:
        raise MigrationError(f"Unknown decision item IDs: {', '.join(unknown)}")
    overlap = sorted(keep_items & replace_items)
    if overlap:
        raise MigrationError(f"Items cannot be both kept and replaced: {', '.join(overlap)}")
    conflict_items = {
        group["item_id"]
        for group in report["recommended_plan"]["groups"]
        if group["statuses"].get("conflict")
    }
    invalid = sorted((keep_items | replace_items) - conflict_items)
    if invalid:
        raise MigrationError(f"Item decisions are only valid for conflicts: {', '.join(invalid)}")
    return conflict_items


def emit_report(report: dict, output: Path | None) -> None:
    if output:
        write_json(output, report)
    else:
        sys.stdout.write(json_text(report))


def command_preview(args: argparse.Namespace) -> int:
    report, _ = evaluate_bundle(args)
    emit_report(report, args.output)
    return 2 if report["summary"].get("blocked") else 0


def journal_write(backup_dir: Path, journal: dict) -> None:
    write_json(backup_dir / "journal.json", journal)


def command_import(args: argparse.Namespace) -> int:
    if args.confirm != "APPLY":
        raise MigrationError("Import requires --confirm APPLY after preview and explicit user approval")
    report, payloads = evaluate_bundle(args)
    if report["summary"].get("blocked") or report["summary"].get("review-required"):
        raise MigrationError("Import blocked; resolve blocked and review-required results first")
    keep_items = set(args.keep)
    replace_items = set(args.replace)
    conflict_items = validate_item_decisions(report, keep_items, replace_items)
    kept_items = conflict_items - replace_items

    codex_home = Path(report["target_codex_home"])
    backup_root = args.backup_root.expanduser().resolve() if args.backup_root else codex_home / "backups"
    backup_dir = backup_root / f"supbewhy-p13n-import-{now_stamp()}"
    backup_dir.mkdir(parents=True, exist_ok=False)
    journal = {
        "format_version": FORMAT_VERSION,
        "created_at": iso_now(),
        "bundle": str(args.bundle),
        "approved_roots": report["approved_roots"],
        "entries": [],
        "complete": False,
        "rolled_back": False,
        "decisions": {
            "kept_items": sorted(kept_items),
            "replaced_items": sorted(replace_items),
        },
    }
    journal_write(backup_dir, journal)

    archive, manifest = open_bundle(args.bundle)
    manifest_by_archive = {entry["archive"]: entry for entry in manifest["files"]}
    archive.close()
    applied = 0
    skipped = 0
    try:
        for result in report["results"]:
            status_value = result["status"]
            item_id = result["item_id"]
            if status_value == "identical":
                skipped += 1
                continue
            if status_value not in {"create", "conflict"}:
                continue
            if item_id in kept_items:
                skipped += 1
                continue

            target = Path(result["target"])
            entry = manifest_by_archive[result["archive"]]
            data = payloads[result["archive"]]
            record = {
                "target": str(target),
                "existed": target.exists(),
                "backup": None,
                "archive": result["archive"],
            }
            if target.exists():
                backup_file = backup_dir / "files" / f"{len(journal['entries']):06d}"
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup_file)
                record["backup"] = str(backup_file.relative_to(backup_dir))
            journal["entries"].append(record)
            journal_write(backup_dir, journal)

            target.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.p13n-", dir=target.parent)
            temporary = Path(temporary_name)
            try:
                with os.fdopen(descriptor, "wb") as handle:
                    handle.write(data)
                os.chmod(temporary, 0o755 if entry.get("executable") else 0o644)
                temporary.replace(target)
            except Exception:
                temporary.unlink(missing_ok=True)
                raise
            record["applied_sha256"] = sha256(data)
            journal_write(backup_dir, journal)
            applied += 1

        journal["complete"] = True
        journal["completed_at"] = iso_now()
        journal_write(backup_dir, journal)
    except Exception:
        journal["failed_at"] = iso_now()
        journal_write(backup_dir, journal)
        raise

    result = {
        "backup": str(backup_dir),
        "applied": applied,
        "skipped": skipped,
        "kept_items": sorted(kept_items),
        "replaced_items": sorted(replace_items),
        "preview": report["summary"],
    }
    sys.stdout.write(json_text(result))
    return 0


def command_verify(args: argparse.Namespace) -> int:
    report, _ = evaluate_bundle(args)
    accepted_keep = set(args.keep)
    known_items = {group["item_id"] for group in report["recommended_plan"]["groups"]}
    unknown = sorted(accepted_keep - known_items)
    if unknown:
        raise MigrationError(f"Unknown kept item IDs: {', '.join(unknown)}")
    failures = []
    accepted = []
    for result in report["results"]:
        if result["status"] == "identical":
            continue
        if result["item_id"] in accepted_keep and result["status"] in {"create", "conflict"}:
            accepted.append(result)
        else:
            failures.append(result)
    verification = {**report, "verified": not failures, "accepted_keep": accepted, "failures": failures}
    emit_report(verification, args.output)
    return 0 if not failures else 2


def command_rollback(args: argparse.Namespace) -> int:
    if args.confirm != "ROLLBACK":
        raise MigrationError("Rollback requires --confirm ROLLBACK after reviewing the journal")
    backup_dir = args.backup.expanduser().resolve()
    journal_path = backup_dir / "journal.json"
    try:
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MigrationError(f"Cannot read rollback journal: {exc}") from exc
    if journal.get("format_version") != FORMAT_VERSION or not isinstance(journal.get("entries"), list):
        raise MigrationError("Unsupported rollback journal")
    if journal.get("rolled_back"):
        raise MigrationError("This transaction was already rolled back")
    allowed_roots = [Path(value).resolve() for value in journal.get("approved_roots", [])]
    restored = 0
    removed = 0

    for record in reversed(journal["entries"]):
        target = Path(record["target"]).resolve(strict=False)
        if not within(target, allowed_roots) or is_denied(target) or target.is_symlink():
            raise MigrationError(f"Unsafe rollback target: {target}")
        applied_hash = record.get("applied_sha256")
        if applied_hash and target.is_file() and sha256(target.read_bytes()) != applied_hash:
            raise MigrationError(f"Target changed after import; review before rollback: {target}")
        if record.get("existed"):
            backup_relative = record.get("backup")
            if not backup_relative:
                raise MigrationError(f"Missing backup reference for: {target}")
            backup_file = (backup_dir / backup_relative).resolve()
            if not within(backup_file, [backup_dir]) or not backup_file.is_file():
                raise MigrationError(f"Unsafe or missing backup file for: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_file, target)
            restored += 1
        elif target.exists():
            if not target.is_file():
                raise MigrationError(f"Refusing to remove non-file rollback target: {target}")
            target.unlink()
            removed += 1

    journal["rolled_back"] = True
    journal["rolled_back_at"] = iso_now()
    journal_write(backup_dir, journal)
    sys.stdout.write(json_text({"backup": str(backup_dir), "restored": restored, "removed": removed}))
    return 0


def add_target_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--target-home", type=Path)
    parser.add_argument("--target-codex-home", type=Path)
    parser.add_argument("--project-map", action="append", default=[], metavar="ID=PATH")
    parser.add_argument("--approve-review", action="append", default=[], metavar="ITEM_ID")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Summarize an inventory")
    audit.add_argument("--inventory", required=True, type=Path)
    audit.set_defaults(func=command_audit)

    export = subparsers.add_parser("export", help="Create a sanitized ZIP bundle")
    export.add_argument("--inventory", required=True, type=Path)
    export.add_argument("--output", required=True, type=Path)
    export.add_argument("--include", action="append", default=[], metavar="ITEM_ID")
    export.add_argument("--max-file-bytes", type=int, default=MAX_DEFAULT_FILE_BYTES)
    export.add_argument("--max-total-bytes", type=int, default=MAX_DEFAULT_TOTAL_BYTES)
    export.add_argument("--confirm")
    export.set_defaults(func=command_export)

    preview = subparsers.add_parser("preview", help="Dry-run a bundle on a target")
    add_target_args(preview)
    preview.add_argument("--output", type=Path)
    preview.set_defaults(func=command_preview)

    import_parser = subparsers.add_parser("import", help="Back up and import confirmed files")
    add_target_args(import_parser)
    import_parser.add_argument("--keep", action="append", default=[], metavar="ITEM_ID")
    import_parser.add_argument("--replace", action="append", default=[], metavar="ITEM_ID")
    import_parser.add_argument("--backup-root", type=Path)
    import_parser.add_argument("--confirm")
    import_parser.set_defaults(func=command_import)

    verify = subparsers.add_parser("verify", help="Verify imported targets match a bundle")
    add_target_args(verify)
    verify.add_argument("--keep", action="append", default=[], metavar="ITEM_ID")
    verify.add_argument("--output", type=Path)
    verify.set_defaults(func=command_verify)

    rollback = subparsers.add_parser("rollback", help="Restore an import transaction")
    rollback.add_argument("--backup", required=True, type=Path)
    rollback.add_argument("--confirm")
    rollback.set_defaults(func=command_rollback)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except MigrationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
