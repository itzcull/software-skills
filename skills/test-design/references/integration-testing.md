# Integration Testing

Integration tests verify that your code honors contracts with things you don't control: databases, APIs, third-party libraries, queues, filesystems, and platform services. They complete the "don't double what you don't own directly" pattern.

## Purpose and Scope

Unit tests use test doubles at architectural boundaries. Integration tests use real dependencies to prove your adapters work:

| Test Level | What It Tests | What It Doubles |
|------------|---------------|---------------|
| Unit | Behavioral contracts within your system | External dependencies |
| Integration | Your code's contract with external systems | Prefer nothing; use protocol stubs only when real dependencies are impractical |

```typescript
// Unit test: use a spy for your abstraction
describe("PaymentProcessor (unit)", () => {
  it("should call gateway with correct amount", () => {
    const paymentGatewaySpy: PaymentGateway = {
      charge: jest.fn().mockResolvedValue({ success: true }),
    };
    const processor = new PaymentProcessor(paymentGatewaySpy);

    processor.charge(getTestPayment({ amount: 100 }));

    expect(paymentGatewaySpy.charge).toHaveBeenCalledWith(100, expect.any(String));
  });
});

// Integration test: prove the adapter works
describe("StripePaymentGateway (integration)", () => {
  it("should charge card via real Stripe API", async () => {
    const gateway = new StripePaymentGateway(stripeTestKey);
    const result = await gateway.charge(100, testCardToken);

    expect(result.success).toBe(true);
    expect(result.chargeId).toMatch(/^ch_/);
  });
});
```

## The Adapter Testing Pattern

Create an interface that belongs to your application, then prove your adapter implements it correctly:

```typescript
// 1. Define the interface in YOUR code
interface PaymentGateway {
  charge(amount: number, cardToken: string): Promise<ChargeResult>;
  refund(chargeId: string): Promise<RefundResult>;
}

// 2. Implement the adapter
class StripePaymentGateway implements PaymentGateway {
  constructor(private apiKey: string) {}

  async charge(amount: number, cardToken: string): Promise<ChargeResult> {
    const stripe = require("stripe")(this.apiKey);
    const charge = await stripe.charges.create({
      amount: amount * 100, // Stripe uses cents
      currency: "usd",
      source: cardToken,
    });
    return { success: true, chargeId: charge.id };
  }

  async refund(chargeId: string): Promise<RefundResult> {
    // Implementation
  }
}

// 3. Unit tests: use a stub or spy for the interface
describe("OrderProcessor with gateway spy", () => {
  it("should process payment", () => {
    const paymentGatewaySpy: PaymentGateway = {
      charge: jest.fn().mockResolvedValue({ success: true }),
    };
    const processor = new OrderProcessor(paymentGatewaySpy);

    const result = processor.checkout(getTestOrder());

    expect(result.status).toBe("paid");
    expect(paymentGatewaySpy.charge).toHaveBeenCalled();
  });
});

// 4. Integration tests: prove the adapter
describe("StripePaymentGateway integration", () => {
  it("should complete charge flow", async () => {
    const gateway = new StripePaymentGateway(process.env.STRIPE_TEST_KEY);

    const result = await gateway.charge(100, "tok_test_card");

    expect(result.success).toBe(true);
    expect(result.chargeId).toBeDefined();

    // Clean up
    await gateway.refund(result.chargeId);
  });
});
```

## Testcontainers Best Practices

Testcontainers provides real Docker containers for integration testing.

Use containers when dependency behavior matters: SQL constraints, transaction isolation, migrations, broker semantics, Redis expiry, object storage behavior, or version-specific quirks. Prefer a fake only when its behavior is intentionally small and contract-tested against the real adapter.

### Core Principles

| Practice | Rationale | Example |
|----------|-----------|---------|
| **Dynamic ports** | Avoid conflicts in parallel runs | `getMappedPort(5432)` |
| **Dynamic host** | Works with remote Docker | `container.getHost()` |
| **Copy files, don't mount** | Works with remote Docker | `withCopyFileToContainer()` |
| **Production versions** | Catch version-specific bugs | `"postgres:16-alpine"` |
| **WaitStrategies** | More reliable than `sleep()` | `waitingFor(Wait.forLogMessage(...))` |

### Node.js Example

```typescript
import { GenericContainer, PostgreSQLContainer } from "@testcontainers/postgresql";

describe("PaymentRepository integration", () => {
  let container: PostgreSQLContainer;
  let repository: PaymentRepository;

  beforeAll(async () => {
    container = new PostgreSQLContainer("postgres:16-alpine")
      .withDatabase("testdb")
      .withUsername("test")
      .withPassword("test");

    await container.start();

    const connectionString = container.getConnectionUri();
    repository = new PaymentRepository(connectionString);
  });

  afterAll(async () => {
    await container.stop();
  });

  it("should persist and retrieve payment", async () => {
    const payment = getTestPayment({ id: "pay_test_1" });

    await repository.save(payment);
    const retrieved = await repository.findById("pay_test_1");

    expect(retrieved).toEqual(payment);
  });
});
```

### Anti-Patterns to Avoid

```typescript
// ❌ BAD - Fixed port causes conflicts
const postgres = new PostgreSQLContainer("postgres:latest")
  .withExposedPorts(5432);
const url = "jdbc:postgresql://localhost:5432/test";

// ✅ GOOD - Dynamic port
const postgres = new PostgreSQLContainer("postgres:16-alpine");
await postgres.start();
const url = postgres.getJdbcUrl();
const port = postgres.getMappedPort(5432);

// ❌ BAD - Hardcoded hostname breaks with remote Docker
registry.add("spring.redis.host", () => "localhost");

// ✅ GOOD - Dynamic host
registry.add("spring.redis.host", () => redis.getHost());

// ❌ BAD - Mounting local files fails with remote Docker
.withFileSystemBind("schema.sql", "/docker-entrypoint-initdb.d/");

// ✅ GOOD - Copying files works everywhere
.withCopyFileToContainer(
  MountableFile.forClasspathResource("schema.sql"),
  "/docker-entrypoint-initdb.d/"
);

// ❌ BAD - Using 'latest' causes flakiness
new PostgreSQLContainer("postgres:latest");

// ✅ GOOD - Pin to production version
new PostgreSQLContainer("postgres:16-alpine");

// ❌ BAD - Sleeping for readiness is unreliable
container.start();
await new Promise(r => setTimeout(r, 5000)); // Hope it's ready

// ✅ GOOD - Wait for specific readiness signal
container = new GenericContainer("redis:7-alpine")
  .withExposedPorts(6379)
  .waitingFor(Wait.forLogMessage("Ready to accept connections"));
```

### Container Lifecycle

```typescript
// Static container - shared across tests in one class
describe("PaymentRepository", () => {
  let container: PostgreSQLContainer;

  beforeAll(async () => {
    container = new PostgreSQLContainer("postgres:16-alpine");
    await container.start();
  });

  afterAll(async () => {
    await container.stop(); // Cleanup after all tests
  });

  it("test one", () => { /* uses container */ });
  it("test two", () => { /* uses container */ });
});

// Dynamic container - one per test (more isolation, slower)
describe("OrderRepository", () => {
  let container: PostgreSQLContainer;

  beforeEach(async () => {
    container = new PostgreSQLContainer("postgres:16-alpine");
    await container.start();
  });

  afterEach(async () => {
    await container.stop(); // Cleanup after each test
  });

  it("test one", () => { /* fresh container */ });
  it("test two", () => { /* fresh container */ });
});
```

## Database Testing Patterns

### Transaction Rollback

Rollback transactions after each test for fast, isolated tests:

```typescript
describe("PaymentRepository", () => {
  let repository: PaymentRepository;
  let db: Pool;

  beforeAll(async () => {
    db = await createTestDatabase();
    repository = new PaymentRepository(db);
  });

  beforeEach(async () => {
    await db.query("BEGIN");
  });

  afterEach(async () => {
    await db.query("ROLLBACK"); // Undo all changes
  });

  afterAll(async () => {
    await db.end();
  });

  it("should find payment by ID", async () => {
    await db.query("INSERT INTO payments (id, amount) VALUES ('pay_1', 100)");

    const payment = await repository.findById("pay_1");

    expect(payment.amount).toBe(100);
    // Rollback undoes the INSERT
  });
});
```

### Per-Test Data Isolation

For tests that need to run in parallel:

```typescript
// Unique data per test
const getUniquePayment = (testId: string) =>
  getTestPayment({
    id: `pay_${testId}_${Date.now()}`,
    description: `Test payment for ${testId}`,
  });

describe("PaymentRepository parallel", () => {
  it("should handle concurrent payments", async () => {
    const payment1 = getUniquePayment("concurrent_1");
    const payment2 = getUniquePayment("concurrent_2");

    await Promise.all([
      repository.save(payment1),
      repository.save(payment2),
    ]);

    expect(await repository.findById(payment1.id)).toBeDefined();
    expect(await repository.findById(payment2.id)).toBeDefined();
  });
});
```

## HTTP Stubbing with MSW

MSW (Mock Service Worker) intercepts requests at the network level, not the module level.

MSW is a protocol-level stub. It is usually better than mocking an HTTP client module because application code still performs a real request through its normal networking path.

### Why MSW Over Module-Level Doubles?

| Aspect | Module-level double | MSW |
|--------|---------------|-----|
| **Works with any HTTP client** | No — only works with replaced module | Yes |
| **Works in Storybook** | No | Yes |
| **Works in browser dev tools** | No | Yes |
| **Tests real network flow** | No | Yes |

### Basic Setup

```typescript
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

const server = setupServer(
  http.get("/api/payments/:id", ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      amount: 100,
      status: "completed",
    });
  }),
  http.post("/api/payments", async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: "pay_new_123", ...body },
      { status: 201 }
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Usage in Tests

```typescript
// Component test with MSW
describe("PaymentList component", () => {
  it("should display payments from API", async () => {
    render(<PaymentList />);

    expect(await screen.findByText("pay_new_123")).toBeInTheDocument();
  });

  it("should handle API error", async () => {
    // Override handler for this test
    server.use(
      http.get("/api/payments/:id", () => {
        return new HttpResponse(null, { status: 500 });
      })
    );

    render(<PaymentList />);

    expect(await screen.findByText("Failed to load payments")).toBeInTheDocument();
  });
});
```

### Reusing Handlers

```typescript
// handlers.ts - shared across tests, Storybook, and dev
export const paymentHandlers = [
  http.get("/api/payments/:id", async ({ params }) => {
    const payment = await db.payments.find(params.id);
    if (!payment) {
      return new HttpResponse(null, { status: 404 });
    }
    return HttpResponse.json(payment);
  }),
  http.post("/api/payments", async ({ request }) => {
    const body = await request.json();
    const created = await db.payments.create(body);
    return HttpResponse.json(created, { status: 201 });
  }),
];

// test/setup.ts
import { setupServer } from "msw/node";
import { paymentHandlers } from "../handlers";

export const server = setupServer(...paymentHandlers);

// test/payments.test.ts
import { server } from "./setup";
import { http, HttpResponse } from "msw";

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Override for specific test
server.use(
  http.get("/api/payments/:id", () => {
    return HttpResponse.json({ id: "stubbed", amount: 999 });
  })
);
```

## Consumer-Driven Contract Testing

Use contract tests when the dependency is a separately deployed service and local mocks could drift from provider reality.

Traditional stubs and mocks encode the consumer team's assumptions. If the provider changes a field name, status code, required header, or error shape, consumer unit tests can still pass because the double keeps returning the old shape. Consumer-driven contract testing turns those assumptions into an executable artifact verified by the provider.

| Test Type | What It Proves | Main Risk |
|---|---|---|
| Unit test with stub | Consumer behavior for a local response shape | Stub can drift from provider |
| Provider integration test | Provider works for its own examples | May miss consumer-specific needs |
| Consumer-driven contract test | Provider satisfies the consumer's expected protocol | Requires broker/process discipline |

### Pact-Style Flow

1. Consumer test runs against a local mock provider supplied by the contract framework.
2. The framework records the request and expected response as a contract.
3. The contract is published to a broker or shared artifact store.
4. Provider CI verifies the contract against the real provider implementation.
5. Breaking provider changes fail before deployment.

### When to Use Contract Tests

- A service boundary crosses team, repository, or deployment boundaries
- An API has multiple consumers with different expectations
- A mock or MSW handler duplicates provider response schemas that change often
- Full E2E coverage would be too slow, flaky, or expensive

### When Not to Use Contract Tests

- The provider and consumer are deployed as one unit
- The boundary is already covered by a cheap integration test against the real dependency
- The API shape is trivial and stable enough that contract infrastructure adds more cost than confidence

## Message Queue Testing

### Kafka Testing

```typescript
import { KafkaContainer } from "@testcontainers/kafka";

describe("OrderProcessor with Kafka", () => {
  let kafkaContainer: KafkaContainer;
  let producer: KafkaProducer;
  let consumer: KafkaConsumer;

  beforeAll(async () => {
    kafkaContainer = new KafkaContainer("confluentinc/cp-kafka:7.5.0")
      .withExposedPorts(9092);

    await kafkaContainer.start();

    producer = new KafkaProducer({
      bootstrapServers: `${kafkaContainer.getHost()}:${kafkaContainer.getMappedPort(9092)}`,
    });
  });

  afterAll(async () => {
    await kafkaContainer.stop();
  });

  it("should publish event when order is processed", async () => {
    const orderCreated = new OrderCreatedEvent({ orderId: "order_123" });

    await producer.send({
      topic: "order-events",
      messages: [{ value: JSON.stringify(orderCreated) }],
    });

    const messages = await consumer.consume("order-events");
    expect(messages[0].value.orderId).toBe("order_123");
  });
});
```

## File System Testing

For code that reads/writes files, use in-memory filesystems:

```typescript
import { memfs } from "memfs";

describe("ReportGenerator", () => {
  const { fs, volume } = memfs();

  beforeEach(() => {
    volume.reset();
  });

  it("should write report to file", async () => {
    const generator = new ReportGenerator({ fs }); // Inject filesystem

    await generator.generateReport("sales_2024.csv", { total: 50000 });

    const exists = fs.existsSync("/reports/sales_2024.csv");
    expect(exists).toBe(true);

    const content = fs.readFileSync("/reports/sales_2024.csv", "utf-8");
    expect(content).toContain("50000");
  });
});
```

## Environment-Safe Testing

Never use real credentials in tests:

```typescript
// ❌ BAD - Real credentials in tests
const stripe = new Stripe("sk_live_123...");

// ✅ GOOD - Test credentials and environment isolation
const stripe = new Stripe(process.env.STRIPE_TEST_KEY || "sk_test_mock");

// Use test-specific setup
beforeAll(() => {
  process.env.STRIPE_TEST_KEY = "sk_test_fake_key";
});

afterAll(() => {
  delete process.env.STRIPE_TEST_KEY;
});
```

## Speed Considerations

Integration tests are slower than unit tests. Optimize where possible:

| Strategy | Impact |
|----------|--------|
| Reuse containers across tests | 10-100x faster |
| Use in-memory databases only when semantics do not matter | 10-50x faster |
| Parallelize independent test files | Linear with worker count |
| Skip integration tests on fast commits | Faster feedback loop |

```typescript
// Reuse container across test suite
const globalPostgres = new PostgreSQLContainer("postgres:16-alpine");

// Singleton pattern
const getPostgres = (() => {
  let container: PostgreSQLContainer | null = null;
  return async () => {
    if (!container) {
      container = new PostgreSQLContainer("postgres:16-alpine");
      await container.start();
    }
    return container;
  };
})();

describe("Integration tests", () => {
  beforeAll(async () => {
    const container = await getPostgres();
    // Setup database schema
  });
});
```

## When to Skip Integration Tests

Integration tests add complexity. Skip when:

- The adapter is trivial (e.g., HTTP client wrapper)
- The external system has comprehensive integration tests
- The cost of infrastructure outweighs the risk
- A unit test with a stub or spy provides sufficient coverage
- A consumer-driven contract test already verifies the remote protocol risk

## See Also

- [Test Doubles](./test-doubles.md) — Test double taxonomy and usage patterns
- [E2E Testing](./e2e-testing.md) — Browser and component testing
- [Testcontainers Node.js Guide](https://testcontainers.com/guides/getting-started-with-testcontainers-for-nodejs/)
- [MSW Documentation](https://mswjs.io/docs/)
- [Testcontainers Best Practices](https://www.docker.com/blog/testcontainers-best-practices/)
