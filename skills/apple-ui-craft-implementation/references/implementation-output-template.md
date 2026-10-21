# Implementation output template

For a bounded change, report the implemented behavior and files, checks and results, and material limitations in concise prose. Use the full template for a complex change, a requested durable report, or an independent review handoff. Omit inapplicable sections and combine repeated evidence. Always preserve implementation/review ownership, actual validation limits, user changes, explicit gates, and the prohibition on self-approval.

Implementation output reports change status and validation evidence. It never returns the implementer's own review verdict. In a combined request this output goes to the coordinator for any remaining independent review and the overall completion report.

```markdown
# Implementation status: COMPLETED | PARTIAL | BLOCKED BY DRIFT | VALIDATION FAILED

**Mode:** implement | plan-only | execute-plan  
**Implementation owner / stage:** <identity>\
**Plan / handoff:** <path, finding IDs, or direct request>  
**Approval verdict issued:** No — independent review required when approval is requested

## Scope completed

- Changed files:
- User-visible behavior:
- Deferred or out-of-scope items:

## Rationale and preserved exceptions

| Change | Rule / claim class | Apple source | Exception or product decision preserved |
| --- | --- | --- | --- |

## Platform and accessibility behavior

| Platform/context | Behavior changed | Input/settings covered | Result/evidence |
| --- | --- | --- | --- |

## Mechanical validation

| Command/check | Result | Evidence or limitation |
| --- | --- | --- |

## Runtime validation

| Context | Scenario | Observed result | Status |
| --- | --- | --- | --- |

## Diff-scope confirmation

- Starting commit/state:
- Implementation-owned files:
- Pre-existing/user changes preserved:
- Unexpected changes: none | <details>

## Independent review handoff

- Review required: yes | no
- Next independent reviewer / stage: <identity or unavailable; same-task delegation allowed>
- Continuation status: not required | ready for coordinator to run | pending explicit gate | unavailable reviewer
- Recommended Skill: `apple-ui-craft-review`
- Findings/areas to re-review:
- Required runtime contexts:
- Remaining evidence gaps:
```

## Prohibited verdict language

Do not use any of these as the implementation conclusion:

- `BLOCK`
- `CHANGES REQUIRED`
- `APPROVE WITH NOTES`
- `APPROVE`

`BLOCKED BY DRIFT` is an implementation execution status, not a HIG review verdict.
