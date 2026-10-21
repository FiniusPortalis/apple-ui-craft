# Review integrity policy

A release verdict is meaningful only when the reviewed input is stable and the review assignment did not mutate it. Its baseline covers that assignment, not later authorized implementation in the overall user task.

## Integrity states

- `PASS` — the reviewed artifact set matches the review-start baseline except for an explicitly allowlisted report artifact.
- `INVALIDATED` — a reviewed file was added, removed, or modified, the baseline cannot be verified, or an unexpected repository write occurred.

`INVALIDATED` is an operational review state, not a fifth HIG verdict. When it occurs, do not issue any HIG verdict.

## Baseline scope

Prefer one of these scopes:

1. **High assurance:** repository root, excluding only known cache/build directories.
2. **Targeted:** every source, test, project/workspace, configuration, resource, and generated-input file that can affect the reviewed behavior.
3. **Artifact-only:** exact screenshots, recordings, or standalone files when no repository is involved.

A narrow baseline must be disclosed as an evidence limitation.

## Bundled guard

Initialize the absolute `CRAFT_REVIEW_SKILL`, `CRAFT_REPOSITORY`, `CRAFT_SCOPE`, and `CRAFT_REVIEW_SNAPSHOT` paths as described in [SKILL.md](../SKILL.md). Keep the app as the working directory.

Create a snapshot outside the repository:

```bash
python3 "$CRAFT_REVIEW_SKILL/scripts/review_integrity_guard.py" snapshot \
  --root "$CRAFT_REPOSITORY" \
  --target "$CRAFT_SCOPE" \
  --output "$CRAFT_REVIEW_SNAPSHOT"
```

Repeat `--target` for multiple scopes. The helper records relative paths, sizes, SHA-256 values, symlink targets, and an aggregate digest.

Verify before the verdict:

```bash
python3 "$CRAFT_REVIEW_SKILL/scripts/review_integrity_guard.py" verify \
  --snapshot "$CRAFT_REVIEW_SNAPSHOT"
```

Allow one report artifact only when it was authorized at review start; set `CRAFT_REVIEW_REPORT` to its exact absolute path:

```bash
python3 "$CRAFT_REVIEW_SKILL/scripts/review_integrity_guard.py" verify \
  --snapshot "$CRAFT_REVIEW_SNAPSHOT" \
  --allow-report "$CRAFT_REVIEW_REPORT"
```

Exit codes:

- `0` — integrity pass
- `2` — invalid arguments or unusable snapshot
- `3` — unexpected drift

## Drift response

When drift is detected:

1. Stop reviewing the mixed state.
2. Record added, removed, modified, and type-changed paths.
3. Do not restore or edit the workspace in the review assignment.
4. Do not treat a change as acceptable because it appears to fix a finding.
5. Return `Review integrity: INVALIDATED` with no HIG verdict.
6. Require a fresh review assignment and new baseline after the workspace owner resolves the drift. It may run in the same user task under the role-boundary contract.

## Transition to implementation

Verify integrity and preserve the completed review output before the coordinator starts authorized implementation. Do not reuse an open review baseline across edits. An intentional implementation after review closure does not retroactively invalidate the preserved initial review; a post-change verdict requires a fresh review baseline and an independent reviewer as defined in `role-boundary-contract.md`.

## Git checks

When Git is available, also record at review start and end:

```bash
git rev-parse --verify HEAD
git status --porcelain=v1 --untracked-files=all
git diff --no-ext-diff --binary
git diff --no-ext-diff --binary --cached
```

Do not run state-changing Git commands. Existing user changes are allowed as baseline data; unexpected changes during the review invalidate the review assignment.

## Report artifact allowlist

At most one report artifact may be written, and only when explicitly requested. It must:

- have a review-output extension such as `.md`, `.txt`, `.json`, or `.sarif`
- be outside source, tests, project/workspace configuration, dependency metadata, generated code, plan directories, build output, and `.git`
- not overwrite an existing artifact unless the user explicitly authorized replacement

If these conditions are not met, return the report inline and write nothing.

## External enforcement

The integrity helper detects changes but cannot prevent them. For high-assurance review, run Codex in read-only permissions or an OS-enforced read-only sandbox and expose a separate report-only write location. Preserve tool traces or file-change events when the execution environment supports them.
