---
name: twelve-factor
description: Twelve-Factor App methodology for building deployable software-as-a-service applications. Use when configuring environment variables, connecting to backing services, structuring startup/shutdown, handling process signals, setting up CI/CD pipelines, or auditing deployment readiness. Core factors (config, dependencies, backing services, logs) apply to any deployed application. Server-specific factors (port binding, concurrency, disposability) apply to backend services.
license: MIT
compatibility: opencode
metadata:
  source: https://12factor.net
  author: Adam Wiggins (methodology), adapted for TypeScript/Node.js
---

## Purpose

Provide actionable guidance for building twelve-factor compliant applications. This skill covers all 12 factors with principles drawn directly from [12factor.net](https://12factor.net), accompanied by TypeScript code patterns, anti-patterns, and a verification checklist.

Core factors (config, dependencies, backing services, logs) apply to any deployed application -- services, frontends, workers, CLI tools. Server-specific factors (port binding, concurrency, disposability) apply only to backend services that run as long-lived processes.

## When to Apply

- **Greenfield projects**: All 12 factors are mandatory. Structure the application to follow every applicable factor from the start.
- **Brownfield projects**: Adopt incrementally in this priority order:
  1. **Config** (Factor III) -- add env var validation without restructuring
  2. **Logs** (Factor XI) -- switch to structured stdout logging
  3. **Disposability** (Factor IX) -- add graceful shutdown handlers
  4. **Backing services** (Factor IV) -- abstract connections behind config URLs
  5. **Stateless processes** (Factor VI) -- migrate in-memory state to backing services

---

## I. Codebase

> One codebase tracked in revision control, many deploys.

There is always a one-to-one correlation between a codebase and an app:

- **Multiple codebases** = not an app, it is a distributed system. Each component is its own app.
- **Multiple apps sharing the same code** = a violation. Factor shared code into libraries managed through the package manager.

There will be many deploys (production, staging, developer environments) but they all share the same codebase. Different versions may be active in each deploy.

**In a monorepo**, each service must have its own entry point, its own deploy pipeline, and its own set of backing service connections. A single repo is acceptable as long as each service deploys independently.

**Code-level implications:**
- Shared utilities between services become packages published to a registry or workspace-linked via the package manager
- No copy-pasting code between services -- extract to a library
- Each deployable unit has exactly one `package.json` (or equivalent manifest)

---

## II. Dependencies

> Explicitly declare and isolate dependencies.

A twelve-factor app never relies on implicit existence of system-wide packages. Two requirements must be met together -- one without the other is insufficient:

1. **Declaration** -- all dependencies declared completely and exactly in a manifest (`package.json`)
2. **Isolation** -- a dependency isolation tool ensures no implicit dependencies leak in from the surrounding system (`node_modules`, not global installs)

```typescript
import which from 'which';

export const checkSystemDependencies = (required: readonly string[]) => {
  const missing = required.filter((cmd) => !which.sync(cmd, { nothrow: true }));
  if (missing.length > 0) {
    throw new Error(`Missing required system dependencies: ${missing.join(', ')}`);
  }
};
```

**Rules:**
- Every dependency in `package.json` with exact or pinned ranges
- Lockfile (`package-lock.json`, `pnpm-lock.yaml`, `bun.lock`) committed to the repo
- Dependencies are isolated -- the app uses `node_modules`, not global installs. Never `npm install -g` for app dependencies.
- No `exec('imagemagick ...')` or `child_process` calls to assumed system tools
- If a system tool is genuinely required, document it explicitly and verify at startup (see example above)
- The full dependency specification applies uniformly to both production and development

**Anti-patterns:**
```typescript
// Assuming a global tool exists
import { execSync } from 'child_process';
execSync('convert input.png output.jpg'); // ImageMagick assumed

// Using globally installed packages
// npm install -g some-tool  <-- not declared in package.json
```

---

## III. Config

> Store config in the environment.

Config is everything that varies between deploys: resource handles, credentials, per-deploy hostnames. This does NOT include internal application config like route definitions or module wiring -- those belong in code.

**The litmus test:** could the codebase be made open source right now without compromising any credentials?

**Env vars must be granular and orthogonal.** Never group them into named "environments" (`development`, `staging`, `production`). Each var is independently managed for each deploy. This scales smoothly as the app expands into more deploys -- no combinatorial explosion of environment names.

**Validate config at startup with a schema. Fail fast if invalid:**

```typescript
import { z } from 'zod';

const ConfigSchema = z.object({
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  API_URL: z.string().url(),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  API_KEY: z.string().min(1),
  SENTRY_DSN: z.string().url().optional(),
  ALLOWED_ORIGINS: z
    .string()
    .default('')
    .transform((s) => (s === '' ? [] : s.split(','))),
});

type Config = z.infer<typeof ConfigSchema>;

export const createConfig = (
  env: Record<string, string | undefined> = process.env,
): Config => {
  const result = ConfigSchema.safeParse(env);
  if (!result.success) {
    console.error(
      JSON.stringify({
        level: 'error',
        message: 'Invalid config',
        errors: result.error.flatten(),
      }),
    );
    process.exit(1);
  }
  return result.data;
};
```

**Inject config via options objects -- never import `process.env` deep in the call tree:**

```typescript
const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});
type User = z.infer<typeof UserSchema>;

export const createUserService = ({
  config,
}: {
  config: Pick<Config, 'API_URL'>;
}) => ({
  async getUser(id: string): Promise<User> {
    const response = await fetch(`${config.API_URL}/users/${id}`);
    if (!response.ok) throw new Error(`Failed to fetch user: ${response.status}`);
    const data: unknown = await response.json();
    return UserSchema.parse(data);
  },
});
```

**Provide `.env.example` as documentation (never `.env` with real values):**

```
PORT=3000
DATABASE_URL=postgres://localhost:5432/myapp
REDIS_URL=redis://localhost:6379
API_URL=http://localhost:8080
LOG_LEVEL=info
API_KEY=your-api-key-here
SENTRY_DSN=
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Config Anti-Patterns

```typescript
// Hardcoded connection string
const DB_HOST = 'prod-db.internal.example.com';

// Environment-name branching -- creates combinatorial explosion
if (process.env.NODE_ENV === 'production') {
  connectTo('prod-db');
} else {
  connectTo('localhost');
}

// Config files grouped by environment name
const config = require(`./config.${process.env.NODE_ENV}.json`);

// Scattered process.env access deep in the codebase
export const fetchUser = async (id: string) => {
  const res = await fetch(`${process.env.API_URL}/users/${id}`); // buried env access
  // ...
};
```

**Why these are wrong:** Config that varies by deploy belongs in env vars, not code. Environment-name branching creates a combinatorial explosion and breaks dev/prod parity. Scattered `process.env` access makes config invisible and untestable -- centralise it at startup and inject via options objects.

---

## IV. Backing Services

> Treat backing services as attached resources.

A backing service is any service the app consumes over the network: databases, caches, queues, SMTP, object storage, third-party APIs. **The code makes no distinction between local and third-party services.** Both are attached resources, accessed via a URL or credentials stored in config.

A deploy should be able to swap a local PostgreSQL for a managed cloud database, or a local SMTP server for a third-party service, with only a config change -- never a code change.

```typescript
export const createApp = ({
  config,
}: {
  config: Pick<Config, 'DATABASE_URL' | 'REDIS_URL'>;
}) => {
  const db = createDbPool({ connectionString: config.DATABASE_URL });
  const cache = createRedisClient({ url: config.REDIS_URL });

  return {
    db,
    cache,
    async shutdown() {
      await Promise.all([db.end(), cache.quit()]);
    },
  } as const;
};
```

**Each distinct backing service is a resource.** Two MySQL databases used for sharding are two distinct resources -- two config URLs, not one URL with logic.

Resources can be attached and detached from deploys at will. Swapping a misbehaving database for a restored backup requires only changing the config URL, not touching code.

---

## V. Build, Release, Run

> Strictly separate build and run stages.

A codebase becomes a deploy through three stages:

1. **Build** -- converts a code repo at a specific commit into an executable bundle. Fetches dependencies, compiles, packages assets.
2. **Release** -- combines the build with the deploy's config. Ready for execution.
3. **Run** -- launches processes against a selected release.

**Releases are immutable and append-only.** Every release has a unique ID (timestamp like `2024-01-15T14:32:00Z` or incrementing like `v142`). A release cannot be mutated once created. Any change creates a new release.

It is impossible to make changes to code at runtime -- there is no way to propagate those changes back to the build stage. The run stage should have as few moving parts as possible.

**Code-level implications:**
- No environment-specific build outputs -- the same build artifact deploys to every environment
- Config comes from env vars at runtime, not from compile-time substitution
- No `process.env.NODE_ENV` checks that change compiled output
- Build scripts and CI pipelines produce a single artifact; config is injected at release/run time

---

## VI. Processes

> Execute the app as one or more stateless processes.

**Twelve-factor processes are stateless and share-nothing.** Any data that must persist lives in a backing service.

The process memory space or filesystem can be used as a brief, single-transaction cache (e.g., download a large file, process it, store results in the database). But the app never assumes anything cached in memory or on disk will be available on a future request -- a different process may serve it, or a restart may wipe local state.

**Sticky sessions are a violation.** Session state belongs in a backing service with time-expiration (Redis, Memcached).

```typescript
export const createSessionStore = <T>({
  redis,
  schema,
}: {
  redis: RedisClient;
  schema: z.ZodType<T>;
}) => ({
  async get(sessionId: string): Promise<T | undefined> {
    const data = await redis.get(`session:${sessionId}`);
    return data ? schema.parse(JSON.parse(data)) : undefined;
  },
  async set({
    sessionId,
    data,
    ttlSeconds,
  }: {
    sessionId: string;
    data: T;
    ttlSeconds: number;
  }) {
    await redis.setex(`session:${sessionId}`, ttlSeconds, JSON.stringify(data));
  },
});
```

### Stateless Anti-Patterns

```typescript
// In-memory sessions -- lost on restart, invisible to other instances
const sessions = new Map<string, UserSession>();

// Local filesystem state -- cannot be shared across processes
app.post('/upload', (req, res) => {
  fs.writeFileSync(`/tmp/uploads/${req.file.name}`, req.file.data);
});

// Module-level mutable counter -- different per process instance
let requestCount = 0;
app.use(() => { requestCount++; });

// In-process scheduler -- runs in only one instance
setInterval(() => sendReport(), 60_000);
```

**Why these are wrong:** In-memory state is lost on restart and invisible to other instances. Local filesystem state cannot be shared. In-process schedulers run in only one instance. Use backing services (Redis, S3, database) and external schedulers instead.

---

## VII. Port Binding

> Export services via port binding.

The twelve-factor app is completely self-contained. It does not rely on runtime injection of a web server (e.g., a separate Apache/Nginx process serving the app). The app **exports HTTP as a service by binding to a port** and listening to requests coming in on that port.

```typescript
const server = app.listen(config.PORT, () => {
  logger.info('Server started', { port: config.PORT });
});
```

The app includes its own HTTP server library as a dependency. In deployment, a routing layer handles routing requests from a public-facing hostname to the port-bound process.

Note: the port-binding approach means one app can become the backing service for another app, by providing its URL as a resource handle in the consuming app's config.

---

## VIII. Concurrency

> Scale out via the process model.

**Processes are a first-class citizen.** The developer architects the app to handle diverse workloads by assigning each type of work to a process type: HTTP requests to a web process, background tasks to a worker process.

The share-nothing, horizontally partitionable nature of twelve-factor processes means adding more concurrency is a simple and reliable operation.

```typescript
// web.ts -- handles HTTP requests
const config = createConfig();
const app = createApp({ config });
await startServer({ app, config });

// worker.ts -- processes background jobs
const config = createConfig();
const queue = createQueueConsumer({ url: config.REDIS_URL });
await queue.process('email', sendEmail);
await queue.process('report', generateReport);
```

**Process types are defined declaratively:**

```
# Procfile
web: node dist/web.js
worker: node dist/worker.js
```

**Rules:**
- Separate entry points for each process type (web, worker, scheduler)
- HTTP handlers dispatch background work to a queue, never process it inline
- Each process type scales independently
- **Never daemonize or write PID files.** Rely on the operating system's process manager (systemd, container orchestrator, Foreman in development) to manage output streams, respond to crashes, and handle restarts and shutdowns.

---

## IX. Disposability

> Maximize robustness with fast startup and graceful shutdown.

Twelve-factor processes are disposable -- they can be started or stopped at a moment's notice. This facilitates fast elastic scaling, rapid deployment, and robust production operation.

### Fast Startup

Minimise startup time. A process should take a few seconds from launch command to ready-to-serve. Short startup enables agile releases and allows the process manager to move processes easily.

### Graceful Shutdown

Processes shut down gracefully on **SIGTERM**:
- Web processes stop listening on the port (refuse new requests), allow in-flight requests to finish, then exit
- Worker processes return the current job to the queue, so it can be retried by another worker

```typescript
const SHUTDOWN_TIMEOUT_MS = 30_000;

export const startServer = async ({
  app,
  config,
}: {
  app: App;
  config: Pick<Config, 'PORT'>;
}) => {
  const server = app.listen(config.PORT);

  const shutdown = async (signal: 'SIGTERM' | 'SIGINT') => {
    const forceExit = setTimeout(() => process.exit(1), SHUTDOWN_TIMEOUT_MS);

    try {
      await new Promise<void>((resolve) => server.close(() => resolve()));
      await app.shutdown();
      clearTimeout(forceExit);
      process.exit(0);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      const stack = err instanceof Error ? err.stack : undefined;
      console.error(
        JSON.stringify({
          level: 'error',
          message: 'Shutdown error',
          signal,
          error: message,
          stack,
        }),
      );
      process.exit(1);
    }
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));

  return server;
};
```

### Health Check Endpoints

```typescript
export const createHealthRoutes = ({ db }: { db: DbPool }) => ({
  '/health': async () => ({ status: 'ok' }),
  '/ready': async () => {
    await db.query('SELECT 1');
    return { status: 'ready' };
  },
});
```

### Crash-Only Design

Processes must also be **robust against sudden death** (SIGKILL, hardware failure). Design so that unexpected termination does not corrupt state:

- Background jobs must be **reentrant** -- wrap results in a transaction or make the operation idempotent so interrupted work can be safely retried
- Use a robust queueing backend that returns jobs to the queue when workers disconnect or time out
- Never rely on in-process cleanup running to completion

```typescript
// Reentrant job pattern -- idempotent via upsert
const processPayment = async ({
  db,
  paymentId,
  amount,
}: {
  db: DbPool;
  paymentId: string;
  amount: number;
}) => {
  await db.transaction(async (tx) => {
    const existing = await tx.query(
      'SELECT id FROM payments WHERE id = $1 FOR UPDATE',
      [paymentId],
    );
    if (existing.rows.length > 0) return; // already processed -- idempotent

    await tx.query(
      'INSERT INTO payments (id, amount, status) VALUES ($1, $2, $3)',
      [paymentId, amount, 'completed'],
    );
  });
};
```

**Rules:**
- Handle SIGTERM and SIGINT for graceful shutdown
- Set a drain timeout -- force exit if shutdown hangs
- Await `server.close()` to drain in-flight connections
- Close database pools, Redis connections, queue consumers on shutdown
- Exit with non-zero code on shutdown failure
- Keep startup fast -- defer heavy initialisation to first request if needed
- Design background jobs to be reentrant/idempotent so interrupted work is safely retried
- Provide `/health` and `/ready` endpoints for orchestrator probes

---

## X. Dev/Prod Parity

> Keep development, staging, and production as similar as possible.

Historically, three gaps exist between development and production:

| Gap | Traditional | Twelve-Factor |
|-----|-------------|---------------|
| **Time gap** | Weeks between code written and deployed | Hours or minutes |
| **Personnel gap** | Developers write code, ops deploys it | Same people write and deploy |
| **Tools gap** | Different stacks in dev vs prod | As similar as possible |

**Resist the urge to use different backing services between dev and production.** Differences between backing services (SQLite in dev, PostgreSQL in prod) mean tiny incompatibilities crop up, causing code that passed tests in development to fail in production. The cost of this friction compounds over the lifetime of the application.

Modern tools (Docker Compose, Homebrew, apt) make running production-grade backing services locally inexpensive.

**Rules:**
- If production uses PostgreSQL, develop against PostgreSQL (not SQLite)
- If production uses Redis, develop against Redis (not in-memory maps)
- Use containers (Docker Compose) to run backing services locally
- Config schema validation (Factor III) catches mismatches at startup
- All deploys (dev, staging, prod) use the **same type and version** of each backing service

---

## XI. Logs

> Treat logs as event streams.

Logs are the stream of aggregated, time-ordered events collected from all running processes. They have no fixed beginning or end -- they flow continuously.

**A twelve-factor app never concerns itself with routing or storage of its output stream.** It does not write to logfiles, manage log rotation, or configure file transports. Each running process writes its event stream, unbuffered, to `stdout`. The execution environment (container orchestrator, PaaS) captures, collates, and routes the stream to its final destinations.

### Semantic Requirements

Regardless of logging library, all loggers must satisfy:

- **Structured output** -- machine-parseable (JSON preferred), not free-form strings
- **stdout/stderr only** -- the app never writes to log files, never configures file transports
- **Standard levels** -- at minimum: `debug`, `info`, `warn`, `error` -- configurable via environment
- **Contextual data** -- logs accept structured metadata (key-value pairs), not just message strings
- **Timestamp** -- every entry includes an ISO 8601 timestamp
- **Request correlation** -- include a `requestId` or trace ID to correlate logs across a single request

Any logging library (pino, winston with console transport, OpenTelemetry) is acceptable as long as these semantics are met.

### Example

```typescript
const LOG_LEVELS = { debug: 0, info: 1, warn: 2, error: 3 } as const;

export const createLogger = ({
  config,
}: {
  config: Pick<Config, 'LOG_LEVEL'>;
}) => {
  const shouldLog = (level: keyof typeof LOG_LEVELS) =>
    LOG_LEVELS[level] >= LOG_LEVELS[config.LOG_LEVEL];

  const log = (
    level: keyof typeof LOG_LEVELS,
    message: string,
    data?: Record<string, unknown>,
  ) => {
    if (!shouldLog(level)) return;
    const output = JSON.stringify({
      timestamp: new Date().toISOString(),
      level,
      message,
      ...data,
    });
    (level === 'error' ? console.error : console.log)(output);
  };

  return {
    debug: (message: string, data?: Record<string, unknown>) =>
      log('debug', message, data),
    info: (message: string, data?: Record<string, unknown>) =>
      log('info', message, data),
    warn: (message: string, data?: Record<string, unknown>) =>
      log('warn', message, data),
    error: (message: string, data?: Record<string, unknown>) =>
      log('error', message, data),
  };
};
```

### Logging Anti-Patterns

```typescript
// Writing to log files -- the app is routing its own logs
import fs from 'fs';
fs.appendFileSync('/var/log/app.log', message);

// File transport -- same violation via library config
import winston from 'winston';
const logger = winston.createLogger({
  transports: [new winston.transports.File({ filename: 'error.log' })],
});

// Unstructured string interpolation -- cannot be parsed or queried
console.log(`User ${userId} logged in`);
```

**Why these are wrong:** File transports mean the app is routing its own logs -- that is the execution environment's responsibility. Unstructured string interpolation produces logs that cannot be parsed, indexed, or queried by log aggregation systems.

---

## XII. Admin Processes

> Run admin/management tasks as one-off processes.

Admin tasks (database migrations, data fixes, console sessions, one-time scripts) must run in an identical environment to the regular long-running processes. They run against a release, using the same codebase, same config, and same dependencies.

```typescript
// scripts/migrate.ts -- admin process using shared config and dependencies
const config = createConfig();
const db = createDbPool({ connectionString: config.DATABASE_URL });
try {
  await runMigrations(db);
} finally {
  await db.end();
}
```

**Rules:**
- Admin scripts live in the repo alongside application code (e.g., `scripts/migrate.ts`)
- They are not separate tools or ad-hoc shell commands
- They import from the main codebase and use the same config module
- The same dependency isolation applies -- use `bundle exec`, `npx`, or the project's runner
- One-off processes run against the same release as the app
- Admin code ships with application code to avoid synchronisation issues

---

## Testing 12-Factor Patterns

Twelve-factor patterns are testable through behavior-driven tests. Config injection via options objects makes all patterns naturally testable without mocking `process.env` or global state.

- **Config**: test that `createConfig` throws on missing required vars and returns correct defaults
- **Disposability**: test that shutdown closes all connections (inject test doubles for db/cache)
- **Backing services**: test that services work with any backing service URL (inject via config)
- **Statelessness**: test that request handlers do not depend on prior request state
- **Reentrant jobs**: test that processing the same job twice produces the same result (idempotency)
- **Health checks**: test that `/health` returns ok and `/ready` fails when the database is unavailable

---

## Checklist

- [ ] One codebase per deployable service; shared code extracted as libraries
- [ ] All dependencies declared in manifest with lockfile committed
- [ ] Dependencies isolated (node_modules, not global installs); no implicit system tools
- [ ] All config from environment variables, validated at startup with a schema
- [ ] Startup fails fast with clear error if config is invalid
- [ ] `.env.example` documents required variables (no real credentials committed)
- [ ] Env vars are granular and orthogonal -- not grouped into named "environments"
- [ ] Backing services connected via config URLs, swappable without code changes
- [ ] No distinction between local and third-party services in code
- [ ] Same build artifact deploys to every environment (no env-specific builds)
- [ ] Releases are immutable with unique IDs; config injected at release/run time
- [ ] No in-memory session state, no local filesystem state between requests
- [ ] Sticky sessions not used
- [ ] App binds to a port from config, includes its own HTTP server
- [ ] Separate entry points for web and worker process types
- [ ] Processes never daemonize or write PID files
- [ ] SIGTERM/SIGINT handlers with drain timeout for graceful shutdown
- [ ] Database pools and connections closed on shutdown
- [ ] Background jobs are reentrant/idempotent (safe to retry after crash)
- [ ] `/health` and `/ready` endpoints for orchestrator probes
- [ ] Same backing service types and versions in development and production
- [ ] Three gaps minimised: time (deploy in hours), personnel (devs deploy), tools (same stack)
- [ ] Logs written as structured JSON to stdout, no file transports
- [ ] Logs include timestamps and request correlation IDs
- [ ] Admin scripts live in repo, use shared config and dependencies, run against same release

