# Performance

Category 6 -- Is the code efficient enough?

## Subcategories

- **Algorithmic inefficiency** -- O(n^2) or worse where O(n) or O(n log n) is feasible
- **Unnecessary computation** -- recalculating values that could be cached or memoised
- **N+1 queries** -- fetching related records one at a time in a loop instead of batching
- **Missing caching** -- repeated expensive operations without caching the result
- **Memory leaks** -- references retained beyond their useful lifetime preventing garbage collection
- **Excessive object allocation** -- creating objects in hot loops that pressure the garbage collector
- **Blocking I/O in async context** -- synchronous file/network operations in an async runtime
- **Unoptimised data structures** -- linear search where a hash lookup would serve; array where a set would be appropriate
- **Missing pagination** -- loading unbounded result sets into memory
- **Unnecessary re-renders** -- React components re-rendering when their inputs have not changed
- **Bundle size impact** -- importing large libraries for trivial operations

## What to Look For

- Nested loops over the same or related collections (potential O(n^2))
- Database queries inside loops -- especially ORM lazy-loading in iteration
- `Array.find` or `Array.includes` in a loop where a `Set` or `Map` lookup would be O(1)
- Large arrays sorted repeatedly when a sorted insertion or priority queue would suffice
- `JSON.parse(JSON.stringify(obj))` for deep cloning (slow, loses non-JSON types)
- `fs.readFileSync`, `execSync`, or other sync I/O in server request handlers
- React components missing `useMemo`, `useCallback`, or `React.memo` where props are stable but expensive to compute
- Fetching entire database tables without `LIMIT` or pagination
- String concatenation in loops (build an array and join instead)
- Regular expressions with catastrophic backtracking patterns (nested quantifiers)
- Importing an entire utility library (`lodash`) for a single function available natively

## Positive Example

```typescript
function findDuplicates(items: string[]): string[] {
  const seen = new Set<string>();
  const duplicates = new Set<string>();
  for (const item of items) {
    if (seen.has(item)) duplicates.add(item);
    else seen.add(item);
  }
  return [...duplicates];
}
```

O(n) with Set lookups. Single pass through the data.

## Negative Example

```typescript
// PERF: O(n^2) -- indexOf is O(n) called n times
function findDuplicates(items: string[]): string[] {
  return items.filter((item, index) => items.indexOf(item) !== index);
}
```

`indexOf` scans from the start on every iteration. Quadratic on large inputs.

## Common False Positives

- O(n^2) on collections that are guaranteed small (< 20 elements) -- the constant factor of a more complex algorithm may be worse
- Missing memoisation in code that runs once or rarely
- Sync I/O during application startup or CLI tools (not in request handlers)
- Creating objects in loops when the loop iteration count is small and bounded
- React re-renders that are cheap (simple components with no expensive children)

## Severity Guide

| Severity | When |
|---|---|
| Critical | N+1 queries or O(n^2) on unbounded user-controlled input in a hot path; memory leak in a long-running process |
| Major | Missing pagination on database queries; blocking I/O in server request handlers; quadratic algorithm on large but bounded data |
| Minor | Suboptimal data structure choice in non-critical code; missing memoisation in occasionally-called code |
| Nitpick | Micro-optimisation with negligible real-world impact |

## Related Categories

- [Logic & Correctness](logic-and-correctness.md) -- algorithmic errors can be both correctness and performance issues
- [Data Handling](data-handling.md) -- incorrect data structure choice overlaps both categories
- [Concurrency & Timing](concurrency-and-timing.md) -- event loop blocking is both a concurrency and performance concern
- [Resource Management](resource-management.md) -- memory leaks bridge performance and resource management
