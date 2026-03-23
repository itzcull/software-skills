# Security

Category 4 -- Is the code safe from attack?

## Subcategories

- **Injection** -- SQL injection, XSS, command injection, path traversal, template injection, header injection
- **Authentication flaws** -- weak password handling, missing MFA enforcement, insecure session management
- **Authorisation bypass** -- missing access checks, IDOR (insecure direct object reference), privilege escalation
- **Secrets exposure** -- hardcoded credentials, API keys in source, secrets in logs or error messages
- **Insecure cryptography** -- weak algorithms (MD5, SHA1 for security), insufficient key length, ECB mode, predictable IVs
- **Insecure deserialization** -- untrusted data passed to deserializers that can execute code
- **Sensitive data logging** -- PII, tokens, passwords, or financial data written to logs
- **Missing input validation** -- user input accepted without sanitization or schema validation
- **CSRF** -- state-changing operations without CSRF tokens or SameSite cookies
- **SSRF** -- user-controlled URLs passed to server-side HTTP clients without allowlist validation
- **Mass assignment** -- binding user input directly to internal objects without field filtering
- **Timing attacks** -- non-constant-time comparison of secrets (tokens, passwords, HMACs)

## What to Look For

- String concatenation or template literals used to build SQL, shell commands, or HTML
- `eval()`, `Function()`, `new Function()`, `vm.runInContext()` with user-controlled input
- `innerHTML`, `dangerouslySetInnerHTML`, `document.write` with unsanitized data
- Hardcoded strings that look like keys, tokens, passwords, or connection strings
- `console.log`, `logger.info`, or error responses that include request bodies, tokens, or user data
- `fs.readFile`, `fs.writeFile`, `path.join` with user-controlled path segments without canonicalisation
- HTTP endpoints that mutate state using GET requests
- `fetch()`, `axios.get()`, or `http.request()` where the URL comes from user input
- Password comparison using `===` instead of a constant-time comparison function
- `crypto.createHash('md5')` or `crypto.createHash('sha1')` for security-sensitive hashing
- JWT tokens created without expiry, or verified without checking `iss`, `aud`, or `exp`
- CORS configuration with `origin: '*'` on authenticated endpoints
- Missing `Content-Security-Policy`, `X-Frame-Options`, or other security headers

## Positive Example

```typescript
const users = await db.query(
  "SELECT * FROM users WHERE email = $1 AND org_id = $2",
  [email, currentUser.orgId]
);
```

Parameterised query prevents SQL injection. Scoped to the current user's organisation prevents IDOR.

## Negative Example

```typescript
// VULN: SQL injection via string interpolation
const users = await db.query(
  `SELECT * FROM users WHERE email = '${req.body.email}'`
);
// VULN: no authorisation check -- any user can query any org's data
```

User input interpolated directly into SQL. No authorisation scope applied.

## Common False Positives

- Template literals used for logging or building strings that never reach a SQL/shell/HTML interpreter
- Hardcoded strings that look like keys but are test fixtures, example values, or public identifiers
- `innerHTML` used with a static, developer-controlled string (no user input)
- `eval` in build tooling or development-only code that does not run in production
- MD5/SHA1 used for non-security purposes (checksums, cache keys, deduplication)

## Severity Guide

| Severity | When |
|---|---|
| Critical | Injection vulnerabilities, secrets in source code, authentication bypass, missing authorisation on data-mutating endpoints |
| Major | Missing input validation on user-facing endpoints, insecure cryptography, sensitive data in logs, CSRF on state-changing operations |
| Minor | Missing security headers, overly permissive CORS on read-only endpoints, weak but non-exploitable configuration |
| Nitpick | Preferring one secure pattern over another equivalent one |

Security findings are almost never Nitpick. When uncertain, err toward higher severity.

## CWE Mapping

Key CWE references for common findings in this category:

- CWE-89: SQL Injection
- CWE-79: Cross-Site Scripting (XSS)
- CWE-78: OS Command Injection
- CWE-22: Path Traversal
- CWE-798: Hardcoded Credentials
- CWE-200: Exposure of Sensitive Information
- CWE-287: Improper Authentication
- CWE-862: Missing Authorisation
- CWE-352: Cross-Site Request Forgery

## Related Categories

- [Data Handling](data-handling.md) -- input validation overlaps both categories
- [Error Handling](error-handling.md) -- error messages that leak information are a security concern
- [API & Interface](api-and-interface.md) -- authentication and authorisation are API concerns
- [Configuration & Build](configuration-and-build.md) -- secrets management and security headers are configuration concerns
