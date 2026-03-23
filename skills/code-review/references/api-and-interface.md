# API & Interface

Category 8 -- Are contracts correct and stable?

## Subcategories

- **Incorrect parameter types or order** -- function signature does not match documented or expected contract
- **Breaking API contract** -- change that breaks existing callers without a migration path
- **Missing backward compatibility** -- removing or renaming fields, endpoints, or parameters without versioning
- **Incorrect HTTP methods/status codes** -- using GET for mutations, returning 200 for errors, wrong status semantics
- **Missing versioning** -- API changes deployed without version bumps or deprecation notices
- **Incorrect error response format** -- error responses that do not match the documented or conventional shape
- **Missing rate limiting** -- endpoints exposed without throttling that could be abused
- **Inconsistent response shapes** -- same endpoint returning different shapes depending on conditions
- **Leaky abstractions** -- internal implementation details exposed through the public interface
- **Missing content negotiation** -- API that does not handle `Accept` or `Content-Type` headers correctly

## What to Look For

- Function parameters that changed order or type without updating all callers in the diff
- Public interface changes (exported functions, REST endpoints, GraphQL schema) without corresponding changelog or version bump
- HTTP POST/PUT/PATCH endpoints that do not return the created/updated resource or a consistent response shape
- Error responses that return a plain string instead of a structured error object
- API endpoints without input validation or schema enforcement on request bodies
- Breaking changes to shared types or interfaces that affect other modules
- Optional parameters added to the middle of a positional argument list (should be at the end or in an options object)
- Return type changes that silently alter the contract (e.g. adding `| undefined` to a previously non-optional return)
- GraphQL resolvers that return raw database entities instead of mapped DTOs
- REST endpoints missing standard headers (`Content-Type`, `Cache-Control`, `ETag`)

## Positive Example

```typescript
// Options object pattern -- extensible without breaking callers
interface FetchUsersOptions {
  readonly orgId: string;
  readonly limit?: number;
  readonly cursor?: string;
}

async function fetchUsers(options: FetchUsersOptions): Promise<PaginatedResult<User>> {
  // ...
}
```

Options object allows adding new parameters without changing the function signature.

## Negative Example

```typescript
// BREAKING: added required parameter to existing public function
// All existing callers now have a type error
async function fetchUsers(
  orgId: string,
  limit: number,  // was optional, now required
  cursor: string, // new required parameter
  includeInactive: boolean // new required parameter
): Promise<User[]> {
  // ...
}
```

Adding required positional parameters breaks all existing callers. Return type lost pagination metadata.

## Common False Positives

- Internal (non-exported) function signature changes that are fully accounted for in the same diff
- Breaking changes that are intentional and documented (major version bump, migration guide)
- Error response format differences between different error types (400 vs 500 may legitimately differ)
- Missing rate limiting on internal service-to-service endpoints behind a network boundary

## Severity Guide

| Severity | When |
|---|---|
| Critical | Breaking change to a public API without versioning; removing required fields from responses consumed by external clients |
| Major | Incorrect HTTP status codes on production endpoints; inconsistent error response format; leaky abstraction exposing database schema |
| Minor | Missing pagination metadata; optional parameter ordering preference; missing `Cache-Control` header |
| Nitpick | Naming convention preference for query parameters or response fields |

## Related Categories

- [Security](security.md) -- authentication, authorisation, and rate limiting are API concerns
- [Data Handling](data-handling.md) -- serialization and deserialization issues surface at API boundaries
- [Compatibility](compatibility.md) -- backward compatibility is a cross-cutting concern
- [Documentation](documentation.md) -- API changes require documentation updates
