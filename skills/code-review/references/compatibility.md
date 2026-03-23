# Compatibility

Category 16 -- Does it work across targets?

## Subcategories

- **Browser incompatibility** -- using APIs not supported in target browsers without polyfills
- **OS-specific assumptions** -- path separators, line endings, case sensitivity, shell commands that differ across operating systems
- **Language version incompatibility** -- using syntax or APIs from a newer language version than the project targets
- **Framework version conflicts** -- using features from a framework version newer than the project's dependency
- **Encoding issues** -- assuming ASCII when the data may be UTF-8 or other encodings
- **Locale and i18n issues** -- hardcoded date formats, currency symbols, sort orders, or text direction
- **Timezone assumptions** -- code that assumes local timezone or UTC without explicit handling
- **Screen size and responsive design** -- layouts that break on certain viewport sizes
- **Accessibility** -- missing ARIA attributes, keyboard navigation, screen reader support (WCAG compliance)
- **API version mismatch** -- client code using API features not available in the deployed server version

## What to Look For

- `path.join` and `path.resolve` vs hardcoded `/` or `\` separators
- `fs` operations that assume case-sensitive or case-insensitive filesystems
- Node.js APIs used without checking the minimum Node version in `engines`
- `window`, `document`, or `navigator` accessed in code that may run server-side (SSR)
- `Date` operations without explicit timezone handling (`.toLocaleDateString()` varies by locale)
- CSS features without fallbacks for browsers in the support matrix (check `browserslist`)
- `Intl.NumberFormat` or `Intl.DateTimeFormat` with locale-specific assumptions
- Missing `alt` text on images, missing `aria-label` on interactive elements
- `onClick` handlers on non-interactive elements (`div`, `span`) without keyboard event equivalents
- Hardcoded English strings in UI code that should be localised
- Shell commands in npm scripts or build tools that only work on Unix (`rm -rf`, `cp`, `mv`)

## Positive Example

```typescript
import path from "node:path";

function getConfigPath(baseDir: string): string {
  return path.join(baseDir, "config", "settings.json");
}
```

Uses `path.join` for OS-independent path construction.

## Negative Example

```typescript
// COMPAT: OS-specific path separator, breaks on Windows
function getConfigPath(baseDir: string): string {
  return `${baseDir}/config/settings.json`;
}
```

Forward slash works on Unix but may fail in certain Windows contexts.

## Common False Positives

- OS-specific code in scripts that will only run in CI (known environment)
- Browser APIs used in code that is guarded by environment detection (`typeof window !== 'undefined'`)
- Locale-specific formatting in code that is intentionally region-locked
- Missing accessibility attributes on decorative or presentational elements
- Node.js API usage that matches the project's declared minimum Node version

## Severity Guide

| Severity | When |
|---|---|
| Critical | Code that crashes on a supported platform; accessibility violations that prevent users from completing core tasks |
| Major | Browser API used without polyfill for a target browser; timezone bug that produces wrong results for international users |
| Minor | Missing accessibility attribute on a non-critical element; locale assumption in a rarely-used feature |
| Nitpick | Preferring one cross-platform approach over another that also works |

## Related Categories

- [Configuration & Build](configuration-and-build.md) -- build targets, polyfills, and browserslist configuration determine compatibility
- [API & Interface](api-and-interface.md) -- API version compatibility is an interface concern
- [Design & Architecture](design-and-architecture.md) -- platform abstraction layers are an architectural decision
