---
name: test-design
description: Authoritative resource on writing great tests: behavior-focused test design, test levels, test doubles, sociable testing, integration testing, E2E/browser testing, test data factories, and anti-patterns. Use when designing test strategies, choosing test levels, writing resilient tests, selecting dummies/stubs/fakes/spies/mocks, avoiding mock-heavy brittleness, or reviewing test quality.
license: MIT
version: 1.0.0
metadata:
  author: itzcull
---

## Purpose

Provide an authoritative resource on writing great tests, grounded in the principle that tests encode intent, not implementation. This skill helps agents choose appropriate test levels, write behavior-focused tests, use test doubles deliberately, prefer real collaborators where practical, and avoid brittle tests that fail during safe refactoring.

## When to use

- Designing a testing strategy for a feature or system
- Choosing between unit, integration, component, and E2E tests
- Writing behavior-focused tests through public APIs
- Deciding whether to use dummies, stubs, fakes, spies, mocks, or real collaborators
- Separating functional core logic from imperative shell effects to reduce mocking needs
- Setting up integration tests for databases, APIs, queues, or filesystems
- Preventing fake drift or mock drift across adapter and service boundaries
- Testing React components or browser flows with Testing Library or Playwright
- Reviewing tests for brittleness, implementation coupling, or missing coverage
- Creating test data factories and schema-validated test fixtures

## Core Principles

- Tests are executable specifications of observable behavior
- A test should fail if and only if the code no longer does what it promises
- Test the unit of behavior, not the unit of code
- Test through public APIs; internals should be invisible to tests
- Prefer sociable tests with real in-process collaborators; use solitary tests when a boundary is awkward, slow, non-deterministic, or still being designed
- Use test doubles at architectural boundaries, not between internal collaborators inside the same behavioral unit
- Do not double what you do not own directly; define your own role or port, double that role in unit tests, and prove adapters with integration or contract tests
- Prefer state and outcome verification over interaction verification when possible
- Use interaction verification only when the outgoing interaction is the observable behavior or when outside-in design is discovering a role
- Avoid header interfaces that merely mirror concrete classes for mockability; interfaces should express roles owned by the application
- Prefer pure functional cores and thin imperative shells: pure domain logic should need no mocks, while shell behavior is proven with sparse integration tests
- Organize tests by behavior rather than mirroring implementation files
- Test data factories should return complete objects with sensible defaults and optional overrides
- Validate factory output against real schemas when schemas exist

## Domain Language

Use these terms precisely when designing, writing, or reviewing tests:

| Term | Role in test design |
|---|---|
| `Test double` | Any replacement collaborator used in a test instead of the real object |
| `Dummy` | A value passed only to satisfy a signature; the test does not exercise it |
| `Stub` | Controls indirect inputs by returning specific values or throwing specific exceptions |
| `Fake` | Lightweight working implementation that behaves like the real collaborator but omits production qualities such as persistence, scale, or stability |
| `Spy` | Records indirect outputs from the system under test so the assert phase can query calls and arguments |
| `Mock` | Strict expectation-based double configured before the act phase; it can fail the test itself when expected role interactions are violated |
| `Temporary stub` | Short-lived scaffold used in outside-in TDD before the real collaborator exists; remove it once the production implementation is available |

Prefer role-first language over tool-specific labels. For example, say "use a Jest mock function to stub this response" or "use a mock function to spy on this interaction" when the library primitive is doing stub or spy work. Reserve `mock` for strict pre-declared interaction expectations.

The key design question is not "what object did the test framework create?" It is "what role does this double play in the test's behavior specification?"

Mocks are not general-purpose isolation tools. In their original design role, mocks discover or enforce application-owned collaboration protocols: "this object tells that role to do this." If a mock only exists so a concrete class can be isolated, it may be introducing test-induced design damage.

## Test Level Heuristic

| Question | Preferred Test Level |
|---|---|
| Does a behavioral rule still hold inside our system? | Unit test |
| Does our adapter honor a dependency contract? | Integration test |
| Does a service still satisfy a consumer-provider protocol? | Contract test |
| Does a UI component behave the way a user experiences it? | Component/browser test |
| Does the whole system complete a critical user journey? | E2E test |

## Reference Files

- [Testing Guidelines](references/testing-guidelines.md) - Core principles, test levels, test double philosophy, test data patterns, coverage guidance, React testing, and anti-patterns
- [Test Doubles](references/test-doubles.md) - Dummy, fake, stub, spy, mock, and temporary stub taxonomy; mock roles; functional core; contract testing; sociable vs solitary tests
- [Integration Testing](references/integration-testing.md) - Adapter testing, Testcontainers, database testing, MSW, consumer-driven contract testing, message queues, filesystem tests, and environment safety
- [E2E and Browser Testing](references/e2e-testing.md) - Testing Library query priority, Playwright locators/assertions, userEvent patterns, E2E structure, CI, debugging, and accessibility testing
