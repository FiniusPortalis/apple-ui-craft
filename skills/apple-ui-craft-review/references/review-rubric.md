# Review rubric

Apply [accessibility-scope.md](accessibility-scope.md) before selecting criteria. Accessibility-only requirements, examples, settings, and checks below apply only to explicitly requested accessibility work; ordinary UI/input requirements remain in the requested task scope.

Select applicable categories and runtime contexts from the declared review scope and mode. Inspect adjacent behavior only where it can explain a finding or realistic regression. A targeted review does not establish whole-application approval. Select accessibility checks only when explicitly requested. Preserve in-scope safety, recovery, and availability checks.

## Severity

Apply severity only to in-scope findings. Excluded accessibility does not create a finding or limit a scoped verdict. Severity is based on user impact, not visual disagreement or rule count.

| Severity | Definition | Examples |
| --- | --- | --- |
| `Blocker` | Prevents a critical task, creates credible data/safety risk, excludes an essential assistive/input path, or makes the app unusable in a declared supported context | irreversible data loss without clear consent; core action unavailable to VoiceOver/keyboard; iPad window loses the only commit action; unsupported API causes runtime/build failure |
| `Major` | Materially harms a common task, recovery, navigation, adaptation, or platform expectation and should be fixed before release | fixed layout breaks common window sizes; macOS command is toolbar-only; permission denial traps the flow; repeated full-screen modality disrupts the main task |
| `Minor` | Noticeable but bounded friction, inconsistency, or accessibility weakness with a viable path remaining | ambiguous label; secondary action hard to discover; one noncritical state lacks clear feedback; target size needs adjustment |
| `Nit` | Low-impact craft or consistency improvement | wording, spacing relationship, symbol consistency, minor material restraint |
| `Investigation` | Plausible concern that current evidence cannot establish | screenshot suggests clipping; contrast or hit area unmeasured; animation quality unknown from code |

A high-confidence `Required` rule failure often becomes Blocker or Major, but never map rule level mechanically to severity.

## Confidence

| Confidence | Standard |
| --- | --- |
| `High` | Direct code/runtime evidence, exact location, clear user impact, applicable official source, exception ruled out |
| `Medium` | Strong evidence but one relevant runtime, platform, or product assumption remains |
| `Low` | Static or incomplete evidence; report only as Investigation unless risk is obvious and clearly qualified |

## Artifact limitations

| Artifact | Maximum ordinary conclusion |
| --- | --- |
| Screenshot only | Visual findings and `APPROVE WITH NOTES (visual-only)` at best |
| Recording only | Flow/motion findings and qualified approval for observed scenarios |
| Code/diff only | Structural/semantic findings and `APPROVE WITH NOTES (code-only)` unless critical runtime behavior is independently tested |
| Running build without source | Runtime behavior for tested contexts, not API/availability correctness |
| Code plus representative runtime testing of the requested scope | Eligible for `APPROVE` within that scope |

## Platform minimum audit

### iOS

- primary task hierarchy and reachable controls
- navigation stack/tab behavior and system back/dismiss paths
- compact-width presentation and popover adaptation
- orientation and safe-area behavior where supported
- Dynamic Type, VoiceOver, non-color cues, assistive gesture alternatives only when requested
- permission timing, failure, cancellation, and destructive recovery
- Ordinary material legibility if custom; Reduce Motion only when requested

### iPadOS

Everything in iOS plus:

- narrow, medium, and wide window resizing
- multitasking and software-keyboard obstruction
- column-collapse priority and selection preservation
- touch, pointer, hardware keyboard, and focus
- sidebars/split views/adaptable tabs
- toolbar overflow and contextual presentation
- minimized unnecessary full-screen modality

### macOS

Use the relevant [macOS runtime scenarios](macos-runtime-scenarios.md) for concrete multiwindow, restoration, and drag/drop checks.

- minimum/typical/large window behavior
- menu bar completeness and command validation
- standard shortcuts, ordinary focus order, escape/cancel; Full Keyboard Access only when requested
- toolbar as a subset, not the only command surface
- standard window chrome and multiple windows when supported
- Settings entry and undo/redo conventions
- tables/outlines, selection, context menus, drag/drop as relevant
- reduced modality, material/vibrancy, contrast, and critical-control placement

## Ten audit categories

### 1. Purpose and hierarchy

Ask:

- What is the primary outcome?
- Is it visually and behaviorally dominant without monopolizing the screen?
- Are secondary actions discoverable but subordinate?
- Does each screen answer where the person is, what is available, and how to leave?

### 2. Native semantics and controls

Hunt for:

- raw gesture recognizers on button-shaped elements
- custom controls without pressed/focus/selected/disabled/progress states
- destructive role misuse
- ambiguous symbols without a clear visible meaning; assess accessibility names only when requested
- standard functionality rebuilt with less-capable custom UI

### 3. Adaptation and layout

Hunt for:

- `UIScreen.main.bounds`, `NSScreen.main`, orientation branching, or fixed frames used as the primary layout model
- content/action loss at narrow sizes
- iPad phone-canvas behavior
- macOS windows that cannot resize usefully
- text clipping, aggressive shrinking, and localization breakage

### 4. Accessibility and assistive input (only when requested)

Hunt for:

- color-only state
- gesture-only core action
- custom control without accessible role/name/value/action
- incorrect grouping or hidden essential content
- keyboard/focus gaps on iPadOS/macOS
- movement with no Reduce Motion path

### 5. Safety and recovery

Hunt for:

- unclear destructive scope
- irreversible action without confirmation
- recoverable routine action with repetitive confirmation instead of undo
- cancellation that discards work without warning
- modal flow with no escape

### 6. State and feedback

Hunt for:

- ideal-state-only implementation
- indefinite spinner
- known progress shown as indeterminate
- errors that disappear silently
- status far from the affected object
- stale or offline data presented as current

### 7. Navigation, commands, and windowing

Hunt for:

- hidden or inconsistent selection
- iOS sidebar used without width/product rationale
- iPad columns that collapse against the agreed product-specific order or lose the active task/access to a pane
- macOS toolbar-only commands or nonstandard Settings access
- custom window chrome that removes expected behavior

### 8. Presentation and search

Hunt for:

- startup/informational alerts
- nested popovers
- tiny compact-width popovers
- full-screen modality for small choices
- search scope that is unclear
- active filters invisible from result context
- iPad autofocus that summons an obstructive software keyboard

### 9. Materials and motion

Hunt for:

- Liquid Glass in content cards/backgrounds by default
- many custom glass controls competing with content
- semantic text replaced by low-contrast appearance colors
- custom animation with no purpose, origin, or interruption behavior; Reduce Motion paths only when requested
- blur transitions under Reduce Motion, when that setting is in scope

### 10. Source and implementation integrity

Hunt for:

- invented API names
- availability mismatch
- web rules presented as native Apple requirements
- third-party preference presented as HIG
- screenshot-only inference presented as measured fact

## Exception discipline

Every finding must name the exception checked. Examples:

- fixed canvas versus fixed shell
- hidden expert acceleration versus hidden core path
- reading measure versus wasted iPad space
- utility panel versus broken custom window chrome
- irreversible deletion versus routine undoable deletion
- direct gesture manipulation versus decorative automatic motion
- semantic “More” menu versus duplicate width-overflow menu

If the exception applies, reject the finding or reduce its severity.

## Finding quality test

A finding is ready only if another engineer can answer all of these without asking the reviewer:

1. Where is it?
2. What exactly happens now?
3. Who is affected and how?
4. What exact behavior should replace it?
5. Which rule and source support the change?
6. Which exception was checked?
7. How do we verify it is fixed?

## Aggressive escalation triggers

Treat applicable in-scope items below as high-priority candidates. Verify an accessibility-only item only when that specific feature is requested:

- a core action is available only through gesture, hover, context menu, or pointer
- a custom button-like view lacks ordinary native control behavior; assess assistive actions only when that feature is requested
- when non-color accessibility is requested, essential state is conveyed only by color
- localization removes an essential action or meaning; assess Dynamic Type only when that feature is requested
- hard-coded device bounds break iPad window resizing or macOS windows
- an iPad app is functionally a fixed phone canvas and loses core content when resized
- a macOS command exists only in a toolbar with no menu or keyboard path where expected
- irreversible or broad destruction has no clear consequence or recovery
- a routine recoverable action is blocked by repeated confirmation alerts
- loading or failure silently discards input or leaves an indefinite spinner
- Liquid Glass is used throughout the content layer or obscures legibility
- when Reduce Motion is requested, custom spatial/blur motion ignores it
- a new API exceeds the deployment target without fallback
- a screenshot is being used to claim unmeasured accessibility, hit-target, contrast, or focus behavior

