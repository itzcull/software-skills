---
name: test-design
description: Authoritative resource on writing great tests: behavior-focused test design, test levels, test doubles, integration testing, E2E/browser testing, test data factories, and anti-patterns. Use when designing test strategies, choosing test levels, writing resilient tests, selecting dummies/stubs/fakes/spies/mocks, or reviewing test quality.
license: MIT
version: 1.0.0
metadata:
  author: itzcull
---

## Purpose

Provide an authoritative resource on writing great tests, grounded in the principle that tests encode intent, not implementation. This skill helps agents choose appropriate test levels, write behavior-focused tests, use test doubles deliberately, and avoid brittle tests that fail during safe refactoring.

## When to use

- Designing a testing strategy for a feature or system
- Choosing between unit, integration, component, and E2E tests
- Writing behavior-focused tests through public APIs
- Deciding whether to use dummies, stubs, fakes, spies, mocks, or real collaborators
- Setting up integration tests for databases, APIs, queues, or filesystems
- Testing React components or browser flows with Testing Library or Playwright
- Reviewing tests for brittleness, implementation coupling, or missing coverage
- Creating test data factories and schema-validated test fixtures

## Core Principles

- Tests are executable specifications of observable behavior
- A test should fail if and only if the code no longer does what it promises
- Test the unit of behavior, not the unit of code
- Test through public APIs; internals should be invisible to tests
- Use test doubles at architectural boundaries, not between internal collaborators
- Do not double what you do not own directly; create your own abstraction and prove adapters with integration tests
- Prefer state and outcome verification over interaction verification when possible
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
| `Mock` | Strict expectation-based double configured before the act phase; it can fail the test itself when expected interactions are violated |

Prefer role-first language over tool-specific labels. For example, say "use a Jest mock function to stub this response" or "use a mock function to spy on this interaction" when the library primitive is doing stub or spy work. Reserve `mock` for strict pre-declared interaction expectations.

The key design question is not "what object did the test framework create?" It is "what role does this double play in the test's behavior specification?"

## Test Level Heuristic

| Question | Preferred Test Level |
|---|---|
| Does a behavioral rule still hold inside our system? | Unit test |
| Does our adapter honor a dependency contract? | Integration test |
| Does a UI component behave the way a user experiences it? | Component/browser test |
| Does the whole system complete a critical user journey? | E2E test |

## Reference Files

- [Testing Guidelines](references/testing-guidelines.md) - Core principles, test levels, test double philosophy, test data patterns, coverage guidance, React testing, and anti-patterns
- [Test Doubles](references/test-doubles.md) - Dummy, fake, stub, spy, and mock taxonomy; Classical vs Mockist TDD; sociable vs solitary tests; speed expectations
- [Integration Testing](references/integration-testing.md) - Adapter testing, Testcontainers, database testing, MSW, message queues, filesystem tests, and environment safety
- [E2E and Browser Testing](references/e2e-testing.md) - Testing Library query priority, Playwright locators/assertions, userEvent patterns, E2E structure, CI, debugging, and accessibility testing
