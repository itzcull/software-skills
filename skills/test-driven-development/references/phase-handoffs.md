# TDD Phase Handoffs

This reference defines the contract between spawned TDD phase contexts. Each phase receives a focused handoff, performs only its own work, and returns a handoff for the next phase.

## Operating Model

- One behavior slice per cycle
- One spawned context per phase: RED, then GREEN, then REFACTOR
- Phases run sequentially, not in parallel
- Each phase may read broader context, but it must only change what its phase allows
- Every handoff must be short, concrete, and executable

## Shared Rules

- TDD is non-negotiable: no production code without a failing test first
- Tests specify behavior, not implementation details
- Each phase stops as soon as its exit criteria are met
- No phase may smuggle in work that belongs to another phase
- If the phase cannot proceed safely without guessing, escalate instead of assuming

## Handoff Template

```md
## TDD Phase Handoff

Phase: <red | green | refactor>
Behavior: <single unit of behavior in domain terms>
Given: <relevant precondition>
When: <single trigger>
Then: <observable outcome>
Observable outcome type: <return value | state change | outgoing external interaction>
Test level: <unit | integration | e2e>

Scope:
- Test file: <path>
- Production file(s): <path list>
- Test name: <exact test or describe block>
- Public API under change: <function/module/component>

Evidence:
- Command: <exact command>
- Result: <failed | passed>
- Key reason: <why it failed or passed>

Constraints:
- <phase-specific constraints>

Open questions:
- <none> or <targeted unresolved issue>

Next prompt:
- <concise prompt for the next spawned context>
```

## Phase Boundaries

### RED

Allowed:

- Add or adjust exactly one test for the next behavioral increment
- Add or adjust test data factories if demanded by that test
- Run focused tests to prove the new test fails for the right reason

Forbidden:

- Production code changes
- Multiple new behaviors in one test batch
- Leaving the test failing for setup, syntax, or unrelated reasons

Exit criteria:

- One new behavior is expressed in a test
- The test fails for the expected behavioral reason
- Previously passing tests in scope still pass, or any broader failures are explained
- The behavior is explicit as `Given / When / Then`

### GREEN

Allowed:

- The smallest production change that makes the red test pass
- Small test fixes only if the red test itself was malformed
- Focused verification to prove the behavior is now green

Forbidden:

- Extra features not demanded by the failing test
- Opportunistic cleanup or structural improvements
- New public API surface unless the test explicitly requires it

Exit criteria:

- The previously failing test now passes
- The implementation is intentionally minimal
- No unrelated behavior has been added

### REFACTOR

Allowed:

- Internal cleanup that preserves external behavior
- Naming, extraction, simplification, and duplication removal when justified
- Broader verification across tests, lint, and typecheck where available

Forbidden:

- Behavior changes
- New tests for new behavior
- Public API changes unless preserving compatibility demands a safe internal adapter

Exit criteria:

- Refactoring assessment is explicit
- Either useful refactoring is complete and verified, or an explicit "no refactor needed" decision is returned
- All relevant checks are green after changes

## Refactoring Priority

Classify findings before changing code:

- Critical: fix now before ending the session
- High value: fix this session if the value is clear
- Nice to have: defer unless the cleanup is tiny and obvious
- Skip: code is already clear enough

Use these checks:

1. Naming clarity
2. Magic values
3. Structural complexity
4. Knowledge duplication
5. Purity and immutability

## Escalation Triggers

Stop and escalate when:

- The next behavior is ambiguous
- The behavior cannot be stated clearly as `Given / When / Then`
- The failing test implies multiple valid public APIs
- A green implementation appears to require unrelated behavior
- Refactoring would spill outside the agreed slice
- The observed failure suggests broken test infrastructure rather than missing behavior
