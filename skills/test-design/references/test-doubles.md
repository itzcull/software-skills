# Test Doubles: Deep Dive

Test doubles replace real objects in tests. This document covers the precise taxonomy, when to use each type, and the philosophical approaches to collaborator replacement.

## The Two Test Failures

Understanding what makes a test valuable starts with understanding how tests can fail:

| Failure Type | What Happens | Why It Matters |
|--------------|--------------|----------------|
| **False Positive** | Test passes, but code is broken | Bugs reach production |
| **False Negative** | Test fails, but code works | Wasted debugging time |

> "A test should fail if and only if the code no longer does what it promises to do." — Testing Core Truth

Tests that fail for reasons unrelated to behavior (implementation changes, refactoring) create **false negatives** — they signal problems that don't exist. Tests that pass when code is broken create **false positives** — they provide false confidence.

The principles in this document help minimize both.

## Taxonomy of Test Doubles

Based on Gerard Meszaros's *xUnit Patterns*:

Use the taxonomy as domain language for test design. Many frameworks call every generated double a "mock", but the design role still matters: a double may be stubbing an indirect input, faking a collaborator, spying on an indirect output, or enforcing mock expectations. Name the role and verb, not just the tool primitive.

| Term | Role | Failure behavior |
|---|---|---|
| Dummy | Satisfies a required parameter that is not exercised | Does not participate in failure except through type/signature errors |
| Stub | Returns controlled values or exceptions as indirect inputs | Does not assert arguments or deliberately fail the test |
| Fake | Provides a lightweight working implementation of a real collaborator | Fails only through normal behavior; should be protected by contract tests when drift matters |
| Spy | Records indirect outputs for later assertions | Does not fail by itself; the assert phase checks recorded calls |
| Mock | Enforces pre-declared expectations about interactions | Can fail during the act phase when expectations are violated |

### Dummy Objects

**Definition**: Objects passed to the code under test but never actually used. They exist only to satisfy type signatures.

**When to use**: Filling parameter lists when the parameter isn't exercised in the test.

```typescript
// A logger that implements the interface but is never called
const dummyLogger: Logger = {
  info: () => {},
  error: () => {},
  warn: () => {},
};

processPayment(paymentData, dummyLogger);
```

**Anti-pattern**: Creating dummies when you could use null/undefined if the type allows.

### Fake Objects

**Definition**: Lightweight working implementations of collaborators that behave like the real object but omit production qualities such as persistence, scale, stability, or infrastructure.

**When to use**: When you need realistic behavior but the real dependency is too heavy, slow, unstable, persistent, or external.

```typescript
// In-memory database - works like a real DB but without persistence
class InMemoryPaymentRepository implements PaymentRepository {
  private payments = new Map<string, Payment>();

  async save(payment: Payment): Promise<void> {
    this.payments.set(payment.id, payment);
  }

  async findById(id: string): Promise<Payment | null> {
    return this.payments.get(id) || null;
  }

  async findByCustomerId(customerId: string): Promise<Payment[]> {
    return Array.from(this.payments.values()).filter(
      (p) => p.customerId === customerId
    );
  }
}

// Usage in tests - fast, in-memory, no external dependencies
const repo = new InMemoryPaymentRepository();
const payment = await repo.findById("pay_123");
```

**When fakes are the best choice**:
- In-memory databases for repository tests
- Simple in-memory event buses
- Fake clock for time-dependent tests

**Risk**: Fakes can drift from real behavior. Use contract tests (same test suite run against both fake and real implementations).

### Stub Objects

**Definition**: Implement an interface to control indirect inputs by returning specific hard-coded values or throwing specific exceptions. Stubs do not check whether particular arguments were passed and do not deliberately fail the test.

**When to use**: When the code under test needs a controlled response from a collaborator to proceed.

```typescript
// Stub provides predefined responses
const paymentValidatorStub: PaymentValidator = {
  validateAmount: (amount) => amount > 0 && amount <= 10000,
  validateCard: (card) => card.cvv.length === 3,
};

// The processor calls these stubs to get answers
const result = processPayment(paymentData, paymentValidatorStub);
```

**Spies that also stub a response**:

```typescript
// Spy records the outgoing call and also returns a controlled response
class SpyPaymentGateway implements PaymentGateway {
  charges: Array<{ amount: number; cardToken: string }> = [];

  async charge(amount: number, cardToken: string): Promise<ChargeResult> {
    this.charges.push({ amount, cardToken });
    return { success: true, chargeId: "ch_mock" };
  }
}

const gateway = new SpyPaymentGateway();
await processPayment(payment, gateway);

// Verify the recorded indirect output
expect(gateway.charges).toHaveLength(1);
expect(gateway.charges[0].amount).toBe(100);
```

### Spy Objects

**Definition**: Test doubles that can do what stubs do and also record indirect outputs from the system under test. Spies capture method calls and arguments so the assert phase can verify the interaction.

**When to use**: When the observable outcome is an outgoing interaction, such as an email sent, event published, metric recorded, or external command issued.

```typescript
// Spy records calls
const emailServiceSpy = {
  sentEmails: [] as Email[],
  async send(email: Email) {
    this.sentEmails.push(email);
  },
};

await orderProcessor.process(order);

// Verify through spy
expect(emailServiceSpy.sentEmails).toHaveLength(1);
expect(emailServiceSpy.sentEmails[0].to).toBe("customer@example.com");
```

**Built-in Jest/Vitest spy**:

```typescript
const emailService = {
  send: jest.fn().mockResolvedValue(undefined),
};

await processOrder(order);

// Use framework call-recording helpers to verify the spy role
expect(emailService.send).toHaveBeenCalledTimes(1);
expect(emailService.send).toHaveBeenCalledWith({
  to: "customer@example.com",
  subject: "Order confirmed",
});
```

### Mock Objects

**Definition**: Pre-programmed with strict expectations about which calls they will receive. A mock is like a trigger-happy spy: it can fail the test on its own during the act phase if expectations are not met.

**Key distinction**: Spies record interactions for later assertions. Mocks enforce expectations that were declared before the system under test acts.

```typescript
// Jest mock functions often play a stub or spy role.
const paymentGateway = {
  charge: jest.fn().mockResolvedValue({ success: true }),
};

await processPayment(payment, paymentGateway);

// This is not a mock in the Meszaros taxonomy: it records a call for later
// assertion, so it is acting as a spy. Strict mocks pre-declare expectations.
```

**Traditional mock object framework pattern** (jMock/EasyMock style):

```typescript
// Not idiomatic Jest/Vitest, but illustrates the pattern
it("should call email service with confirmation", () => {
  const context = new Mockery();
  const emailService = context.mock("EmailService");

  context.expects()
    .once()
    .method(emailService, "send")
    .with(order.email, "confirmation");

  const processor = new OrderProcessor(emailService);
  processor.process(order);

  context.assertIsSatisfied();
});
```

## State vs Behavior Verification

### State Verification

Verify by examining the state of the system after the operation.

```typescript
// State verification - check the outcome
it("should reduce inventory after purchase", () => {
  const inventory = { widgets: 10 };
  const processor = new PurchaseProcessor(inventory);

  processor.buy("widget", 5);

  expect(inventory.widgets).toBe(5); // Check state change
});
```

### Behavior Verification

Verify by checking that the system made the correct calls to collaborators.

```typescript
// Behavior verification - check the interaction
it("should notify warehouse after purchase", () => {
  const warehouse = { notifyPurchase: jest.fn() };
  const processor = new PurchaseProcessor(warehouse);

  processor.buy("widget", 5);

  expect(warehouse.notifyPurchase).toHaveBeenCalledWith("widget", 5);
});
```

| Aspect | State Verification | Behavior Verification |
|--------|-------------------|----------------------|
| **What it checks** | Final state | Method calls made |
| **Coupling** | Loose — doesn't care how | Tight — cares about which methods called |
| **Refactoring resilience** | Higher | Lower — can break if call patterns change |
| **Best for** | Checking results | Checking side effects |
| **Risk** | May need query methods | Brittle to implementation changes |

**Recommendation**: Prefer state verification when possible. Use behavior verification for side effects (notifications, API calls, writes to external systems).

## Classical vs Mockist TDD

Two philosophical schools of thought on when and how to use test doubles:

### Classical TDD (Detroit School)

**Approach**: Use real objects if possible. Use test doubles only for awkward collaborations.

> "A classical TDDer would use a real warehouse and a double for the mail service." — Martin Fowler

**Principles**:
- Use test doubles only at architectural boundaries (external systems)
- Within your system, use real collaborators
- Verify through state when possible

```typescript
// Classical style - use real collaborator
describe("OrderProcessor", () => {
  it("should calculate total correctly", () => {
    const pricingEngine = new PricingEngine(); // Real object
    const order = getTestOrder();

    const total = pricingEngine.calculateTotal(order);

    expect(total).toBe(150);
  });
});
```

### Mockist TDD (London School)

**Approach**: Replace all collaborators with test doubles. Mockist literature often calls all of those doubles "mocks", even when they are technically stubs or spies.

> "A mockist TDD practitioner will always use a mock for any object with interesting behavior." — Martin Fowler

**Principles**:
- Test behavior through interactions
- Each class is tested in isolation
- Use behavior verification

```typescript
// Mockist style - replace all collaborators with doubles
describe("OrderProcessor", () => {
  it("should calculate total using pricing engine", () => {
    const pricingEngine = {
      calculateTotal: jest.fn().mockReturnValue(150),
    };
    const order = getTestOrder();

    const total = new OrderProcessor(pricingEngine).calculateTotal(order);

    expect(pricingEngine.calculateTotal).toHaveBeenCalledWith(order);
    expect(total).toBe(150);
  });
});
```

### Comparison

| Aspect | Classical | Mockist |
|--------|-----------|---------|
| **Design guidance** | Middle-out | Outside-in |
| **Test coupling** | Loose to implementation | Tight to implementation |
| **Debugging** | Can have ripple failures | Failures are isolated |
| **Refactoring** | Tests survive changes | Tests may break |
| **Test scope** | Can test clusters | Single class focus |

### Martin Fowler's Assessment

> "Personally I've always been a classic TDDer... I really like the fact that while writing the test you focus on the result of the behavior, not how it's done. A mockist is constantly thinking about how the SUT is going to be implemented."

**Our recommendation**: Default to Classical TDD. Use test doubles only at architectural boundaries. Use behavior verification sparingly for side effects.

## Solitary vs Sociable Unit Tests

Another dimension of unit testing, named by Jay Fields:

### Sociable Unit Tests

**Definition**: Tests that use real implementations of collaborating classes.

```typescript
// Sociable - uses real PricingEngine
describe("OrderProcessor", () => {
  it("should apply discount correctly", () => {
    const pricingEngine = new PricingEngine(); // Real
    const discountCalculator = new DiscountCalculator(); // Real
    const processor = new OrderProcessor(pricingEngine, discountCalculator);

    const result = processor.process(getTestOrder());

    expect(result.discountApplied).toBe(true);
  });
});
```

### Solitary Unit Tests

**Definition**: Tests where collaborators are replaced by test doubles.

```typescript
// Solitary - collaborators replaced by test doubles
describe("OrderProcessor", () => {
  it("should apply discount correctly", () => {
    const pricingEngine = { calculateTotal: jest.fn() };
    const discountCalculator = { calculateDiscount: jest.fn().mockReturnValue(0.1) };
    const processor = new OrderProcessor(pricingEngine, discountCalculator);

    const result = processor.process(getTestOrder());

    expect(pricingEngine.calculateTotal).toHaveBeenCalled();
    expect(result.discountApplied).toBe(true);
  });
});
```

**When to use solitary tests**:
- When collaborators are awkward (external services, databases)
- When you want to isolate the class for debugging
- When testing error paths that are hard to trigger with real collaborators

**When to use sociable tests**:
- Default case
- When collaborators are simple and fast
- When testing integration between classes within a bounded context

## Anti-Patterns in Test Doubles

### Over-Doubling

**Problem**: Replacing every collaborator with a test double creates tests that model your assumptions rather than verify behavior.

```typescript
// ❌ BAD - Doubling everything, testing little
it("should process payment", () => {
  const gateway = { charge: jest.fn().mockResolvedValue({ success: true }) };
  const validator = { validate: jest.fn().mockReturnValue(true) };
  const logger = { log: jest.fn() };
  const notifier = { notify: jest.fn() };
  const metrics = { record: jest.fn() };

  const processor = new PaymentProcessor(gateway, validator, logger, notifier, metrics);
  const result = processor.process(getTestPayment());

  expect(result.success).toBe(true);
  expect(gateway.charge).toHaveBeenCalled();
  expect(validator.validate).toHaveBeenCalled();
  expect(logger.log).toHaveBeenCalled();
  expect(notifier.notify).toHaveBeenCalled();
  expect(metrics.record).toHaveBeenCalled();
});
```

**Solution**: Test behavior through public API. Don't verify every internal call.

```typescript
// ✅ GOOD - Test behavior, not implementation details
it("should reject payment with invalid card", () => {
  const gateway = { charge: jest.fn() }; // Minimal stub
  const processor = new PaymentProcessor(gateway, getTestValidator());

  const result = processor.process(getTestPayment({ cardNumber: "invalid" }));

  expect(result.success).toBe(false);
  expect(result.error.code).toBe("INVALID_CARD");
  // Don't verify internal calls - the public behavior is what matters
});
```

### Spying on Implementation Details

**Problem**: Tests couple to internal structure and break on refactoring.

```typescript
// ❌ BAD - Replacing an internal collaborator
jest.mock("./payment-validator");
import { validatePayment } from "./payment-validator";

it("should validate payment", () => {
  const processor = new PaymentProcessor();
  processor.process(getTestPayment());

  expect(validatePayment).toHaveBeenCalled();
});
```

**Solution**: Test through public API. If internal logic needs testing, it should be refactored to its own unit with its own tests.

### Stub Setup Complexity

**Problem**: Stub configuration becomes more complex than the test logic.

```typescript
// ❌ BAD - Complex stub setup obscures test intent
it("should process payment with tiered discount", () => {
  const pricingEngine = {
    calculateBasePrice: jest.fn().mockImplementation((items) => {
      if (items.length > 10) return 1000;
      if (items.length > 5) return 600;
      return 300;
    }),
    applyDiscount: jest.fn().mockImplementation((price, tier) => {
      if (tier === "gold") return price * 0.9;
      if (tier === "silver") return price * 0.95;
      return price;
    }),
    calculateTax: jest.fn().mockImplementation((price) => price * 0.08),
    formatPrice: jest.fn().mockImplementation((price) => `$${price.toFixed(2)}`),
  };
  // ... 30 more lines of stub setup
});
```

**Solution**: Use real objects when they're simple, or create a test fixture helper.

```typescript
// ✅ GOOD - Real object for simple logic
it("should apply gold tier discount", () => {
  const pricingEngine = new PricingEngine(); // Real object
  const order = getTestOrder({ items: [/* items */], tier: "gold" });

  const result = pricingEngine.calculateFinalPrice(order);

  expect(result.discount).toBe(0.1); // 10% gold discount
});
```

### Verification Overkill

**Problem**: Testing call counts and exact arguments when only outcome matters.

```typescript
// ❌ BAD - Over-verifying interactions
it("should process order", () => {
  const warehouse = { remove: jest.fn(), reserve: jest.fn() };
  const email = { send: jest.fn() };
  const metrics = { record: jest.fn(), start: jest.fn(), end: jest.fn() };
  const processor = new OrderProcessor(warehouse, email, metrics);

  processor.process(getTestOrder());

  expect(warehouse.remove).toHaveBeenCalledTimes(1);
  expect(warehouse.remove).toHaveBeenCalledWith("item-1", 2, "order-123");
  expect(warehouse.reserve).toHaveBeenCalledTimes(1);
  expect(email.send).toHaveBeenCalledTimes(1);
  expect(email.send).toHaveBeenCalledWith(
    expect.objectContaining({
      to: "customer@example.com",
      template: "order_confirmed",
    })
  );
  expect(metrics.record).toHaveBeenCalledWith("order_processed", 1500);
  expect(metrics.start).toHaveBeenCalledWith("order_processing");
  expect(metrics.end).toHaveBeenCalledWith("order_processing");
});
```

**Solution**: Verify outcomes, not every interaction.

```typescript
// ✅ GOOD - Verify outcomes, not interactions
it("should complete order and send confirmation", () => {
  const warehouse = { remove: jest.fn() }; // Stub
  const email = { send: jest.fn() }; // Spy
  const processor = new OrderProcessor(warehouse, email);

  const result = processor.process(getTestOrder());

  expect(result.status).toBe("completed");
  expect(warehouse.remove).toHaveBeenCalled(); // Only verify critical interaction
  expect(email.send).toHaveBeenCalledWith(
    expect.objectContaining({ to: "customer@example.com" })
  );
});
```

### Fakes Without Contract Tests

**Problem**: Fakes drift from real implementation behavior, giving false confidence.

```typescript
// ❌ BAD - Fake that doesn't match real behavior
class InMemoryUserRepository {
  private users = new Map<string, User>();

  async findByEmail(email: string): Promise<User | null> {
    // BUG: Returns first match, not exact match
    for (const user of this.users.values()) {
      if (user.email.includes(email)) return user;
    }
    return null;
  }

  // Real implementation does exact match
}

class PostgresUserRepository {
  async findByEmail(email: string): Promise<User | null> {
    return db.query("SELECT * FROM users WHERE email = $1", [email]);
  }
}

// Tests pass with fake, fail in production
```

**Solution**: Run the same test suite against both fake and real implementations.

```typescript
// ✅ GOOD - Contract tests ensure fake matches real
describeContract("UserRepository", (createRepo) => {
  it("should find user by exact email", async () => {
    const repo = await createRepo();
    await repo.save({ id: "1", email: "alice@example.com" });
    await repo.save({ id: "2", email: "bob@example.com" });

    const user = await repo.findByEmail("alice@example.com");

    expect(user?.id).toBe("1"); // Not bob!
  });
});

// Run with both implementations
describe("UserRepository (InMemory)", () =>
  describeContract("UserRepository", () => Promise.resolve(new InMemoryUserRepository())));

describe("UserRepository (Postgres)", () =>
  describeContract(
    "UserRepository",
    () => new PostgresUserRepository(db)
  ));
```

## Speed Expectations

Unit tests should be fast enough to support TDD:

| Context | Target Time | Source |
|---------|-------------|--------|
| Single test | < 10ms | Practical limit for TDD |
| Test file | < 100ms | Kent Beck's suggestion |
| Unit suite (100 tests) | < 1 second | Fast enough for instant feedback |
| Commit suite | < 10 minutes | Maximum acceptable |

**Why speed matters**:
- Slow tests → developers stop running them
- Slow tests → longer CI cycles
- Slow tests → break TDD flow

**Speed tips for double-heavy tests**:
- Use doubles at boundaries, not internally
- Use in-memory fakes for databases
- Parallelize independent test files

## See Also

- [Integration Testing](./integration-testing.md) — Testing adapters with real dependencies
- [E2E Testing](./e2e-testing.md) — Browser and component testing patterns
- [Martin Fowler: Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- [Martin Fowler: Test Double](https://martinfowler.com/bliki/TestDouble.html)
- [Gerard Meszaros: xUnit Patterns](http://xunitpatterns.com/)
