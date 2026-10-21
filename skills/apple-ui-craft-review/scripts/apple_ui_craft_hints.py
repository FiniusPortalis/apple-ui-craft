#!/usr/bin/env python3
"""Find native Apple UI code patterns that deserve human HIG review.

This is intentionally a candidate scanner, not a compliance checker. Every result
requires source-context, exception, user-impact, and runtime verification before it
becomes a finding.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

VERSION = "2.0.0"
DEFAULT_EXCLUDES = {
    ".build",
    ".git",
    "DerivedData",
    "Pods",
    "Carthage",
    "SourcePackages",
    "node_modules",
    "vendor",
    "Generated",
}
SEVERITY_RANK = {
    "investigation": 0,
    "nit": 1,
    "minor": 2,
    "major": 3,
    "blocker": 4,
}


@dataclass(frozen=True)
class Rule:
    scanner_id: str
    rule_ids: tuple[str, ...]
    title: str
    severity: str
    platforms: tuple[str, ...]
    pattern: str
    message: str
    exception_to_check: str
    source: str
    flags: int = 0

    @property
    def regex(self) -> re.Pattern[str]:
        return re.compile(self.pattern, self.flags)


@dataclass(frozen=True)
class Hint:
    scanner_id: str
    rule_ids: tuple[str, ...]
    title: str
    severity: str
    platforms: tuple[str, ...]
    path: str
    line: int
    column: int
    snippet: str
    message: str
    exception_to_check: str
    source: str


RULES: tuple[Rule, ...] = (
    Rule(
        "container.screen-bounds-ios",
        ("ADAPT-01", "IPAD-01"),
        "Device screen bounds used as layout input",
        "major",
        ("ios", "ipados"),
        r"UIScreen\s*\.\s*main\s*\.\s*bounds",
        "Device bounds are not the current app-window container, especially on iPadOS.",
        "Is this a fixed media/document canvas rather than the surrounding interface shell?",
        "https://developer.apple.com/design/human-interface-guidelines/layout",
    ),
    Rule(
        "container.screen-bounds-macos",
        ("ADAPT-01", "MAC-03"),
        "Display bounds used as window layout input",
        "major",
        ("macos",),
        r"NSScreen\s*\.\s*(?:main|screens)\b",
        "Display dimensions can bypass the current resizable window or container.",
        "Is this code positioning a window across displays rather than sizing in-window content?",
        "https://developer.apple.com/design/human-interface-guidelines/windows",
    ),
    Rule(
        "container.device-orientation",
        ("ADAPT-01", "ADAPT-02"),
        "Physical device orientation drives layout",
        "minor",
        ("ios", "ipados"),
        r"UIDevice\s*\.\s*current\s*\.\s*orientation",
        "Container size and traits are usually more reliable than physical-device orientation.",
        "Is this sensor/orientation functionality rather than layout branching?",
        "https://developer.apple.com/design/human-interface-guidelines/layout",
    ),
    Rule(
        "control.swiftui-on-tap",
        ("NATIVE-01", "NATIVE-02", "A11Y-03"),
        "Raw SwiftUI tap gesture may be acting as a control",
        "minor",
        ("ios", "ipados", "macos"),
        r"\.onTapGesture\s*(?:\(|\{)",
        "Button-like actions usually gain better semantics, state, keyboard activation, and accessibility from a native control.",
        "Is this direct manipulation of content, and is an equivalent discoverable/accessibility action available?",
        "https://developer.apple.com/design/human-interface-guidelines/buttons",
    ),
    Rule(
        "control.uikit-tap-recognizer",
        ("NATIVE-01", "A11Y-03"),
        "UIKit tap recognizer may replace a native control",
        "minor",
        ("ios", "ipados"),
        r"UITapGestureRecognizer\s*\(",
        "A gesture recognizer on button-shaped content can omit control semantics and primary-action behavior.",
        "Is the gesture direct manipulation rather than a command, and is an alternate path present?",
        "https://developer.apple.com/design/human-interface-guidelines/buttons",
    ),
    Rule(
        "control.appkit-click-recognizer",
        ("NATIVE-01", "A11Y-03", "A11Y-05"),
        "AppKit click recognizer may replace a native control",
        "minor",
        ("macos",),
        r"NSClickGestureRecognizer\s*\(",
        "A click recognizer used as a command can bypass standard control, focus, and keyboard behavior.",
        "Is the gesture direct manipulation rather than a button or menu command?",
        "https://developer.apple.com/design/human-interface-guidelines/buttons",
    ),
    Rule(
        "type.swiftui-fixed-size",
        ("A11Y-06", "ADAPT-04"),
        "Fixed SwiftUI font size",
        "minor",
        ("ios", "ipados", "macos"),
        r"\.font\s*\(\s*\.system\s*\(\s*size\s*:",
        "Custom fixed type needs an explicit legibility and scaling strategy.",
        "Is this intentional display typography with equivalent scaling and adequate size?",
        "https://developer.apple.com/design/human-interface-guidelines/accessibility",
    ),
    Rule(
        "type.uikit-fixed-size",
        ("A11Y-06", "ADAPT-04"),
        "Fixed UIKit font size",
        "minor",
        ("ios", "ipados"),
        r"UIFont\s*\.\s*(?:systemFont|boldSystemFont|italicSystemFont)\s*\(\s*ofSize\s*:",
        "Fixed UIKit type should adopt preferred text styles or scale metrics where text growth is expected.",
        "Is this an intentional non-scaling display element rather than body/control text?",
        "https://developer.apple.com/design/human-interface-guidelines/typography",
    ),
    Rule(
        "type.appkit-fixed-size",
        ("A11Y-06", "ADAPT-04"),
        "Fixed AppKit font size",
        "minor",
        ("macos",),
        r"NSFont\s*\.\s*(?:systemFont|boldSystemFont)\s*\(\s*ofSize\s*:",
        "Custom macOS type needs to meet platform legibility guidance and user settings.",
        "Is this an intentional display treatment or a native control already handling type?",
        "https://developer.apple.com/design/human-interface-guidelines/accessibility",
    ),
    Rule(
        "type.single-line",
        ("ADAPT-04", "A11Y-06"),
        "Single-line truncation needs content-pressure review",
        "investigation",
        ("ios", "ipados", "macos"),
        r"\.lineLimit\s*\(\s*1\s*\)",
        "One-line text can lose meaning under localization or larger text sizes.",
        "Is this a compact label with an accessible full value or expandable detail?",
        "https://developer.apple.com/design/human-interface-guidelines/typography",
    ),
    Rule(
        "type.minimum-scale",
        ("ADAPT-04", "A11Y-06"),
        "Text shrinking may mask layout pressure",
        "investigation",
        ("ios", "ipados", "macos"),
        r"\.minimumScaleFactor\s*\(",
        "Aggressive shrinking can undermine text growth and localization.",
        "Is the value conservative and limited to a compact, nonessential label with full semantics?",
        "https://developer.apple.com/design/human-interface-guidelines/typography",
    ),
    Rule(
        "layout.fixed-frame",
        ("ADAPT-01", "ADAPT-03", "ADAPT-04"),
        "Both width and height appear fixed",
        "investigation",
        ("ios", "ipados", "macos"),
        r"\.frame\s*\([^\n)]*width\s*:\s*\d+(?:\.\d+)?[^\n)]*height\s*:\s*\d+(?:\.\d+)?",
        "A fully fixed frame can break window resizing, text growth, or localization.",
        "Is this a bounded icon/thumbnail/canvas whose interaction shell remains adaptive?",
        "https://developer.apple.com/design/human-interface-guidelines/layout",
    ),
    Rule(
        "layout.ignore-safe-area",
        ("ADAPT-01",),
        "Safe area is ignored",
        "investigation",
        ("ios", "ipados", "macos"),
        r"\.ignoresSafeArea\s*(?:\(|\b)",
        "Ignoring safe areas can place controls or essential content under system regions.",
        "Is only decorative/media background extending while controls remain inside safe regions?",
        "https://developer.apple.com/design/human-interface-guidelines/layout",
    ),
    Rule(
        "accessibility.hidden",
        ("A11Y-01", "A11Y-08"),
        "Content is hidden from accessibility",
        "major",
        ("ios", "ipados", "macos"),
        r"\.accessibilityHidden\s*\(\s*true\s*\)",
        "Essential information or actions may disappear for assistive technologies.",
        "Is the element purely decorative or fully represented by a correctly grouped parent?",
        "https://developer.apple.com/design/human-interface-guidelines/accessibility",
    ),
    Rule(
        "accessibility.ignore-children",
        ("A11Y-01", "A11Y-08"),
        "Child accessibility semantics are discarded",
        "investigation",
        ("ios", "ipados", "macos"),
        r"\.accessibilityElement\s*\(\s*children\s*:\s*\.ignore\s*\)",
        "Ignoring children can remove actions, state, or reading order unless the parent replaces them completely.",
        "Does the parent expose the combined label, value, state, and all required actions?",
        "https://developer.apple.com/design/human-interface-guidelines/accessibility",
    ),
    Rule(
        "accessibility.empty-label",
        ("A11Y-01", "A11Y-08"),
        "Accessibility label is empty",
        "major",
        ("ios", "ipados", "macos"),
        r"\.accessibilityLabel\s*\(\s*(?:Text\s*\(\s*)?\"\"",
        "An empty label can make an interactive or informative element undiscoverable.",
        "Is the element decorative and should it be hidden instead, or is a parent providing complete semantics?",
        "https://developer.apple.com/design/human-interface-guidelines/accessibility",
    ),
    Rule(
        "state.conditional-red-green",
        ("A11Y-02",),
        "Conditional red/green state may rely on color alone",
        "major",
        ("ios", "ipados", "macos"),
        r"\?\s*(?:Color\.)?(?:red|green)\s*:\s*(?:Color\.)?(?:red|green)",
        "Red/green state needs a non-color cue such as text, symbol, shape, or semantics.",
        "Are text/symbol/state semantics already present in the same component?",
        "https://developer.apple.com/design/human-interface-guidelines/accessibility",
        re.IGNORECASE,
    ),
    Rule(
        "command.context-menu",
        ("NATIVE-03", "MENU-01"),
        "Context menu command needs an alternate-path check",
        "investigation",
        ("ios", "ipados", "macos"),
        r"\.contextMenu\s*(?:\(|\{)",
        "Core commands must not exist only in a context menu.",
        "Is the same command discoverable in a visible control, toolbar, row action, menu bar, or shortcut?",
        "https://developer.apple.com/design/human-interface-guidelines/context-menus",
    ),
    Rule(
        "presentation.alert",
        ("ALERT-01", "ALERT-02", "RECOVERY-01"),
        "Alert usage needs action and recoverability review",
        "investigation",
        ("ios", "ipados", "macos"),
        r"(?:\.alert\s*\(|UIAlertController\s*\(|NSAlert\s*\()",
        "Alerts should be critical and actionable rather than informational or routine confirmation.",
        "Is this an uncommon irreversible/safety decision, or could inline feedback/undo preserve flow?",
        "https://developer.apple.com/design/human-interface-guidelines/alerts",
    ),
    Rule(
        "presentation.popover",
        ("PRESENT-02", "PRESENT-03", "IPAD-07"),
        "Popover needs width, anchoring, and nesting review",
        "investigation",
        ("ios", "ipados", "macos"),
        r"(?:\.popover\s*\(|NSPopover\s*\()",
        "Popovers must fit the task, remain anchored, and adapt appropriately in compact contexts.",
        "Does the framework adapt automatically, and is the task small, source-related, and nonnested?",
        "https://developer.apple.com/design/human-interface-guidelines/popovers",
    ),
    Rule(
        "material.custom-glass",
        ("MATERIAL-01", "MATERIAL-02", "MATERIAL-04"),
        "Custom Liquid Glass usage needs hierarchy review",
        "investigation",
        ("ios", "ipados", "macos"),
        r"\.glassEffect\s*\(",
        "Custom glass should be sparse and belong to the functional control/navigation layer.",
        "Is this a high-value control/navigation element or a transient active control rather than content background?",
        "https://developer.apple.com/design/human-interface-guidelines/materials",
    ),
    Rule(
        "material.standard-material",
        ("MATERIAL-01", "MATERIAL-03"),
        "Material usage needs semantic-purpose review",
        "investigation",
        ("ios", "ipados", "macos"),
        r"\.(?:ultraThinMaterial|thinMaterial|regularMaterial|thickMaterial)\b",
        "Materials should be selected for semantic structure and tested across settings/backgrounds.",
        "Is this content-layer separation with sufficient contrast rather than appearance-only styling?",
        "https://developer.apple.com/design/human-interface-guidelines/materials",
    ),
    Rule(
        "motion.swiftui-animation",
        ("MOTION-01", "MOTION-02", "A11Y-04"),
        "Custom SwiftUI animation needs purpose and Reduce Motion review",
        "investigation",
        ("ios", "ipados", "macos"),
        r"(?:\.animation\s*\(|withAnimation\s*\()",
        "Custom motion should have a purpose, preserve control, and provide a reduced-motion path where spatial/depth motion is involved.",
        "Is the motion nonspatial or gesture-tracked, and is accessibilityReduceMotion handled elsewhere?",
        "https://developer.apple.com/design/human-interface-guidelines/accessibility",
    ),
    Rule(
        "motion.uikit-animation",
        ("MOTION-01", "MOTION-02", "A11Y-04"),
        "UIKit animation needs purpose and Reduce Motion review",
        "investigation",
        ("ios", "ipados"),
        r"UIView\s*\.\s*animate\s*\(",
        "Custom UIKit motion needs interruption and reduced-motion behavior where applicable.",
        "Is the animation purely feedback/nonspatial, and is Reduce Motion respected?",
        "https://developer.apple.com/design/human-interface-guidelines/accessibility",
    ),
    Rule(
        "motion.appkit-animation",
        ("MOTION-01", "MOTION-02", "A11Y-04"),
        "AppKit animation needs purpose and Reduce Motion review",
        "investigation",
        ("macos",),
        r"NSAnimationContext\s*\.\s*runAnimationGroup",
        "Custom AppKit motion needs interruption and reduced-motion behavior where applicable.",
        "Is the motion essential feedback, and is Reduce Motion respected?",
        "https://developer.apple.com/design/human-interface-guidelines/accessibility",
    ),
    Rule(
        "window.borderless",
        ("MAC-03",),
        "Borderless macOS window style",
        "major",
        ("macos",),
        r"(?:NSWindow\s*\.\s*StyleMask[^\n]*\.borderless|styleMask[^\n]*\.borderless)",
        "Borderless windows can remove expected movement, resizing, focus, controls, and accessibility.",
        "Is this an intentional utility panel/HUD with explicit window and escape behavior?",
        "https://developer.apple.com/design/human-interface-guidelines/windows",
    ),
    Rule(
        "window.hidden-titlebar",
        ("MAC-03",),
        "Hidden title bar needs standard-window behavior review",
        "investigation",
        ("macos",),
        r"\.windowStyle\s*\(\s*\.hiddenTitleBar\s*\)",
        "Title-bar customization should preserve standard window behavior and command access.",
        "Does the window remain movable, resizable, closable, accessible, and platform-consistent?",
        "https://developer.apple.com/design/human-interface-guidelines/windows",
    ),
)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find Swift UI patterns that deserve human Apple HIG review. Results are candidates, not violations."
    )
    parser.add_argument("paths", nargs="+", help="Swift file or directory to scan")
    parser.add_argument(
        "--platform",
        choices=("all", "ios", "ipados", "macos"),
        default="all",
        help="Limit platform-specific rules (default: all)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "sarif"),
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Directory name or path fragment to exclude; repeatable",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=500,
        help="Maximum result count (default: 500)",
    )
    parser.add_argument(
        "--fail-on",
        choices=("none", "blocker", "major", "minor", "nit", "investigation"),
        default="none",
        help="Exit 2 when a candidate meets this severity threshold; default never fails",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    return parser.parse_args(argv)


def should_exclude(path: Path, extra: Sequence[str]) -> bool:
    parts = set(path.parts)
    if parts & DEFAULT_EXCLUDES:
        return True
    rendered = str(path)
    return any(item and (item in parts or item in rendered) for item in extra)


def iter_swift_files(inputs: Sequence[str], excludes: Sequence[str]) -> Iterable[Path]:
    seen: set[Path] = set()
    for raw in inputs:
        path = Path(raw).expanduser()
        if not path.exists():
            print(f"warning: path does not exist: {path}", file=sys.stderr)
            continue
        if path.is_file():
            if path.suffix == ".swift" and not should_exclude(path, excludes):
                resolved = path.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    yield path
            continue
        for candidate in path.rglob("*.swift"):
            if should_exclude(candidate, excludes):
                continue
            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                yield candidate


def platform_applies(rule: Rule, platform: str) -> bool:
    return platform == "all" or platform in rule.platforms


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path.resolve())


def scan_file(path: Path, platform: str) -> list[Hint]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    hints: list[Hint] = []
    relative = display_path(path)

    for rule in RULES:
        if not platform_applies(rule, platform):
            continue
        regex = rule.regex
        for line_number, line in enumerate(lines, start=1):
            match = regex.search(line)
            if not match:
                continue
            hints.append(
                Hint(
                    scanner_id=rule.scanner_id,
                    rule_ids=rule.rule_ids,
                    title=rule.title,
                    severity=rule.severity,
                    platforms=rule.platforms,
                    path=relative,
                    line=line_number,
                    column=match.start() + 1,
                    snippet=line.strip()[:300],
                    message=rule.message,
                    exception_to_check=rule.exception_to_check,
                    source=rule.source,
                )
            )

    # File-level density candidate for repeated custom glass.
    glass_lines = [
        number for number, line in enumerate(lines, start=1) if re.search(r"\.glassEffect\s*\(", line)
    ]
    if len(glass_lines) >= 4 and platform in ("all", "ios", "ipados", "macos"):
        hints.append(
            Hint(
                scanner_id="material.custom-glass-density",
                rule_ids=("MATERIAL-01", "MATERIAL-02"),
                title="Repeated custom glass in one file",
                severity="minor",
                platforms=("ios", "ipados", "macos"),
                path=relative,
                line=glass_lines[0],
                column=1,
                snippet=f"{len(glass_lines)} .glassEffect calls in this file",
                message="Repeated custom glass may blur the distinction between functional chrome and content.",
                exception_to_check="Are these separate high-value functional controls rather than content surfaces, and are standard components insufficient?",
                source="https://developer.apple.com/design/human-interface-guidelines/materials",
            )
        )

    return hints


def sort_hints(hints: Iterable[Hint]) -> list[Hint]:
    return sorted(
        hints,
        key=lambda item: (
            -SEVERITY_RANK[item.severity],
            item.path,
            item.line,
            item.column,
            item.scanner_id,
        ),
    )


def emit_text(hints: Sequence[Hint], file_count: int, platform: str) -> None:
    print(f"Apple UI HIG candidate scan {VERSION}: {file_count} Swift file(s), platform={platform}")
    if not hints:
        print("No candidates found. A clean scan is not HIG approval.")
        return
    for hint in hints:
        rules = ", ".join(hint.rule_ids)
        platforms = ", ".join(hint.platforms)
        print(f"\n[{hint.severity.upper()}] {hint.path}:{hint.line}:{hint.column} {hint.title}")
        print(f"  scanner: {hint.scanner_id}")
        print(f"  rules: {rules} | platforms: {platforms}")
        print(f"  code: {hint.snippet}")
        print(f"  review: {hint.message}")
        print(f"  exception: {hint.exception_to_check}")
        print(f"  source: {hint.source}")
    print(f"\n{len(hints)} candidate(s). Confirm context before reporting any finding.")


def emit_json(hints: Sequence[Hint], file_count: int, platform: str) -> None:
    payload = {
        "tool": "apple_ui_craft_hints",
        "version": VERSION,
        "platform": platform,
        "files_scanned": file_count,
        "candidate_count": len(hints),
        "disclaimer": "Candidates require human context and do not prove HIG violations.",
        "candidates": [asdict(hint) for hint in hints],
    }
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    print()


def sarif_level(severity: str) -> str:
    return "error" if severity in ("blocker", "major") else "warning" if severity == "minor" else "note"


def emit_sarif(hints: Sequence[Hint], file_count: int, platform: str) -> None:
    unique_rules: dict[str, Hint] = {}
    for hint in hints:
        unique_rules.setdefault(hint.scanner_id, hint)
    rules = []
    for scanner_id, hint in sorted(unique_rules.items()):
        rules.append(
            {
                "id": scanner_id,
                "name": hint.title,
                "shortDescription": {"text": hint.message},
                "helpUri": hint.source,
                "properties": {
                    "ruleIds": list(hint.rule_ids),
                    "platforms": list(hint.platforms),
                    "candidateOnly": True,
                },
            }
        )
    results = []
    for hint in hints:
        uri = Path(hint.path).as_posix()
        results.append(
            {
                "ruleId": hint.scanner_id,
                "level": sarif_level(hint.severity),
                "message": {
                    "text": f"{hint.message} Exception to check: {hint.exception_to_check}"
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": uri},
                            "region": {
                                "startLine": hint.line,
                                "startColumn": hint.column,
                            },
                        }
                    }
                ],
                "properties": {
                    "severity": hint.severity,
                    "ruleIds": list(hint.rule_ids),
                    "platforms": list(hint.platforms),
                    "snippet": hint.snippet,
                    "candidateOnly": True,
                },
            }
        )
    payload = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "apple_ui_craft_hints",
                        "version": VERSION,
                        "informationUri": "https://developer.apple.com/design/human-interface-guidelines/",
                        "rules": rules,
                    }
                },
                "invocations": [
                    {
                        "executionSuccessful": True,
                        "properties": {
                            "filesScanned": file_count,
                            "platform": platform,
                            "candidateOnly": True,
                        },
                    }
                ],
                "results": results,
            }
        ],
    }
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    print()


def should_fail(hints: Sequence[Hint], threshold: str) -> bool:
    if threshold == "none":
        return False
    minimum = SEVERITY_RANK[threshold]
    return any(SEVERITY_RANK[hint.severity] >= minimum for hint in hints)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.max_results < 1:
        print("--max-results must be at least 1", file=sys.stderr)
        return 2

    files = list(iter_swift_files(args.paths, args.exclude))
    hints: list[Hint] = []
    for path in files:
        hints.extend(scan_file(path, args.platform))
        if len(hints) >= args.max_results:
            hints = hints[: args.max_results]
            break
    hints = sort_hints(hints)

    if args.format == "json":
        emit_json(hints, len(files), args.platform)
    elif args.format == "sarif":
        emit_sarif(hints, len(files), args.platform)
    else:
        emit_text(hints, len(files), args.platform)

    return 2 if should_fail(hints, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
