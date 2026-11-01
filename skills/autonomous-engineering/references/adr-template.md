# ADR Template

Architecture Decision Records (ADRs) document significant design decisions made during autonomous implementation. Each ADR captures the context, decision, alternatives, and consequences to enable informed review.

## When to Create an ADR

Create an ADR when the decision:

- Affects the public API or module boundaries
- Introduces a new dependency or pattern
- Chooses between two or more viable approaches with distinct tradeoffs
- Constrains future implementation options
- Affects testability, performance, or maintainability in non-obvious ways

Do NOT create an ADR for:

- Routine implementation choices with no meaningful alternatives
- Naming decisions within established conventions
- Test structure that follows existing patterns

## File Naming Convention

```
docs/decisions/NNNN-short-descriptive-title.md
```

- `NNNN`: Sequential four-digit number (0001, 0002, ...)
- Title: Lowercase, hyphen-separated, describing the decision

## Template

```markdown
# ADR-NNNN: [Descriptive Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-NNNN]

## Context

What is the problem or situation that requires a decision? What forces are at play?
Include relevant constraints, requirements, and assumptions.

## Decision

What is the chosen approach and why? Be specific about what will be done.

## Alternatives Considered

### Alternative A: [Name]

- **Description**: What this approach entails
- **Pros**: Benefits of this approach
- **Cons**: Drawbacks of this approach
- **Rejected because**: Specific reason this was not chosen

### Alternative B: [Name]

- **Description**: What this approach entails
- **Pros**: Benefits of this approach
- **Cons**: Drawbacks of this approach
- **Rejected because**: Specific reason this was not chosen

## Consequences

### Positive

- [Benefit 1]
- [Benefit 2]

### Negative

- [Cost or risk 1]
- [Cost or risk 2]

### Tradeoffs

Explicit analysis of what is gained versus what is given up.

## Testability Impact

How does this decision affect the testing approach? Consider:

- Does it introduce boundaries that need integration tests?
- Does it affect the ability to test through public APIs?
- Does it require new test doubles or change existing mocking strategies?

## Review Notes

_This section is populated by the Review agent. Leave empty during creation._
```

## Quality Criteria for ADRs

An ADR is complete when:

1. **Context is sufficient**: A reader unfamiliar with the codebase can understand the problem
2. **Alternatives are genuine**: At least two viable options were considered (not strawmen)
3. **Tradeoffs are explicit**: Both gains and costs are articulated for the chosen approach
4. **Decision is actionable**: The decision clearly states what will be done
5. **Testability is addressed**: Impact on testing strategy is documented
