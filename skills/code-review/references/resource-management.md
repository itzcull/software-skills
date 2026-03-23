# Resource Management

Category 7 -- Are resources properly acquired and released?

## Subcategories

- **Unclosed connections** -- database connections, HTTP connections, WebSocket connections not closed after use
- **Unclosed file handles/streams** -- files or streams opened but never closed, especially on error paths
- **Missing cleanup in error paths** -- resources acquired before an error but not released in the catch/finally
- **Resource exhaustion** -- unbounded resource acquisition that can exhaust system limits
- **Missing connection pooling** -- creating new connections per request instead of reusing from a pool
- **Improper lifecycle management** -- resources not tied to the lifecycle of their owner (component, request, process)
- **Missing graceful shutdown** -- process termination without closing open connections and flushing buffers
- **Subscription leaks** -- event emitter or observable subscriptions without corresponding unsubscription
- **Timer leaks** -- `setInterval` or `setTimeout` without cleanup

## What to Look For

- File operations (`fs.open`, `fs.createReadStream`) without corresponding close in both success and error paths
- Database connections obtained but not returned to the pool, especially in error branches
- `new AbortController()` created but never aborted on cleanup
- React `useEffect` that creates subscriptions, timers, or listeners without returning a cleanup function
- Express/Koa middleware that acquires resources but does not release them if `next()` throws
- `child_process.spawn` without handling process exit and stream cleanup
- WebSocket connections opened in loops or event handlers without tracking or limiting
- Event listeners added with `addEventListener` or `.on()` without corresponding removal
- Temporary files created but never deleted
- `setInterval` without `clearInterval` on component unmount or server shutdown

## Positive Example

```typescript
async function processFile(path: string): Promise<Result> {
  const handle = await fs.open(path, "r");
  try {
    const content = await handle.readFile("utf-8");
    return processContent(content);
  } finally {
    await handle.close();
  }
}
```

`finally` ensures the file handle is closed regardless of success or failure.

## Negative Example

```typescript
// BUG: file handle leaked on error
async function processFile(path: string): Promise<Result> {
  const handle = await fs.open(path, "r");
  const content = await handle.readFile("utf-8");
  const result = processContent(content); // if this throws, handle is never closed
  await handle.close();
  return result;
}
```

If `processContent` throws, the file handle is never closed. Over time this exhausts file descriptors.

## Common False Positives

- Short-lived CLI scripts where the process exits immediately and the OS reclaims all resources
- Resources managed by a framework's lifecycle (e.g. Prisma client managed by NestJS module lifecycle)
- `useEffect` without cleanup when the effect runs once on mount and the component lives for the entire application lifetime
- Database connections in serverless functions where the runtime manages connection lifecycle

## Severity Guide

| Severity | When |
|---|---|
| Critical | Connection or handle leak in a hot path of a long-running server; missing graceful shutdown on a production service |
| Major | Resource leak on error paths; missing cleanup in `useEffect` for frequently mounted/unmounted components |
| Minor | Missing cleanup in rarely-triggered code paths; timer not cleared for a component that unmounts once |
| Nitpick | Stylistic preference for resource management approach (explicit close vs using-block pattern) |

## Related Categories

- [Error Handling](error-handling.md) -- resource cleanup on error paths bridges both categories
- [Concurrency & Timing](concurrency-and-timing.md) -- deadlocks are a form of resource management failure
- [Performance](performance.md) -- memory leaks and exhaustion degrade performance
- [Configuration & Build](configuration-and-build.md) -- connection pool configuration is a config concern
