# Self-contained implementation plan template

Use this template only when a persisted plan is required or requested. Keep the plan self-contained; include applicable sections and omit empty or unrelated matrices. Separate independent root causes only when execution or review benefits from separate plans.

```markdown
# NNN — <Imperative title>

- **Status**: TODO | IN PROGRESS | BLOCKED | DONE
- **Plan mode**: plan-only | implement
- **Commit**: <git rev-parse --short HEAD or “not a Git worktree”>
- **Created**: YYYY-MM-DD
- **Platforms**: iOS | iPadOS | macOS
- **Minimum OS / framework**: <explicit>
- **Source task / handoff**: <review task ID, report path, plan path, or direct request>
- **Finding IDs**: HIG-001, HIG-002
- **Rule IDs / classes**: IPAD-01 · APPLE-HIG; ADAPT-01 · APPLE-HIG
- **Severity**: Blocker | Major | Minor | Nit
- **Estimated scope**: <files and rough size>
- **Independent re-review required**: yes | no

## 1. Problem

Explain current behavior, affected people/context, and why it matters.
Cite every location and include the exact current excerpt:

```swift
// Sources/BrowserView.swift:88 — current
.frame(width: UIScreen.main.bounds.width)
```

## 2. Source basis and exception analysis

| Rule ID | Class | Apple topic / API doc | URL | Verified | Exception checked | Conclusion |
| --- | --- | --- | --- | --- | --- | --- |

Separate product heuristics from Apple guidance.

## 3. Target behavior

Describe the exact end state for each platform and context.
Include target code or API shape when it removes ambiguity:

```swift
NavigationSplitView {
    SidebarView()
} detail: {
    BrowserView()
}
```

State availability/fallback behavior. Never say “make it more native” or “use a better animation.”

## 4. Repository conventions to follow

- Architecture/state ownership:
- Native exemplar with `file:line`:
- Design tokens/styles:
- Localization pattern:
- Accessibility/testing pattern:
- Command/menu pattern:

## 5. Platform behavior matrix

| Context | Structure | Selection/state preserved | Commands/input | Expected result |
| --- | --- | --- | --- | --- |
| iOS compact | | | | |
| iPadOS narrow | | | | |
| iPadOS medium/wide | | | | |
| macOS minimum/typical/large | | | | |

Remove rows outside the selected platform scope.

## 6. State and recovery matrix

| State/event | UI | Accessible feedback | Available actions | Data preservation/recovery |
| --- | --- | --- | --- | --- |

## 7. Accessibility and input contract

| Concern | Exact target | Verification |
| --- | --- | --- |
| Semantics / VoiceOver | | |
| Text growth / localization | | |
| Keyboard / focus | | |
| Pointer / touch / gesture alternative | | |
| Non-color cues | | |
| Reduce Motion / transparency / contrast | | |

## 8. Ordered steps

1. `path/to/file.swift`: <one concrete edit and resulting behavior>.
2. `path/to/test.swift`: <specific test and assertion>.
3. ...

Each step names files, APIs, ownership, and expected result.

## 9. Boundaries

- Do not change:
- Preserve public interfaces/state:
- Do not add dependencies:
- Do not migrate framework/navigation outside scope:
- Generated files excluded:
- If current code differs materially from the excerpts or architecture, stop and report drift.

## 10. Verification

### Mechanical

```bash
<exact repository-valid commands>
```

Expected outcome:

- ...

### Runtime

| Platform/context | Steps | Expected observable result | Evidence |
| --- | --- | --- | --- |

### Accessibility/input

- VoiceOver:
- Dynamic Type / text pressure:
- Keyboard / Full Keyboard Access:
- Pointer/touch:
- Reduce Motion:
- Increase Contrast / Reduce Transparency:

### Done when

- [ ] <machine- or eye-checkable criterion>
- [ ] ...

## 11. Independent review handoff

- Approval verdict in this implementation task: not issued
- Review required after implementation: yes | no
- Findings and areas to re-review:
- Required runtime/accessibility/window/input contexts:
- Remaining evidence gaps:

## 12. Risks and rollback

- Risk:
- Mitigation:
- Rollback boundary:
- Follow-up deliberately excluded:
```

## Plan index

Maintain `plans/apple-ui-craft/README.md` only when the user or repository requests it, or when multiple plan files need an execution/dependency index. A single requested plan does not require a separate README. When needed, use:

```markdown
| # | Plan | Platforms | Severity | Status | Commit | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |
```

Include recommended execution order and which plans require independent review after execution.
