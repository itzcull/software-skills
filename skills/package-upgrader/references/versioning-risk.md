# Versioning Risk

Dependency upgrade risk is the probability that a version change alters build behavior, runtime behavior, public APIs, generated artifacts, deployment compatibility, or operational characteristics in a way the repository does not expect.

Version numbers are useful risk signals, but they are never proof of compatibility. Always combine version deltas with ecosystem conventions, dependency role, changelog evidence, and repository verification strength.

## Semantic Versioning

Semantic Versioning uses `MAJOR.MINOR.PATCH`:

| Delta | Meaning when SemVer is honored | Default risk |
|---|---|---|
| Major | Breaking changes are allowed | High |
| Minor | Backward-compatible functionality is added | Medium |
| Patch | Backward-compatible bug fixes are added | Low |

SemVer applies only when the package author follows it. Treat SemVer as a statement of intent, not a compatibility contract.

### Pre-1.0.0 Caveat

For `0.y.z` versions, SemVer treats the public API as unstable. A minor change such as `0.4.0` to `0.5.0` may include breaking changes.

Default risk for pre-`1.0.0` upgrades:

- `0.x.0` minor change: high risk
- `0.x.y` patch change: medium risk unless release notes show it is a narrow fix
- Any pre-release tag change: high risk unless the repository intentionally tracks previews

## Pre-release and Build Metadata

Versions with pre-release identifiers such as `alpha`, `beta`, `rc`, `preview`, `next`, `dev`, or timestamped snapshots are not stable releases unless the ecosystem explicitly treats them that way.

Risk signals:

- Stable to pre-release: high risk; usually avoid unless explicitly requested
- Pre-release to stable: medium risk; verify migration notes because APIs may have changed since the preview
- Pre-release to newer pre-release: high risk; breaking changes can happen without major version changes
- Build metadata-only changes: low versioning risk, but verify artifact provenance when supply-chain trust matters

## Non-SemVer Schemes

Not every ecosystem uses SemVer.

### Calendar Versioning

Calendar Versioning encodes release date in the version. A change from `2024.12` to `2025.01` is not automatically equivalent to a SemVer major upgrade.

For CalVer dependencies, inspect:

- Project compatibility policy
- Deprecation policy
- Supported runtime or platform matrix
- Release notes between current and target versions

Classify risk from documented compatibility, not from the year/month delta alone.

### Ecosystem-Specific Versioning

Some ecosystems use schemes such as PEP 440, epoch versions, post releases, revision suffixes, distro package revisions, or registry-specific constraints.

When version semantics are ecosystem-specific:

- Read the package manager's versioning rules if they affect candidate selection
- Identify whether the maintainer promises SemVer, CalVer, API stability, LTS compatibility, or no stability guarantee
- Prefer the repository's existing dependency automation configuration when it already encodes grouping or compatibility rules

## Version Ranges and Constraints

The manifest constraint and the resolved version are different facts.

Review both:

- Manifest range: what versions the project allows
- Lockfile or resolver output: what version the project actually uses
- Transitive constraints: what versions are selected because another dependency requires them
- Runtime/platform constraints: engines, language versions, operating systems, architectures, native toolchains, or framework peer ranges

Risk increases when an upgrade broadens allowed ranges without updating the resolved lockfile, updates the resolved lockfile without changing explicit constraints, or bypasses constraints with force/override mechanisms.

## Dependency Role Risk

Classify dependencies by the behavior they can affect.

| Role | Risk considerations |
|---|---|
| Runtime dependency | Can change production behavior, APIs, data formats, performance, security, or compatibility |
| Development dependency | Can change local workflows, generated artifacts, tests, linting, formatting, or build output |
| Build dependency | Can change bundles, binaries, compilation, transpilation, minification, dependency resolution, or packaging |
| Test dependency | Can change test semantics, timing, mocks, assertions, snapshots, or coverage |
| Compiler/runtime dependency | Can change language semantics, standard libraries, type checking, generated code, or deployment requirements |
| Plugin/extension dependency | Compatibility depends on host versions and plugin APIs, often outside simple SemVer guarantees |
| Peer/compatibility dependency | Must satisfy another package's expected host version; conflicts can be runtime failures even if install succeeds |
| Transitive dependency | May be invisible to source code but can affect security, resolution, generated artifacts, or runtime paths |
| Optional/platform dependency | Can affect specific operating systems, architectures, native builds, or production environments only |

Runtime, compiler, framework, and build-tool upgrades usually deserve more verification than ordinary development-only patch updates.

## Direct vs Transitive Dependencies

Direct dependencies appear in the repository's manifests. Transitive dependencies are brought in by direct dependencies.

Direct dependency upgrades need source-level compatibility checks because repository code may call their APIs directly.

Transitive dependency upgrades need resolver and behavior checks because they may alter nested behavior, security posture, binary artifacts, or peer dependency satisfaction.

Security fixes often require transitive updates. Prefer the package manager's supported override, resolution, or constraint mechanism when the direct dependency cannot yet move.

## Breaking-Change Signals Beyond Versions

Treat an upgrade as high risk when any of these are present:

- Release notes mention breaking changes, removals, deprecations becoming errors, migration guides, codemods, or changed defaults
- Runtime, language, platform, operating system, architecture, or engine requirements changed
- Peer dependency ranges changed
- Configuration format changed
- Generated artifact format changed
- Database, schema, protocol, serialization, wire format, or file format changed
- Security behavior changed, such as stricter parsing, authentication defaults, TLS defaults, sandboxing, or permission handling
- Maintainer changed package name, ownership, license, provenance, registry, or signing process
- The package is a framework, compiler, bundler, ORM, HTTP client, test runner, linter, formatter, or deployment/runtime adapter

## Default Classification Heuristic

Use this as the starting point, then adjust with evidence:

| Candidate | Default classification |
|---|---|
| Stable SemVer patch | Low risk |
| Stable SemVer minor | Medium risk |
| Stable SemVer major | High risk |
| Pre-`1.0.0` minor | High risk |
| Pre-release involved | High risk |
| Runtime/compiler/framework/build-tool change | High risk unless proven narrow |
| Security patch with no API change | Low to medium risk |
| Lockfile-only transitive update | Low to medium risk depending on dependency role |
| Package manager, runtime, or ecosystem migration | High risk and usually out of scope for routine upgrades |
