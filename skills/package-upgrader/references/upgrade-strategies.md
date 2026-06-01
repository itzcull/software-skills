# Upgrade Strategies

Choose the smallest upgrade strategy that satisfies the user's goal while preserving a clear verification and rollback path.

## Strategy Selection Matrix

| Strategy | Use when | Avoid when |
|---|---|---|
| `major-isolated` | Major, runtime, framework, compiler, build-tool, plugin, or compatibility-sensitive upgrades | The user needs only urgent patch fixes |
| `minor-batch` | Multiple medium-risk upgrades with strong tests and no concerning release notes | Verification is weak or dependencies are tightly coupled to production behavior |
| `patch-security` | Vulnerability remediation, low-risk bugfixes, production hotfixes, or minimal-change updates | The fix requires a major upgrade or migration |
| `single-dependency` | The user named one dependency, a bug points to one package, or a change needs focused debugging | Dependency compatibility requires a coordinated group update |
| `all-at-once` | Internal, low-risk repositories with strong CI and cheap rollback | User-facing, poorly tested, high-risk, or broad dependency changes |
| `defer` | Risk exceeds available context, verification, time, or compatibility confidence | A security fix is urgent and an acceptable mitigation exists |

## `major-isolated`

Upgrade high-risk dependencies one at a time.

Use for:

- Major version changes
- Pre-`1.0.0` minor upgrades
- Framework, runtime, compiler, build-tool, database client, ORM, plugin host, or deployment adapter upgrades
- Changes with migration guides or changed peer dependency ranges

Process:

1. Select one high-risk dependency or one tightly coupled compatibility group.
2. Read release notes, migration guides, deprecation notes, and compatibility matrices.
3. Apply the upgrade using the repository's existing dependency manager.
4. Review manifest and lockfile changes for scope.
5. Make required code or configuration migrations only when directly caused by the upgrade.
6. Run the strongest relevant verification available.
7. Stop on failure and report the rollback or remediation path.

Keep each high-risk upgrade reviewable. Do not mix unrelated refactors or opportunistic dependency cleanup into the same change.

## `minor-batch`

Group compatible medium-risk updates when automated verification is strong.

Use for:

- Stable SemVer minor upgrades with no breaking-change signals
- Development or test dependencies with narrow blast radius
- Dependency groups that the repository automation already batches safely

Process:

1. Group dependencies by role or ecosystem convention.
2. Exclude anything with breaking-change signals, changed runtime requirements, peer conflicts, or migration notes.
3. Apply the batch through the existing dependency manager.
4. Review manifest and lockfile changes.
5. Run normal repository verification.
6. If verification fails, split the batch to isolate the failing dependency.

Prefer smaller batches when verification is slow, flaky, or incomplete.

## `patch-security`

Apply the narrowest update that remediates vulnerability or bugfix risk.

Use for:

- Security advisories
- CVE remediation
- Production hotfixes
- Known bugfix releases
- Patch-level transitive dependency updates

Process:

1. Identify the advisory, affected versions, fixed versions, and whether the dependency is direct or transitive.
2. Prefer the smallest compatible fixed version.
3. Use supported constraint, override, resolution, or lockfile update mechanisms.
4. Verify the vulnerable version is no longer resolved.
5. Run targeted tests plus any security, build, or smoke checks relevant to the affected dependency.

Do not use force or legacy resolver flags as the first option. If a workaround is required, document why and what follow-up removes it.

## `single-dependency`

Upgrade one named dependency or compatibility group.

Use for:

- User-requested package updates
- Debugging upgrade failures
- Isolating a suspected dependency issue
- Evaluating one high-impact dependency before broader upgrades

Process:

1. Confirm the current constraint, resolved version, and target version.
2. Check direct usage in source code and configuration.
3. Read release notes between current and target versions.
4. Apply only that dependency and necessary peer or companion packages.
5. Verify relevant behavior.
6. Report whether broader related upgrades are still needed.

Treat companion packages as part of the same upgrade unit only when they are version-coupled by documented compatibility.

## `all-at-once`

Upgrade many dependencies in one operation.

Use only when:

- The repository is low-risk or internal
- Verification is fast and comprehensive
- Rollback is trivial
- The user explicitly prefers speed over isolation
- The expected upgrade set excludes high-risk migrations

Process:

1. State that failure isolation will be harder.
2. Apply the broad upgrade with existing tooling.
3. Run full verification.
4. If verification fails, split by risk category and retry smaller batches.

This is not the default strategy for production applications, libraries with external consumers, or repositories with weak tests.

## `defer`

Do not upgrade yet when the safe path is not available.

Use when:

- The authoritative package manager or lockfile is unclear
- The upgrade requires a platform, runtime, framework, or ecosystem migration the user did not request
- Verification is absent and the dependency is high risk
- Release notes indicate breaking changes but migration scope is unknown
- Security fixes require incompatible versions and no tested mitigation is available

Output should include:

- Why deferral is safer than proceeding
- What information or verification is missing
- The smallest next step that would make the upgrade actionable
- Any temporary mitigation for security-driven deferrals

Deferral is a strategy, not a failure. It protects the repository from blind changes.
