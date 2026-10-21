# Verification matrix

Select checks that establish the requested behavior and cover realistic regressions. The lists below are candidates, not a requirement to exercise every context. Report required but unavailable checks as `NOT RUN`. Stop once selected acceptance criteria are satisfied; broaden only for new failures or material uncertainty.

## Mechanical check selection

- Use the narrowest existing affected tests first.
- Build an affected target/platform when compilation, configuration, resources, or integration could change and the selected checks do not already cover it. Do not duplicate the same build.
- Use configured formatter/linter checks within the authorized scope.
- Inspect relevant availability, concurrency, localization, or accessibility warnings.
- Inspect the final diff and run `git diff --check` when applicable.

Discover schemes and destinations before constructing `xcodebuild` commands. Do not assume simulator names.

## iOS runtime checks

| Area | Contexts |
| --- | --- |
| Layout | smallest supported width, representative large phone, supported orientations |
| Navigation | back gesture, toolbar/back button, modal cancel/commit, deep link/restoration if affected |
| Text | default and representative accessibility size, long localization string |
| States | loading/partial, empty, error/retry, denied permission, cancellation, success |
| Accessibility | VoiceOver names/order/actions, non-color state, Reduce Motion when custom motion changes |
| Interruption | background/foreground, repeated action, network interruption where relevant |

## iPadOS runtime checks

| Area | Contexts |
| --- | --- |
| Windows | narrow, medium, wide/full-screen; free resizing where supported |
| Columns | collapse order, selection persistence, inspector/sidebar visibility |
| Inputs | touch, pointer, hardware keyboard, Full Keyboard Access for changed commands |
| Software keyboard | search focus, fields, content obstruction, dismissal |
| Toolbars/menus | system overflow, command availability, enabled state |
| Presentation | popover anchoring at width and compact adaptation |
| Accessibility | VoiceOver, text growth, Reduce Motion, contrast/transparency settings as affected |

## macOS runtime checks

For affected multiwindow, restoration, or drag/drop behavior, use [macos-runtime-scenarios.md](macos-runtime-scenarios.md). Record exact steps and observed source/destination state; do not mark these cases PASS from code inspection alone.

| Area | Contexts |
| --- | --- |
| Windows | minimum, typical, large, full screen; reopen/restoration if affected |
| Commands | menu bar completeness, enabled state, shortcut, toolbar/context-menu parity |
| Focus | keyboard-only navigation, first responder, Tab/Shift-Tab, Escape/Return |
| Settings/undo | Command-comma, Undo/Redo menu and shortcuts when affected |
| Data views | selection, sorting/resizing, contextual actions, drag/drop as affected |
| Accessibility | VoiceOver, Increase Contrast, Reduce Transparency, Reduce Motion |
| Multiple windows | independent state and command targeting when supported |

## Evidence language

Use:

- `PASS — <exact context and result>`
- `FAIL — <exact context, expected, actual>`
- `NOT RUN — <reason>`
- `NOT APPLICABLE — <reason>`

Do not write “tested responsive behavior” without listing sizes/contexts.

## Feel checks for custom motion/material

Mechanical correctness is insufficient. Verify:

- the motion begins at the causal source or uses a justified nonspatial transition
- rapid reversal does not jump or lock input
- gesture-driven elements stay with the gesture
- Reduce Motion removes spatial/depth/blur movement while retaining comprehensible feedback
- glass/material remains legible over sparse, bright, dark, and visually rich content
- Increase Contrast and Reduce Transparency produce a coherent hierarchy

When feel cannot be judged in the available environment, report a remaining device/manual check rather than guessing.
