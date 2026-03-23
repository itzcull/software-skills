---
name: test-driven-development
description: Complete TDD skill covering the RED-GREEN-REFACTOR cycle, phase orchestration across spawned contexts, individual phase execution (RED, GREEN, REFACTOR), handoff contracts, and guided TDD pairing for collaborative test-first development. Use when implementing features test-first, running TDD cycles, pairing on test-driven discovery, or enforcing strict phase boundaries.
license: MIT
version: 1.0.0
metadata:
  author: itzcull
---

## Purpose

Provide everything needed to practice strict Test-Driven Development: orchestrate RED-GREEN-REFACTOR cycles, execute individual phases with clear boundaries, validate handoffs between phases, and guide collaborative test-first discovery sessions.

## When to use

- Implementing features using strict TDD
- Running a full RED-GREEN-REFACTOR cycle through separate context windows
- Breaking a feature into discrete behavior slices
- Pairing on test-driven discovery to collaboratively design interfaces through tests
- Enforcing phase boundaries between test writing, implementation, and refactoring
- Creating a clearer audit trail for TDD compliance

## Core Principles

- TDD is non-negotiable: no production code without a failing test first
- Tests encode intent, not implementation
- One behavior slice per cycle
- Each phase stops as soon as its exit criteria are met
- No phase may smuggle in work that belongs to another phase
- If a phase cannot proceed safely without guessing, escalate instead of assuming

## Cycle Orchestration

Coordinate a strict RED-GREEN-REFACTOR cycle across separate spawned contexts. The orchestrator decides the next behavior slice, invokes the right phase in order, validates each handoff, and ensures the work stays test-first and behavior-preserving.

### Orchestration Model

- One behavior slice per cycle
- Spawn phases sequentially: RED -> GREEN -> REFACTOR
- Do not overlap phases or run them in parallel
- Require a valid handoff before starting the next phase
- Stop the cycle immediately if any phase escalates ambiguity or unsafe scope

### Process

1. Select the next smallest observable behavior.
2. Spawn a RED context with only the behavior slice and relevant local context.
3. Validate the RED handoff against `references/phase-handoffs.md`.
4. Spawn a GREEN context using the RED handoff as the primary input.
5. Validate the GREEN handoff against the same contract.
6. Spawn a REFACTOR context using the GREEN handoff as the primary input.
7. Record the outcome as either:
   - completed cycle with `no refactor needed`, or
   - completed cycle with verified refactoring, or
   - escalated cycle requiring user input
8. Decide whether the next behavior slice should start immediately or wait for a commit boundary.

### Handoff Validation

Before spawning the next phase, confirm the prior handoff includes:

- `Phase`
- `Behavior`
- `Test level`
- `Scope`
- `Evidence`
- `Constraints`
- `Open questions`
- `Next prompt`

Reject or rework the handoff if:

- The behavior is broader than one slice
- The evidence is missing or vague
- The phase performed work outside its boundary
- The next prompt lacks exact files, commands, or test identifiers

### Exit Criteria

- The full RED-GREEN-REFACTOR cycle is complete for one behavior slice
- The handoff chain is preserved from phase to phase
- Any ambiguity or blocked work is surfaced explicitly
- The result is ready for commit or the next cycle

### Cycle Report

Return a compact cycle report with:

- The behavior slice completed
- The three phase outcomes
- Key commands used in each phase
- Whether refactoring was applied or skipped
- Any unresolved questions before the next cycle

## RED Phase

Execute only the RED phase for one behavior slice. Define the next observable behavior as a test, run it, confirm it fails for the expected reason, and stop before any production implementation.

### RED Process

1. Identify the next smallest observable behavior.
2. Write exactly one test that captures that behavior through the public API.
3. Use factory functions for test data where needed.
4. Run the narrowest useful test command.
5. Confirm the new test fails for the right reason.
6. Prepare a concise handoff for the GREEN phase.

### RED Exit Criteria

- Exactly one new behavior is captured in a test
- The test fails for a behavioral reason, not a syntax or setup issue
- No production code was changed
- The GREEN handoff is ready

### RED Constraints

- No production code edits
- No batching multiple tests
- No implementation advice beyond what the test implies
- No interaction assertions against internal collaborators

## GREEN Phase

Execute only the GREEN phase for one behavior slice. Consume a RED handoff, implement the smallest change that makes the failing test pass, verify the result, and stop before opportunistic cleanup.

### GREEN Process

1. Read the RED handoff and relevant files only.
2. Confirm the failing behavior being implemented.
3. Make the smallest production change that satisfies the failing test.
4. Re-run the narrowest useful verification command.
5. Stop as soon as the test passes.
6. Prepare a concise handoff for the REFACTOR phase.

### GREEN Exit Criteria

- The previously failing test now passes
- The implementation is minimal and behavior-driven
- No unrelated cleanup or new behavior was added
- The REFACTOR handoff is ready

### GREEN Constraints

- No new tests unless correcting a malformed RED test is unavoidable
- No speculative abstractions
- No opportunistic refactoring
- No extra features beyond the failing test's demand
- Preserve existing conventions and public behavior outside the targeted slice

## REFACTOR Phase

Execute only the REFACTOR phase for one behavior slice. Consume a GREEN handoff, assess the code explicitly, improve internals only when that adds value, and verify behavior remains unchanged.

### REFACTOR Process

1. Read the GREEN handoff and affected files.
2. Assess refactoring need using the checklist below.
3. Classify findings as critical, high value, nice to have, or skip.
4. If useful refactoring exists, apply only behavior-preserving changes.
5. Re-run tests and other relevant quality gates.
6. Return either a verified refactor handoff or an explicit no-refactor decision.

### Refactoring Checklist

Assess these explicitly:

1. Naming clarity
2. Magic values and constants
3. Structural complexity and nesting
4. Knowledge duplication
5. Purity and immutability

### Refactoring Priority

- **Critical**: fix now before ending the session
- **High value**: fix this session if the value is clear
- **Nice to have**: defer unless the cleanup is tiny and obvious
- **Skip**: code is already clear enough

### REFACTOR Exit Criteria

- Refactoring assessment is explicit
- Any applied refactor preserves behavior and keeps checks green
- Or a clear `no refactor needed` outcome is documented
- The resulting state is ready for commit or the next behavior slice

### REFACTOR Constraints

- No behavior changes
- No new user-visible functionality
- No public API changes unless preserving compatibility demands a safe internal adapter
- Prefer semantic abstractions over structural ones
- Skip refactoring if the code is already clear enough

## Guided TDD Pairing

A collaborative mode for discovering requirements and designing interfaces through tests.

### Philosophy

- **Most valuable behavior next** -- always ask "what is the next most important behavior?"
- **Tests encode intent** -- each test is an executable specification of behavior
- **One test at a time** -- propose a single test, discuss it, implement it, then ask what's next
- **User controls the pace** -- always wait for approval before writing code
- **Interface emerges from tests** -- the test implies the design; discuss what it reveals

### Pairing Process

1. **Understand** -- ask what the user wants to build, listen for the problem, users, definition of done, and constraints
2. **Discover the next most important behavior** -- prioritize by value, not convenience
3. **Propose a test** -- present one test case, explain the implied interface, get approval
4. **RED** -- write the test, run it, confirm it fails for the right reason
5. **GREEN** -- write minimum code to pass, run tests to confirm
6. **REFACTOR** -- assess explicitly, improve if warranted, confirm tests still pass
7. **Next** -- re-evaluate what matters most and repeat

### Behavior Priority

When suggesting candidates, rank by value to the core problem:

1. **Core behaviors** -- directly solves the user's problem
2. **Critical paths** -- system fails meaningfully without this
3. **Error handling** -- what happens when expected input is missing
4. **Edge cases** -- unusual but valid scenarios
5. **Nice-to-haves** -- convenience, polish, optimization

### Test Data Patterns

Use factory functions with optional overrides:

```typescript
const createItem = (overrides?: Partial<Item>): Item => ({
  id: 'item-1',
  name: 'Test Item',
  price: 10.00,
  ...overrides,
});
```

### Interface Design Through Tests

Tests reveal interface requirements. When proposing a test, explicitly discuss:

- What types/interfaces does this imply?
- What are the inputs and outputs?
- What's the simplest signature that satisfies this test?

## Escalation Conditions

Stop and ask when:

- The next behavior slice is not clear enough to write one focused test
- A phase handoff is invalid or incomplete after reasonable correction
- GREEN would require broad API design decisions beyond the slice
- REFACTOR reveals larger pre-existing design issues outside current scope
- Project test infrastructure is too broken to prove RED or GREEN honestly
- The observed failure suggests broken test infrastructure rather than missing behavior

## Constraints

- Never merge phases into one context if separate phase windows are the goal
- Never allow production code before a proven RED state
- Never skip refactor assessment, even if the result is `no refactor needed`
- Never widen the slice just because adjacent work looks convenient
- Prefer multiple small cycles over one large ambiguous cycle
- Test behavior, not implementation -- no spying on internal methods
- Use factory functions -- no `let`/`beforeEach` for test data

## Technology Agnostic

- Use whatever test runner is available in the project
- Infer conventions from existing codebase patterns
- If conventions are unclear, ask the user
- Adapt syntax to the language being used

## Reference Documentation

- [Phase Handoffs](references/phase-handoffs.md) -- handoff contracts between TDD phases
