# Implementation-ready design specification template

Use detailed sections only at the requested depth. Follow [accessibility-scope.md](accessibility-scope.md): omit accessibility-only sections, rows, and columns by default; retain ordinary input, layout, and validation details that affect the task. In a formal report, identify the selected scope once rather than listing excluded features as `NOT RUN`.

Use this template when a detailed implementation-ready specification is requested. For a bounded concept or local design decision, include applicable behavior, assumptions, material Apple sources, ordinary input, risks, and acceptance criteria in concise prose; include accessibility only when requested. Omit unrelated sections; do not leave material behavior or readiness limitations implicit.

Use this structure. Remove sections that are truly inapplicable; do not leave unresolved behavior implicit.

```markdown
# <Feature or flow> — Native UI specification

- **Readiness**: NOT READY | READY WITH RISKS | READY
- **Platforms**: iOS | iPadOS | macOS
- **Minimum OS / framework assumptions**: <explicit>
- **Primary outcome**: When <context>, a person can <outcome> without <avoidable cost/risk>.

## 1. Blocking issues or named risks

| ID | Risk | Impact | Decision needed | Safe default |
| --- | --- | --- | --- | --- |

## 2. Assumptions and boundaries

- In scope:
- Out of scope:
- Product assumptions:
- Evidence limitations:

## 3. Source ledger

| Rule ID | Claim class | Apple topic | URL | Verified | How used | Exception checked |
| --- | --- | --- | --- | --- | --- | --- |

## 4. Cross-platform strategy

| Dimension | iOS | iPadOS | macOS | Shared semantics |
| --- | --- | --- | --- | --- |
| App navigation | | | | |
| Selection | | | | |
| Search/filter | | | | |
| Commands | | | | |
| Presentation | | | | |
| Windows/scenes | | | | |
| Inputs | | | | |

## 5. Information architecture

- Objects and hierarchy:
- Entry points:
- Primary path:
- Secondary paths:
- Exit and recovery paths:
- Restoration/deep-link behavior:

## 6. Screen, window, and flow specification

### <Surface name>

- Purpose:
- Primary content:
- Primary action:
- Secondary actions:
- Native container/component:
- Selection and focus:
- Presentation and dismissal:
- State preservation:
- Platform differences:

## 7. Native component and command map

| Capability | Native component/pattern | iOS surface | iPadOS surface | macOS surface | Accessibility/input contract | Availability question |
| --- | --- | --- | --- | --- | --- | --- |

## 8. Canonical field, query, and artifact contract

### Canonical fields

| Field ID | User label | Type/cardinality | Source/provenance states | Editor and accessibility group | Validation/conflict behavior | Compact behavior |
| --- | --- | --- | --- | --- | --- | --- |

Keep one row and one independently identifiable editor/accessibility group per canonical field ID. Compact layouts may scroll, collapse, disclose, or abbreviate labels; they must not silently combine distinct fields.

### Search and filters

| Query/filter ID | Visible label and scope | Exact predicate/precedence | Included and excluded fixture examples | Count/order derivation | Selection and clear/reset behavior | Empty/error behavior |
| --- | --- | --- | --- | --- | --- | --- |

For every required scenario that selects a record after filtering, name the expected record and show why it satisfies the predicate.

### Cross-artifact consistency ledger

| Artifact/variant | Canonical fields and commands represented | States/scenarios represented | Intentional omissions or abbreviations | Consistency result |
| --- | --- | --- | --- | --- |

Use `PASS`, `CONTRADICTION`, or `NOT APPLICABLE`. Any unexplained material `CONTRADICTION` prevents `READY`.

## 9. Redesign findings (redesign mode only)

| ID | Before | After | Why | Rule / class | Exception checked |
| --- | --- | --- | --- | --- | --- |

## 10. State and recovery matrix

| State/event | Visible UI | Accessible feedback | Available actions | Data preserved | Exit/recovery |
| --- | --- | --- | --- | --- | --- |
| Initial/restored | | | | | |
| Loading/partial | | | | | |
| Empty | | | | | |
| Failure | | | | | |
| Offline/stale | | | | | |
| Permission denied | | | | | |
| Destructive pending | | | | | |
| Success | | | | | |
| Interrupted/cancelled | | | | | |

## 11. Adaptation matrix

| Context | Structure | Hidden/collapsed first | Persistent state | Command access | Acceptance criterion |
| --- | --- | --- | --- | --- | --- |
| iOS compact | | | | | |
| iPadOS narrow | | | | | |
| iPadOS medium | | | | | |
| iPadOS wide | | | | | |
| macOS minimum window | | | | | |
| macOS typical window | | | | | |
| macOS large/full screen | | | | | |

## 12. Input behavior and optional accessibility

| Concern | Required behavior | iOS | iPadOS | macOS | Verification |
| --- | --- | --- | --- | --- | --- |
| VoiceOver/semantics | | | | | |
| Text growth/localization | | | | | |
| Keyboard/focus | | | | | |
| Pointer/touch/gesture alternatives | | | | | |
| Non-color cues | | | | | |
| Reduce Motion | | | | | |
| Increase Contrast/Reduce Transparency | | | | | |

## 13. Material and motion

- Functional Liquid Glass surfaces:
- Standard content materials:
- Semantic color/text treatment:
- Motion purpose and origin:
- Interruption behavior:
- Reduce Motion alternative:

## 14. Implementation boundaries

- Preserve:
- May change:
- Must not change:
- APIs/components to verify:
- Deployment fallbacks:
- Prototype or usability checks:

## 15. Acceptance criteria

1. <Context → action/condition → observable result>
2. ...

## 16. Validation matrix

| Platform/context | Scenario | Input/settings | Expected result | Evidence to capture |
| --- | --- | --- | --- | --- |
```
