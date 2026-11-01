# Review Contract

This document defines the formal interface between the Autonomous Engineer agent and the future Review agent. It specifies what the Autonomous Engineer produces, what the Review agent evaluates, and the criteria for acceptance or rejection.

## Contract Principle

The Autonomous Engineer produces structured artifacts. The Review agent evaluates those artifacts against defined criteria. This separation ensures the Review agent can operate independently without needing to understand the implementation process -- only its outputs.

## Artifacts Produced by the Autonomous Engineer

### 1. Git History

The commit history IS the primary evidence of TDD compliance. The Review agent examines commit messages and diffs to verify the RED-GREEN-REFACTOR progression.

**Expected commit pattern per feature increment:**

```
test: [describe failing test]           ← RED (test exists, no implementation)
feat: [describe passing implementation] ← GREEN (minimum code to pass)
refactor: [describe improvement]        ← REFACTOR (optional, only if warranted)
```

**Commit stability invariant**: Every commit must pass all tests, build, lint, and typecheck.

### 2. ADR Files

Located in `docs/decisions/NNNN-title.md`, following the template defined in [adr-template.md](./adr-template.md).

One ADR per significant design decision. The Review agent evaluates ADR completeness and tradeoff quality.

### 3. Test Suite

The test files themselves serve as executable specifications. Each behavioral requirement from the original user request should be traceable to one or more test cases.

**Test naming convention**: Test descriptions should read as behavioral specifications, not implementation descriptions.

```typescript
// Good: behavioral specification
describe('when a user submits an order with insufficient stock', () => {
  it('rejects the order with an out-of-stock error', () => { ... })
  it('does not deduct from available inventory', () => { ... })
})

// Bad: implementation description
describe('OrderService.processOrder', () => {
  it('calls inventoryCheck and returns false', () => { ... })
})
```

### 4. Review Summary

A structured summary produced at the end of the workflow. This is the primary entry point for the Review agent.

**Format:**

```markdown
# Review Summary

## Original Requirement
[The natural language requirement as provided by the user]

## Derived Acceptance Criteria
1. Given [context], when [action], then [expected outcome]
2. Given [context], when [action], then [expected outcome]
...

## Test-to-Criteria Mapping
| Criterion | Test File | Test Description |
|-----------|-----------|------------------|
| 1         | path/to/test.unit.test.ts | "rejects the order with an out-of-stock error" |
| 2         | path/to/test.unit.test.ts | "does not deduct from available inventory" |

## ADR References
- [ADR-0001: Title](../decisions/0001-title.md) - [one-line summary]
- [ADR-0002: Title](../decisions/0002-title.md) - [one-line summary]

## Quality Gate Results
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Lint passes
- [ ] Typecheck passes
- [ ] Git history shows RED-GREEN-REFACTOR progression
- [ ] No `any` types without justification
- [ ] All acceptance criteria have corresponding tests

## Known Limitations
- [Any deferred items, out-of-scope decisions, or known gaps]

## Deferred Items
- [Items explicitly postponed with rationale]
```

## Review Evaluation Criteria

The Review agent evaluates work against these criteria, grouped by severity.

### Rejection Criteria (MUST reject if violated)

These are non-negotiable. Any violation results in rejection with specific feedback.

| Criterion | Evidence Source | What Constitutes Violation |
|-----------|---------------|---------------------------|
| **TDD Compliance** | Git history | Production code committed without a preceding failing test commit |
| **Acceptance Criteria Coverage** | Review summary + test suite | Any derived acceptance criterion has no corresponding test |
| **Type Safety** | Source code | `any` type used without documented justification |
| **Test Behavioral Focus** | Test files | Tests verify implementation details (mocking internals, testing private methods, asserting on call counts of collaborators) |
| **Commit Stability** | Git history | Any commit that would fail tests, build, lint, or typecheck |

### Feedback Criteria (SHOULD flag for improvement)

These warrant feedback but do not require rejection on their own.

| Criterion | Evidence Source | What to Flag |
|-----------|---------------|--------------|
| **ADR Quality** | ADR files | Alternatives are strawmen, tradeoffs are vague, testability impact missing |
| **Refactoring Hygiene** | Git history | Refactoring mixed with feature commits (not separated) |
| **Test Naming** | Test files | Test descriptions are implementation-focused rather than behavioral |
| **Code Style** | Source code | Mutation, nested conditionals (>2 levels), functions >30 lines, comments in code |
| **DRY Knowledge** | Source code | Same business rule encoded in multiple locations |

### Advisory Criteria (MAY suggest)

These are improvement opportunities, not defects.

| Criterion | Evidence Source | What to Suggest |
|-----------|---------------|-----------------|
| **Pattern Opportunities** | Source code | Places where a design pattern would reduce complexity |
| **Test Coverage Gaps** | Test suite | Edge cases or boundary conditions not covered |
| **ADR Candidates** | Source code | Implicit decisions that would benefit from explicit documentation |
| **Naming Improvements** | Source code | Variables, functions, or types that could be more descriptive |

## Rejection Workflow

When the Review agent rejects work:

1. **Identify the specific violation(s)** with evidence (commit hash, file path, line number)
2. **Classify the severity** (rejection vs feedback vs advisory)
3. **Provide actionable remediation** -- what specifically needs to change
4. **Reference the relevant principle** from the knowledge base (e.g., "See testing.md: Mock at architectural boundaries, not between collaborators")

The Autonomous Engineer then addresses the rejection feedback and resubmits. The Review agent re-evaluates only the flagged items plus a spot-check of the overall work.

## Contract Versioning

This contract is versioned alongside the agent definitions. Changes to rejection criteria require updating both the Autonomous Engineer workflow (so it knows what to comply with) and this contract (so the Review agent knows what to enforce).

Current version: 1.0
