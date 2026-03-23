# Design & Architecture

Category 14 -- Are structural decisions sound?

## Subcategories

- **Violation of SOLID principles** -- single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion
- **Missing design patterns** -- a well-known pattern would simplify the code but is not used
- **Over-engineering** -- unnecessary abstractions, premature generalisation, speculative features
- **Incorrect abstraction level** -- mixing high-level orchestration with low-level implementation details
- **Missing separation of concerns** -- business logic mixed with UI rendering, persistence, or transport
- **Tight coupling to implementation details** -- depending on concrete classes or specific library APIs where an abstraction is warranted
- **God objects** -- objects that know too much or do too much, concentrating system knowledge
- **Wrong architectural layer** -- logic placed in the wrong layer (e.g. validation in the UI, business rules in the database layer)
- **Missing domain modelling** -- using primitives or generic structures where domain types (value objects, entities) would be clearer
- **Premature optimisation architecture** -- building for scale or performance problems that do not exist yet

## What to Look For

- Classes or modules with more than one clear responsibility (ask: "what could change that would require modifying this?")
- Business logic inside HTTP handlers, React components, or database repositories
- Direct use of third-party library types in domain code (framework coupling)
- Abstract base classes or interfaces with only one implementation and no prospect of others
- Factory classes, builders, or strategies introduced for a single use case
- Domain concepts modelled as raw strings, numbers, or plain objects instead of typed domain objects
- Shared mutable state used to communicate between modules instead of explicit dependencies
- New modules that duplicate the responsibility of existing modules
- Inheritance hierarchies deeper than 2 levels
- Configuration or feature flags that control entirely different code paths (suggests two separate features)

## Positive Example

```typescript
// Clear separation: handler orchestrates, domain logic is independent
async function handleCreateOrder(req: Request): Promise<Response> {
  const input = CreateOrderSchema.parse(req.body);
  const order = createOrder(input);
  const saved = await orderRepository.save(order);
  return Response.json(toOrderResponse(saved), { status: 201 });
}
```

The handler parses input, delegates to domain logic, persists, and maps the response. Business logic in `createOrder` has no HTTP or database awareness.

## Negative Example

```typescript
// ARCHITECTURE: business logic, persistence, HTTP, and formatting all mixed
async function handleCreateOrder(req: Request): Promise<Response> {
  const body = req.body;
  if (!body.items || body.items.length === 0) {
    return new Response(JSON.stringify({ error: "No items" }), { status: 400 });
  }
  let total = 0;
  for (const item of body.items) {
    const product = await db.query(`SELECT price FROM products WHERE id = ${item.id}`);
    total += product.price * item.quantity;
  }
  if (total > 10000) total *= 0.95; // 5% discount
  await db.query(`INSERT INTO orders (total, items) VALUES (${total}, '${JSON.stringify(body.items)}')`);
  return new Response(JSON.stringify({ total: `$${total.toFixed(2)}` }), { status: 200 });
}
```

Validation, price calculation, discount logic, SQL queries (with injection), and response formatting are all in one function. Every concern is entangled.

## Common False Positives

- Simple CRUD applications where layered architecture adds complexity without value
- Prototype or spike code that is intentionally minimal and will be replaced
- Single-implementation interfaces that exist to satisfy dependency injection for testing (legitimate use)
- Small microservices where a flat structure is appropriate for the scope
- Over-engineering complaints about reasonable abstractions that have already proven their value

## Severity Guide

| Severity | When |
|---|---|
| Critical | Architectural decision that will be very expensive to reverse later (wrong database choice, wrong service boundary) |
| Major | Business logic mixed with infrastructure; god object at the centre of the system; missing separation of concerns in a growing codebase |
| Minor | Slight over-engineering; missing domain type for a concept used in 2-3 places; suboptimal pattern choice |
| Nitpick | Preference for one valid architectural approach over another |

## Related Categories

- [Code Structure & Organisation](code-structure-and-organisation.md) -- structural issues at the function level; architectural issues at the system level
- [API & Interface](api-and-interface.md) -- interface design is an architectural concern
- [Testing](testing.md) -- poor architecture makes testing difficult
- [Security](security.md) -- missing separation of concerns can expose internal details
