# Units of Behavior

This reference defines what a behavior is, what counts as a unit of behavior, and how to decide whether a proposed test is the right size for one TDD cycle.

## Core Definitions

- A behavior is a domain-expressed `Given / When / Then` state transition with an observable outcome.
- A unit of behavior is the smallest atomic behavior that is still meaningful in domain terms.
- A unit of code is a function, class, or module. A unit of behavior is the smallest domain promise worth specifying.
- A behavior slice is the implementation target for one RED-GREEN-REFACTOR cycle and should normally map to one unit of behavior.

## Behavior Structure

Use this model:

- `Given` -- establish the relevant precondition
- `When` -- trigger one action on the system under test
- `Then` -- assert an observable outcome

### Given

`Given` sets up only the precondition that matters to the behavior:

- system state
- incoming dependency responses
- relevant domain facts

Do not treat incidental setup as the behavior itself.

### When

`When` is the single triggering action on the system under test.

- Prefer one call, event, or user action
- If multiple actions are required, the slice is probably too large

### Then

`Then` must be observable in at least one of these ways:

1. Return value
2. Observable state change
3. Outgoing interaction with an external dependency

If the proof is not observable, the test is probably asserting implementation details.

## Unit Of Behavior Criteria

A candidate counts as a unit of behavior only if all of these are true:

- It is describable in domain language, not implementation language
- It has a clear precondition
- It has a single trigger
- It has an observable outcome
- It succeeds or fails atomically from the caller's perspective
- A refactor that preserves behavior should not invalidate the test

## Small Enough For One Cycle

A behavior is usually the right size for one TDD cycle when:

- It captures one rule, decision, or workflow step
- One test can express it clearly through the public API
- One minimal production change can make that test pass
- It does not bundle unrelated domain outcomes
- It does not split one domain outcome across multiple tests purely because the implementation is split

If a proposed test needs multiple `When` steps, multiple unrelated `Then` claims, or broad API design decisions, split it before starting RED.

## Review Checklist

Ask these questions when reviewing a test:

1. Can a stakeholder understand what promise the test describes?
2. Is the test name phrased as a rule, outcome, or domain promise?
3. Does the setup establish only the precondition that matters?
4. Does the action trigger exactly one behavior?
5. Does the assertion verify a return value, state change, or outgoing external effect?
6. Would the test survive internal refactoring that preserves behavior?

## Good And Weak Examples

Good behavior statements:

- Given an account with insufficient funds, when a withdrawal is requested, then the withdrawal is declined
- Given a rejected application, when the decision is finalized, then the applicant is notified
- Given an expired password reset token, when the user submits a new password, then the reset is refused

Weak behavior statements:

- maps field `x` to field `y`
- calls `calculateTotal` twice
- uses the repository before the mapper

The weak examples may describe real implementation details, but they do not describe domain behavior.

## Practical Heuristic

- If the test name sounds like implementation detail, it is probably not a unit of behavior
- If the test name reads like a business rule or domain promise, it probably is
