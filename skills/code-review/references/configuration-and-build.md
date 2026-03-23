# Configuration & Build

Category 15 -- Is configuration correct and environment-safe?

## Subcategories

- **Hardcoded configuration values** -- URLs, ports, timeouts, feature flags baked into source code instead of externalised
- **Missing environment variable validation** -- environment variables read without checking they exist or have valid values
- **Incorrect build configuration** -- wrong output targets, missing polyfills, incorrect source maps, broken tree-shaking
- **Dependency version issues** -- unpinned dependencies, incompatible version ranges, missing lockfile updates
- **Missing or incorrect CI/CD configuration** -- build steps that do not match the project's actual requirements
- **Secrets in configuration files** -- API keys, passwords, or tokens in committed config files
- **Environment leakage** -- production configuration values in development config or vice versa
- **Missing feature flags** -- risky changes deployed without a kill switch
- **Incorrect file permissions** -- scripts missing execute bits, config files with overly permissive access
- **Missing health checks** -- deployed services without liveness or readiness probes

## What to Look For

- Strings that look like URLs, connection strings, or API endpoints hardcoded in source (not from environment)
- `process.env.SOME_VAR` used without a fallback or validation (will be `undefined` if not set)
- `package.json` changes that add dependencies without corresponding lockfile updates
- `devDependencies` that should be `dependencies` or vice versa
- Build scripts that reference absolute paths or paths specific to one developer's machine
- `.env` files or files containing secrets added to version control (check `.gitignore`)
- Docker images using `latest` tag instead of pinned versions
- CI configuration that does not run the same checks as the local development workflow
- TypeScript `tsconfig.json` changes that relax strict mode settings
- Missing `engines` field in `package.json` for Node.js version requirements

## Positive Example

```typescript
import { z } from "zod";

const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  PORT: z.coerce.number().int().positive().default(3000),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
  API_KEY: z.string().min(1),
});

export const env = EnvSchema.parse(process.env);
```

Environment variables validated at startup with a schema. Missing or invalid values fail fast with clear error messages.

## Negative Example

```typescript
// CONFIG: hardcoded values, no validation, secrets in source
const DB_HOST = "prod-db.internal.company.com";
const API_KEY = "sk_live_abc123def456";
const TIMEOUT = 5000;

const db = new Database(`postgres://admin:password@${DB_HOST}:5432/myapp`);
```

Production hostname, live API key, and database credentials hardcoded in source. No environment variable usage.

## Common False Positives

- Hardcoded values in test fixtures that are intentionally fixed
- Default values used as fallbacks when the environment variable is optional
- Development-only configuration files that are clearly marked and gitignored
- Constants that are genuinely constant and do not vary by environment (e.g. mathematical constants, HTTP status codes)

## Severity Guide

| Severity | When |
|---|---|
| Critical | Secrets committed to source control; production credentials in configuration files |
| Major | Missing environment variable validation on required config; hardcoded production URLs; unpinned dependency versions in production |
| Minor | Missing lockfile update; build config that works but is suboptimal; missing health check |
| Nitpick | Preference for configuration file format; ordering of environment variables |

## Related Categories

- [Security](security.md) -- secrets in configuration is a security concern
- [Resource Management](resource-management.md) -- connection pool configuration is a resource concern
- [Compatibility](compatibility.md) -- build targets and polyfills affect compatibility
