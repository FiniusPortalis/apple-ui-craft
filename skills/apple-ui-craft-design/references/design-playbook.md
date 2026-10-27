# Design playbook

Apply [accessibility-scope.md](accessibility-scope.md) before selecting criteria. Accessibility-only requirements, examples, settings, and checks below apply only to explicitly requested accessibility work; ordinary UI/input requirements remain in the requested task scope.

Apply gates to features and artifacts in the requested scope. A gate for a feature absent from that scope is inapplicable; do not invent fields, filters, additional platforms, or mock artifacts to satisfy it.

## Non-negotiable gates

A design cannot receive `READY` when any applicable gate fails.

| Gate | Pass condition | Typical failure |
| --- | --- | --- |
| Purpose | One primary outcome and a clear hierarchy | Feature list with multiple equal primary actions |
| Agency | People can exit, cancel, undo, or recover where the product allows it | Guided mode traps people or discards work unexpectedly |
| Data safety | Destructive scope, reversibility, confirmation, and undo are explicit | “Delete” behavior unspecified |
| Native structure | Platform navigation and command surfaces are selected and justified | Same mockup forced onto iPhone, iPad, and Mac |
| Adaptation | Minimum, representative, and expanded contexts have defined behavior | “Responsive” with no column-collapse or window strategy |
| Accessibility (only when requested) | Semantics, text growth, non-color cues, focus, input alternatives, and motion settings are explicit | Accessibility deferred until after implementation |
| State completeness | Likely loading, empty, failure, permission, offline, and interruption states are defined | Only ideal loaded screenshot exists |
| Canonical data | Every field keeps a stable ID, cardinality, provenance, validation, and editor across layout variants; specify accessibility grouping only when requested | A compact mock silently combines two independent fields |
| Query determinism | Every search scope and filter has an exact predicate, example membership, count derivation, ordering, selection, and reset behavior | A named filter exists but required fixture membership is undefined |
| Artifact consistency | Specifications, mocks, state sheets, and required scenarios agree, with intentional omissions recorded | Wide and compact artifacts imply different field counts |
| Evidence boundary | Runtime-only properties are assigned to explicit implementation validation instead of being inferred from static artifacts | A mock is treated as proof of VoiceOver, focus order, resizing, contrast, or atomic recovery |
| Feasibility | APIs are plausible for deployment targets and custom work is bounded | Invented API or unbounded design-system rewrite |
| Verification | Acceptance criteria are observable and platform-specific | “Feels native” is the only completion test |

## Readiness rules

### NOT READY

Use when any of these is unresolved and material:

- primary outcome or object hierarchy is contradictory
- irreversible/destructive consequences are unknown
- a core action has no discoverable ordinary input path, or lacks a specifically requested assistive path
- the design loses the primary task at supported window sizes
- iPadOS resizing/multitasking behavior is absent for an iPad target
- macOS menu/keyboard/window behavior is absent for a Mac target
- required state or permission behavior can discard user work
- the design requires an unverified API with no fallback
- a canonical field changes cardinality, editor ownership, or explicitly requested accessibility grouping between layout variants without an explicit product decision
- a required search/filter scenario lacks a deterministic predicate or fixture membership
- specification, mock, state sheet, and scenario artifacts contradict one another on a material field, state, command, or recovery path

### READY WITH RISKS

Use when architecture is implementable but one or more of these remains:

- a reversible product assumption needs stakeholder confirmation
- exact content density or minimum window size needs prototype testing
- a custom control has a complete contract but requires usability testing
- motion/material quality needs device evaluation
- a noncritical API fallback remains to be selected

### READY

Use only when an implementer can begin without inventing product behavior, canonical fields and query predicates are deterministic, cross-artifact checks pass, and every critical acceptance criterion is observable.

## Canonical field contract

For every editable or reviewable field, record:

- stable field ID and user-visible label
- value type and cardinality
- source/provenance states, including manual versus suggested values when relevant
- validation, dirty-state, persistence, and conflict behavior
- editor ownership; accessible name/value/group only when requested
- representation at minimum, typical, and expanded layouts

Compact layouts may change presentation, not semantics. Scrolling, disclosure, and inspector relocation are valid; combining two independent field IDs into one editor is not. Evaluate assistive grouping only when requested.

## Deterministic query and filter contract

For every search scope or filter, record:

- exact predicate and precedence when combined with search or other filters
- included and excluded examples from the supplied or synthetic fixture
- count derivation and refresh timing
- ordering and tie-breaking
- selection preservation or clearing behavior
- clear/reset, no-results, stale, and failure behavior

Walk every required scenario against the contract. A scenario that names a record after filtering must prove that record satisfies the predicate.

## Cross-artifact consistency gate

Create a ledger covering the specification, each layout mock, each state sheet, and each required scenario. For every artifact, account for canonical field IDs, state IDs, commands, and expected records. Mark intentional omissions or label abbreviations; otherwise, a contradiction blocks `READY`.

Static artifacts can specify runtime behavior but cannot prove it. Put only required in-scope runtime checks in the validation matrix. Include VoiceOver, assistive focus, and accessibility contrast checks only when requested; excluded checks are not evidence gaps.

## Structure chooser

### App-level navigation

| Situation | iOS default | iPadOS default | macOS default |
| --- | --- | --- | --- |
| A few peer destinations | Tab structure | Adaptable tab/sidebar or sidebar | Sidebar, toolbar, or app-specific navigation |
| Hierarchical drill-down | Navigation stack | Split view or stack depending width | Sidebar/outline plus detail; separate windows for independent documents |
| Master-detail selection | Stack or list-to-detail | `NavigationSplitView`/split view | Split view, outline/table plus detail/inspector |
| Document-centric work | Document browser/editor as appropriate | Multiwindow document workflow | Document windows, standard File commands, undo/redo |
| Single focused task | One primary view with contextual presentation | One view or split only if it adds value | One window with modeless supporting surfaces |

Do not choose by framework convenience alone. Selection persistence, restoration, deep linking, and command scope matter.

### Presentation chooser

| Need | Prefer | Avoid |
| --- | --- | --- |
| Local validation or status | Inline feedback | Informational alert |
| Small source-related choice | Popover at sufficient width | Full-screen transition |
| Compact-width contextual task | Adaptive sheet | Forced tiny popover |
| Focused multistep task | Sheet or dedicated flow with clear cancel/commit | Nested popovers |
| App-wide settings | iOS/iPadOS settings flow as product requires; macOS app Settings | macOS toolbar gear as sole entry |
| Parallel reference or inspection | iPad/macOS inspector, sidebar, split region, or separate window | Blocking dialog |
| Uncommon irreversible action | Alert/confirmation with clear consequence | Routine alert for recoverable deletion |

### Search chooser

- Place search near what it scopes.
- A sidebar search filters sidebar content; a toolbar search can search the current window; a dedicated search area is justified when discovery is the primary task.
- Show active filters or scope strongly enough to explain surprising results.
- On iPadOS, avoid surprising software-keyboard invocation from automatic focus unless typing is clearly the immediate task.
- Define no-results, partial-results, stale-results, search-error, and cleared-history behavior as applicable.

## Command-surface mapping

For every command, classify:

- frequency: constant, frequent, occasional, rare
- scope: selection, view, window, document, app
- consequence: reversible, confirmable, irreversible
- availability: always, selection-dependent, permission-dependent, state-dependent
- surfaces: visible control, toolbar, row action, context menu, app/menu bar, keyboard shortcut, gesture

Rules:

- iOS: visible and contextual controls carry most ordinary commands; gestures accelerate but do not monopolize the core path.
- iPadOS: combine visible controls with menus and keyboard commands; verify framework overflow and use a More menu for additional actions when needed.
- macOS: the menu bar is the complete command surface; toolbars and context menus are convenient subsets.

## Custom-control burden of proof

A custom control specification answers the applicable in-scope questions below:

1. What task cannot a standard control perform?
2. What are normal, pressed, focused, hovered, selected, disabled, loading, error, and destructive states?
3. When accessibility is requested, what is the accessible role, name, value, state, and action set?
4. How does it work with touch, pointer, and ordinary keyboard input? Include Full Keyboard Access, VoiceOver, and Switch Control only when requested.
5. What is its minimum interaction region and spacing behavior?
6. How does it reflow with localization and ordinary content growth? Include accessibility text sizes only when requested.
7. When requested, what happens under Reduce Motion, Increase Contrast, and Reduce Transparency?
8. How is it tested at supported OS versions?

If required in-scope answers are absent, prefer the standard component. Excluded accessibility answers do not block readiness.

## Cross-platform reconciliation

Create a table with rows for:

- primary navigation
- selection model
- search/filter placement
- command exposure
- modal versus modeless support
- window/scene behavior
- keyboard/pointer/touch paths
- destructive recovery
- state restoration
- material and motion

For each row, mark:

- `Shared semantics`
- `Platform-specific presentation`
- `Intentional exception`
- `Validation required`

This prevents false consistency while preserving product identity.

## Acceptance-criterion quality

Bad:

```text
The app should look native and be responsive.
```

Good:

```text
For this example product, at the narrowest supported iPad window, the tertiary inspector collapses before the sidebar (a product-specific decision, not a universal Apple order); the selected PDF and current search/filter state remain visible, and every toolbar command remains reachable through system overflow or a menu.
```

Every criterion needs:

- context
- action or condition
- observable result
- preserved state or recovery expectation
- platform/input/accessibility variant when material
