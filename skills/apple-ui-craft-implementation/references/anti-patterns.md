# Native anti-pattern catalog

Apply [accessibility-scope.md](accessibility-scope.md) before selecting criteria. Accessibility-only requirements, examples, settings, and checks below apply only to explicitly requested accessibility work; ordinary UI/input requirements remain in the requested task scope.

Use these examples as diagnostic patterns, not blind search-and-replace recipes. Confirm repository context, deployment targets, and the documented exceptions before reporting or changing code.

## Summary table

| Pattern | Before | After | Why | Exception or check |
| --- | --- | --- | --- | --- |
| Raw tap gesture as a control | `Image(...).onTapGesture { save() }` | `Button(action: save) { Image(...) }` | Native control semantics, pressed state, keyboard activation, accessibility, and roles | A tap gesture used for direct manipulation of content can remain if it is not masquerading as a button and an alternative exists where needed |
| Screen-bound layout | `frame(width: UIScreen.main.bounds.width)` | derive from container; use flexible stacks, layout priorities, `ViewThatFits`, or constraints | iPad windows and macOS windows resize; device bounds are not the current container | A fixed media/document canvas may remain fixed inside an adaptive shell |
| Fixed text as the default | `.font(.system(size: 13)).lineLimit(1)` | semantic text style, wrapping, priority, or expandable detail | Supports Dynamic Type, localization, and legibility | Compact status tokens can abbreviate visually with a full accessible label |
| Color-only state | `.foregroundStyle(isError ? .red : .green)` | add label/symbol/state semantics and keep color as reinforcement | Color cannot be the only differentiator | Decorative gradients need no semantic duplication |
| Gesture-only core action | swipe/long-press is the only delete or dismiss path | add visible button, menu command, row action, or keyboard command | Mobility and discoverability | Expert acceleration may remain hidden when the full action is elsewhere |
| Context-menu-only command | `.contextMenu { Button("Rename")... }` with no other path | expose Rename in row/detail toolbar or menu as appropriate | Context menus supplement the main interface | An equivalent action can be contextual; it need not be a permanent button |
| Routine confirmation alert | ask “Are you sure?” before every recoverable item deletion | delete with undo; alert only for uncommon irreversible loss | Preserves flow and recoverability without habituating dismissal | Regulated or high-risk workflows can require confirmation |
| Informational startup alert | alert describing a feature at launch | inline onboarding, empty-state guidance, or contextual disclosure | Alerts should be actionable interruptions | Legal/safety acknowledgement may require explicit acceptance |
| Destructive action as primary | `.buttonStyle(.borderedProminent)` on Delete | normal/cancel primary; destructive role and placement at the end | Avoid visually encouraging destructive choices | A dedicated irreversible confirmation screen can make the final destructive commit prominent after clear review |
| Unknown progress represented as a fake percentage | incrementing timer to 100% | indeterminate progress until real progress is known | False precision erodes trust | A reliable server estimate can drive determinate progress |
| Known progress shown only as spinner | `ProgressView()` for a large local import with known item count | determinate progress, context label, cancel/pause when safe | Better expectation and agency | Very short operations may not need a percentage |
| Custom glass across content | every card/background uses `.glassEffect()` or custom blur | reserve glass for functional navigation/controls; standard content material/background | Preserves hierarchy and legibility | A transient active control in content can adopt glass |
| Appearance-selected material | choose blur because it looks “blue enough” | select semantic material; use semantic colors/vibrancy | Material appearance changes with settings and background | Static artwork is content, not material |
| Unconditional spatial animation (when Reduce Motion is requested) | always slide/zoom/blur on state change | branch for Reduce Motion; use fade/highlight/nonspatial alternative | Reduces vestibular load and respects system settings | Gesture-tracked motion can remain when direct and controlled |
| iPad as enlarged phone | fixed narrow `VStack` centered in wide window | responsive columns, split view, adaptable tab/sidebar, or intentional reading width with useful surrounding UI | Uses space and survives resizing | Reading content can retain a comfortable measure; navigation and tools should still use the window well |
| Duplicate toolbar overflow | a custom More menu duplicates actions already exposed by framework overflow | verify actual framework behavior; prioritize items and provide additional actions only where needed | HIG supports a More menu when needed; automatic overflow depends on the API and OS | A single purposeful More menu is valid, including for limited width |
| iPad search steals focus | dedicated search field auto-focuses on appearance | keep focus neutral when software keyboard would cover content; focus when typing is clearly next or hardware keyboard is present | Prevents unexpected obstruction | Search-only launch experiences can autofocus intentionally |
| macOS toolbar-only commands | Save/Export/Delete exist only as toolbar buttons | add menu commands and standard shortcuts; keep toolbar for frequent access | The menu bar is the complete command surface | Local transient controls need not all appear in menus |
| macOS Settings via toolbar gear only | toolbar gear opens preferences | provide app-menu Settings and Command-comma; toolbar entry optional | Matches platform convention and keyboard access | A per-document inspector is not app Settings |
| Borderless custom window by default | replace title bar and traffic-light behavior to match mockup | retain standard window chrome and customize only supported areas | Preserves resizing, movement, focus, accessibility, and expectations | Utility panels/HUDs can use special styles with explicit behavior testing |
| Compact popover | force a popover in narrow iPhone width | use adaptive sheet/full-screen presentation | Popovers need source context and sufficient space | System adaptation may already handle this; do not wrap it twice |
| Hidden failure | operation fails and spinner simply disappears | inline error, retry/recovery, retained user input; assistive announcement only when requested | Feedback must explain state and recovery | Silent background refresh may fail quietly if stale content remains clearly usable and no user action was promised |

## SwiftUI examples

### 1. Semantic control instead of a raw tap target

Before:

```swift
Image(systemName: "trash")
    .foregroundStyle(.red)
    .onTapGesture {
        deleteSelectedItem()
    }
```

After:

```swift
Button(role: .destructive, action: deleteSelectedItem) {
    Label("Delete", systemImage: "trash")
}
```

Check before changing:

- Is the object actually a button, or is it direct manipulation of content?
- Does the surrounding toolbar or menu already provide the semantic action?
- Would adding a visible label overcrowd the platform surface? An icon-only button can be correct with a clear accessibility label and adequate interaction region.

### 2. Container-relative adaptation

Before:

```swift
VStack {
    SidebarView()
    ContentView()
}
.frame(width: UIScreen.main.bounds.width)
```

After:

```swift
NavigationSplitView {
    SidebarView()
} detail: {
    ContentView()
}
```

For a custom adaptive composition:

```swift
ViewThatFits(in: .horizontal) {
    HStack(spacing: 0) {
        SidebarView()
        ContentView()
    }

    ContentView()
}
```

Do not introduce `NavigationSplitView` blindly. Verify navigation ownership, state restoration, minimum OS, selection model, and compact-column behavior.

### 3. Dynamic text and reflow

Before:

```swift
Text(title)
    .font(.system(size: 13, weight: .semibold))
    .lineLimit(1)
    .minimumScaleFactor(0.6)
```

After:

```swift
Text(title)
    .font(.headline)
    .lineLimit(2)
    .fixedSize(horizontal: false, vertical: true)
```

The exact target depends on the component. A one-line toolbar label may be correct; the problem is using shrinking and clipping as the default response to content growth.

### 4. Non-color status

Before:

```swift
Circle()
    .fill(isConnected ? Color.green : Color.red)
```

After:

```swift
Label(
    isConnected ? "Connected" : "Disconnected",
    systemImage: isConnected ? "checkmark.circle.fill" : "exclamationmark.triangle.fill"
)
```

### 5. Reduce Motion branch (only when requested)

Before:

```swift
withAnimation(.spring(response: 0.5, dampingFraction: 0.65)) {
    isPresented.toggle()
}
```

After:

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

private var transition: AnyTransition {
    reduceMotion ? .opacity : .move(edge: .trailing).combined(with: .opacity)
}

withAnimation(reduceMotion ? .easeOut(duration: 0.15) : .spring) {
    isPresented.toggle()
}
```

The `0.15` seconds value above is an implementation example, not an Apple HIG number. Match the repository's motion tokens and validate the feel; the HIG-backed requirement is the reduced spatial-motion alternative.

### 6. Recoverable deletion

Before:

```swift
.alert("Delete item?", isPresented: $showDeleteAlert) {
    Button("Delete", role: .destructive) { delete(item) }
    Button("Cancel", role: .cancel) {}
}
```

Potential after for a routine recoverable deletion:

```swift
Button(role: .destructive) {
    pendingDeletion = item
    delete(item)
    showUndo = true
} label: {
    Label("Delete", systemImage: "trash")
}
```

Do not remove confirmation when deletion is irreversible, uncommon, security-sensitive, or affects more data than the interface makes obvious.

### 7. Progress that reflects real work

Before:

```swift
ProgressView()
Text("Importing…")
```

After when item counts are reliable:

```swift
ProgressView(value: Double(completed), total: Double(total)) {
    Text("Importing \(completed) of \(total)")
}
```

Keep the rest of the interface usable and add Cancel only when cancellation is real and safe.

## UIKit examples

### 8. Use a control instead of a tap recognizer for a button-shaped action

Before:

```swift
let imageView = UIImageView(image: UIImage(systemName: "square.and.arrow.up"))
imageView.isUserInteractionEnabled = true
imageView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(share)))
```

After:

```swift
let button = UIButton(type: .system)
button.setImage(UIImage(systemName: "square.and.arrow.up"), for: .normal)
button.addTarget(self, action: #selector(share), for: .primaryActionTriggered)
```

### 9. Container constraints instead of screen bounds

Before:

```swift
contentView.widthAnchor.constraint(equalToConstant: UIScreen.main.bounds.width).isActive = true
```

After:

```swift
NSLayoutConstraint.activate([
    contentView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor),
    contentView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor)
])
```

A custom readable width can use a maximum-width constraint while still allowing the surrounding container to resize.

## AppKit examples

### 10. Complete command surface

Before:

```swift
NSToolbarItem(itemIdentifier: .export)
```

with no menu command or shortcut.

After:

- keep the toolbar item for frequent access
- add an Export command to the appropriate menu
- assign a nonconflicting shortcut only when the command is frequent
- ensure enabled/disabled state is consistent across menu and toolbar

In SwiftUI macOS apps, this often means a `Commands` declaration plus toolbar placement. In AppKit, use `NSMenuItem`, the responder chain, and matching validation.

### 11. App Settings versus document inspector

Before: a toolbar gear is the only path to global preferences.

After:

- expose app Settings from the application menu
- support the standard Settings shortcut
- use a toolbar inspector button only for settings scoped to the current document, selection, or task

## Review discipline

For every match:

1. Cite the actual file and line or visible region.
2. Show the current behavior or code in `Before`.
3. Give an exact target in `After`.
4. Explain user impact in `Why`.
5. Name the rule ID and claim class.
6. State the exception checked.
7. Give a reproducible verification step.

A scanner match is not a finding until context confirms it.
