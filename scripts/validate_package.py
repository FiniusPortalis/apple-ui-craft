#!/usr/bin/env python3
"""Read-only package and optional Apple section-anchor validation.

Live checks establish reachability and anchors, not semantic HIG compliance.
No verification dates or package files are rewritten.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen


SKILLS = ("apple-ui-craft-design", "apple-ui-craft-review", "apple-ui-craft-implementation")
SHARED_REFERENCES = (
    "native-rule-catalog.md", "source-policy.md", "apple-hig-sources.md",
    "source-verification.md", "platform-profiles.md", "anti-patterns.md",
    "macos-runtime-scenarios.md",
)
RULE_ROW = re.compile(r"^\s*\|?\s*`?([A-Z][A-Z0-9]*-\d+)`?\s*\|")
LINK = re.compile(r"\[[^\]\n]+\]\(([^\s)]+)\)")
APPLE_PREFIX = "/design/human-interface-guidelines/"
VALID_CLASSES = {"APPLE-HIG", "APPLE-API", "PLATFORM-CONVENTION", "PRODUCT-HEURISTIC", "EVIDENCE-GAP"}


def rule_links(catalog: str) -> tuple[set[str], set[str], list[str]]:
    ids: set[str] = set()
    urls: set[str] = set()
    errors: list[str] = []
    for line in catalog.splitlines():
        match = RULE_ROW.match(line)
        if not match:
            continue
        rid = match.group(1)
        if rid in ids:
            errors.append(f"Duplicate rule: {rid}")
        ids.add(rid)
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) not in (6, 7):
            errors.append(f"{rid}: malformed rule table row")
            continue
        if cells[2] not in VALID_CLASSES:
            errors.append(f"{rid}: unknown claim class {cells[2]}")
        source_links = LINK.findall(cells[-1])
        if not source_links:
            errors.append(f"{rid}: missing official section link")
        for url in source_links:
            parts = urlsplit(url)
            if (parts.scheme != "https" or parts.netloc != "developer.apple.com"
                    or not parts.path.startswith(APPLE_PREFIX) or not parts.fragment):
                errors.append(f"{rid}: expected an exact official HIG section: {url}")
            else:
                urls.add(url)
        if cells[2] not in {"APPLE-HIG", "APPLE-API"} and "Background, not a direct requirement:" not in cells[-1]:
            errors.append(f"{rid}: inferred rule must label its source as background")
    if not ids:
        errors.append("No catalog rules found")
    return ids, urls, errors


def validate_source(topic: str, fragments: set[str], data: dict) -> list[str]:
    # Inspect Apple-provided section anchors, not guessed GitHub slug rules.
    if data.get("kind") != "article" or not data.get("metadata", {}).get("title"):
        return [f"{topic}: expected an Apple article body"]
    expected_id = "/design/human-interface-guidelines/" + topic
    identifier = data.get("identifier", {}).get("url", "").lower()
    if not identifier.endswith(expected_id):
        return [f"{topic}: returned article identifier does not match the requested topic"]
    blocks = [b for s in data.get("primaryContentSections", []) for b in s.get("content", [])]
    anchors = {b.get("anchor") for b in blocks if b.get("type") == "heading"}
    if not any(b.get("type") == "paragraph" for b in blocks):
        return [f"{topic}: article body missing; title-only response is insufficient"]
    return [f"{topic}: missing section #{anchor}" for anchor in sorted(fragments - anchors)]


def check_sources(urls: set[str], cache: Path | None = None) -> list[str]:
    grouped: dict[str, set[str]] = {}
    for url in urls:
        parts = urlsplit(url)
        topic = parts.path.removeprefix(APPLE_PREFIX).rstrip("/")
        if not re.fullmatch(r"[a-z0-9-]+", topic):
            return [f"Unsupported HIG topic path: {topic}"]
        grouped.setdefault(topic, set()).add(unquote(parts.fragment))

    def check(item: tuple[str, set[str]]) -> list[str]:
        topic, fragments = item
        try:
            if cache:
                data = json.loads((cache / f"{topic}.json").read_text())
            else:
                url = f"https://developer.apple.com/tutorials/data/design/human-interface-guidelines/{topic}.json"
                request = Request(url, headers={"User-Agent": "AppleUICraftSourceCheck/1.0"})
                with urlopen(request, timeout=20) as response:
                    if urlsplit(response.url).hostname != "developer.apple.com":
                        return [f"{topic}: redirected outside the official Apple host"]
                    data = json.load(response)
            return validate_source(topic, fragments, data)
        except Exception as exc:
            return [f"{topic}: source unavailable: {exc}"]

    errors = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(check, sorted(grouped.items())):
            errors.extend(result)
    return errors


def validate_package(root: Path) -> tuple[list[str], set[str], int]:
    errors = []
    skill_paths = [root / "skills" / name for name in SKILLS]
    for skill in skill_paths:
        entry = skill / "SKILL.md"
        if not entry.is_file():
            errors.append(f"Missing {entry.relative_to(root)}")
            continue
        text = entry.read_text()
        front = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
        if not front or not re.search(r"^name: " + re.escape(skill.name) + r"\s*$", front.group(1), re.MULTILINE):
            errors.append(f"{skill.name}: missing or incorrect skill name")
        if not front or not re.search(r"^description: .+", front.group(1), re.MULTILINE):
            errors.append(f"{skill.name}: missing description")
        if not (skill / "agents/openai.yaml").is_file():
            errors.append(f"{skill.name}: missing agent metadata")

    for filename in SHARED_REFERENCES:
        paths = [skill / "references" / filename for skill in skill_paths]
        if not all(p.is_file() for p in paths):
            errors.append(f"Missing shared reference: {filename}")
        elif any(p.read_bytes() != paths[0].read_bytes() for p in paths[1:]):
            errors.append(f"Shared reference drift: {filename}")

    catalog = skill_paths[0] / "references/native-rule-catalog.md"
    ids, urls, catalog_errors = rule_links(catalog.read_text() if catalog.is_file() else "")
    errors.extend(catalog_errors)

    for path in root.rglob("*"):
        if any(part in {".git", "__pycache__", ".venv"} for part in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            errors.append(f"Symlink not portable: {path.relative_to(root)}")
            continue
        if not path.is_file():
            continue
        if path.suffix == ".py":
            try:
                compile(path.read_text(), str(path), "exec")
            except SyntaxError as exc:
                errors.append(f"Python syntax: {path.relative_to(root)}: {exc}")
        if path.suffix != ".md":
            continue
        text = path.read_text()
        if re.search(r"/Users/[^/\s]+/|/home/[^/\s]+/", text):
            errors.append(f"Personal absolute path in {path.relative_to(root)}")
        for url in LINK.findall(text):
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            target = (path.parent / unquote(parts.path)).resolve()
            if not target.is_relative_to(root.resolve()) or not target.exists():
                errors.append(f"Broken/nonportable local link in {path.relative_to(root)}: {url}")
    return errors, urls, len(ids)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--live", action="store_true", help="Check official Apple article section anchors over HTTPS")
    source.add_argument("--source-cache", type=Path, help="Validate against previously fetched Apple DocC JSON; not a fresh online check")
    args = parser.parse_args()
    errors, urls, count = validate_package(args.root)
    if not errors and (args.live or args.source_cache):
        errors.extend(check_sources(urls, args.source_cache))
    if errors:
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        return 1
    print(f"PASS: {len(SKILLS)} skills, {count} rules, {len(urls)} unique official section URLs; local structure and shared references consistent")
    if args.live or args.source_cache:
        mode = "live Apple sources" if args.live else "provided source cache"
        print(f"PASS: article identities, bodies and anchors checked against {mode}")
    print("Semantic review and verification dates are unchanged by this command.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
