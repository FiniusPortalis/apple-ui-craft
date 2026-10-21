#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Iterable

SCHEMA_VERSION = 1
SAFE_REPORT_SUFFIXES = {".md", ".txt", ".json", ".sarif"}
FORBIDDEN_REPORT_PARTS = {
    ".git",
    ".agents",
    ".build",
    "build",
    "deriveddata",
    "plans",
    "sources",
    "source",
    "tests",
    "test",
}
DEFAULT_EXCLUDES = (
    ".git",
    ".git/**",
    ".build",
    ".build/**",
    "DerivedData",
    "DerivedData/**",
    "build",
    "build/**",
    "**/__pycache__",
    "**/__pycache__/**",
    "**/*.pyc",
    "**/*.pyo",
)


class GuardError(RuntimeError):
    pass


@dataclass(frozen=True)
class Entry:
    kind: str
    size: int
    sha256: str
    link_target: str | None = None

    def as_json(self) -> dict[str, object]:
        value: dict[str, object] = {
            "kind": self.kind,
            "size": self.size,
            "sha256": self.sha256,
        }
        if self.link_target is not None:
            value["link_target"] = self.link_target
        return value


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            size += len(block)
            digest.update(block)
    return size, digest.hexdigest()


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def normalize_inside_root(raw: str, root: Path, label: str) -> Path:
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve(strict=False)
    if not is_relative_to(resolved, root):
        raise GuardError(f"{label} must be inside root: {raw}")
    return resolved


def relative_posix(path: Path, root: Path) -> str:
    rel = path.relative_to(root).as_posix()
    return rel or "."


def matches_exclude(rel: str, patterns: Iterable[str]) -> bool:
    posix = PurePosixPath(rel)
    return any(posix.match(pattern) for pattern in patterns)


def iter_target_entries(
    target: Path, root: Path, excludes: tuple[str, ...], *, allow_missing: bool = False
) -> Iterable[tuple[str, Entry]]:
    if not target.exists() and not target.is_symlink():
        if allow_missing:
            return
        raise GuardError(f"Target does not exist: {target}")

    def emit(path: Path) -> tuple[str, Entry] | None:
        rel = relative_posix(path, root)
        if matches_exclude(rel, excludes):
            return None
        if path.is_symlink():
            link_target = os.readlink(path)
            payload = f"symlink\0{link_target}".encode("utf-8", errors="surrogateescape")
            return rel, Entry("symlink", len(payload), sha256_bytes(payload), link_target)
        if path.is_file():
            size, digest = sha256_file(path)
            return rel, Entry("file", size, digest)
        return None

    if target.is_symlink() or target.is_file():
        item = emit(target)
        if item is not None:
            yield item
        return

    for current_root, dirnames, filenames in os.walk(target, topdown=True, followlinks=False):
        current = Path(current_root)
        kept_dirs: list[str] = []
        for name in sorted(dirnames):
            path = current / name
            rel = relative_posix(path, root)
            if matches_exclude(rel, excludes):
                continue
            if path.is_symlink():
                item = emit(path)
                if item is not None:
                    yield item
                continue
            kept_dirs.append(name)
        dirnames[:] = kept_dirs

        for name in sorted(filenames):
            path = current / name
            item = emit(path)
            if item is not None:
                yield item


def collect(
    root: Path, targets: list[Path], excludes: tuple[str, ...], *, allow_missing: bool = False
) -> dict[str, Entry]:
    entries: dict[str, Entry] = {}
    for target in targets:
        for rel, entry in iter_target_entries(target, root, excludes, allow_missing=allow_missing):
            previous = entries.get(rel)
            if previous is not None and previous != entry:
                raise GuardError(f"Overlapping targets produced inconsistent entry: {rel}")
            entries[rel] = entry
    return dict(sorted(entries.items()))


def aggregate_digest(entries: dict[str, Entry]) -> str:
    digest = hashlib.sha256()
    for rel, entry in sorted(entries.items()):
        digest.update(rel.encode("utf-8", errors="surrogateescape"))
        digest.update(b"\0")
        digest.update(entry.kind.encode("ascii"))
        digest.update(b"\0")
        digest.update(str(entry.size).encode("ascii"))
        digest.update(b"\0")
        digest.update(entry.sha256.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def snapshot_command(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise GuardError(f"Root is not a directory: {root}")

    output = Path(args.output).expanduser().resolve(strict=False)
    if is_relative_to(output, root):
        raise GuardError("Snapshot output must be outside the review root")

    targets = [normalize_inside_root(raw, root, "Target") for raw in args.target]
    excludes = tuple(dict.fromkeys((*DEFAULT_EXCLUDES, *args.exclude)))
    entries = collect(root, targets, excludes)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "targets": [relative_posix(path, root) for path in targets],
        "excludes": list(excludes),
        "aggregate_sha256": aggregate_digest(entries),
        "file_count": len(entries),
        "entries": {rel: entry.as_json() for rel, entry in entries.items()},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "SNAPSHOT_CREATED",
        "snapshot": str(output),
        "root": str(root),
        "file_count": len(entries),
        "aggregate_sha256": payload["aggregate_sha256"],
    }, ensure_ascii=False))
    return 0


def load_snapshot(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GuardError(f"Cannot read snapshot: {path}: {exc}") from exc
    if data.get("schema_version") != SCHEMA_VERSION:
        raise GuardError(f"Unsupported snapshot schema: {data.get('schema_version')!r}")
    for key in ("root", "targets", "excludes", "entries"):
        if key not in data:
            raise GuardError(f"Snapshot is missing {key!r}")
    return data


def parse_entries(raw: object) -> dict[str, Entry]:
    if not isinstance(raw, dict):
        raise GuardError("Snapshot entries must be an object")
    result: dict[str, Entry] = {}
    for rel, value in raw.items():
        if not isinstance(rel, str) or not isinstance(value, dict):
            raise GuardError("Malformed snapshot entry")
        try:
            result[rel] = Entry(
                kind=str(value["kind"]),
                size=int(value["size"]),
                sha256=str(value["sha256"]),
                link_target=str(value["link_target"]) if "link_target" in value else None,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise GuardError(f"Malformed snapshot entry: {rel}") from exc
    return result


def classify_changes(before: dict[str, Entry], after: dict[str, Entry]) -> dict[str, list[str]]:
    before_paths = set(before)
    after_paths = set(after)
    added = sorted(after_paths - before_paths)
    removed = sorted(before_paths - after_paths)
    modified: list[str] = []
    type_changed: list[str] = []
    for rel in sorted(before_paths & after_paths):
        old = before[rel]
        new = after[rel]
        if old.kind != new.kind:
            type_changed.append(rel)
        elif old != new:
            modified.append(rel)
    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "type_changed": type_changed,
    }


def report_change_paths(changes: dict[str, list[str]]) -> set[str]:
    result: set[str] = set()
    for values in changes.values():
        result.update(values)
    return result


def filter_allowed(changes: dict[str, list[str]], allowed: set[str]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    unexpected: dict[str, list[str]] = {}
    accepted: dict[str, list[str]] = {}
    for kind, paths in changes.items():
        accepted[kind] = [path for path in paths if path in allowed]
        unexpected[kind] = [path for path in paths if path not in allowed]
    return unexpected, accepted


def verify_command(args: argparse.Namespace) -> int:
    snapshot_path = Path(args.snapshot).expanduser().resolve(strict=True)
    data = load_snapshot(snapshot_path)
    root = Path(str(data["root"])).resolve(strict=True)
    if not root.is_dir():
        raise GuardError(f"Snapshot root is not available: {root}")

    raw_targets = data["targets"]
    raw_excludes = data["excludes"]
    if not isinstance(raw_targets, list) or not all(isinstance(item, str) for item in raw_targets):
        raise GuardError("Snapshot targets are malformed")
    if not isinstance(raw_excludes, list) or not all(isinstance(item, str) for item in raw_excludes):
        raise GuardError("Snapshot excludes are malformed")

    targets = [normalize_inside_root(item, root, "Snapshot target") for item in raw_targets]
    before = parse_entries(data["entries"])
    after = collect(root, targets, tuple(raw_excludes), allow_missing=True)
    changes = classify_changes(before, after)

    if len(args.allow_report) > 1:
        raise GuardError("The review contract permits at most one allowed report artifact")

    target_rels = [relative_posix(path, root) for path in targets]
    allowed: set[str] = set()
    for raw in args.allow_report:
        allowed_path = normalize_inside_root(raw, root, "Allowed report")
        if allowed_path.is_dir():
            raise GuardError(f"Allowed report must be an exact file path: {raw}")
        if allowed_path.suffix.lower() not in SAFE_REPORT_SUFFIXES:
            raise GuardError(
                f"Allowed report must use one of {sorted(SAFE_REPORT_SUFFIXES)}: {raw}"
            )
        rel = relative_posix(allowed_path, root)
        rel_parts = tuple(part.lower() for part in PurePosixPath(rel).parts)
        if any(part in FORBIDDEN_REPORT_PARTS for part in rel_parts):
            raise GuardError(f"Allowed report path is inside a forbidden repository area: {raw}")
        if any(part.endswith((".xcodeproj", ".xcworkspace")) for part in rel_parts):
            raise GuardError(f"Allowed report path cannot be inside project/workspace metadata: {raw}")
        covered = any(
            target_rel == "." or rel == target_rel or rel.startswith(f"{target_rel}/")
            for target_rel in target_rels
        )
        if not covered:
            raise GuardError(
                f"Allowed report must be inside the original snapshot scope: {raw}"
            )
        allowed.add(rel)

    unexpected, accepted = filter_allowed(changes, allowed)
    status = "PASS" if not report_change_paths(unexpected) else "INVALIDATED"
    payload = {
        "status": status,
        "root": str(root),
        "snapshot": str(snapshot_path),
        "baseline_file_count": len(before),
        "current_file_count": len(after),
        "baseline_aggregate_sha256": aggregate_digest(before),
        "current_aggregate_sha256": aggregate_digest(after),
        "unexpected_changes": unexpected,
        "allowed_report_changes": accepted,
    }

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Review integrity: {status}")
        print(f"Baseline files: {len(before)}")
        print(f"Current files: {len(after)}")
        for kind in ("added", "removed", "modified", "type_changed"):
            for rel in unexpected[kind]:
                print(f"UNEXPECTED {kind.upper()}: {rel}")
        for kind in ("added", "removed", "modified", "type_changed"):
            for rel in accepted[kind]:
                print(f"ALLOWED_REPORT {kind.upper()}: {rel}")

    return 0 if status == "PASS" else 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and verify read-only review integrity snapshots.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot = subparsers.add_parser("snapshot", help="Create a SHA-256 manifest for review targets.")
    snapshot.add_argument("--root", required=True, help="Repository or artifact root.")
    snapshot.add_argument("--target", action="append", required=True, help="File or directory inside root; repeatable.")
    snapshot.add_argument("--output", required=True, help="Snapshot JSON path outside root.")
    snapshot.add_argument("--exclude", action="append", default=[], help="Additional root-relative glob to exclude.")
    snapshot.set_defaults(func=snapshot_command)

    verify = subparsers.add_parser("verify", help="Compare current files with a prior snapshot.")
    verify.add_argument("--snapshot", required=True, help="Snapshot JSON created by the snapshot command.")
    verify.add_argument("--allow-report", action="append", default=[], help="Exact report file allowed to differ; repeatable for tooling, but the Skill contract permits at most one.")
    verify.add_argument("--format", choices=("text", "json"), default="text")
    verify.set_defaults(func=verify_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except GuardError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
