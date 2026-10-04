---
name: git-conventions
description: Git commit conventions covering stability invariants, conventional commit types (feat, fix, refactor, test, chore), message formatting (imperative voice, 50/72 rule), TDD commit rhythm (stable checkpoints after GREEN and REFACTOR), and PR standards. Use when writing commit messages, structuring commits, or reviewing git history quality.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Define the conventions for git commits that maintain a clean, bisectable, and meaningful project history. Every commit represents stable, working software with incremental, focused changes.

## Relationship to structured development

Within [structured development](../structured-development/SKILL.md), this skill supplies [traceable change records](../structured-development/SKILL.md#conformance-requirements) and information for [review or continuation at scope handoff](../structured-development/SKILL.md#7-close-the-agreed-scope) across increments. Its commit boundaries preserve understandable history; they are not substitutes for the enclosing procedure's acceptance or release boundaries.

Use the intended change, repository policy, available verification evidence, and the Git operation the user has authorized. Return proposed commit boundaries and messages, or the resulting commit or PR references when execution is requested, with an honest account of verification. Apply TDD-specific cadence when the procedure uses TDD rather than imposing test-first development on every procedure.

A commit records a change; a PR presents it for review. Neither establishes acceptance or release readiness. If stability cannot be demonstrated, report the missing or failed checks instead of asserting a verified commit. This skill's conventions do not independently authorize committing, pushing, or merging.

## When to use

- Writing commit messages
- Deciding what to include in a single commit
- Structuring commits during TDD (when to commit in RED-GREEN-REFACTOR)
- Reviewing commit history quality
- Setting up commit conventions for a new project
- Understanding conventional commit types and their usage

## Key principles

- **Stability first** - every commit must satisfy the repository's applicable stability checks; skipped required checks are not passes
- **Incremental progress** - small, focused changes easy to review, revert, and bisect
- **Imperative voice** - describe what the code DOES when applied
- **Semantic clarity** - type prefixes indicate the nature of change at a glance
- **TDD rhythm** - use stable checkpoints after GREEN and REFACTOR within the enclosing procedure's authorized commit boundaries

## Reference files

- [Git commit conventions](references/git-commits.md) - Complete guide including stability invariants, commit types, message formatting, TDD commit rhythm, and PR standards
