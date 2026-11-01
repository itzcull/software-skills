# Autonomous Engineer Workflow

This document describes the six-phase workflow the Autonomous Engineer agent follows when implementing a user requirement. Each phase has explicit entry criteria, activities, exit criteria, and escalation conditions.

For the review contract that governs the artifacts produced, see [review-contract.md](./review-contract.md).
For the ADR template used in Phase 2, see [adr-template.md](./adr-template.md).

## Guiding Principles

1. **Autonomous in execution, not in interpretation.** The agent executes implementation autonomously but surfaces ambiguity to the user rather than guessing.
2. **TDD is non-negotiable.** Every line of production code must be preceded by a failing test. No exceptions.
3. **Decisions are documented, not hidden.** Significant design decisions produce ADRs with explicit tradeoff analysis.
4. **Tests are executable specifications.** Acceptance criteria exist transiently in context but are translated into tests that persist as the living specification.
5. **Small, stable increments.** Every commit is stable. The codebase is always in a working state.

## Phase 1: Requirement Decomposition

### Entry Criteria

- User has provided a natural language requirement
- The target project's codebase is accessible

### Activities

1. **Parse the requirement** into its constituent parts:
   - What is the desired behavior? (functional)
   - What qualities must it have? (non-functional: performance, security, usability)
   - What are the constraints? (technical, business, time)

2. **Explore the codebase** to understand:
   - Existing patterns and conventions
   - Test infrastructure (framework, naming, structure)
   - Module boundaries and dependency graph
   - Related existing functionality

3. **Derive acceptance criteria** in Given-When-Then format:
   - Cover the happy path first
   - Then error conditions and edge cases
   - Then boundary conditions
   - Each criterion must be independently testable

4. **Identify domain concepts** using ubiquitous language:
   - What entities, value objects, or aggregates are involved?
   - What bounded context does this belong to?
   - Are there existing domain terms that apply?

### Exit Criteria

- Acceptance criteria are defined and unambiguous
- Each criterion maps to a specific testable behavior
- Edge cases and error conditions are explicitly identified
- Domain concepts are named using existing ubiquitous language

### Escalation Conditions

**Stop and ask the user when:**

- The requirement contains ambiguous terms with multiple valid interpretations
- The requirement conflicts with existing behavior in the codebase
- The requirement scope is unclear (could be interpreted as small or large)
- Domain terms are used inconsistently or without clear definition
- Non-functional requirements are implied but not specified (e.g., "fast" without a target)

## Phase 2: Planning and Design Decisions

### Entry Criteria

- Phase 1 complete with defined acceptance criteria

### Activities

1. **Generate a test list** ordered by complexity (simplest first):
   - Map each acceptance criterion to one or more test cases
   - Order tests so each builds incrementally on the last
   - Identify which test level applies (unit, integration, E2E)

2. **Identify design decisions** that warrant ADRs:
   - Apply the ADR triggers from [adr-template.md](./adr-template.md)
   - For each decision, evaluate at least two genuine alternatives
   - Document tradeoffs explicitly
   - Commit ADR files to `docs/decisions/`

3. **Identify architectural boundaries**:
   - Where are trust boundaries that need schema validation?
   - Which dependencies are external (need integration tests)?
   - Where should abstractions be introduced for testability?

4. **Determine the implementation strategy**:
   - Vertical slice: which layers are touched?
   - What is the minimal slice that delivers user value?
   - Are there dependencies between acceptance criteria that constrain ordering?

### Exit Criteria

- Test list is complete and ordered
- ADRs committed for all significant decisions
- Architectural boundaries identified
- Implementation strategy is clear

### Escalation Conditions

**Stop and ask the user when:**

- Two alternatives are roughly equivalent with no clear winner
- The decision has significant long-term architectural implications
- The decision affects areas outside the immediate requirement scope

## Phase 3: TDD Implementation

### Entry Criteria

- Phase 2 complete with test list and ADRs
- Target project test infrastructure is functional

### Activities

For each test in the ordered test list:

1. **RED: Write a failing test**
   - Write exactly one test that describes the next behavioral increment
   - The test name reads as a behavioral specification
   - Run the test suite -- the new test MUST fail
   - All previously passing tests MUST still pass
   - Commit: `test: [describe the behavior being specified]`

2. **GREEN: Make it pass**
   - Write the MINIMUM production code to make the failing test pass
   - Resist writing more than the test demands
   - Run the full test suite -- all tests MUST pass
   - Commit: `feat: [describe the behavior now implemented]`

3. **REFACTOR: Assess and improve**
   - Evaluate against the refactoring checklist:
     - Naming: Are names clear and descriptive?
     - Magic values: Are constants extracted?
     - Structure: Is nesting <= 2 levels? Functions < 30 lines?
     - Knowledge duplication: Is the same business rule repeated?
     - Purity: Are functions pure where possible?
   - Apply the priority classification:
     - **Critical**: Fix before commit (immutability violations, security issues)
     - **High**: Fix this session (unclear names, magic numbers, long functions)
     - **Nice to have**: Consider later (minor naming, helper extraction)
     - **Skip**: Code is already clean
   - If refactoring was applied, run full test suite, then commit: `refactor: [describe improvement]`
   - If code is already clean, proceed to next test

4. **Update the test list**: Remove completed test, add any newly discovered tests

### Exit Criteria

- All tests in the test list are implemented and passing
- Every acceptance criterion has at least one corresponding test
- Git history shows consistent RED-GREEN-REFACTOR progression
- No production code exists without a preceding test

### Escalation Conditions

**Stop and ask the user when:**

- A test reveals that the requirement has an inherent contradiction
- The implementation approach requires changing existing public APIs
- A test cannot be written without making assumptions about undefined behavior
- Integration with an external system behaves differently than documented

## Phase 4: Structural Assessment

### Entry Criteria

- Phase 3 complete with all acceptance criteria met

### Activities

1. **Holistic code review** of all changes:
   - Assess the implementation as a whole (not just individual commits)
   - Look for patterns that emerged across multiple RED-GREEN-REFACTOR cycles
   - Identify opportunities for structural improvement

2. **Apply refactoring priority classification** to the complete change set:
   - **Critical refactoring**: Must be done before review
   - **High-value refactoring**: Should be done in this session
   - **Nice-to-have**: Document for future consideration
   - **Skip**: Code is fit for purpose

3. **Verify behavioral equivalence** after any structural changes:
   - All tests MUST remain green
   - No behavior change is introduced
   - Refactoring commits are separate from feature commits

### Exit Criteria

- Critical and high-value refactoring applied (or explicitly deferred with rationale)
- All tests pass
- Refactoring commits are cleanly separated from feature commits

### Escalation Conditions

**Stop and ask the user when:**

- A beneficial refactoring would require changing code outside the current scope
- The refactoring reveals a design issue in existing code that predates this change

## Phase 5: Quality Gate Verification

### Entry Criteria

- Phase 4 complete

### Activities

Run each quality gate and record the result:

1. **Test suite**: `[test command]` -- all tests pass
2. **Build**: `[build command]` -- builds successfully
3. **Lint**: `[lint command]` -- no lint errors
4. **Typecheck**: `[typecheck command]` -- no type errors
5. **Git history audit**:
   - Verify RED-GREEN-REFACTOR progression in commit messages
   - Verify no production code precedes its test
   - Verify refactoring commits are separate from feature commits
   - Verify every commit is individually stable
6. **Type safety audit**:
   - No `any` types without documented justification
   - No type assertions without documented justification
   - TypeScript strict mode satisfied
7. **Test quality audit**:
   - Tests verify behavior through public API
   - No mocking of internal collaborators
   - Test names read as behavioral specifications
   - Factory functions used (no `let`/`beforeEach` shared mutable state)

### Exit Criteria

- All quality gates pass
- Any failures are addressed before proceeding

### Escalation Conditions

**Stop and ask the user when:**

- A pre-existing quality issue (not introduced by this change) blocks a gate
- A quality gate failure requires changes outside the current scope

## Phase 6: Review Preparation

### Entry Criteria

- Phase 5 complete with all gates passing

### Activities

1. **Produce the review summary** following the format defined in [review-contract.md](./review-contract.md):
   - Original requirement
   - Derived acceptance criteria
   - Test-to-criteria mapping
   - ADR references
   - Quality gate results
   - Known limitations and deferred items

2. **Self-assess against rejection criteria**:
   - Walk through each rejection criterion in the review contract
   - If any would trigger rejection, go back and fix before submitting
   - This is a pre-flight check, not a substitute for the Review agent

3. **Prepare the deliverable**:
   - Ensure all files are committed
   - Review summary is ready for the Review agent
   - ADRs are committed and referenced

### Exit Criteria

- Review summary is complete and accurate
- Self-assessment passes all rejection criteria
- All artifacts are committed and ready for review

## Decision Frameworks

### When to Create an ADR

Ask these questions about each design decision:

1. Does it affect the public API or module boundaries? -> ADR
2. Does it introduce a new dependency? -> ADR
3. Are there two or more viable approaches with distinct tradeoffs? -> ADR
4. Does it constrain future implementation options? -> ADR
5. Does it affect testability in non-obvious ways? -> ADR

If none apply, skip the ADR.

### How Acceptance Criteria Map to Test Levels

| Criterion Type | Test Level | Example |
|---------------|------------|---------|
| Business rule (pure logic) | Unit test | "When order total exceeds $100, apply 10% discount" |
| Data transformation | Unit test | "When CSV is parsed, return array of typed records" |
| External system integration | Integration test | "When payment is submitted, charge appears in Stripe" |
| Cross-boundary data flow | Integration test | "When API receives request, database record is created" |
| User-visible behavior | E2E test (sparingly) | "When user clicks checkout, order confirmation appears" |

### When to Stop and Ask

The agent is autonomous in execution but NOT in interpretation. Apply this test:

> "If I proceed with my best guess and I'm wrong, would the resulting code need to be significantly reworked?"

If yes, stop and ask. The cost of a question is always less than the cost of rework.
