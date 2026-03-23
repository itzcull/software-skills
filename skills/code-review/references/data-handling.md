# Data Handling

Category 2 -- Is data used safely and correctly?

## Subcategories

- **Null/undefined dereference** -- accessing properties on a value that may be null or undefined
- **Uninitialized variables** -- using a variable before it has been assigned a value
- **Incorrect type usage** -- using a value as the wrong type without validation
- **Buffer overflow/underflow** -- reading or writing beyond allocated bounds
- **Incorrect data structure choice** -- using a structure that does not fit the access pattern
- **Data loss through truncation** -- narrowing a value and losing precision or information
- **Incorrect serialization/deserialization** -- data shape mismatch between encode and decode
- **Stale data** -- using a cached or previously fetched value that may be outdated
- **Encoding errors** -- incorrect character encoding, byte order, or escaping

## What to Look For

- Optional chaining (`?.`) missing where a value could be null/undefined
- Object property access without checking if the object exists
- Array indexing without bounds checking
- Type narrowing that does not cover all union variants
- `JSON.parse` without try/catch or schema validation
- Floating-point comparisons using `===` instead of epsilon-based comparison
- String-to-number conversions without handling `NaN`
- Date operations without timezone awareness
- Map/Set operations assuming reference equality on object keys
- Destructuring with default values that mask upstream null/undefined problems
- Passing user input directly to functions expecting validated data

## Positive Example

```typescript
function getUserName(response: unknown): string {
  const parsed = UserResponseSchema.parse(response);
  return parsed.user.name;
}
```

Schema validation at the trust boundary ensures downstream code operates on known-good data.

## Negative Example

```typescript
// BUG: response.data could be undefined; response.data.user could be null
function getUserName(response: ApiResponse): string {
  return response.data.user.name;
}
```

No null checks on potentially absent nested properties. A runtime `TypeError: Cannot read properties of undefined` is likely.

## Common False Positives

- Optional chaining on a value that the type system guarantees is present (strict TypeScript with no `any` leaks)
- Non-null assertion (`!`) on a value that has been validated on the previous line (though this is still a smell)
- Array index access in a loop that is already bounded by `array.length`
- Intentional use of `undefined` as a sentinel value with clear handling downstream

## Severity Guide

| Severity | When |
|---|---|
| Critical | Null dereference in production path that will crash; data truncation that loses financial or user data |
| Major | Unsafe deserialization that could corrupt state; missing type validation at a trust boundary |
| Minor | Using a less optimal data structure; missing optional chaining in rarely-reached code |
| Nitpick | Preferring one safe access pattern over another equivalent one |

## Related Categories

- [Logic & Correctness](logic-and-correctness.md) -- type coercion errors overlap both categories
- [Security](security.md) -- unsanitized data handling is a security concern
- [Error Handling](error-handling.md) -- missing null checks are also a form of missing error handling
- [API & Interface](api-and-interface.md) -- serialization issues often surface at API boundaries
