# Testing Principles

## The Core Truth

Tests encode intent, not implementation. A test should fail if and only if the code no longer does what it promises to do.

Tests are executable specifications—living documentation that verifies your system honors its contracts.

**Coverage targets**: 100% coverage through business behavior, not implementation details.

## The Two Test Failures

Tests can fail in two ways that indicate different problems:

| Failure Type | Description | Consequence |
|--------------|-------------|-------------|
| **False Positive** | Test passes, but code is broken | Bugs reach production |
| **False Negative** | Test fails, but code works | Wasted debugging time |

A test should fail if and only if the code no longer does what it promises to do.

**False negatives** occur when tests are coupled to implementation details. Refactor the code, and the test breaks — but nothing is actually wrong. This wastes developer time investigating non-existent bugs.

**False positives** occur when tests don't actually verify the behavior. The test passes, but the code doesn't work correctly.

See [Test Doubles: The Two Test Failures](./test-doubles.md#the-two-test-failures) for more on this framework.

## Test Levels

Each level tests contracts at a different boundary.

### Unit Tests

Specify contracts between behavioral units within your system.

- **"Unit" = unit of behavior, not unit of code** - test the behavior a caller depends on, not individual functions
- Test through the public API exclusively - internals should be invisible to tests
- Prefer sociable tests with real in-process collaborators
- Use test doubles at architectural boundaries, not between internal collaborators inside the same behavioral unit
- Should survive refactoring that preserves observable behavior
- No 1:1 mapping between test files and implementation files

```typescript
// Unit tests verify behavioral contracts
describe("Payment processing", () => {
  it("should reject payments with negative amounts", () => {
    const payment = getTestPayment({ amount: -100 });
    const result = processPayment(payment);

    expect(result.success).toBe(false);
    expect(result.error.message).toBe("Invalid amount");
  });
});
```

### Integration Tests

Specify that your code honors contracts with things you don't control—databases, APIs, third-party libraries.

- Verify your adapters work against real dependencies
- Complete the "don't double what you don't own" pattern: use stubs or spies for your abstraction in unit tests, prove the abstraction works here
- Test at the boundary between your code and external systems
- Prefer high-fidelity test infrastructure when practical: real databases, real queues, containerized services, or protocol-level HTTP stubs

See [Integration Testing](./integration-testing.md) for Testcontainers patterns, MSW setup, and database testing strategies.

```typescript
// Integration test - proves our adapter works with real database
describe("PaymentRepository", () => {
  it("should persist payment to database", async () => {
    const payment = getTestPayment({ amount: 100 });
    const repository = new PaymentRepository(testDatabase);

    await repository.save(payment);
    const retrieved = await repository.findById(payment.id);

    expect(retrieved).toEqual(payment);
  });
});
```

### End-to-End Tests

Specify that the whole system honors its contract with users or external consumers.

- Test real user flows through real entry points
- Slow and coarse-grained by nature; use sparingly for critical paths
- Verify the system works as a whole, not just individual parts
- Catches composition failures that unit and integration tests miss

```typescript
// E2E test - proves the whole system works for a user flow
describe("Checkout flow", () => {
  it("should complete purchase from cart to confirmation", async () => {
    await page.goto("/cart");
    await page.getByRole("button", { name: /checkout/i }).click();
    await page.getByLabelText(/card number/i).fill("4242424242424242");
    await page.getByRole("button", { name: /pay/i }).click();

    await expect(page.getByRole("heading", { name: /order confirmed/i })).toBeVisible();
  });
});
```

See [E2E Testing](./e2e-testing.md) for selector strategies and patterns.

### Why All Three

Each layer alone leaves gaps. The combination gives confidence that intent is preserved from internal behavior through to user-observable outcomes.

| Gap | What catches it |
|-----|-----------------|
| Behavioral regression | Unit tests |
| Adapter/dependency mismatch | Integration tests |
| Consumer-provider drift | Contract tests |
| Composition failure | E2E tests |

## Test Double Philosophy

Use test doubles at architectural boundaries, not between internal collaborators. Reserve `mock` for strict expectation-based doubles; use `stub`, `spy`, or `fake` when that is the role the double plays.

Default to state and outcome verification. Use behavior verification only when the outgoing interaction is the observable behavior, such as publishing an event, sending an email, recording a metric, or issuing a command to an external port.

Prefer a functional core and imperative shell where the architecture allows it. Pure domain functions should take data and return data; they need no mocks. The shell should be thin and tested with a small number of adapter or integration tests.

Mocks were originally a design tool for discovering role-based interfaces in outside-in TDD. They are not a license to replace every class with a generated double. If an interface merely mirrors a concrete class so the class can be mocked, it is probably a header interface and a design smell.

See [Test Doubles](./test-doubles.md) for detailed coverage of dummy, stub, spy, mock, and fake objects.

### Don't Double What You Don't Own Directly

When you depend on something you don't control (database, external API, third-party library), create your own role or port and use a stub or spy for that abstraction in unit tests:

```typescript
// ❌ BAD - Replacing a third-party library directly
jest.mock("stripe", () => ({
  charges: {
    create: jest.fn().mockResolvedValue({ id: "ch_123" }),
  },
}));

// ✅ GOOD - Define your own abstraction
interface PaymentGateway {
  charge(amount: number, cardToken: string): Promise<ChargeResult>;
}

// In unit tests: use a stub for PaymentGateway
const paymentGatewayStub: PaymentGateway = {
  charge: jest.fn().mockResolvedValue({ success: true, chargeId: "ch_123" }),
};

// In integration tests: prove StripePaymentGateway implements PaymentGateway correctly
describe("StripePaymentGateway", () => {
  it("should charge card via Stripe API", async () => {
    const gateway = new StripePaymentGateway(stripeTestKey);
    const result = await gateway.charge(1000, testCardToken);
    expect(result.success).toBe(true);
  });
});
```

### Where to Use Test Doubles

- **Unit tests**: Stub or spy on application-owned roles or ports at architectural boundaries
- **Integration tests**: Use real dependencies, containers, or faithful protocol stubs to prove adapters work
- **Contract tests**: Capture consumer-provider expectations when mocks could drift from a remote service
- **Never double**: Internal collaborators within the same behavioral unit

```typescript
// ❌ BAD - Spying on an internal collaborator
it("should call validateAmount", () => {
  const spy = jest.spyOn(validator, "validateAmount");
  processPayment(payment);
  expect(spy).toHaveBeenCalled();
});

// ✅ GOOD - Test the behavior, not the internals
it("should reject payments with negative amounts", () => {
  const payment = getTestPayment({ amount: -100 });
  const result = processPayment(payment);
  expect(result.success).toBe(false);
});
```

## Heuristics

- **Test the what, not the how** - verify outcomes, not steps
- **Test from the caller's perspective** - what does the consumer care about?
- **If a refactor breaks your tests but preserves behavior, those tests were wrong**
- **"calls X with Y" is weaker than "given A, when B, then C"** - specify outcomes, not interactions
- **Mock roles, not objects** - double an application-owned collaboration role, not a concrete class or third-party API
- **Prefer real collaborators until they hurt** - introduce doubles for boundaries, speed, determinism, unbuilt collaborators, or explicit interaction design

## Four Pillars of Good Tests

All good tests balance these properties (Vladimir Khorikov's framework):

| Pillar | Description | Tradeoff |
|--------|-------------|----------|
| **Protection against regressions** | How well the test catches defects | Inversely related to speed |
| **Resistance to refactoring** | Whether tests survive internal changes | Binary — either coupled or not |
| **Fast feedback** | How quickly the test runs | Inversely related to protection |
| **Maintainability** | How easy the test is to understand | Binary — either readable or not |

All tests must have resistance to refactoring and maintainability — tests that fail on refactoring or are incomprehensible provide no value. The tradeoff is between protection (more thorough = slower) and speed (faster = less thorough).

See [Test Doubles: Speed Expectations](./test-doubles.md#speed-expectations) for practical benchmarks.

## Testing Tools

- **Jest** or **Vitest** for testing frameworks
- **React Testing Library** for React components
- **MSW (Mock Service Worker)** for HTTP stubbing at the network level
- **Testcontainers** for integration tests with real databases
- **Pact** or equivalent contract tooling for consumer-provider API drift
- **Playwright** for E2E browser testing

See [E2E Testing](./e2e-testing.md) for Playwright and Testing Library patterns.

## Test Organization

Tests should be organized by behavior, not by implementation file structure:

```
src/
  features/
    payment/
      payment-processor.ts
      payment-validator.ts       // implementation detail
      payment-processor.test.ts  // tests behavior through public API
      payment-repository.integration.test.ts  // tests adapter
```

## Test Data Patterns

Use factory functions with optional overrides for test data:

```typescript
const getTestPaymentRequest = (
  overrides?: Partial<PaymentRequest>
): PaymentRequest => {
  return {
    cardAccountId: "1234567890123456",
    amount: 100,
    source: "Web",
    accountStatus: "Normal",
    lastName: "Doe",
    dateOfBirth: "1980-01-01",
    payingCardDetails: {
      cvv: "123",
      token: "token",
    },
    addressDetails: getTestAddressDetails(),
    brand: "Visa",
    ...overrides,
  };
};

const getTestAddressDetails = (
  overrides?: Partial<AddressDetails>
): AddressDetails => {
  return {
    houseNumber: "123",
    houseName: "Test House",
    addressLine1: "Test Address Line 1",
    addressLine2: "Test Address Line 2",
    city: "Test City",
    ...overrides,
  };
};
```

Key principles:

- Always return complete objects with sensible defaults
- Accept optional `Partial<T>` overrides
- Build incrementally - extract nested object factories as needed
- Compose factories for complex objects
- Consider using a test data builder pattern for very complex objects

## Validating Test Data

When schemas exist, validate factory output to catch test data issues early:

```typescript
import { PaymentSchema, type Payment } from '../schemas/payment.schema';

const getTestPayment = (overrides?: Partial<Payment>): Payment => {
  const basePayment = {
    amount: 100,
    currency: "GBP",
    cardId: "card_123",
    customerId: "cust_456",
  };

  const paymentData = { ...basePayment, ...overrides };

  // Validate against real schema to catch type mismatches
  return PaymentSchema.parse(paymentData);
};

// This catches errors in test setup:
const payment = getTestPayment({
  amount: -100  // ❌ Schema validation fails: amount must be positive
});
```

**Why validate test data:**

- Ensures test factories produce valid data that matches production schemas
- Catches test data bugs immediately rather than in test assertions
- Documents constraints (e.g., "amount must be positive") in schema, not in every test
- Prevents tests from passing with invalid data that would fail in production

## Anti-Patterns

### Testing Implementation Instead of Behavior

```typescript
// ❌ BAD - Implementation-focused test
it("should call validateAmount", () => {
  const spy = jest.spyOn(validator, 'validateAmount');
  processPayment(payment);
  expect(spy).toHaveBeenCalled();
});

// ✅ GOOD - Behavior-focused test
it("should reject payments with negative amounts", () => {
  const payment = getTestPayment({ amount: -100 });
  const result = processPayment(payment);
  expect(result.success).toBe(false);
  expect(result.error.message).toBe("Invalid amount");
});
```

### Shared Mutable State

```typescript
// ❌ BAD - Using let and beforeEach (shared mutable state)
let payment: Payment;
beforeEach(() => {
  payment = { amount: 100 };
});
it("should process payment", () => {
  processPayment(payment);
});

// ✅ GOOD - Factory functions (isolated, immutable)
it("should process payment", () => {
  const payment = getTestPayment({ amount: 100 });
  processPayment(payment);
});
```

### Spying on Internal Collaborators

```typescript
// ❌ BAD - Replacing something you own and control
jest.mock("./payment-validator");
it("should validate payment", () => {
  processPayment(payment);
  expect(validatePayment).toHaveBeenCalled();
});

// ✅ GOOD - Test the outcome, not the wiring
it("should reject invalid payment", () => {
  const result = processPayment(invalidPayment);
  expect(result.success).toBe(false);
});
```

### Replacing What You Don't Own Directly

```typescript
// ❌ BAD - Replacing a third-party library directly
jest.mock("axios");
(axios.get as jest.Mock).mockResolvedValue({ data: testData });

// ✅ GOOD - Create your own abstraction
interface HttpClient {
  get<T>(url: string): Promise<T>;
}

// Unit test: stub or spy on HttpClient
// Integration test: prove AxiosHttpClient works with real HTTP
```

## Achieving 100% Coverage Through Business Behavior

Example showing how validation code gets 100% coverage without testing it directly:

```typescript
// payment-validator.ts (implementation detail)
export const validatePaymentAmount = (amount: number): boolean => {
  return amount > 0 && amount <= 10000;
};

export const validateCardDetails = (card: PayingCardDetails): boolean => {
  return /^\d{3,4}$/.test(card.cvv) && card.token.length > 0;
};

// payment-processor.ts (public API)
export const processPayment = (
  request: PaymentRequest
): Result<Payment, PaymentError> => {
  if (!validatePaymentAmount(request.amount)) {
    return { success: false, error: new PaymentError("Invalid amount") };
  }

  if (!validateCardDetails(request.payingCardDetails)) {
    return { success: false, error: new PaymentError("Invalid card details") };
  }

  return { success: true, data: executedPayment };
};

// payment-processor.test.ts - achieves 100% coverage of validator
describe("Payment processing", () => {
  it("should reject payments with negative amounts", () => {
    const payment = getTestPaymentRequest({ amount: -100 });
    const result = processPayment(payment);

    expect(result.success).toBe(false);
    expect(result.error.message).toBe("Invalid amount");
  });

  it("should reject payments exceeding maximum amount", () => {
    const payment = getTestPaymentRequest({ amount: 10001 });
    const result = processPayment(payment);

    expect(result.success).toBe(false);
    expect(result.error.message).toBe("Invalid amount");
  });

  it("should reject payments with invalid CVV format", () => {
    const payment = getTestPaymentRequest({
      payingCardDetails: { cvv: "12", token: "valid-token" },
    });
    const result = processPayment(payment);

    expect(result.success).toBe(false);
    expect(result.error.message).toBe("Invalid card details");
  });

  it("should process valid payments successfully", () => {
    const payment = getTestPaymentRequest({
      amount: 100,
      payingCardDetails: { cvv: "123", token: "valid-token" },
    });
    const result = processPayment(payment);

    expect(result.success).toBe(true);
    expect(result.data.status).toBe("completed");
  });
});
```

## React Component Testing

Test user-visible behavior, not component internals:

```typescript
describe("PaymentForm", () => {
  it("should show error when submitting invalid amount", async () => {
    render(<PaymentForm />);

    const amountInput = screen.getByLabelText("Amount");
    const submitButton = screen.getByRole("button", { name: "Submit Payment" });

    await userEvent.type(amountInput, "-100");
    await userEvent.click(submitButton);

    expect(screen.getByText("Amount must be positive")).toBeInTheDocument();
  });

  it("should call onSuccess when payment completes", async () => {
    const onSuccess = jest.fn();
    render(<PaymentForm onSuccess={onSuccess} />);

    await userEvent.type(screen.getByLabelText(/amount/i), "100");
    await userEvent.click(screen.getByRole("button", { name: /submit payment/i }));

    await waitFor(() => {
      expect(onSuccess).toHaveBeenCalledWith(expect.objectContaining({
        amount: 100,
        status: "completed",
      }));
    });
  });
});
```

See [E2E Testing](./e2e-testing.md) for Testing Library query priority, userEvent patterns, and accessibility testing.

## See Also

- [Test Doubles](./test-doubles.md) — Deep dive on mocks, stubs, spies, fakes; Classical vs Mockist TDD; solitary vs sociable tests
- [Integration Testing](./integration-testing.md) — Testcontainers patterns, MSW for HTTP stubbing, adapter testing strategies
- [E2E Testing](./e2e-testing.md) — Playwright best practices, Testing Library query priority, component testing patterns

## Authoritative Sources

- Martin Fowler: [Unit Test](https://martinfowler.com/bliki/UnitTest.html), [Test Double](https://martinfowler.com/bliki/TestDouble.html), [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- Kent C. Dodds: [Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details)
- Ian Cooper: [TDD, Where Did It All Go Wrong?](https://www.youtube.com/watch?v=EZ05e7EMOLM)
- Gerard Meszaros: [xUnit Patterns](http://xunitpatterns.com/)
- Vladimir Khorikov: [Unit Testing Principles, Practices, and Patterns](https://www.manning.com/books/unit-testing-principles-practices-and-patterns)
