---
name: apple-ui-craft-design
description: Design implementation-ready native interfaces for macOS, iOS, and iPadOS using official Apple HIG sources. Use for new features, screens, windows, navigation, user flows, adaptive layouts, and redesigns. Use apple-ui-craft-review for existing UI audits or approval, and apple-ui-craft-implementation for code changes.
license: MIT
---

# Apple UI Craft Design

## One job

Turn a product requirement or redesign request into an implementation-ready native interface specification for iOS, iPadOS, and macOS. Do not audit for release approval and do not edit production code.

## Reference selection

Read `references/source-policy.md` before making platform decisions. Select affected sections of `references/native-rule-catalog.md`, `references/platform-profiles.md`, and `references/design-playbook.md`. Consult `references/anti-patterns.md` for relevant redesign mechanisms, and `references/apple-hig-sources.md` to locate the smallest relevant set of live Apple topics. Use `references/design-spec-template.md` for a detailed specification.

Do not read unrelated sections by default. Live Apple HIG and framework documentation override bundled summaries.


For each selected rule, follow its direct Apple section link and paragraph locator in `references/native-rule-catalog.md`; use `references/source-verification.md` for the dated coverage and corrections. Recheck meaning, platform, and availability before treating a rule as current.

For macOS window, restoration, or drag/drop acceptance criteria, select applicable cases from [macos-runtime-scenarios.md](references/macos-runtime-scenarios.md). Do not require features outside the product scope.

## Modes

Infer the mode from the request.

- `implementation-ready` — default; produce a complete specification and acceptance criteria.
- `concept` — compare viable platform structures and choose a direction, but still identify critical states and risks.
- `redesign` — inspect an existing concept, screenshot, or flow and include a strict Before/After/Why table.

None of these modes edit source code. Route implementation work to `apple-ui-craft-implementation`.

## Inputs to resolve

Apply these items to the requested design scope. Reuse established surrounding contracts; do not redesign or re-document unaffected application areas.

Use the prompt, repository documentation, and existing product behavior. State reversible assumptions instead of blocking unnecessarily.

- target platform subset: iOS, iPadOS, macOS
- minimum OS and UI framework constraints
- primary audience and primary task
- entry point and surrounding navigation
- content volume and density
- object hierarchy and selection model
- canonical field contract: stable ID, label, type/cardinality, provenance, validation, edit scope, and accessibility grouping
- search and filter contract: deterministic predicate, count derivation, ordering, selection preservation, and fixture/example membership
- cross-artifact obligations: which fields, states, commands, and scenarios every specification, mock, and state sheet must represent
- destructive, private, permissioned, offline, or long-running operations
- required window sizes, orientations, multitasking contexts, and input methods
- persistence, restoration, synchronization, and undo expectations
- deliverable depth and any fixed product constraints

If a missing fact changes architecture materially, present the safest default and mark the decision as an explicit assumption.

## Workflow

### 1. Establish an evidence and source contract

- Record which requirements are supplied, inferred, or unknown.
- Separate direct Apple guidance from platform convention and product heuristics using `references/source-policy.md`.
- Open specific Apple topics for any material numeric or platform claim.
- Do not design from the HIG landing page alone.

### 2. Frame the primary outcome

Write one sentence in this form:

```text
When <context>, a person can <primary outcome> without <main avoidable cost or risk>.
```

Then identify:

- primary action
- secondary and infrequent actions
- critical information needed before commitment
- interruption and recovery points
- success evidence

Reject a feature list that has no coherent user outcome. Simplicity is not hiding every control; it is making hierarchy and next actions clear.

### 3. Choose structure before styling

Apply these items to the requested design scope. Reuse established surrounding contracts; do not redesign or re-document unaffected application areas.

For each platform, choose and justify:

- app-level navigation
- screen/window hierarchy
- sidebar, split-view, tab, stack, document, or multiwindow structure
- selection ownership
- toolbar, menu, context-menu, and keyboard command surfaces
- sheet, popover, alert, inspector, or separate-window presentation
- search placement and filter visibility

Do not force one layout across all three platforms. Keep terminology and command semantics stable while adapting navigation, density, modality, and command placement.

### 4. Map every surface to native components

Create a component map containing:

- purpose and scope
- preferred native SwiftUI/UIKit/AppKit component or pattern
- custom behavior only when a standard component is insufficient
- accessible name/value/state/action expectations
- input paths: touch, pointer, keyboard, menu, gesture
- availability and fallback questions for implementation

A custom control carries the burden of proof. State what native capability it replaces and how it preserves pressed/selected/disabled/progress states, accessibility, focus, keyboard activation, and platform behavior.

### 5. Lock the canonical data, query, and artifact contract

Apply these items to the requested design scope. Reuse established surrounding contracts; do not redesign or re-document unaffected application areas.

Before drawing compact variants or declaring readiness:

- enumerate every user-visible canonical field with a stable field ID, label, type/cardinality, provenance states, validation, edit scope, and accessible grouping
- preserve a one-to-one mapping between canonical field IDs and editors across window sizes; compact layouts may scroll, collapse, disclose, or abbreviate labels, but must not merge logically distinct fields into one editor or accessibility group
- define every search scope and filter as a deterministic predicate, including included/excluded examples, count derivation, ordering, selection preservation, clear/reset behavior, and empty/error behavior
- bind required scenarios and synthetic fixtures to the exact records each query or filter must return; if a required record's membership is ambiguous, the design is `NOT READY`
- compare the specification, every layout mock, every state sheet, and every scenario. Record intentional visual omissions explicitly; treat an unexplained field, state, command, or scenario contradiction as a readiness failure

Do not let a visually compressed artifact silently change the product data model.

### 6. Specify the full state model

Cover only states the product can produce, but do not omit likely failure paths:

- initial and restored
- loading and partial data
- empty
- success
- validation error
- operation failure and retry
- offline or stale content
- permission not determined, denied, restricted, and granted
- disabled or unavailable action
- destructive preview, commit, undo, and irreversible completion
- cancellation and interruption

For each state, specify visible feedback, accessible feedback, available actions, data preservation, and exit/recovery behavior.

### 7. Design adaptation as behavior

Apply these items to the requested design scope. Reuse established surrounding contracts; do not redesign or re-document unaffected application areas.

Specify observable changes, not “make responsive.”

- iOS: compact width, supported orientation, reachable controls, system navigation gestures, text growth.
- iPadOS: narrow, medium, and wide windows; multitasking; software keyboard; touch, pointer, and hardware keyboard; which column collapses first.
- macOS: minimum, typical, large, and full-screen windows; menu completeness; shortcuts; focus; table/outline behavior; multiple windows if valuable.
- All: safe areas, localization, right-to-left layout where relevant, light/dark, Increase Contrast, Reduce Transparency, Reduce Motion, and representative accessibility text sizes.

For every compact or collapsed variant, account for every canonical field and core command by stable ID. State whether it remains visible, scrolls, moves into a disclosure/inspector, or becomes reachable through another native surface.

State the minimum usable layout and any justified minimum window size.

### 8. Specify feedback, recovery, material, and motion

- Prefer immediate inline status near the affected object.
- Prefer undo for routine recoverable destruction; reserve confirmation for uncommon or irreversible loss.
- Use determinate progress only when it reflects real progress.
- Keep Liquid Glass in the functional control/navigation layer and standard materials in content.
- Give every custom motion a purpose and a Reduce Motion alternative.
- Keep gesture-driven movement under direct control and define interruption behavior.

Do not import web animation curves or duration tables as Apple-native rules. Repository motion tokens are implementation choices, not HIG facts.

### 9. Run design gates

Evaluate the design against the non-negotiable gates in `references/design-playbook.md`.

Use one readiness verdict:

- `NOT READY` — a material product, safety, recovery, accessibility, platform, or feasibility gap prevents responsible implementation.
- `READY WITH RISKS` — implementable, but named assumptions or validation risks remain.
- `READY` — architecture, states, adaptation, accessibility, and acceptance criteria are sufficiently explicit for implementation.

Approval is earned. Do not use `READY` while a critical path, destructive consequence, iPad resizing strategy, macOS command surface, accessibility behavior, canonical field mapping, required filter predicate, or cross-artifact contradiction is unspecified.

### 10. Make the handoff self-contained

The output must be usable by an implementer who has no access to this conversation. Include exact behavior, platform differences, native component mapping, state and input matrices, rule IDs, source URLs, exceptions, boundaries, and testable completion criteria.

## Hard rules

- Do not edit production code.
- Do not claim that copying an Apple app automatically satisfies the HIG.
- Do not call a product preference an Apple requirement.
- Do not invent framework APIs or deployment availability.
- Do not hide an unresolved architecture decision behind “follow HIG.”
- Do not make a screenshot-perfect fixed layout the acceptance criterion.
- Do not use color, material, motion, gesture, hover, or context menus as the sole carrier of meaning or core action.
- Do not make iPadOS a widened iOS screen or macOS an iPad screen with a title bar.
- Do not recommend a custom control without its semantic, focus, input, state, and accessibility contract.
- Do not use a numeric rule without an exact source or dated-snapshot label.
- Do not merge distinct canonical fields in a compact mock unless the product data model itself intentionally changes and the decision is explicit.
- Do not name a search scope or filter without an exact predicate, example membership, count behavior, and selection/reset semantics.
- Do not claim that a static specification or mock proves runtime focus order, VoiceOver output, resizing behavior, contrast, motion, or recovery atomicity.

## Required output

Use `references/design-spec-template.md` for an implementation-ready specification. For a bounded concept or local design decision, include applicable behavior, assumptions, material Apple sources, accessibility/input implications, risks, and acceptance criteria in concise prose. Omit unrelated sections; do not leave material behavior or readiness limitations implicit.

For a full specification, include the applicable items in this order:

1. readiness verdict and blocking/risk summary
2. design summary and primary outcome
3. assumptions, constraints, and evidence limits
4. source ledger with claim classes
5. cross-platform strategy matrix
6. information architecture and navigation rationale
7. screen/window/flow specification
8. native component and command mapping
9. canonical field, query/filter, and cross-artifact consistency contract
10. Before/After/Why table for redesign mode
11. state and recovery matrix
12. adaptation matrix
13. accessibility and input matrix
14. material and motion specification
15. implementation boundaries and API questions
16. acceptance criteria and validation matrix
