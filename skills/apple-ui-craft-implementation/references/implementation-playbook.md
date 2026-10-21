# Implementation playbook

Apply checks only to platform behaviors changed by the implementation or exposed to a realistic regression risk. This is a selection checklist, not an instruction to retest unrelated application features.

## Framework mapping

Prefer existing repository framework and patterns. Do not migrate solely for stylistic preference.

| Capability | SwiftUI | UIKit | AppKit |
| --- | --- | --- | --- |
| Stack navigation | `NavigationStack` | `UINavigationController` | Window/view-controller hierarchy appropriate to product |
| Multi-column | `NavigationSplitView` | `UISplitViewController` | `NSSplitViewController` |
| Peer destinations | `TabView` / adaptable tab structure | `UITabBarController` | Sidebar, toolbar, segmented navigation, or app-specific structure |
| Commands | `Commands`, `keyboardShortcut` | `UIKeyCommand`, menus, responder chain | `NSMenu`, `NSMenuItem`, responder chain |
| App Settings | `Settings` scene where applicable | Product settings flow | App menu Settings / `Settings` scene or `NSWindowController` |
| Progress | `ProgressView` | `UIProgressView`, `UIActivityIndicatorView` | `NSProgressIndicator` |
| Semantic action | `Button`, roles, `Toggle`, `Picker` | `UIButton`, `UIAction`, standard controls | `NSButton`, `NSControl`, menu actions |
| Accessibility | SwiftUI accessibility modifiers and native semantics | `UIAccessibility` plus native controls | `NSAccessibility` plus native controls |
| Focus | Focus APIs and native container behavior | Focus environment, key commands, first responder | First responder, key view loop, menu validation |
| Windows/scenes | `WindowGroup`, document/window scenes as supported | `UIScene`, `UIWindowScene` | `NSWindow`, `NSWindowController`, document architecture |

Verify exact API availability; this table is a direction map, not a substitute for documentation.

## Native-first replacement hierarchy

When fixing a custom mechanism, prefer:

1. existing repository-native component
2. system component with semantic style/role
3. small wrapper preserving native behavior
4. custom control with complete semantic/input/state contract

Do not start at step 4 to match a mockup.

## Layout implementation

### Prefer

- container-driven constraints and layout
- semantic safe-area behavior
- adaptive stacks/columns/split views
- layout priority and content compression/hugging appropriate to framework
- explicit minimum usable window size only when task constraints require it
- scroll for genuinely overflowing content, not as a substitute for hierarchy

### Investigate before retaining

- `UIScreen.main.bounds`
- `NSScreen.main` as layout width
- `UIDevice.current.orientation`
- many fixed frames
- `minimumScaleFactor` as default localization strategy
- unconditional `ignoresSafeArea`
- manual width-based toolbar overflow

These can be legitimate in narrow contexts; they are not automatic defects.

## State and recovery implementation

For every long or fallible operation, define:

- source of truth and cancellation ownership
- in-flight state and duplicate-action prevention
- partial result policy
- error representation
- retry semantics
- user-input preservation
- background/interruption behavior
- success feedback
- undo/rollback where possible

Avoid a single Boolean such as `isLoading` when the operation has distinct idle, running, success, failed, cancelled, or partial states that affect behavior.

## Accessibility implementation

### Native semantics first

- Use native controls before manually adding traits.
- Add labels when the visible symbol/text is ambiguous, not redundantly.
- Expose dynamic value and selected/expanded/disabled state.
- Group only when the combined announcement and actions remain understandable.
- Avoid `accessibilityHidden(true)` on essential content as a layout workaround.

### Dynamic content

- Announce meaningful asynchronous completion/error when the visible change may not be discovered automatically.
- Preserve focus when content updates; move focus only when the task requires it and the change is predictable.
- Make custom actions available when visual gestures have no direct assistive equivalent.

### Keyboard and focus

- iPadOS/macOS core commands need focusable controls or command/menu paths.
- Do not override standard shortcuts.
- Keep enabled state consistent across toolbar, menu, context menu, and shortcut.
- Verify Escape/Cancel and default-button behavior where applicable.

## Material implementation

- Let standard navigation and controls adopt current system material behavior.
- Use official APIs and semantic styles rather than layered opacity/blur replicas.
- Keep content layer distinct from the functional control/navigation layer.
- Test on varied content backgrounds and with Reduce Transparency/Increase Contrast.
- Do not globally add glass to “modernize” an app.

## Motion implementation

- Name the purpose: continuity, direct manipulation, state, feedback, or explanation.
- Start from current presentation state when interruption is possible.
- Track direct gestures continuously and preserve cancellation/reversal.
- Add a Reduce Motion branch for spatial/depth/blur motion.
- Reuse repository motion tokens; if none exist, keep local values explicit and label them implementation choices, not HIG values.
- Test on device or a representative simulator when feel matters.

## Platform implementation checks

### iOS

- preserve native back/dismiss behavior
- keep modal commit/cancel clear
- verify compact presentation and system gesture conflicts
- request permission in context
- do not hide core action behind swipe/long press only

### iPadOS

- verify narrow/medium/wide window behavior
- specify column collapse and selection persistence
- support pointer/keyboard/focus for productivity commands
- avoid duplicate toolbar overflow
- verify software-keyboard obstruction and search focus

### macOS

- add/update menu commands with toolbar actions
- use standard Settings entry and shortcuts
- preserve window resizing and state restoration
- validate first responder, key view loop, Escape/Return behavior
- keep context menu and toolbar command enabled state aligned with menus
- use undo/redo where editing semantics support it

## Minimal-change test

Before expanding scope, ask:

- Can the issue be fixed by replacing one custom control with a native control?
- Can one shared state model resolve multiple symptoms?
- Can layout become container-relative without rewriting navigation?
- Can a menu/command addition preserve the toolbar?
- Can an inline status replace a blocking alert?
- Can one Reduce Motion branch cover the custom transition?

Prefer the smallest change that fully fixes behavior, not the smallest diff that leaves the root cause.
