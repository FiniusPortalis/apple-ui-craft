# Review output template

Use detailed sections only at the requested depth. Follow [accessibility-scope.md](accessibility-scope.md): omit accessibility-only sections, rows, and columns by default; retain ordinary input, layout, and validation details that affect the task. In a formal report, identify the selected scope once rather than listing excluded features as `NOT RUN`.

Preserve the integrity result and scope, reviewer identity, evidence-qualified verdict, actionable Before/After/Why findings, sources, validation limits, and required role-boundary handoff. Use the full template for a detailed audit or formal handoff; for a narrow review, combine these facts into a concise report and omit empty tables or repeated sections.

For a detailed report, keep findings in one Before/After/Why table. For a narrow review, concise prose may preserve the same actionable facts; omit an empty table when no findings remain.

## Integrity pass output

```markdown
# Verdict: BLOCK | CHANGES REQUIRED | APPROVE WITH NOTES | APPROVE

**Review integrity:** PASS  
**Integrity scope:** <repository root or exact reviewed paths; file count and aggregate digest when available>  
**Review owner / stage:** <identity; initial or post-change review>\
**Reviewed input:** <baseline/state to which this verdict applies>\
**Evidence qualifier:** visual-only | recording-only | code-only | runtime-limited | runtime-tested  
**Highest risk:** <one sentence, or “No Blocker/Major finding.”>

## Context and evidence limits

- Platforms / OS range:
- Artifact reviewed:
- Primary task:
- Contexts represented:
- Contexts not verified:
- Material assumptions:
- Source changes requested by user: yes | no
- Report artifact allowlisted: none | <exact path>

## Findings

| ID | Severity | Confidence | Platform | Location | Before | After | Why | Rule / class | Exception checked | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIG-001 | Major | High | iPadOS | `Sources/BrowserView.swift:88` | `frame(width: UIScreen.main.bounds.width)` pins the shell to device bounds | derive from the current container and define narrow/medium/wide column behavior | Resized windows can lose content and commands | `IPAD-01`, `ADAPT-01` · APPLE-HIG | Fixed canvas? No; the whole shell is fixed | Resize through narrow/medium/wide contexts and confirm selection and commands persist |

If there are no actionable findings, keep the header and state directly below it: “No actionable findings in the validated scope.”

## Positive observations to preserve

Maximum three, each specific and evidenced.

- ...

## Remediation order

| Order | Finding(s) | Dependency / reason | Safe to combine? |
| --- | --- | --- | --- |

## Role-boundary handoff

- Source changes requested: yes | no
- Source changes performed by this review: no
- Implementation invoked by the review assignment: no
- Review assignment closed: yes | no
- Continuation: review complete only | authorized implementation next | pending explicit gate | unavailable execution boundary
- Next owner / stage and authorization: <scope, identity, user gate if any>
- Recommended next Skill: `apple-ui-craft-implementation` | none
- Implementation handoff findings: <IDs and ordered scope>
- Required implementation boundaries: <files/behaviors not to broaden into>
- Independent re-review after implementation: yes | no
- Required contexts before approval: <runtime/accessibility/window/input contexts>

## Validation matrix

| Platform/context | Scenario | Input/settings | Expected result | Status/evidence |
| --- | --- | --- | --- | --- |

## Source ledger

| Finding | Apple topic | URL | Verified | Claim class |
| --- | --- | --- | --- | --- |
```

## Integrity invalidation output

When the reviewed input changed unexpectedly, do not issue a HIG verdict. Use this form instead:

```markdown
# Review integrity: INVALIDATED

**HIG verdict issued:** No  
**Baseline scope:** <targets, file count, aggregate digest>  
**Reason:** input drift or unexpected repository write

## Detected changes

| Change kind | Path | Baseline | Current |
| --- | --- | --- | --- |

## Evidence collected before invalidation

State only observations that remain useful. Do not approve, reject, or continue reviewing the mixed state.

## Fresh-review requirements

- restore or intentionally accept the workspace state outside this review assignment
- start a fresh review assignment under the role-boundary contract; no new sidebar task is required unless the user requested one
- capture a new integrity baseline
- rerun the affected checks
```

## Table rules

- `Before` contains the observed code or behavior, not a generic label.
- `After` is specific enough to implement, but does not require a full patch.
- `Why` explains user impact, not “because HIG.”
- `Exception checked` prevents mechanical rule application.
- `Verification` is observable and platform-specific.
- Keep repeated root causes together when one structural fix resolves them.
- Never include claims that source was fixed by this review assignment.
- In a combined request, this is the reviewer output to the coordinator, not the final completion report for implementation. The coordinator reports actual implementation/validation and any independently issued post-change verdict separately.
