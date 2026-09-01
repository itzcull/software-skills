---
name: package-upgrader
description: Dependency upgrades, package upgrades, update packages, outdated packages, version bumps, security updates, and dependency management. Use when planning, executing, or reviewing safe dependency upgrades across any package ecosystem using versioning standards, risk classification, verification, and rollback guidance.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Guide safe dependency upgrades in any repository. The skill helps an agent discover the repository's dependency tooling, classify upgrade risk using software versioning standards, choose an upgrade strategy, execute changes incrementally, verify behavior with repository-native checks, and preserve a clear rollback path.

Dependency upgrade guidance must be grounded in the project being changed. Do not assume a language, package manager, registry, lockfile format, or command syntax before inspecting the repository.

## When to use

- The user asks to upgrade dependencies, update packages, bump versions, refresh outdated dependencies, or manage dependency drift
- The user asks for security updates, vulnerability remediation, CVE-driven dependency upgrades, or patch-only dependency changes
- The user wants to understand upgrade risk before changing dependencies
- A branch or pull request changes dependency manifests, lockfiles, package constraints, runtime versions, SDK versions, plugin versions, or generated dependency metadata
- The user wants an incremental strategy for major upgrades, ecosystem migrations, framework upgrades, or dependency cleanup

Do not use this skill for release versioning of the user's own product unless dependency upgrades are part of the release. Use `git-conventions` when the main question is commit structure or history quality.

## Core principles

- **Discover before deciding**: infer tooling from manifests, lockfiles, build files, CI config, repository docs, and existing scripts.
- **Do not switch ecosystems accidentally**: use the repository's existing package manager and lockfile strategy unless the user explicitly approves a migration.
- **Version numbers are signals, not guarantees**: SemVer, CalVer, PEP 440, and ecosystem conventions inform risk but do not replace changelogs, migration guides, and verification.
- **High-risk changes deserve isolation**: upgrade major, framework, runtime, compiler, build-tool, and plugin changes one at a time unless verification is unusually strong.
- **Lockfiles are safety artifacts**: preserve reproducible installs and review lockfile changes as part of the upgrade.
- **Verification defines confidence**: prefer existing CI, build, test, lint, typecheck, integration, and smoke-test commands over invented checks.
- **Rollback must stay cheap**: know the pre-upgrade state before changing manifests or lockfiles.

## Workflow

### Step 1: Discover dependency tooling

Inspect the repository for:

- Dependency manifests and workspace manifests
- Lockfiles, vendored dependency metadata, generated dependency snapshots, or dependency pin files
- Build files, package-manager config, language-version files, container files, and toolchain files
- CI configuration and documented verification commands
- Existing dependency update automation, such as Renovate, Dependabot, or ecosystem-specific bots

Use the discovered tooling. Do not install a different package manager, delete a lockfile, or regenerate dependency metadata with unfamiliar tooling unless that is the user's explicit goal.

### Step 2: Establish a baseline

Before changing dependencies:

- Check whether the worktree already has user changes and avoid overwriting them
- Record the current branch, commit, changed files, and relevant manifest or lockfile state
- Identify the repository's normal verification commands from docs, scripts, CI, and existing automation
- Run or inspect baseline verification when practical so failures introduced by upgrades can be distinguished from pre-existing failures

### Step 3: Classify upgrade risk

Use `references/versioning-risk.md` to classify each candidate upgrade by:

- Version delta: major, minor, patch, pre-release, build metadata, or non-SemVer scheme
- Dependency role: runtime, development, build, test, compiler, plugin, peer, transitive, optional, or platform dependency
- Blast radius: direct API use, framework behavior, generated output, deployment runtime, data format, security posture, or operational behavior
- Evidence: changelogs, release notes, migration guides, deprecations, security advisories, and known ecosystem conventions

Treat major version changes and pre-`1.0.0` minor changes as high risk until evidence shows otherwise.

### Step 4: Choose an upgrade strategy

Use `references/upgrade-strategies.md` to choose the smallest strategy that satisfies the user's goal:

- `major-isolated` for high-risk direct, framework, runtime, compiler, or build-tool upgrades
- `minor-batch` for compatible upgrades when verification coverage is strong
- `patch-security` for low-risk bugfixes or urgent vulnerability remediation
- `single-dependency` for targeted fixes, debugging, or one package requested by the user
- `all-at-once` only for low-risk/internal repositories with strong automated verification
- `defer` when upgrade risk exceeds available context or verification

Ask for user choice only when multiple strategies are plausible and the decision affects risk, time, or scope. Otherwise select the safest strategy and proceed.

### Step 5: Execute incrementally

Use the repository's package manager, dependency manager, or documented upgrade workflow. Prefer commands that respect the existing lockfile and workspace structure.

For each upgrade unit:

- Change only the intended dependency set
- Review manifest and lockfile changes before moving on
- Check release notes or migration guidance for high-risk changes
- Run the relevant verification checks before proceeding to the next high-risk unit
- Stop when verification fails unless the user explicitly chooses to continue

### Step 6: Verify and report

Use `references/upgrade-workflow.md` for detailed verification and failure handling.

Report:

- What changed: dependency names, current versions, target versions, and risk category
- What verification ran and whether it passed
- Any skipped checks and why they were skipped
- Any warnings, peer or compatibility issues, lockfile anomalies, or migration follow-ups
- The rollback path if failures remain

## Escalation conditions

Stop and ask before proceeding when:

- Multiple lockfiles or package managers conflict and the repository does not document which one is authoritative
- The upgrade implies an ecosystem migration, package manager migration, language runtime migration, or framework migration
- Verification is absent or already failing and the upgrade is high risk
- A dependency upgrade requires code migrations beyond straightforward API adjustments
- Security guidance conflicts with compatibility constraints or pinned transitive dependencies
- The lockfile changes far more than expected for the requested upgrade

## Anti-patterns

- Running package-manager commands before identifying the repository's actual tooling
- Updating every dependency at once in a poorly tested codebase
- Treating SemVer as a guarantee that minor and patch updates cannot break behavior
- Ignoring pre-release tags, peer dependency constraints, engine/runtime constraints, or plugin compatibility matrices
- Deleting or replacing lockfiles to make an upgrade "work"
- Continuing through failed verification without making the risk explicit
- Committing dependency upgrades with unrelated refactors or feature work

## Reference files

- `references/versioning-risk.md` -- versioning standards, risk signals, dependency role impact, and breaking-change indicators
- `references/upgrade-strategies.md` -- strategy selection for major, minor, patch, security, targeted, batch, and deferred upgrades
- `references/upgrade-workflow.md` -- discovery, baseline, execution, verification, failure handling, rollback, and reporting workflow
