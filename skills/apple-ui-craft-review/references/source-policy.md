# Source and claim policy

**Original supporting-reference snapshot:** 2026-08-04<br>
**Mapped rule/source check:** 2026-10-17; scope and changes are in [source-verification.md](source-verification.md).<br>
**Supported platforms:** iOS, iPadOS, macOS only.

This package is intentionally stricter about evidence than about visual taste. A recommendation is only as strong as its source and the artifact that was inspected.

## Authority order

Use sources in this order:

1. The live Apple Human Interface Guidelines page for the exact topic and platform.
2. Current Apple framework documentation and current Apple sample code for API behavior.
3. The bundled source summaries in this skill, which are an offline snapshot rather than an evergreen authority.
4. Established platform convention inferred from multiple Apple patterns.
5. Product-specific reasoning or usability heuristics.

When live guidance conflicts with a bundled summary, the live Apple source wins. When an API is unavailable for the repository's deployment target, preserve the intent with a supported native alternative rather than forcing the newer API.

## Claim classes

Every substantive design decision or review finding must use one of these classes.

| Class | Meaning | Permitted wording |
| --- | --- | --- |
| `APPLE-HIG` | Directly supported by a current Apple HIG topic | “Apple recommends…”, “The HIG calls for…” |
| `APPLE-API` | Supported by current Apple framework documentation or API behavior | “The framework provides…”, “This API preserves…” |
| `PLATFORM-CONVENTION` | A synthesized native-platform expectation without one controlling HIG sentence | “For platform consistency, prefer…” |
| `PRODUCT-HEURISTIC` | A product or usability recommendation that is not Apple policy | “For this product, prefer…” |
| `EVIDENCE-GAP` | The available artifact cannot prove or disprove the behavior | “Verify at runtime…” |

Never present a `PLATFORM-CONVENTION` or `PRODUCT-HEURISTIC` as an HIG violation. Never use “noncompliant” for a preference, an unmeasured concern, or a screenshot-only inference.

## Numeric guidance

- Use a number only when the exact live source has been checked or the number is marked as coming from this dated snapshot.
- Preserve Apple’s qualifiers such as “default,” “minimum,” “strive to,” and “in general.”
- Do not import CSS animation durations, easing curves, web hit targets, or third-party design-system numbers into native Apple guidance.
- Native controls may provide a larger interaction region than their visible glyph. Measure behavior before reporting a target-size defect.

## Evidence levels

| Evidence | Can establish | Cannot establish alone |
| --- | --- | --- |
| Screenshot | hierarchy, labels, visible density, visible state, obvious clipping | focus order, hit area, VoiceOver output, keyboard access, animation, recovery behavior |
| Recording | visible flow, timing, transitions, some recovery behavior | source semantics, all accessibility behavior, all window sizes |
| Code or diff | API choices, semantics declarations, state paths, availability handling | actual contrast, final layout under every runtime context, perceived motion quality |
| Running build | behavior in exercised contexts | untested states, untested assistive settings, untested devices |
| Code plus representative runtime testing | strongest basis for approval | future OS behavior and contexts not covered by the validation matrix |

A static artifact can receive a visual verdict, but not a full accessibility or release approval.

## Citation format inside outputs

For each important decision or finding, include:

- rule ID from `native-rule-catalog.md`
- claim class
- exact Apple topic title
- exact section URL and the relevant passage (not merely an accessible page)
- access date when live browsing is available
- any material exception or evidence limitation

Example:

```text
Basis: IPAD-01 · APPLE-HIG · Designing for iPadOS
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados/
Verified: 2026-08-04
Exception: A deliberately fixed-canvas media tool may retain a fixed work surface, but its surrounding controls still need to adapt.
```

## Freshness workflow

When web access is available:

1. Follow the exact section links and paragraph locators in `native-rule-catalog.md`, not only the HIG landing page. If a section moved, locate the current passage within the official topic before citing it.
2. Check the platform-specific section and change log when present.
3. Open related component guidance if the finding concerns a button, alert, menu, toolbar, sidebar, search field, window, or material.
4. Record only the sources actually used.
5. If the current source cannot be verified, label the claim with the verification date recorded for that mapped rule (currently 2026-10-17), or the original 2026-08-04 snapshot for other bundled guidance. Do not describe an unavailable source as verified-current.
6. If the HTML page only presents a JavaScript shell, follow its official Markdown link or use Apple's official DocC data for the same topic. A page title, HTTP success, or valid section anchor alone is not substantive verification.
7. Keep automated reachability checks separate from human/agent review of meaning. Only advance a semantic verification date after re-reading the relevant passage. If the source is weaker or narrower than the rule, narrow the rule or classify the extra inference as a convention/product heuristic.

## Rule-to-finding fit

Use a catalog rule ID only when that rule directly supports the reported behavior. If no catalog rule fits, write `no matching catalog rule` and cite the exact API documentation or product contract; do not attach a nearby window/layout rule merely to fill an ID field. A test-scenario ID names a verification procedure, not an Apple requirement.
