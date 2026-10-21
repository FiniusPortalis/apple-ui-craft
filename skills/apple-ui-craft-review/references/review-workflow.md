# Detailed review workflow

Read for a standard/deep audit or a formal implementation handoff. For a narrow quick review, the entrypoint and selected rubric sections suffice. Script examples reuse the absolute paths initialized in [SKILL.md](../SKILL.md).

## Establish scope and evidence

Identify or infer:

- target platforms and minimum OS range
- artifact type: screenshot, recording, code, diff, or running build
- device/window contexts and inputs represented
- primary task and critical path
- states present and absent
- repository conventions and deliberate exceptions
- review mode
- whether source modification was requested
- whether a report artifact is allowlisted

State what the artifact can and cannot prove using `source-policy.md`. A screenshot-only review cannot receive an unqualified full approval.

## Workflow

### 1. Recon before judgment

Select applicable categories and runtime contexts from the declared review scope and mode. Inspect adjacent behavior only where it can explain a finding or realistic regression. A targeted review does not establish whole-application approval. Do not omit relevant accessibility, safety, recovery, or availability checks merely to keep the review short.

For code or a PR:

- read `AGENTS.md`, relevant README/design docs, deployment targets, build configuration, and test conventions
- inspect affected framework, navigation/state ownership, design tokens, commands, scenes, localization, and accessibility helpers only as needed for the declared scope
- identify the smallest files that explain each behavior
- inspect tests and preview/sample states
- preserve the integrity snapshot and do not edit any inspected artifact

For screenshots or recordings:

- map visible hierarchy, navigation, labels, presentation, density, selection, and state
- do not infer semantics, target size, focus order, keyboard access, contrast ratio, or hidden recovery behavior without evidence

For a running build:

- exercise the main path, interruption, recovery, resize/orientation, text growth, and relevant accessibility/input settings
- record exact context and observed result
- keep runtime/build outputs outside the repository or downgrade the evidence qualifier

### 2. Select specific source topics

Open the platform overview and only the component/foundation topics needed for the actual findings. Do not cite the HIG home page as the sole basis for a specific claim.

Classify each candidate as:

- `APPLE-HIG`
- `APPLE-API`
- `PLATFORM-CONVENTION`
- `PRODUCT-HEURISTIC`
- `EVIDENCE-GAP`

### 3. Select applicable review areas

Select applicable categories and runtime contexts from the declared review scope and mode. Inspect adjacent behavior only where it can explain a finding or realistic regression. A targeted review does not establish whole-application approval. Do not omit relevant accessibility, safety, recovery, or availability checks merely to keep the review short.

1. primary task and hierarchy
2. native controls, roles, and interaction states
3. adaptive layout and supported window/orientation contexts
4. accessibility semantics, text growth, non-color cues, and alternate input
5. destructive action, cancellation, undo, and data preservation
6. loading, empty, error, offline, permission, and feedback behavior
7. platform navigation, window, menu, toolbar, shortcut, and focus behavior
8. search, sidebar, split-view, popover, sheet, alert, and context-menu usage
9. material, contrast, custom motion, and Reduce Motion
10. source accuracy, deployment availability, and evidence honesty

Use the platform minimums in `review-rubric.md`. Do not spend time on polish while a critical path or accessibility barrier remains.

### 4. Use static hints only as candidates

For Swift sources, optionally run:

```bash
python3 "$CRAFT_REVIEW_SKILL/scripts/apple_ui_craft_hints.py" "$CRAFT_SCOPE" --platform all
```

Useful variants:

```bash
python3 "$CRAFT_REVIEW_SKILL/scripts/apple_ui_craft_hints.py" "$CRAFT_SCOPE" --platform ipados --format json
```

```bash
python3 "$CRAFT_REVIEW_SKILL/scripts/apple_ui_craft_hints.py" "$CRAFT_SCOPE" --format sarif
```

Every result is a candidate. Confirm context, exception, and user impact before reporting it. A clean scan is not approval.

### 5. Vet and classify findings

For every finding:

- cite `file:line`, visible region, or exact runtime step
- show current behavior/code in `Before`
- specify the exact target behavior/code in `After`
- explain user impact in `Why`
- assign severity and confidence
- name the directly applicable rule ID and claim class; if none fits, state `no matching catalog rule` and use the exact API/product-contract basis
- link the most specific official Apple source
- state the exception checked
- give a reproducible verification or done criterion

When the correct fix depends on runtime evidence, report `Investigation` rather than inventing a solution.

### 6. Apply strict escalation and remediation order

Use the escalation triggers and severity rules in `review-rubric.md`.

Prefer remediation in this order:

1. restore task completion, safety, and data recovery
2. restore native semantics and accessible input
3. fix navigation, windowing, resizing, and platform command structure
4. complete state, status, and recovery behavior
5. remove unnecessary custom controls, glass, motion, and modality
6. consolidate consistency and polish

The strongest recommendation is often to remove an unnecessary custom mechanism rather than tune it.

### 7. Verify review integrity

Run the integrity verification before determining the verdict. Compare the ending state with the exact baseline captured for this review assignment, before the coordinator starts implementation.

- `PASS` — no unexpected reviewed-artifact change occurred; verdict evaluation may continue.
- `INVALIDATED` — input drift or an unexpected write occurred; stop without a HIG verdict.

Do not silently accept a change because it appears to fix a finding. That change belongs to a separate implementation assignment or closed-stage continuation and requires a new baseline for any post-change review.

### 8. Determine the verdict

Only when review integrity is `PASS`, use exactly one verdict from `verdict-policy.md`:

- `BLOCK`
- `CHANGES REQUIRED`
- `APPROVE WITH NOTES`
- `APPROVE`

Add an evidence qualifier when material, such as `visual-only`, `code-only`, or `runtime-tested`. Do not soften a Blocker because the overall interface looks polished.

### 9. Hand findings to the coordinator for continuation

The review never edits source or writes implementation plans. When mutation was requested, return findings and a self-contained handoff to the coordinator so the implementation role can act without rediscovering intent. For review-only requests, recommendations are not authorization to implement.

Specify:

- recommended execution order
- dependencies and shared root causes
- findings safe to combine
- findings requiring independent prototype or measurement
- exact validation contexts needed before approval
- source changes requested: yes/no
- source changes performed by this review: no
- completed review baseline, integrity result, and reviewer/stage identity
- authorized findings, explicit user gates, and next implementation owner/stage
- whether independent re-review is required after implementation

The coordinator continues authorized work after this review assignment closes. Preserve the review result as evidence for its input state; do not present it as approval of later edits. If a gate or unavailable execution boundary prevents continuation, report what remains and the specific next action instead of claiming the whole request is complete.

