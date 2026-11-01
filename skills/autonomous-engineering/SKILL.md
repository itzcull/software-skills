---
name: autonomous-engineering
description: Autonomous engineering workflow for end-to-end feature delivery using strict TDD. Covers the six-phase workflow (requirement decomposition, design decisions, acceptance criteria, TDD implementation, integration, review preparation), ADR templates for architectural decisions, and review contracts for artifact quality. Use when implementing features autonomously, writing ADRs, or following structured TDD delivery workflows.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Define the structured workflow for autonomous feature delivery following strict TDD practices. This skill covers the complete lifecycle from natural language requirements through to review-ready artifacts.

## When to use

- Implementing features end-to-end with autonomous execution
- Following the six-phase TDD delivery workflow
- Writing Architecture Decision Records (ADRs)
- Preparing artifacts for code review
- Understanding the review contract between autonomous agent and reviewer

## Guiding principles

1. **Autonomous in execution, not in interpretation** - execute autonomously but surface ambiguity rather than guessing
2. **TDD is non-negotiable** - every line of production code preceded by a failing test
3. **Decisions are documented** - significant design decisions produce ADRs with tradeoff analysis
4. **Tests are executable specifications** - acceptance criteria translate into persistent tests
5. **Small, stable increments** - every commit is stable, codebase always works

## Six-phase workflow

1. **Requirement Decomposition** - parse requirements, explore codebase, identify ambiguity
2. **Design Decisions** - evaluate options, produce ADRs, select approach
3. **Acceptance Criteria** - translate requirements into testable behavioral specifications
4. **TDD Implementation** - RED-GREEN-REFACTOR cycles for each acceptance criterion
5. **Integration** - verify all criteria met, run full test suite, check stability
6. **Review Preparation** - produce structured artifacts for reviewer

## Reference files

- [Workflow](references/workflow.md) - Complete six-phase workflow with entry/exit criteria
- [TDD Workflow](references/tdd-workflow.md) - RED-GREEN-REFACTOR process, quality gates, compliance verification, refactoring priority, and DRY decision framework
- [ADR Template](references/adr-template.md) - Architecture Decision Record template
- [Review Contract](references/review-contract.md) - Contract governing review artifacts
