---
name: test-driven-development
description: Behavior-level test-first implementation and design-feedback protocol for use within a structured-development procedure. Covers RED-GREEN-REFACTOR cycles, phase orchestration across spawned contexts, individual phase execution, handoff contracts, and guided TDD pairing. Use when implementing features test-first, running TDD cycles, pairing on test-driven discovery, or connecting TDD evidence and escalation to an enclosing development procedure.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Provide a behavior-level implementation and design-feedback protocol using strict Test-Driven Development: orchestrate RED-GREEN-REFACTOR cycles, execute individual phases with clear boundaries, validate handoffs between phases, and guide collaborative test-first discovery sessions.

## Relationship to Structured Development

[Structured development](../structured-development/SKILL.md) owns the methodology-independent contract. This skill owns the TDD protocol that a concrete procedure can use within a behavior-level development loop; it is not a complete delivery procedure or a replacement for the contract.

Within that loop, behavior selection and executable tests prepare an increment, implementation and refactoring realize it, and test results support evaluation and adaptation. The [cycle report](#cycle-report) closes or escalates that local scope. These contributions span several [abstract responsibilities](../structured-development/SKILL.md#abstract-procedure), rather than belonging only to execution.

The enclosing procedure owns broader outcome selection, integration, acceptance, and lifecycle handoffs. It determines which obligations are assigned to TDD cycles and which require evaluation elsewhere. Completing a cycle supplies evidence to that procedure; it does not establish feature acceptance, operational readiness, or release authorization.

Guided pairing and separate-context orchestration are participation arrangements for the protocol. Selecting this skill does not itself authorize delegation, commits, or deployment.

### Cycle Inputs

Before starting a cycle, establish from the enclosing procedure or the user's agreed task:

- The intended behavior and its connection to a broader goal or acceptance criterion; use guided discovery when the behavior still needs clarification.
- The allowed scope, inherited decisions and constraints, and relevant [concern obligations](../structured-development/SKILL.md#concern-placement) due at this cycle's boundary.
- The verification needed for those obligations, including relevant integration or regression checks beyond the new test.
- Who can select the next behavior, resolve ambiguity, or approve changes to scope and acceptance criteria, and who receives the cycle's results.

Reuse existing plans, tests, and discussions rather than requiring a new input document. Check that inherited decisions still apply to the selected behavior. Resolve missing inputs that prevent safe progress before RED; do not invent approvals or obligations. A standalone TDD request can use the user's agreed scope and authority without inventing a larger process.

### Results and Handoffs

Return the [cycle report](#cycle-report) to the enclosing procedure before selecting further work under its decision authority. Preserve the connection from the intended behavior to implementation evidence and any remaining obligations. Work outside the cycle, including deferred concerns, returns to that procedure for disposition; it is not silently treated as completed.

For a single-phase invocation, return the [phase handoff](references/phase-handoffs.md), not a claim that the cycle is complete. When a discovery invalidates inherited decisions or affects another scope, use the [escalation conditions](#escalation-conditions) to obtain a decision before continuing.

## When to use

- Implementing features using strict TDD
- Running a full RED-GREEN-REFACTOR cycle through separate context windows
- Breaking a feature into discrete units of behavior
- Pairing on test-driven discovery to collaboratively design interfaces through tests
- Enforcing phase boundaries between test writing, implementation, and refactoring
- Creating a clearer audit trail for TDD compliance

## Core Principles

- TDD is non-negotiable: no production code without a failing test first
- Tests encode intent, not implementation
- One unit of behavior per cycle
- Each phase stops as soon as its exit criteria are met
- No phase may smuggle in work that belongs to another phase
- If a phase cannot proceed safely without guessing, escalate instead of assuming

## Behavior Model

- A behavior is a domain-expressed `Given / When / Then` state transition with an observable outcome
- A unit of behavior is the smallest atomic behavior that is still meaningful to a stakeholder or domain expert
- A behavior slice is a planning term for the implementation target of one RED-GREEN-REFACTOR cycle and should normally map to exactly one unit of behavior
- A valid `Then` outcome must be observable in at least one of these ways:
  - return value
  - observable state change
  - outgoing interaction with an external dependency

### Behavior Structure

- `Given` establishes the relevant precondition:
  - current system state
  - responses from incoming dependencies the SUT reads from
- `When` is the single triggering action on the system under test
- `Then` states the observable outcome in domain terms

### Unit Of Behavior Checklist

Treat a candidate as a unit of behavior only if all of these are true:

- It can be described in domain language, not implementation language
- It has a clear precondition
- It has a single trigger
- It produces an observable outcome
- It succeeds or fails atomically from the caller's perspective
- The test should remain valid after internal refactoring

### Small Enough For One Cycle

A behavior is usually small enough for one TDD cycle when:

- It captures one rule, decision, or workflow step
- It does not split a domain outcome across multiple tests just because the code is split
- It does not bundle unrelated domain outcomes into one test
- One RED test can express it clearly through the public API
- One GREEN step can satisfy it without adding speculative behavior

### Naming Heuristic

- If the test name sounds like an implementation detail, it is probably not a behavior
- If the test name reads like a business rule or domain promise, it is probably a behavior

## Cycle Orchestration

Coordinate a strict RED-GREEN-REFACTOR cycle across separate spawned contexts when delegation is authorized. The orchestrator selects the next unit of behavior within the enclosing procedure's authority, invokes the right phase in order, validates each handoff, and ensures the work stays test-first and behavior-preserving.

### Orchestration Model

- One unit of behavior per cycle
- Spawn phases sequentially: RED -> GREEN -> REFACTOR
- Do not overlap phases or run them in parallel
- Require a valid handoff before starting the next phase
- Stop the cycle immediately if any phase escalates ambiguity or unsafe scope

### Process

1. Select the next smallest unit of behavior with a clear observable outcome.
2. Spawn a RED context with only that unit of behavior and relevant local context.
3. Validate the RED handoff against `references/phase-handoffs.md`.
4. Spawn a GREEN context using the RED handoff as the primary input.
5. Validate the GREEN handoff against the same contract.
6. Spawn a REFACTOR context using the GREEN handoff as the primary input.
7. Record the outcome as either:
   - completed cycle with `no refactor needed`, or
   - completed cycle with verified refactoring, or
   - escalated cycle requiring user input
8. Return the cycle report and, within the enclosing procedure's authority, decide whether to start another cycle, wait for a commit boundary, or seek a decision.

### Handoff Validation

Before spawning the next phase, confirm the prior handoff includes:

- `Phase`
- `Behavior`
- `Given`
- `When`
- `Then`
- `Observable outcome type`
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

- The full RED-GREEN-REFACTOR cycle is complete for one unit of behavior
- The handoff chain is preserved from phase to phase
- Any ambiguity or blocked work is surfaced explicitly
- The result is ready for commit or the next cycle

### Cycle Report

For either orchestration or guided pairing, return a compact report on completion or escalation with:

- The unit of behavior and its originating goal or acceptance criterion
- Cycle disposition: completed or escalated, with outcomes for phases performed and those not reached
- Changed files, relevant test identifiers, exact verification commands and results, including required checks not performed or still failing
- Whether refactoring was applied or skipped, and why
- Evidence for the concern obligations assigned to this cycle, and any outstanding work or limitations
- Discoveries affecting other scopes or inherited decisions, unresolved questions, and the decision or action needed from the receiving user or procedure

A completed report establishes only the verified cycle scope. If a required check cannot be completed, report the limitation and escalate rather than claiming completion.

## RED Phase

Execute only the RED phase for one unit of behavior. Define that unit of behavior as a test, run it, confirm it fails for the expected reason, and stop before any production implementation.

### RED Process

1. Identify the next smallest unit of behavior.
2. Write exactly one test that captures that behavior as a `Given / When / Then` state transition through the public API.
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

Execute only the GREEN phase for one unit of behavior. Consume a RED handoff, implement the smallest change that makes the failing test pass, verify the result, and stop before opportunistic cleanup.

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

Execute only the REFACTOR phase for one unit of behavior. Consume a GREEN handoff, assess the code explicitly, improve internals only when that adds value, and verify behavior remains unchanged.

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
- The resulting state is ready for commit or the next unit of behavior

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

### Behavior Discovery

Before proposing the next test, make the behavior explicit:

- `Given` -- what precondition matters here?
- `When` -- what single action triggers the behavior?
- `Then` -- what observable outcome should happen?
- `Outcome type` -- is the proof a return value, state change, or outgoing external interaction?

### Pairing Process

1. **Understand** -- ask what the user wants to build, listen for the problem, users, definition of done, and constraints
2. **Discover the next most important behavior** -- prioritize by value, not convenience
3. **Propose a test** -- present one test case, explain the implied interface, get approval
4. **RED** -- write the test, run it, confirm it fails for the right reason
5. **GREEN** -- write minimum code to pass, run tests to confirm
6. **REFACTOR** -- assess explicitly, improve if warranted, confirm tests still pass
7. **Next** -- return the cycle report, re-evaluate what matters most with the user, and repeat within the agreed scope

### Behavior Priority

When suggesting candidates, rank by value to the core problem:

1. **Core behaviors** -- directly solves the user's problem
2. **Critical paths** -- system fails meaningfully without this
3. **Error handling** -- what happens when expected input is missing
4. **Edge cases** -- unusual but valid scenarios
5. **Nice-to-haves** -- convenience, polish, optimization

Value priority decides what to do next. The behavior model decides whether the candidate is specific enough for one cycle.

### Test Review Rubric

Use this quick rubric to spot tests that drift into implementation detail:

- `Domain phrasing` -- does the test name read like a business rule or user-visible promise?
- `Single trigger` -- does the `When` step trigger one behavior rather than a script of actions?
- `Observable proof` -- does `Then` verify a return value, state change, or outgoing external interaction?
- `Boundary discipline` -- are doubles used to control incoming dependencies or verify outgoing effects, not internal chatter?
- `Refactor resilience` -- would the test still pass if internals were reorganized without changing behavior?

Treat these as warning signs of implementation-detail tests:

- assertions about private methods or internal helper calls
- assertions about call counts on stubs that only provide inputs
- test names that mention mappers, loops, branches, or algorithm steps instead of domain outcomes
- multi-step scenarios that hide multiple behaviors in one example

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

Stop and ask the user or the decision-maker identified in the cycle inputs when:

- The next unit of behavior is not clear enough to write one focused test
- A phase handoff is invalid or incomplete after reasonable correction
- GREEN would require broad API design decisions beyond the slice
- REFACTOR reveals larger pre-existing design issues outside current scope
- Project test infrastructure is too broken to prove RED or GREEN honestly
- The observed failure suggests broken test infrastructure rather than missing behavior
- Discoveries invalidate inherited decisions, affect another scope, or prevent a required cycle-boundary obligation from being met

Return the relevant evidence, affected scope or constraint, and the decision needed. Resume only after the blocker is resolved or an authorized decision establishes revised inputs; revalidate the applicable phase entry conditions rather than skipping them.

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
- [Units of Behavior](references/units-of-behavior.md) -- formal behavior definitions, checklists, and examples for picking the next slice
- [Reviewing Behavior Tests](references/reviewing-behavior-tests.md) -- reviewer rubric for distinguishing domain behavior tests from implementation-detail tests
