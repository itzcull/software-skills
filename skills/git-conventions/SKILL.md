---
name: git-conventions
description: Git commit conventions covering stability invariants, conventional commit types (feat, fix, refactor, test, chore), message formatting (imperative voice, 50/72 rule), TDD commit rhythm (commit after each RED-GREEN-REFACTOR step), and PR standards. Use when writing commit messages, structuring commits, or reviewing git history quality.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Define the conventions for git commits that maintain a clean, bisectable, and meaningful project history. Every commit represents stable, working software with incremental, focused changes.

## When to use

- Writing commit messages
- Deciding what to include in a single commit
- Structuring commits during TDD (when to commit in RED-GREEN-REFACTOR)
- Reviewing commit history quality
- Setting up commit conventions for a new project
- Understanding conventional commit types and their usage

## Key principles

- **Stability first** - every commit must pass all tests, build, lint, and type check
- **Incremental progress** - small, focused changes easy to review, revert, and bisect
- **Imperative voice** - describe what the code DOES when applied
- **Semantic clarity** - type prefixes indicate the nature of change at a glance
- **TDD rhythm** - commit after GREEN, commit after REFACTOR

## Reference files

- [Git commit conventions](references/git-commits.md) - Complete guide including stability invariants, commit types, message formatting, TDD commit rhythm, and PR standards
