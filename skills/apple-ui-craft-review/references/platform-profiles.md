# Platform profiles

Apply [accessibility-scope.md](accessibility-scope.md) before selecting criteria. Accessibility-only requirements, examples, settings, and checks below apply only to explicitly requested accessibility work; ordinary UI/input requirements remain in the requested task scope.

Use this file with `native-rule-catalog.md`. It describes default platform posture, not an excuse to make the three platforms artificially different.

## iOS

### Default posture

- Optimize the first view for the primary task and content.
- Keep persistent controls limited; move secondary actions to discoverable menus or contextual locations without hiding critical actions completely.
- Use touch-first navigation and preserve familiar system gestures, including back navigation and edge gestures.
- Prefer `NavigationStack`, tab-based structure, lists, sheets, and full-screen presentation only when the task warrants it.
- A sidebar is usually not the default iPhone structure. Use one only when the product and available width justify it.
- Request permissions at the point of need with a clear reason.

### Required validation contexts

- smallest supported iPhone width
- a large iPhone
- portrait and landscape where the product supports both
- default text and long/localized content; accessibility text sizes only when requested
- light and dark appearances
- VoiceOver, Reduce Motion, Increase Contrast, Reduce Transparency only when explicitly requested
- interrupted flows: backgrounding, cancellation, denied permission, failed network operation

### Common structural failures

- desktop-like persistent panes squeezed into compact width
- custom back controls that break interactive dismissal
- critical actions available only through swipe or long press
- fixed-height text regions that clip ordinary/localized text; Dynamic Type checks only when requested
- repeated full-screen transitions for small related tasks

## iPadOS

### Default posture

- Treat iPad as a resizable, multitasking environment, not a scaled iPhone canvas.
- Use the large display to keep content and relevant controls visible while minimizing unnecessary full-screen transitions and blocking modality.
- Support touch, pointer, hardware keyboard, and—when the product genuinely benefits—Apple Pencil.
- Prefer `NavigationSplitView`, adaptable tab/sidebar structures, split views, columns, toolbars, menus, and popovers when width permits.
- Prioritize toolbar actions and add a More menu only when needed. Verify the framework's actual overflow behavior; do not assume automatic overflow or duplicate an existing mechanism.
- Preserve the active task and logical access to each pane as space narrows. Choose and document a product-specific collapse order; Apple does not mandate a universal tertiary-first order (IPAD-05).

### Required validation contexts

- compact/narrow app window
- medium-width split or tiled window
- wide/full-screen window
- portrait and landscape
- touch-only and hardware keyboard/pointer
- virtual keyboard visible and hidden
- Stage Manager or equivalent free resizing when supported by the OS
- default text; accessibility text sizes only when requested

### Common structural failures

- centered fixed-width phone screen with unused margins
- sidebar that cannot collapse or consumes the core content at narrow widths
- controls that work with touch but have no hover, focus, keyboard, or pointer affordance where expected
- auto-focused search that unexpectedly summons the software keyboard and covers content
- full-screen modal flow for a small contextual choice

## macOS

### Default posture

- Treat the app as a windowed, keyboard-and-pointer environment with potentially high information density.
- Make windows movable and resizable and preserve useful behavior at minimum, typical, and large sizes.
- Expose app commands through the menu bar. A toolbar is a convenient subset, not the only command surface.
- Use standard menu names, command placement, keyboard shortcuts, Settings entry, undo/redo, window chrome, and focus behavior.
- Prefer modeless or inline workflows when a blocking modal is unnecessary.
- Use tables, outlines, inspectors, sidebars, split views, and multiple windows when they match the information architecture.

### Required validation contexts

- minimum supported window size
- typical working size
- large/full-screen window
- ordinary keyboard navigation; Full Keyboard Access only when that feature is requested
- pointer, contextual menus, and drag-and-drop where relevant
- menu bar command availability and standard shortcuts
- light/dark; increased contrast, reduced transparency, reduced motion only when requested
- multiple windows/scenes when supported

### Common structural failures

- toolbar-only commands with no menu equivalent
- a gear button in the main toolbar as the only way to open app Settings
- custom borderless chrome that loses standard window behavior
- touch-sized sparse layout that wastes desktop space without a product reason
- critical controls placed only at the bottom edge of a tall or resizable window
- blocking alerts for routine, undoable actions

## Cross-platform consistency

Keep these stable when the product is shared across platforms:

- terminology and object names
- data model and state meaning
- command semantics
- destructive-action consequences
- search scope and filter meaning
- accessibility labels and result announcements only when requested
- user-visible persistence and synchronization rules

Adapt these intentionally rather than forcing parity:

- navigation container
- control placement
- density
- modality
- menu and keyboard command exposure
- window and multi-column behavior
- pointer and hover affordances
