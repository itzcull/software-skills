# Concurrency & Timing

Category 5 -- Is the code safe under concurrent access?

## Subcategories

- **Race conditions** -- outcome depends on the timing of concurrent operations
- **Deadlocks** -- two or more operations waiting for each other indefinitely
- **Missing synchronisation** -- shared mutable state accessed without coordination
- **Incorrect lock scope** -- lock held too long (contention) or too short (missed protection)
- **Thread-unsafe shared state** -- global or module-level mutable state accessed from concurrent contexts
- **Incorrect atomic operations** -- check-then-act patterns that are not atomic
- **Missing timeout handling** -- operations that can hang indefinitely without a timeout
- **Event loop blocking** -- synchronous CPU-intensive work blocking the Node.js/browser event loop
- **Callback ordering assumptions** -- assuming callbacks execute in a specific order without guarantees
- **Double execution** -- event handlers or effects that fire more than expected

## What to Look For

- Read-modify-write sequences on shared state without locks or atomic operations
- Check-then-act patterns (e.g. "if file exists, then read file" without atomic open)
- Global or module-level `let` variables modified by async functions or request handlers
- Missing `await` on async operations that should complete before the next line
- `Promise.all` used where one rejection should not cancel sibling operations (should be `Promise.allSettled`)
- `setTimeout` or `setInterval` without cleanup on component unmount or server shutdown
- Database read followed by conditional write without a transaction or optimistic locking
- Missing `AbortController` or timeout on `fetch` calls and external service requests
- React `useEffect` missing cleanup for subscriptions, timers, or async operations
- Event listeners registered multiple times without deregistration
- Concurrent HTTP requests that modify the same resource without idempotency keys

## Positive Example

```typescript
async function transferFunds(
  fromId: string,
  toId: string,
  amount: number
): Promise<void> {
  await db.transaction(async (tx) => {
    const from = await tx.account.findUnique({ where: { id: fromId } });
    if (from.balance < amount) throw new InsufficientFundsError();
    await tx.account.update({ where: { id: fromId }, data: { balance: { decrement: amount } } });
    await tx.account.update({ where: { id: toId }, data: { balance: { increment: amount } } });
  });
}
```

Database transaction ensures atomicity. Read and writes happen within the same isolation boundary.

## Negative Example

```typescript
// BUG: race condition -- balance check and deduction are not atomic
async function transferFunds(fromId: string, toId: string, amount: number): Promise<void> {
  const from = await db.account.findUnique({ where: { id: fromId } });
  if (from.balance < amount) throw new InsufficientFundsError();
  // Another request could modify the balance between these two operations
  await db.account.update({ where: { id: fromId }, data: { balance: { decrement: amount } } });
  await db.account.update({ where: { id: toId }, data: { balance: { increment: amount } } });
}
```

The check and the deduction are separate operations. A concurrent request could drain the balance between them.

## Common False Positives

- Module-level `const` bindings that are initialised once at startup and never mutated
- Async operations that are intentionally fire-and-forget (logging, analytics)
- React state updates that appear racy but are batched by the framework
- Server-side code in environments that process requests sequentially (single-threaded workers with no shared state)

## Severity Guide

| Severity | When |
|---|---|
| Critical | Race condition on financial or data-integrity operations; deadlock potential in production |
| Major | Missing timeout on external service calls; event loop blocking in a server |
| Minor | Missing `AbortController` cleanup; theoretically possible but unlikely race in low-traffic code |
| Nitpick | Preferring one concurrency pattern over another equivalent one |

## Related Categories

- [Logic & Correctness](logic-and-correctness.md) -- race conditions produce incorrect logic under load
- [Resource Management](resource-management.md) -- deadlocks and missing timeouts are resource concerns
- [Performance](performance.md) -- lock contention and event loop blocking are performance concerns
- [Error Handling](error-handling.md) -- missing timeout handling is an error handling gap
