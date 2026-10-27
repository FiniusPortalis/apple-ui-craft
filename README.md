# Apple UI Craft

Three Codex skills for designing, reviewing, and implementing native **macOS, iOS, and iPadOS** interfaces with SwiftUI, UIKit, and AppKit.

## Features

- **Traceable guidance:** 68 rules linked to specific sections across 31 Apple HIG topics.
- **Clear reasoning:** distinguishes Apple guidance, API behavior, platform conventions, and product decisions.
- **Scoped coverage:** navigation, resizing, ordinary keyboard access, loading, errors, and recovery; accessibility-specific work only when explicitly requested.
- **Concise by default:** report the result, essential reasons, and relevant checks; detailed matrices are for requested specifications, audits, and handoffs.
- **Actionable reviews:** findings include location, impact, proposed changes, and verification steps.

## Choose a skill

| Skill | Use it for |
| --- | --- |
| [apple-ui-craft-design](skills/apple-ui-craft-design/SKILL.md) | New features and redesigns: implementation-ready specifications and acceptance criteria. |
| [apple-ui-craft-review](skills/apple-ui-craft-review/SKILL.md) | Read-only reviews with evidence-backed findings. Choose `quick`, `standard`, or `deep`. |
| [apple-ui-craft-implementation](skills/apple-ui-craft-implementation/SKILL.md) | Scoped UI changes, fixes, and validation. |

Use them individually or together. Review-and-fix requests proceed from a completed review to implementation. Formal post-change approval requires an independent reviewer.

## Install

Copy the desired folders from `skills/` to `~/.agents/skills/` or your project's `.agents/skills/`. Review existing copies before replacing them. Restart Codex if the skills do not appear. See [Codex skill setup](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills).

<details>
<summary>Install all three skills from the repository root</summary>

This command stops if a destination already exists.

```bash
python3 - <<'PY'
from pathlib import Path
import shutil

source = Path.cwd() / "skills"
destination = Path.home() / ".agents" / "skills"
names = ("apple-ui-craft-design", "apple-ui-craft-review", "apple-ui-craft-implementation")
for name in names:
    if not (source / name / "SKILL.md").is_file():
        raise SystemExit(f"Missing source skill: {name}")
    if (destination / name).exists():
        raise SystemExit(f"Already exists; review before updating: {destination / name}")
destination.mkdir(parents=True, exist_ok=True)
for name in names:
    shutil.copytree(source / name, destination / name)
print("Installed three skills")
PY
```

</details>

The helpers require **Python 3.10+** with no third-party packages. Live source checks need network access; builds and runtime checks need macOS, Xcode, and a suitable simulator or device.

## Usage

Specify the target screen or files and the work you want done. Invoke a skill by name or select it in your environment's skill picker.

**Design**

```text
Use $apple-ui-craft-design to design this macOS library and detail editor.
Cover resizing, keyboard access, and state transitions. Produce a specification only.
```

**Review**

```text
Use $apple-ui-craft-review to review this screen and its code.
Report issues by severity, cite Apple sources, and give verification steps. Do not edit code.
```

**Implement**

```text
Use $apple-ui-craft-implementation to apply the agreed UI changes.
Preserve existing work, check OS availability, and run relevant tests and runtime checks.
```

## Accessibility scope

Accessibility-specific design, implementation, auditing, and testing are excluded by default, including for a general HIG review. Existing accessibility, native control behavior, and UI test identifiers are preserved. Ordinary readability, resizing, menus, and keyboard behavior remain in scope when relevant. This is a work-scope choice; Apple continues to recommend accessibility. See the [scope policy](skills/apple-ui-craft-design/references/accessibility-scope.md).

To include a feature, request it explicitly, for example: “Review VoiceOver labels and reading order for this result list.” This does not enable unrelated accessibility checks. Scope-limited verdicts do not certify full HIG, accessibility, or release readiness.

The optional candidate scanner also excludes accessibility rules by default. Add `--include-accessibility voiceover` for that feature, or `--include-accessibility all` for an explicitly requested comprehensive accessibility scan. The option is repeatable for `voiceover`, `text`, `motion`, `vision`, and `input`.

## Usage notes

- Verify findings and generated changes with relevant tests and runtime checks. Scanner results are review candidates.
- The review guard detects file changes; use a read-only sandbox to prevent writes.
- Keep small tasks scoped. Deeper reviews require more time and context.

## Sources and maintenance

Current Apple documentation takes precedence. The [rule catalog](skills/apple-ui-craft-design/references/native-rule-catalog.md) was checked on **2026-10-17**; other references include a **2026-08-04** snapshot. Recheck guidance and API availability for your target OS.

See the [source policy](skills/apple-ui-craft-design/references/source-policy.md), [verification record](skills/apple-ui-craft-design/references/source-verification.md), and [Apple source index](skills/apple-ui-craft-design/references/apple-hig-sources.md).

Each skill includes shared references for standalone use. Keep copies listed in `SHARED_REFERENCES` in `scripts/validate_package.py` synchronized, then run the checks below.

## Validation

Run from the repository root:

```bash
python3 scripts/validate_package.py
python3 scripts/validate_package.py --live
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

These check package structure, local links, shared references, Python syntax, and helper behavior. `--live` also checks Apple article identities, bodies, and section anchors; it does not validate the meaning of each rule. Tests use temporary files and `/bin/sh`.

Call skill helpers through the loaded skill's absolute path, as shown in its `SKILL.md`.

## License

[MIT](LICENSE). Independent project, not affiliated with or endorsed by Apple. Review verdicts are project assessments, not Apple certification. Apple documentation and trademarks retain their respective rights; see [NOTICE.md](NOTICE.md).
