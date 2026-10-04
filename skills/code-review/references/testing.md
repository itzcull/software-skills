# Testing

Category 13 -- Are changes adequately tested?

Use [test-design](../../test-design/SKILL.md) as the authority for test levels, doubles, and application-owned test data. Assess whether the chosen tests demonstrate the intended behavior and inherited evaluation criteria; do not require a test per code unit or reject deliberate integration tests merely for using real dependencies.

## Subcategories

- **Missing unit tests** -- new behaviour without corresponding test coverage
- **Inadequate edge case coverage** -- happy path tested but boundary conditions, empty inputs, and error cases are not
- **Brittle tests** -- tests that break on refactoring because they test implementation details
- **Missing integration tests** -- new external service interactions or database operations without integration tests
- **Incorrect assertions** -- assertions that do not actually verify the intended behaviour
- **Test logic errors** -- bugs in the test itself (setup that does not match the scenario description)
- **Uncontrolled external dependencies** -- tests that contact shared or production services, depend on undeclared environment state, or lack deliberate isolation at the chosen test level
- **Flaky tests** -- tests with timing dependencies, shared mutable state, or non-deterministic behaviour
- **Tests not covering the changed code** -- new tests exist but do not exercise the code that was modified
- **Test structure issues** -- missing arrange/act/assert separation, multiple assertions per test without clear reason
- **Snapshot overuse** -- snapshot tests used where explicit assertions would catch regressions more precisely

## What to Look For

- Changed observable behavior without meaningful coverage through the appropriate public interface
- Assertions on internal collaborator calls rather than domain outcomes or observable outgoing effects
- Shared mutable state or setup hooks that leak between tests or hide behavior-specific preconditions
- Tests where the description says one thing but the assertion checks something else
- Tests that rely on execution order (test B depends on state created by test A)
- Missing tests for error paths (what happens when the API returns 500? when the input is empty?)
- Tests that assert on the exact structure of a log message or console output (fragile)
- Fixtures that bypass authoritative application definitions or duplicate domain constraints instead of reusing application-owned constructors, schemas, or factories
- `expect(result).toBeTruthy()` where `expect(result).toEqual(expectedValue)` would be more precise
- Tests that mock the module under test instead of its dependencies
- Large test files with no logical grouping (missing `describe` blocks)

## Positive Example

```typescript
describe("calculateDiscount", () => {
  it("applies 10% discount for orders over 100", () => {
    const order = createOrder({ subtotal: 150 });

    const discount = calculateDiscount(order);

    expect(discount).toEqual(money(15));
  });

  it("returns zero discount for orders at or below 100", () => {
    const order = createOrder({ subtotal: 100 });

    const discount = calculateDiscount(order);

    expect(discount).toEqual(money(0));
  });

  it("returns zero discount for empty orders", () => {
    const order = createOrder({ subtotal: 0 });

    const discount = calculateDiscount(order);

    expect(discount).toEqual(money(0));
  });
});
```

Tests cover the threshold boundary (at 100, above 100, at zero). Each test is independent with its own factory-created data. Assertions check exact expected values.

## Negative Example

```typescript
// BRITTLE: tests implementation, not behaviour
let service: OrderService;
let mockRepo: jest.Mocked<OrderRepository>;

beforeEach(() => {
  mockRepo = createMockRepo();
  service = new OrderService(mockRepo);
});

it("should call repo with correct params", async () => {
  await service.processOrder(testOrder);

  expect(mockRepo.save).toHaveBeenCalledWith(
    expect.objectContaining({ status: "processed" }),
  );
  expect(mockRepo.save).toHaveBeenCalledTimes(1);
});
```

This is a negative example when `save` is an internal implementation choice rather than the behavior promised by `processOrder`. In that case, the assertions couple the test to internal collaboration. If persistence through an application-owned role is the observable outgoing effect, interaction verification can be appropriate; establish that boundary before reporting a finding.

## Common False Positives

- Missing tests for trivial one-line functions that are fully covered by integration or E2E tests
- Tests that appear to share state but actually reset it correctly via framework mechanisms
- Snapshot tests that are appropriate for the use case (e.g. verifying serialised output format)
- Tests for code that is being deleted in the same diff
- Integration tests deliberately using isolated real databases, filesystems, or service instances
- Fixtures built with application-owned constructors or factories
- Assertions on outgoing interactions that are the observable behavior through an application-owned role

## Severity Guide

| Severity | When |
|---|---|
| Critical | No tests at all for a new feature or significant behaviour change |
| Major | Missing edge case tests for error-prone logic; tests that do not actually verify the changed code; flaky tests merged to main |
| Minor | Missing test for an unlikely edge case; test structure issues; snapshot where assertion would be better |
| Nitpick | Test naming preference; arrange/act/assert spacing style |

## Related Categories

- [Logic & Correctness](logic-and-correctness.md) -- testing is the primary defence against logic errors
- [Error Handling](error-handling.md) -- error path tests verify error handling works
- [Code Structure & Organisation](code-structure-and-organisation.md) -- untestable code is usually poorly structured
