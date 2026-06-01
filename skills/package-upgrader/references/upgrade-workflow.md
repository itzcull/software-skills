# Upgrade Workflow

Use this workflow to turn dependency upgrade requests into controlled, reviewable changes.

## Phase 1: Discovery

Identify the dependency system before running upgrade commands.

Look for:

- Manifests that declare direct dependencies, workspaces, plugins, runtime constraints, or dependency groups
- Lockfiles, pinned dependency snapshots, vendored dependency directories, generated resolver output, or checksum files
- Toolchain files for language, runtime, compiler, package manager, SDK, or platform versions
- Package manager configuration, registry configuration, dependency override files, or workspace configuration
- CI configuration, scripts, Makefiles, task runners, container files, and repository docs
- Existing dependency automation configuration and grouping rules

If multiple ecosystems exist, identify the requested scope before updating anything. A monorepo may have separate dependency graphs with separate verification commands.

## Phase 2: Baseline

Create a rollback-friendly baseline.

Before changing files:

- Inspect worktree status and note unrelated user changes
- Identify the current branch and commit
- Identify which manifests and lockfiles are authoritative
- Record current and target versions for requested dependencies
- Determine normal verification commands from repository evidence
- Run baseline verification when practical, especially before high-risk upgrades

If baseline verification already fails, report that clearly. Continue only when the user accepts that post-upgrade failures may not be attributable to the dependency change.

## Phase 3: Risk Classification

For each candidate dependency, classify:

- Version delta and versioning scheme
- Direct or transitive relationship
- Runtime, development, build, test, compiler, plugin, peer, optional, or platform role
- Expected blast radius
- Release-note or migration-guide evidence
- Security urgency or advisory requirements
- Verification strength available in this repository

Use this classification to choose the strategy from `upgrade-strategies.md`.

## Phase 4: Strategy Selection

Prefer the safest strategy that satisfies the request:

- High-risk changes: isolate
- Medium-risk compatible changes: batch cautiously
- Security patches: keep narrow
- User-named dependency: target directly
- Weak verification: slow down or defer

Ask before broadening scope. Examples of scope broadening include upgrading companion packages, changing runtime versions, applying overrides, replacing lockfiles, switching package managers, or migrating configuration formats.

## Phase 5: Execution

Use the repository's existing package manager and documented workflow.

Execution rules:

- Do not switch package managers
- Do not delete lockfiles to resolve conflicts
- Do not use force flags, legacy resolver flags, or constraint bypasses unless necessary and documented
- Prefer lockfile-respecting commands for routine upgrades
- Keep generated dependency metadata synchronized with manifests
- Review changed manifests and lockfiles after each upgrade unit
- Keep unrelated source refactors out of dependency upgrade commits

For high-risk upgrades, read release notes before applying or before finalizing the change. For low-risk patches, release notes can be checked after the resolver selects the target version if the change remains narrow.

## Phase 6: Verification

Use repository-native verification. Prefer commands already present in scripts, CI, docs, or task runners.

Verification may include:

- Dependency resolver/install check
- Build or compile check
- Unit, integration, component, contract, end-to-end, or smoke tests
- Linting, formatting, type checking, static analysis, or generated-code checks
- Security audit or vulnerability scan
- License, provenance, or supply-chain checks
- Runtime startup, migration dry run, or compatibility smoke test

Choose checks based on the dependency's role. A compiler upgrade deserves compile and type checks. A database client upgrade deserves integration or adapter tests. A test runner upgrade deserves confidence that tests still execute with the intended semantics.

When verification is too expensive to run locally, state what was not run and why. Do not imply confidence from checks that did not run.

## Phase 7: Failure Handling

When verification fails after an upgrade:

1. Stop the upgrade sequence.
2. Identify the upgrade unit that introduced the failure.
3. Summarize the failing command and the relevant error output.
4. Decide whether the failure is a migration requirement, a compatibility issue, a flaky/pre-existing failure, or an unrelated environment issue.
5. Recommend one of: fix forward, split the batch, rollback the upgrade unit, defer the dependency, or ask the user for scope approval.

Do not continue through failed verification unless the user explicitly accepts the risk.

## Phase 8: Rollback

Rollback should restore manifests, lockfiles, generated dependency metadata, and any code/config changes made for the failed upgrade.

Preferred rollback paths:

- Revert the uncommitted files for the failed upgrade unit when no unrelated user changes are present in those files
- Use version-control revert for committed upgrade changes
- Reapply the previous dependency constraint and regenerate the lockfile with the repository's package manager
- Remove temporary overrides or forced resolutions introduced for the failed attempt

Never overwrite unrelated user changes. If rollback would touch files with user changes, stop and ask how to proceed.

## Phase 9: Reporting

Report results in a compact, reviewable format:

```markdown
## Dependency Upgrade Report

**Strategy:** major-isolated | minor-batch | patch-security | single-dependency | all-at-once | defer
**Scope:** direct packages, transitive packages, workspace, runtime, or ecosystem area
**Result:** completed | partially completed | failed | deferred

### Changed
| Dependency | From | To | Role | Risk |
|---|---|---|---|---|

### Verification
| Check | Result | Notes |
|---|---|---|

### Follow-ups
- Migration work, skipped checks, compatibility warnings, or deferred upgrades
```

Include rollback guidance when the result is failed, partial, or high risk.

## Review Checklist

Before finishing, confirm:

- The upgrade used the repository's existing tooling
- Manifest and lockfile changes match the intended scope
- No unrelated files were changed
- High-risk upgrades were isolated or explicitly approved as a batch
- Verification ran or skipped checks are clearly stated
- Security advisories are remediated or documented with mitigation/follow-up
- Rollback remains possible from the current state
