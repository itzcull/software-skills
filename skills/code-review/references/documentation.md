# Documentation

Category 12 -- Is intent captured where needed?

## Subcategories

- **Missing function/class documentation** -- public API without any description of purpose, parameters, or return value
- **Outdated comments** -- comments that describe what the code used to do, not what it does now
- **Commented-out code** -- code blocks preserved in comments instead of being removed (use version control)
- **Missing README updates** -- new features or changed behaviour without corresponding documentation updates
- **Incorrect API documentation** -- JSDoc, OpenAPI, or README that contradicts the implementation
- **Missing changelog entry** -- notable user-facing changes without a changelog or release note
- **Comments explaining "what" instead of "why"** -- restating the code in English rather than explaining intent
- **Missing inline context for non-obvious decisions** -- tricky workarounds or business rules without explanation
- **TODO/FIXME/HACK without context** -- markers without an explanation or a tracking reference
- **Missing type documentation** -- complex types or interfaces without descriptions of fields

## What to Look For

- Public functions with complex signatures but no JSDoc or docstring
- Comments that paraphrase the next line of code (`// increment counter` before `counter++`)
- Comments that reference ticket numbers, dates, or names without explaining the actual constraint
- Commented-out code blocks (should be deleted and recovered from version control if needed)
- `TODO` comments without an associated issue link or explanation of when the work should happen
- Changed function signatures where the JSDoc has not been updated to match
- New configuration options without documentation in the README or config reference
- Non-obvious regular expressions without a comment explaining what they match
- Business rules embedded in code without referencing the business requirement
- Workarounds for framework bugs or external service quirks without a link to the upstream issue

## Positive Example

```typescript
/**
 * Calculates the pro-rated refund amount based on the remaining days
 * in the billing period. Uses calendar days, not business days, per
 * the billing policy established in BILLING-234.
 */
function calculateRefund(
  subscription: Subscription,
  cancellationDate: Date,
): Money {
  // Calendar days remaining, not business days (intentional per policy)
  const remainingDays = differenceInCalendarDays(
    subscription.periodEnd,
    cancellationDate,
  );
  // ...
}
```

The docstring explains the business rule. The inline comment clarifies a choice that might otherwise be "corrected" by a reviewer.

## Negative Example

```typescript
// get the user
const user = getUser(id);
// check if user exists
if (!user) {
  // throw error
  throw new Error("not found");
}
// TODO: fix this later
const result = user.balance * 0.15;
```

Every comment restates the code. The TODO has no context. The magic number `0.15` has no explanation.

## Common False Positives

- Self-documenting code that genuinely does not need comments (clear function name, clear variable names, simple logic)
- Internal utility functions with obvious purpose that do not need JSDoc
- Missing documentation on code that is about to be replaced or is part of a spike/prototype
- Test files where the test name and structure serve as the documentation

## Severity Guide

| Severity | When |
|---|---|
| Critical | Incorrect API documentation that will cause callers to use the API wrong |
| Major | Missing documentation on a public API consumed by external teams; outdated comments that actively mislead |
| Minor | Missing comments on non-obvious business logic; TODO without context; missing README update for internal tools |
| Nitpick | Missing docs on simple internal functions; stylistic preferences for documentation format |

## Related Categories

- [Naming & Readability](naming-and-readability.md) -- good naming reduces the need for documentation
- [API & Interface](api-and-interface.md) -- API documentation is critical for contract stability
- [Code Structure & Organisation](code-structure-and-organisation.md) -- commented-out code is also a structural concern (dead code)
