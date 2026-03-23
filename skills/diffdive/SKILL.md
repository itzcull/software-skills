---
name: diffdive
description: Branch analysis and context loading. Analyses the diff between the current branch and trunk (master/main) to get up to speed quickly. Use when switching to an unfamiliar branch, resuming work after time away, onboarding onto a colleague's branch, reviewing a PR, or when you need a situation report on what a branch has changed relative to trunk.
license: MIT
version: 1.0.0
metadata:
  author: itzcull
---

## Purpose

Get up to speed on a branch by analysing its divergence from trunk. Produces a structured situation report covering what changed, why it likely changed, areas of risk, and open questions.

## When to use

- Switching to an unfamiliar branch
- Resuming work on a branch after time away
- Onboarding onto a colleague's branch or PR
- Before a code review to understand the full scope of changes
- When asking "what has this branch done?" or "catch me up"

## Process

### Step 1: Detect current branch

Run `git branch --show-current` to identify the active branch.

If on a detached HEAD, report this and ask the user which branch to analyse.

### Step 2: Determine trunk branch

If the user provided an argument, use that as the trunk branch name.

Otherwise, auto-detect by checking which of these exist (in order of preference):

1. `main`
2. `master`

Verify the chosen trunk branch exists with `git rev-parse --verify <trunk>`. If neither exists, ask the user to specify the trunk branch.

### Step 3: Find the divergence point

Run `git merge-base <trunk> HEAD` to find where this branch diverged from trunk.

### Step 4: Gather context

Collect the following information using git commands:

1. **Commit count**: `git rev-list --count <merge-base>..HEAD`
2. **Commit log**: `git log --oneline --no-decorate <merge-base>..HEAD`
3. **Diff stats**: `git diff --stat <merge-base>..HEAD`
4. **Full diff**: `git diff <merge-base>..HEAD`
5. **Files changed count**: `git diff --name-only <merge-base>..HEAD | wc -l`
6. **Trunk commits since divergence** (optional context): `git rev-list --count <merge-base>..<trunk>`

If the full diff is very large (many files or thousands of lines), prioritise the diff stats and commit log for the high-level summary, then read the full diff in sections grouped by module/directory.

### Step 5: Analyse and present the report

Study the gathered information and produce the structured report described below. Focus on understanding the **intent** behind the changes, not just describing what lines changed.

Look for:

- The overarching goal or feature being built
- Patterns in the changes (new modules, refactoring, bug fixes, test additions)
- Architectural decisions (new dependencies, structural changes, API changes)
- Potential risks (large files changed, missing tests, complex logic)
- Incomplete work (TODOs, commented-out code, partial implementations)

## Output Format

Present the report using this structure:

```
## Diff Dive: [branch-name]

**Branch:** [current branch]
**Trunk:** [trunk branch]
**Divergence point:** [short merge-base hash]
**Commits on branch:** [count]
**Commits on trunk since divergence:** [count]
**Files changed:** [count]

---

### Summary

[2-4 sentence high-level summary of what this branch is doing and why.
Frame it as a narrative: "This branch introduces...", "This branch refactors...", etc.]

### Changes by Area

**[area/module/directory]**
- [What changed and the likely intent behind it]
- [Notable additions, removals, or modifications]

**[area/module/directory]**
- [What changed and the likely intent behind it]

[...repeat for each significant area...]

### Architectural Observations

- [Patterns, design decisions, or structural changes worth noting]
- [New dependencies or tooling changes]
- [API surface changes (new endpoints, changed interfaces, etc.)]

### Risk Areas

- [Files or changes that warrant careful review]
- [Missing test coverage for new functionality]
- [Complex logic that could harbour bugs]
- [Breaking changes or backwards compatibility concerns]

### Open Questions

- [Things that are unclear from the diff alone]
- [Decisions that might need discussion]
- [Incomplete work that may need follow-up]
```

## Constraints

- **Read-only analysis** — do not modify any files, make commits, or change branch state
- **Intent over mechanics** — explain WHY changes were made, not just WHAT lines changed
- **Honest assessment** — flag genuine risks and gaps; do not gloss over problems
- **Proportional detail** — spend more analysis time on complex or risky changes, less on trivial ones
- **Respect scope** — analyse only the diff between trunk and the current branch; do not conflate with unrelated changes
