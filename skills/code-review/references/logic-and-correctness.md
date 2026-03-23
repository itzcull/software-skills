# Logic & Correctness

Category 1 -- Does the code behave as intended?

## Subcategories

- **Incorrect conditional logic** -- wrong boolean operator, inverted condition, missing branch
- **Off-by-one errors** -- loop bounds, array indexing, range calculations
- **Wrong operator** -- arithmetic, comparison, bitwise, or logical operator errors
- **Incorrect algorithm** -- fundamentally wrong approach to solving the problem
- **Unreachable code paths** -- dead branches that can never execute
- **Incorrect return values** -- function returns the wrong value or type for a given input
- **Infinite loops** -- loop termination condition that can never be satisfied
- **Incorrect type coercion** -- implicit conversions that change semantic meaning
- **Short-circuit evaluation errors** -- relying on evaluation order incorrectly
- **State machine errors** -- missing transitions, unreachable states, incorrect terminal states

## What to Look For

- Conditional expressions that do not match the stated intent (comments, function name, variable name)
- Boundary conditions: first element, last element, empty collection, single element, maximum value
- Loops where the index starts at 0 vs 1, or uses `<` vs `<=`
- Boolean expressions with mixed `&&` and `||` without explicit grouping
- Switch/match statements missing a default or exhaustive case
- Early returns that skip necessary cleanup or state updates
- Comparisons between different types without explicit conversion
- Ternary expressions where the true/false branches are swapped
- Regex patterns that are subtly wrong (greedy vs lazy, missing anchors, incorrect character classes)
- Functions that return different shapes depending on code path (e.g. sometimes an object, sometimes undefined)

## Positive Example

```typescript
function clamp(value: number, min: number, max: number): number {
  if (value < min) return min;
  if (value > max) return max;
  return value;
}
```

Boundaries are correct: values exactly equal to min or max pass through unchanged.

## Negative Example

```typescript
// BUG: off-by-one -- excludes the last element
function lastN(items: string[], n: number): string[] {
  return items.slice(items.length - n, items.length - 1);
}
```

`slice` end index is exclusive, so this drops the final element. Should be `items.slice(items.length - n)` or `items.slice(-n)`.

## Common False Positives

- Code that looks like it has an off-by-one but is correct for a 0-indexed vs 1-indexed context
- Conditions that appear inverted but are intentionally written for early-return guard clause style
- Seemingly unreachable code that serves as a defensive fallback (TypeScript exhaustive checks, assertion branches)
- Implicit type coercion that is intentional and idiomatic (e.g. `!!value` for boolean conversion)

## Severity Guide

| Severity | When |
|---|---|
| Critical | Logic error in a hot path, data mutation path, or financial calculation |
| Major | Logic error that affects correctness but in a less critical code path |
| Minor | Edge case that is unlikely to be hit in practice |
| Nitpick | Technically imprecise but functionally equivalent in context |

## Related Categories

- [Data Handling](data-handling.md) -- incorrect type usage often manifests as logic errors
- [Error Handling](error-handling.md) -- missing error paths are a form of incorrect logic
- [Testing](testing.md) -- logic errors are caught by testing; missing tests for edge cases belong there
