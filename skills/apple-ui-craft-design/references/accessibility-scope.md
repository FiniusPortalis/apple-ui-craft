# Accessibility scope

Accessibility-specific design, implementation, auditing, and testing are **excluded by default**. Include only the features the user explicitly requests, including an applicable accessibility requirement the user has established for the project. A general request to follow the HIG, improve UI, review deeply, or prepare for release does not enable this work. Do not repeatedly ask whether to enable it.

## When excluded

- Do not add custom accessibility labels, hints, values, grouping, announcements, assistive focus, rotors, or actions solely for accessibility.
- Do not introduce VoiceOver, Voice Control, Switch Control, Full Keyboard Access, accessibility text-size, Reduce Motion, Increase Contrast, or Reduce Transparency implementation or dedicated checks.
- Skip accessibility-only catalog rules, scanner candidates, gates, template rows, and source research. Do not turn them into failures, readiness blockers, evidence gaps, follow-up tasks, or repeated `NOT RUN` notices.
- Preserve existing accessibility code, native control behavior, semantic system styles, and test hooks. Do not remove or disable them to satisfy this scope. Existing tests remain intact; a relevant ordinary test suite may include existing accessibility assertions.
- Ordinary UI requirements still apply within the task: readable text, clear visible state, usable controls, localization, resizing, standard keyboard/menu commands, and ordinary focus. Do not use these as a pretext to add a dedicated assistive-technology audit.
- `accessibilityIdentifier` is a testing hook; it may be used when an authorized UI test needs it. It is not a request for spoken labels or an accessibility audit.

## When requested

Work only on the named features and affected surfaces. A VoiceOver request does not automatically include Dynamic Type, reduced motion, or every other accessibility feature. Use relevant catalog rules and Apple sources, prefer the built-in behavior of native controls, and add customization only for a demonstrated or explicitly specified need. Record actual checks; required but unavailable checks are `NOT RUN` and may limit a verdict within the requested scope.

## Reporting and verdicts

Judge readiness and review results against the selected scope. For a formal specification, audit, or handoff, identify that scope once (for example, `accessibility excluded` or `VoiceOver for the result list`). An excluded dimension is not a failed or unperformed required check. Any approval is limited to the reviewed scope and evidence; do not call it full HIG, accessibility, or whole-release approval. Ordinary short replies need no accessibility disclaimer.

## Source distinction

This is a task-scoping policy, not an Apple recommendation to omit accessibility. Apple's [HIG accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility) recommends supporting accessibility. The [SwiftUI](https://developer.apple.com/documentation/swiftui/accessibility-fundamentals), [UIKit](https://developer.apple.com/documentation/uikit/accessibility-for-uikit), and [AppKit](https://developer.apple.com/documentation/appkit/accessibility-for-appkit) documentation describes built-in support and further customization. [`accessibilityIdentifier(_:)`](https://developer.apple.com/documentation/swiftui/view/accessibilityidentifier%28_%3A%29) is documented for testing. These passages were checked on 2026-10-27; this does not advance other rule-source verification dates.
