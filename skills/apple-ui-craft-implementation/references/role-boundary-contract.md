# Review / implementation role-boundary contract

Separate **responsibilities and evidence**, not necessarily user-visible tasks. A user task is the overall request; an assignment is one agent's role; a stage is a closed interval of work with explicit input, permissions, and output. Skill names describe responsibilities, not technical permissions. User instructions determine scope and stage gates.

## Canonical routing

| User intent | Execution path | Source mutation | Completion report |
| --- | --- | --- | --- |
| Review, audit, findings, release readiness, or approval only | `apple-ui-craft-review` assignment | Forbidden; only an explicitly allowlisted report artifact may be written | Findings and evidence-qualified verdict when integrity/evidence requirements pass; no implementation |
| Fix, implement, apply, patch, or refactor only | `apple-ui-craft-implementation` assignment | Only within authorized scope | Changes and implementation validation; no self-approval |
| Review and fix | Coordinator → read-only reviewer → implementation agent or coordinator's separate implementation stage → validation | Reviewer never edits; implementation starts after review closes | Coordinator reports findings addressed, actual changes, checks, and remaining work; a handoff alone is incomplete |
| Review and fix with a final formal verdict | Same path, then independent read-only post-change reviewer | No writes during either review assignment | Implementation status and independent verdict reported separately; missing formal review remains pending |

## Coordination and stage boundaries

- For review-and-fix, use a read-only review subagent when delegation is available and allowed. Keep that agent in the reviewer role; the coordinator or another implementation agent applies the authorized findings.
- Before delegation, identify the user's requested outcome, edit scope, explicit stage gates, and whether a final formal verdict is needed. Give the reviewer the unchanged input scope and read-only assignment, not authority to fix.
- Wait for the reviewer to finish and return its findings, baseline/integrity result, evidence limits, and handoff before changing reviewed inputs. Do not run implementation concurrently against an open review baseline. An `INVALIDATED` review cannot serve as a completed review gate; resolve the drift outside the reviewer and obtain a fresh valid review when required.
- Close and preserve the review output before opening the implementation stage. Identify its owner, authorized files/findings, permitted writes, and required validation. Refresh handoff locations and current state as required by the implementation Skill.
- Continue through authorized implementation and validation without routinely asking again or requiring the user to create another task. For review-only, finish with the review; recommendations do not authorize edits.
- Honor “first review only”, “fix after my approval”, and “audit and implementation in separate tasks”. A requested independent technical verdict is distinct from a user approval gate. Do not infer a user gate merely from the need for independent review.
- Do not create new sidebar tasks unless explicitly requested. Delegation within the current task does not authorize external writes, permission escalation, or a wider change scope.

## Independence and unavailable execution paths

An implementation agent never returns `BLOCK`, `CHANGES REQUIRED`, `APPROVE WITH NOTES`, or `APPROVE` as its own review verdict. Its post-change checks are **implementation validation**. Final formal review requires a reviewer who did not implement the change, no mutation authority in that assignment, a fresh post-change baseline, and evidence sufficient for the claimed verdict. The coordinator may relay that result with attribution; it must not relabel its own checks as independent approval.

When subagents are unavailable or disallowed, an ordinary review-and-fix request may use clearly separated sequential stages: finish the read-only assessment, preserve its findings and integrity result, then enter the already authorized implementation stage and validate. Disclose that the same agent performed both stages and do not claim independent formal approval. Stage labels alone do not enforce read-only access.

If the user selected a formally independent or technically enforced audit, preserve that contract. A same-agent sequence does not satisfy independence, and a stage transition cannot bypass actual read-only permissions. If neither permitted delegation nor an appropriate separated stage is available, complete the allowed review and report the unavailable boundary, pending implementation, and the needed execution context. If only the final independent reviewer is unavailable, finish authorized implementation/validation unless an explicit gate forbids it, then report the formal verdict as pending. Do not invent a new task or claim overall completion while a requested step remains.

## Handoff minimum

A review-to-implementation handoff must be usable without conversation context and include:

- reviewer/agent or stage identity, reviewed input baseline, and integrity result
- finding IDs, severity, platform, and exact locations
- current behavior/code and exact target behavior/code
- Apple source/classification and exceptions checked
- execution order, dependencies, and safe combinations
- authorized scope, prohibited changes, and explicit user stage gates
- verification contexts and done criteria
- statement that the review assignment performed no source mutation
- next implementation owner/stage, or the concrete reason continuation is unavailable
- requirement for independent re-review when a final formal verdict is needed

An implementation-to-review handoff must include:

- implementation owner/stage, mode, and plan path, if any
- changed files and user-visible behavior
- exact commands/tests and results
- runtime and accessibility contexts actually checked
- remaining checks, known limitations, and plan drift
- diff-scope confirmation
- explicit statement that the implementer issued no approval verdict

The coordinator's final response distinguishes initial findings, implementation and validation, any independent post-change verdict with attribution, and unfinished work. Preserve the original review as evidence about its original input; it does not approve later edits.

## Assurance levels

The Skill instructions provide **best-effort role adherence**. They do not themselves revoke filesystem or tool permissions.

- Best-effort read-only: routing rules and mutation firewall in `SKILL.md`.
- Detectable read-only: start/end manifests, Git diff checks, and file-event traces.
- Enforced read-only: OS/filesystem sandbox, tool allowlist, and a separate report-only write root.

Use enforced read-only execution when write prevention is a requirement rather than a behavioral preference. Report the level actually provided; neither an integrity `PASS` nor a new stage proves technical enforcement or reviewer independence.
