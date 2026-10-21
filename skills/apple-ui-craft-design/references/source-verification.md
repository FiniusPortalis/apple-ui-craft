# Rule-source verification

**Checked:** 2026-10-17 (Asia/Tokyo)<br>
**Scope:** all 68 IDs in `native-rule-catalog.md`, against 31 Apple HIG topics.

The check read Apple's official DocC article bodies and matched every linked section to its actual `heading.anchor`. Each catalog row includes a short paraphrased passage locator. Apple article copies, images, and downloaded JSON are not redistributed in this package. The date records source review, not approval of any app or automatic future freshness.

## Interpretation

- A mapped section supports the stated recommendation; it does not turn this skill's review severity or contextual exception into Apple policy.
- `NATIVE-03`, `ADAPT-05`, and `MOTION-03` are platform syntheses. `A11Y-08`, `STATE-01`, and `IPAD-05` are product/verification heuristics. Their links are explicitly background, not direct Apple requirements.
- APIs, availability, and runtime behavior must still be checked for the target project. This pass did not revalidate every code example or other reference in the three skills.
- The repository validator can check links/anchors again. It cannot certify semantic agreement and must not advance this date automatically.

## Corrections made during source mapping

| Rules | Correction and reason |
| --- | --- |
| LABEL-02 | Separate menu-item ellipsis guidance from macOS push-button guidance; do not apply a single rule to every control. |
| ADAPT-03, IPAD-05 | Keep access to panes across window sizes; classify the product's collapse order as a heuristic rather than a universal Apple order. |
| A11Y-01, A11Y-08, STATE-01 | Distinguish HIG descriptions/navigation from framework-specific semantics and the skill's chosen verification/state matrix. |
| SEARCH-04 | Express both parts of the official advice: consider focus in a dedicated search area, except on iPad with only a virtual keyboard. The prior wording already contained a hardware-keyboard exception; this is a clarification, not evidence that Apple reversed its guidance. |
| MENU-01, MENU-02 | Preserve access to context-menu actions in the main UI. Remove a universal destructive-last ordering assertion not established by the linked general-menu guidance. |
| TOOLBAR-01, IPAD-06 | Current HIG recommends a More menu when needed. Do not infer universal automatic overflow; verify framework and OS behavior. Related profile/playbook/anti-pattern wording was aligned. |
| MOTION-02 | Preserve Apple's qualified recommendation for gesture-following, cancelable motion; use Expected rather than an unconditional requirement. |
| IOS-02, IOS-04, IPAD-01 | Ground compact navigation, button emphasis, and window adaptation in the actual sections; remove unsupported blanket wording. |

## Reviewed topics

- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)
- [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
- [Context menus](https://developer.apple.com/design/human-interface-guidelines/context-menus)
- [Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles)
- [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios)
- [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados)
- [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos)
- [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)
- [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)
- [Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)
- [Loading](https://developer.apple.com/design/human-interface-guidelines/loading)
- [Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
- [Menus](https://developer.apple.com/design/human-interface-guidelines/menus)
- [Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- [Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers)
- [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy)
- [Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators)
- [Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields)
- [Settings](https://developer.apple.com/design/human-interface-guidelines/settings)
- [Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)
- [Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars)
- [Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)
- [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)
- [The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)
- [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)
- [Typography](https://developer.apple.com/design/human-interface-guidelines/typography)
- [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)
- [VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover)
- [Windows](https://developer.apple.com/design/human-interface-guidelines/windows)
