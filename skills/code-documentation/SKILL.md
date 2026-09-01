---
name: code-documentation
description: Source-level code comments and API documentation. Use when writing, revising, or reviewing docstrings, rustdoc, JSDoc, Doxygen, C# XML comments, TODO/FIXME markers, or documentation of intent, contracts, invariants, ownership, concurrency, safety, and failures.
license: MIT
metadata:
  author: itzcull
---

# Code Documentation

## Purpose

Create trustworthy comments that lower cognitive load without duplicating the implementation. Treat documentation as part of an abstraction's design: code explains the mechanism; comments preserve intent and contracts that code and types cannot express.

## Core principles

- **Abstraction disconnect**: useful comments operate at a different level from the code. Explain higher-level purpose and rationale or lower-level guarantees and constraints, never a prose translation of syntax.
- **Truth before coverage**: omit optional prose rather than inventing it. If a required public, safety, security, or resource contract cannot be established, report the discrepancy.
- **Refactor before narrating**: use clear names, types, functions, and control flow to reveal mechanism. Refactor only within task scope; otherwise preserve necessary context and report the opportunity.
- **Proportional rigor**: public APIs, unsafe code, security boundaries, ownership, concurrency, resource handling, and mandated licensing require strict documentation. Obvious private code usually does not.
- **Single source of truth**: put each fact at the narrowest authoritative boundary. Link stable specifications or policy instead of copying them, but state the local consequence so the comment is meaningful on its own.
- **Local style, semantic truth**: nearby code and configured tools govern syntax, structure, and grammatical mood. They cannot override observable behavior, safety obligations, or organizational policy.

## Workflow

### 1. Establish authority and scope

Read repository instructions, analogous code, public types, tests, documentation tooling, and linter configuration. Identify the audience, public surface, local comment format, and established grammatical mood.

For a broad audit, use structural or symbol-aware tooling to inventory exported items. For a focused change, inspect the changed symbols, their callers, and adjacent comments. For generated or vendored source, change the generator, schema, or authoritative upstream source unless repository policy explicitly owns the output.

### 2. Choose the documentation surface

| Surface | Information it should own | Placement |
| --- | --- | --- |
| System or module documentation | Purpose, architectural role, major data flow, and non-discoverable configuration assumptions | Entry point or enclosing module |
| Interface documentation | Capability, semantic inputs and outputs, side effects, failures, ownership, concurrency, compatibility, and safety obligations | Exported declaration visible to callers |
| Implementation comment | Non-obvious rationale, domain rule, invariant, algorithmic choice, optimization constraint, or workaround | Beside the protected decision |
| Call-site label | Meaning of an ambiguous literal or boolean argument | Beside the argument |
| Tool directive | Precisely scoped compiler, linter, coverage, bundler, or runtime instruction | Exact location required by the owning tool |
| Action marker | Known limitation, why it remains, and the condition or tracked work that closes it | Beside the constrained code |

For each in-scope item, choose one outcome: document the contract, add focused implementation context, refactor within scope, report a refactor opportunity, point to an authoritative source, or leave it uncommented because the code is already complete and obvious.

A comment is justified when removing it would erase information needed to use or change the code safely.

### 3. Write across the abstraction disconnect

Preserve the smallest amount of information unavailable from the implementation:

- **Higher-level intuition**: purpose, architectural role, domain meaning, rationale, or why an apparently simpler alternative is wrong.
- **Lower-level precision**: preconditions, postconditions, invariants, units, bounds, ordering, ownership, lifetime, concurrency, failures, or safety obligations.
- **Workarounds**: state the observable external constraint and include a stable upstream reference when available.
- **TODO/FIXME/HACK**: state the unresolved condition and a removal trigger or tracked issue.
- **Tool directives**: preserve exact syntax and placement, choose the narrowest effective scope, and record the reason where supported.

Use synthetic values in examples. Never introduce credentials or personal data, and keep sensitive endpoints or operational details in their approved authoritative location.

### 4. Format for the ecosystem

Follow repository conventions first. When no stronger convention exists:

- Begin an API block with one concise sentence that stands alone in IDE hovers and generated indexes.
- Keep the summary to one physical line of at most 80 characters when practical, end it with punctuation, and separate extended detail with a blank line.
- Use either imperative mood ("Fetch rows.") or indicative mood ("Fetches rows.") consistently with nearby code.
- Describe semantic constraints, units, defaults, side effects, and failures. Do not merely restate parameter names or types.
- Include structured sections only when they contain real contract information.
- Keep examples minimal, realistic, and executable when the toolchain supports it.

| Ecosystem | Pragmatic standard |
| --- | --- |
| Python | Use triple-double-quoted PEP 257 docstrings and the project's Google, NumPy, Sphinx, or other format. With typed signatures, omit redundant types from `Args:` and `Returns:`. Keep `Raises:` limited to intentional contract failures. Validate with configured Ruff, Pylint, pydocstyle, Sphinx, or doctest tooling. |
| Rust | Use `//!` for the enclosing crate/module and `///` for the following item. Add `# Errors`, `# Panics`, and `# Safety` only when applicable. Every public `unsafe` item needs caller obligations under `# Safety`; explain the proof beside unsafe blocks with focused `// SAFETY:` comments. Prefer rustdoc doctests and validate with `cargo doc` and `cargo test`. |
| C++ | Use the configured Doxygen form on public declarations visible to consumers, normally in headers. Document ownership, lifetime, invalidation, thread safety, and exception guarantees where relevant. Use tags such as `@param`, `@return`, `@throws`, `@note`, and `@warning` only when meaningful. |
| C# | Use XML comments with well-formed `<summary>`, `<param>`, `<returns>`, and `<exception>` elements. Names must match declarations. Prefer `<inheritdoc/>` only when behavior truly preserves the inherited contract. Validate with Roslyn and configured documentation warnings. |
| JavaScript | Use JSDoc type tags when they improve checking in dynamic code. Keep `@param`, `@returns`, `@throws`, `@callback`, and `@example` synchronized with behavior and signatures. |
| TypeScript | Let the signature own types. Use JSDoc for semantics, constraints, side effects, failures, deprecation, and examples. Avoid parallel typedefs that can drift from TypeScript declarations. Validate with the type checker and configured JSDoc lint rules. |

For another ecosystem, inspect its official generator and nearby repository examples before writing.

### 5. Verify truth and drift

Compare every changed or retained comment with the implementation, tests, public types, and authoritative specifications. Account for each applicable contract dimension:

- Inputs, units, accepted forms, nullability, and mutation
- Outputs, empty or partial results, and side effects
- Errors, exceptions, panics, rejection, retry, and cancellation
- Ownership, lifetime, invalidation, and resource release
- Concurrency, ordering, idempotency, and reentrancy
- Security, privacy, compatibility, deprecation, and unsafe-code obligations

Check exact parameter and symbol names. Run the documentation generator, doctests, type checker, or comment linter when available. Verify directive comments with the tool that consumes them. Review adjacent comments affected by the same code change.

When code, tests, specifications, and comments disagree, report the discrepancy rather than silently deciding which artifact is correct.

## Pragmatic examples

### Explain intent and invariants, not syntax

```python
# Bad: repeats the assignment.
# Increment the cursor.
cursor += 1

# Good: preserves protocol rationale and the parser invariant.
# Skip section 3.2 padding; frame validation guarantees the new cursor remains
# within the payload boundary.
cursor += alignment_offset(cursor, boundary_size)
```

### Let typed signatures own types

```typescript
/**
 * Resolves after every batch is durably committed to cold storage.
 *
 * @throws {StorageUnavailableError} When storage cannot be reached.
 */
declare function syncBatch(
  records: readonly StorageRecord[],
  onProgress: ProgressCallback,
): Promise<number>;
```

The comment adds durability and failure semantics without repeating the parameter or return types.

### State unsafe caller obligations precisely

```rust
/// Reads a value from `address`.
///
/// # Safety
///
/// `address` must be non-null, properly aligned, and valid for reads of `T`.
pub unsafe fn read_at<T: Copy>(address: *const T) -> T {
    // SAFETY: The public contract transfers these pointer obligations to the caller.
    unsafe { address.read() }
}
```

### Disambiguate call-site literals narrowly

```cpp
pipeline.Configure(/*enable_cache=*/true);
```

Repeated labels are design pressure toward an enum, options object, or stronger type.

## Anti-patterns

- **Echo comments** translate the next statement or control-flow keyword into prose.
- **Comment rot** describes old names, behavior, failures, or examples.
- **Shallow comments** repeat the same contract across pass-through layers.
- **Defensive comment overload** explains tangled mechanism that should be clarified in code.
- **Commented-out code** duplicates history already owned by version control.
- **Opaque provenance** cites a person, date, ticket, or URL without stating the local constraint.
- **Speculative promises** guarantee behavior not established by code and tests.
- **Boilerplate sections** repeat names, types, or empty behavior.
- **Actionless markers** say only "fix later" without a condition or tracked issue.
- **Broad suppressions** disable more checking than the local exception requires.

## Completion criteria

The work is complete when:

- Every public or high-risk boundary in scope has a justified documentation outcome.
- Every added or retained comment contributes information not already carried by code and types.
- Comments match current behavior, local format, and the exact symbols they name.
- Required documentation and analysis tooling passes.
- Unresolved contract discrepancies and out-of-scope refactor opportunities are reported.

An outcome with no new comment is valid when names, types, and structure already communicate the full intent.
