# Verdict policy

Use these formal labels for an explicit approval/readiness request, detailed audit report, or required coordinator handoff. An ordinary narrow review may state its conclusion in plain language; the same severity and evidence standards still apply, and it must not imply formal approval.

Issue a formal HIG verdict only when `Review integrity` is `PASS`. Add an evidence qualifier in parentheses when necessary. Every verdict applies only to the identified reviewed input. All verdicts, including `APPROVE WITH NOTES`, require a reviewer who did not implement the change.

If review integrity is `INVALIDATED`, do not issue a HIG verdict. `INVALIDATED` is an operational state, not a fifth verdict.

## Verdict scope

Apply [accessibility-scope.md](accessibility-scope.md) before evaluating severity or evidence. Excluded accessibility is not a Blocker, Major, missing check, or reason to downgrade. A formal verdict identifies the reviewed scope once, for example `APPROVE (reviewed scope; accessibility excluded)`. `APPROVE` is not full HIG or whole-release approval. Only explicitly requested accessibility features enter its requirements.

## BLOCK

Use when at least one confirmed `Blocker` exists.

Typical conditions:

- critical task cannot complete in a declared supported context
- credible data-loss, privacy, or safety risk
- essential core workflow unavailable to an expected ordinary input path, or a specifically requested assistive path
- navigation or modal state traps people or discards work
- deployment/API mismatch prevents correct execution

A polished visual layer does not offset a Blocker.

## CHANGES REQUIRED

Use when:

- no Blocker remains, and
- at least one confirmed `Major` finding remains.

The interface may work, but it should not be treated as release-ready until the listed Major findings are fixed and independently revalidated.

## APPROVE WITH NOTES

Use when:

- no Blocker or Major remains
- only Minor, Nit, or Investigation items remain
- or critical dimensions are not fully evidenced

Required evidence qualifiers include:

- `visual-only`
- `recording-only`
- `code-only`
- `runtime-limited`

Examples:

```text
APPROVE WITH NOTES (visual-only)
```

```text
APPROVE WITH NOTES (code-only; requested runtime checks not performed)
```

Do not phrase this as full release approval.

## APPROVE

Use only when all are true:

- review integrity is `PASS`
- the current reviewer did not implement the change or mutate it during the review assignment
- no actionable Blocker or Major remains
- material Minor findings are resolved or explicitly accepted with rationale
- code and representative runtime behavior were inspected
- critical path and relevant failure/recovery, adaptation, and ordinary input were exercised; accessibility settings were exercised only for explicitly requested features
- official-source and deployment-target questions are resolved
- the validation matrix records exact contexts and outcomes

An empty scanner report is not sufficient. Do not add excluded dimensions to the validation matrix.

## Review-limited handling

When evidence is too weak even for a meaningful visual/code verdict, use:

```text
APPROVE WITH NOTES (evidence insufficient for release verdict)
```

Then list exactly what must be inspected. Do not invent a fifth verdict.

## Independent re-review

An agent that implemented a change cannot approve that change, even in a renamed stage or with a fresh baseline. Implementation-side post-change checks are validation evidence only.

For independent re-review:

1. Assign an independent reviewer who did not implement the change, with no mutation authority. Use a subagent or independently staffed review stage within the same user task unless the user requires separate tasks.
2. Capture a fresh integrity baseline before substantive inspection.
3. Verify every prior Blocker/Major against the new code and runtime behavior.
4. Detect regressions introduced by the fix.
5. Preserve accepted exceptions and documented product decisions.
6. Update the verdict from current evidence, not from the previous verdict.
7. Do not reopen unrelated polish unless it became newly material.
