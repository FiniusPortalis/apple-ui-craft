# macOS runtime scenarios

Use only cases affected by the requested change or review scope. These are test procedures, not new Apple requirements or a mandate to add multiwindow, persistence, or drag/drop to every app. Establish supported behavior from product requirements first. This reference is shared by design, review, and implementation.

## Setup and evidence

Use disposable documents and a test profile. Record app revision, macOS version, device, window sizes, input method, restoration preference, and the initial dataset. Foreground the intended app, confirm the control is operable, and read back entered values before judging a result. Keep review build outputs and evidence outside the source workspace. Do not change the user's global system preferences or use live documents merely to run a case.

For every selected case record `PASS`, `FAIL`, `NOT RUN` (reason), or `N/A` (product reason), steps, expected behavior, actual result, and evidence location. Static inspection can identify a candidate; it does not mark a runtime case PASS. Record restore, quit/relaunch, and crash recovery separately; ordinary relaunch does not establish crash recovery.

## MW-1: Independent windows and command targeting

Precondition: the product supports multiple windows; specify what data is shared and what selection, filter, navigation, and unsaved edits are per-window.

1. Open windows A and B with distinct items. Give them different selections/filters and different widths.
2. Activate A, invoke an affected menu command and its keyboard shortcut, then repeat in B. Where applicable, also try no selection and an auxiliary panel as key window.
3. Edit in A, switch to B, close A, and continue in B. For Undo/Redo, check which document/operation owns the undo history.

Pass: each command's target and enabled state follow the intended active context; local selection/navigation does not leak; intentionally shared document changes propagate coherently; closing one window does not discard another's work. Native menu/toolbar equivalents reach the same operation. Record any deliberately synchronized selection as a product exception.

## RS-1: Reopen and state restoration

Precondition: record the product's restoration contract and existing macOS reopen preference. Distinguish closing a window, opening it again, and quitting/relaunching the app.

1. In disposable data, set distinct selections, navigation locations, sidebar/inspector visibility, and window sizes/positions in A and B. Save or leave an edit unsaved according to the contract.
2. Close and reopen one window. Separately quit normally and relaunch under the recorded reopen setting.
3. If the product restores item references, repeat with a test item removed or made unavailable between runs. Check one supported minimum-size context for restored offscreen controls.

Pass: contracted state restores to the correct window without duplication, stale references, or cross-window leakage; unsaved changes follow the documented save/recovery behavior. Missing content provides a usable fallback. Do not require persistence of transient state that the product intentionally resets, or claim failure when the user's reopen setting intentionally suppresses restoration.

## DD-1: Supported drops and cancellation

Precondition: define supported content types, same-container versus cross-container behavior, and copy/move semantics. Use disposable files and destinations.

1. Drag one item and multiple items within a container and between supported windows. Include a drag from an inactive window if supported.
2. When copy/move modifiers apply, hold and release Option before dropping; verify the operation at drop time.
3. Cancel with Escape and drag outside the target. Check both source and destination contents and selection.

Pass: allowed destinations and intended copy/move behavior are understandable; committed content and selection match the product contract; cancellation leaves data intact. Check Undo where the operation promises it. A successful visual animation alone is insufficient evidence of a successful transfer.

## DD-2: Unsupported, failed, or delayed drops

1. Try an unsupported type, a mixed valid/invalid selection, and a supported but unreadable disposable source or rejected test destination.
2. If transfer is asynchronous, use a controlled delay/failure supported by the test harness. Observe progress, cancellation, retry, and repeated drop handling where provided.
3. Confirm source/destination contents after completion or failure. Exercise the offered keyboard/menu alternative for the same core task.

Pass: invalid targets do not imply success; partial acceptance is explicit; failures preserve source data and give an actionable result; delayed transfers signal progress and do not silently duplicate imports. Judge exact retry and duplicate rules against the product contract.

## Source boundaries

Apple background, consulted 2026-10-17: [Windows](https://developer.apple.com/design/human-interface-guidelines/windows#macOS) describes key/main/inactive windows and standard window behavior; [Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop) covers feedback, supported destinations, cancellation/recovery, modifiers, and inactive-window dragging. The cases above are **PRODUCT-HEURISTIC verification procedures**; restoration scope, data ownership, and success expectations come from the product contract. Check the framework's current restoration APIs and availability only if selecting or changing an implementation.
