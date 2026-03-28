# Reviewing Behavior Tests

This reference helps reviewers distinguish tests that specify domain behavior from tests that overspecify implementation details.

## Review Goal

Prefer tests that describe stable domain promises over tests that constrain internal structure.

A good behavior test should fail when the promised behavior breaks and stay green when internals are refactored without changing behavior.

## Quick Rubric

Check each test against these questions:

1. `Domain phrasing` -- does the name read like a rule, promise, or user-visible outcome?
2. `Clear precondition` -- does `Given` establish only the facts that matter?
3. `Single trigger` -- does `When` perform one meaningful action?
4. `Observable outcome` -- does `Then` verify a return value, state change, or outgoing external interaction?
5. `Boundary discipline` -- are doubles used only at architectural boundaries?
6. `Refactor resilience` -- would the test survive internal reorganization that preserves behavior?

## Strong Signals Of A Good Behavior Test

- The test can be explained to a stakeholder without translating implementation vocabulary
- The assertion proves an externally visible outcome
- The test exercises the public API
- The setup is minimal and focused on the precondition
- Internal collaborators may change without breaking the test

## Warning Signs Of Implementation-Detail Tests

- The test name mentions helper methods, mapper steps, branch counts, or loop mechanics
- The assertions verify internal call order or internal helper invocation counts
- The test spies on private methods or same-process collaborators that are not external dependencies
- The test breaks after harmless refactoring even though user-visible behavior is unchanged
- The test uses mocks for objects that only supply data to the SUT

## Double Usage Heuristic

Use doubles according to direction of dependency flow:

- Stub incoming dependencies the SUT reads from
- Verify outgoing interactions with external dependencies the SUT writes to
- Do not assert internal chatter between collaborators inside the behavioral unit

When a test fails only because the collaboration pattern changed, the test is probably overspecified.

## Reframing Weak Tests

Weak framing:

- `maps customer status before saving`
- `calls calculateTotal twice`
- `uses repository before publisher`

Stronger framing:

- `persists an approved application with approved status`
- `returns the total charge for all billable items`
- `publishes an order-confirmed event after a successful checkout`

The stronger versions describe domain outcomes. The weaker versions describe one possible implementation.
