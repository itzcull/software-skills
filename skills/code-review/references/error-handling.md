# Error Handling

Category 3 -- Does the code fail gracefully?

## Subcategories

- **Missing error handling** -- operations that can fail but have no failure path
- **Swallowed exceptions** -- catch blocks that discard errors silently
- **Incorrect error propagation** -- errors that are caught and re-thrown incorrectly, losing context
- **Missing finally/cleanup blocks** -- resources not released when an error occurs
- **Overly broad catch blocks** -- catching all exceptions when only specific ones are expected
- **Incorrect error messages** -- messages that mislead or expose internal details
- **Missing retry logic** -- transient failures treated as permanent
- **Inconsistent error types** -- mixing error conventions (exceptions, error codes, Result types) within one module
- **Unhandled promise rejections** -- async operations without `.catch()` or try/catch in async functions
- **Error swallowing in callbacks** -- error parameters ignored in callback-style APIs

## What to Look For

- `try/catch` blocks with empty catch bodies or only `console.log`
- Async functions without `try/catch` around awaited operations that can fail
- Promise chains without a terminal `.catch()`
- `catch (e)` that re-throws a new error without wrapping the original (loses stack trace)
- Network calls, file I/O, and database operations without error handling
- `catch` blocks that catch `Error` when they should catch a specific subclass
- Error messages that include raw stack traces, internal paths, or sensitive data
- Functions that return `null` on failure without documenting that convention
- Event listeners that can throw without a surrounding error boundary
- `JSON.parse`, `parseInt`, `new URL()`, and similar parsing operations without guards

## Positive Example

```typescript
async function fetchUser(id: string): Promise<Result<User, FetchError>> {
  try {
    const response = await httpClient.get(`/users/${id}`);
    return ok(UserSchema.parse(response.data));
  } catch (error) {
    if (error instanceof HttpError && error.status === 404) {
      return err(new UserNotFoundError(id));
    }
    return err(new FetchError("Failed to fetch user", { cause: error }));
  }
}
```

Specific error types are caught and mapped to domain errors. The original error is preserved as a cause.

## Negative Example

```typescript
async function fetchUser(id: string): Promise<User | null> {
  try {
    const response = await httpClient.get(`/users/${id}`);
    return response.data;
  } catch (e) {
    // TODO: handle this properly
    return null;
  }
}
```

All errors (network failure, auth error, server error, parse error) collapse into `null`. Callers cannot distinguish "not found" from "network down". The original error is discarded.

## Common False Positives

- Intentionally ignoring errors in best-effort operations (e.g. analytics, logging) where failure is acceptable
- Top-level error boundaries that catch broadly by design (framework error handlers, process-level handlers)
- Functions that return `undefined` as a valid domain value, not as an error signal
- Test code that intentionally triggers and asserts on errors

## Severity Guide

| Severity | When |
|---|---|
| Critical | Missing error handling on data-mutating operations (writes, deletes, financial transactions) |
| Major | Swallowed exceptions hiding real failures; unhandled promise rejections in production paths |
| Minor | Missing error handling on read-only operations; overly broad catch in non-critical code |
| Nitpick | Stylistic preference for error handling approach (Result vs exceptions) in code that handles both |

## Related Categories

- [Logic & Correctness](logic-and-correctness.md) -- missing error paths can produce incorrect behaviour
- [Data Handling](data-handling.md) -- parse errors and type errors are often error handling concerns
- [Resource Management](resource-management.md) -- cleanup on error paths is critical for resource safety
- [Security](security.md) -- error messages can leak sensitive information
