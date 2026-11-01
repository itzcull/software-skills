# TDD Workflow

## TDD Process - THE FUNDAMENTAL PRACTICE

**CRITICAL**: TDD is not optional. Every feature, every bug fix, every change MUST follow this process:

Follow Red-Green-Refactor strictly:

1. **Red**: Write a failing test for the desired behavior. NO PRODUCTION CODE until you have a failing test.
2. **Green**: Write the MINIMUM code to make the test pass. Resist the urge to write more than needed.
3. **Refactor**: Assess the code for improvement opportunities. If refactoring would add value, clean up the code while keeping tests green. If the code is already clean and expressive, move on.

**Common TDD Violations to Avoid:**

- Writing production code without a failing test first
- Writing multiple tests before making the first one pass
- Writing more production code than needed to pass the current test
- Skipping the refactor assessment step when code could be improved
- Adding functionality "while you're there" without a test driving it

**Remember**: If you're typing production code and there isn't a failing test demanding that code, you're not doing TDD.

## TDD Quality Gates

Before allowing any commit, verify:

- All production code has a test that demanded it
- Tests verify behavior, not implementation
- Implementation is minimal (only what's needed)
- Refactoring assessment completed (if tests green)
- All tests pass
- TypeScript strict mode satisfied
- No `any` types or unjustified assertions
- Factory functions used (no `let`/`beforeEach`)

## Verifying TDD Compliance Retrospectively

To verify that code was developed test-first, examine git history:

```bash
# Check if test was written before implementation
git log -p --follow src/features/payment/payment-processor.ts
git log -p --follow src/features/payment/payment-processor.test.ts

# Look for:
# GOOD: Test commit comes BEFORE implementation commit
# BAD: Implementation committed without corresponding test
# BAD: Test and implementation in same commit without clear RED phase
```

**During code review, check:**

- Was there a failing test before each production code change?
- Do commit messages indicate RED-GREEN-REFACTOR progression?
- Are refactoring commits separate from feature commits?

**Example good commit sequence:**

```
feat(test): add test for payment validation (RED)
feat: implement payment validation (GREEN)
refactor: extract payment validation constants (REFACTOR)
```

**Example bad commit sequence:**

```
feat: add payment validation with tests
```

(Combined test+implementation suggests test wasn't written first)

## TDD Example Workflow

```typescript
// Step 1: Red - Start with the simplest behavior
describe("Order processing", () => {
  it("should calculate total with shipping cost", () => {
    const order = createOrder({
      items: [{ price: 30, quantity: 1 }],
      shippingCost: 5.99,
    });

    const processed = processOrder(order);

    expect(processed.total).toBe(35.99);
    expect(processed.shippingCost).toBe(5.99);
  });
});

// Step 2: Green - Minimal implementation
const processOrder = (order: Order): ProcessedOrder => {
  const itemsTotal = order.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );

  return {
    ...order,
    shippingCost: order.shippingCost,
    total: itemsTotal + order.shippingCost,
  };
};

// Step 3: Red - Add test for free shipping behavior
describe("Order processing", () => {
  it("should apply free shipping for orders over 50", () => {
    const order = createOrder({
      items: [{ price: 60, quantity: 1 }],
      shippingCost: 5.99,
    });

    const processed = processOrder(order);

    expect(processed.shippingCost).toBe(0);
    expect(processed.total).toBe(60);
  });
});

// Step 4: Green - Add the conditional
const processOrder = (order: Order): ProcessedOrder => {
  const itemsTotal = order.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  );

  const shippingCost = itemsTotal > 50 ? 0 : order.shippingCost;

  return {
    ...order,
    shippingCost,
    total: itemsTotal + shippingCost,
  };
};

// Step 5: Add edge case tests
// Step 6: Refactor - Extract constants and improve readability
const FREE_SHIPPING_THRESHOLD = 50;

const calculateItemsTotal = (items: OrderItem[]): number => {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
};

const qualifiesForFreeShipping = (itemsTotal: number): boolean => {
  return itemsTotal > FREE_SHIPPING_THRESHOLD;
};

const processOrder = (order: Order): ProcessedOrder => {
  const itemsTotal = calculateItemsTotal(order.items);
  const shippingCost = qualifiesForFreeShipping(itemsTotal)
    ? 0
    : order.shippingCost;

  return {
    ...order,
    shippingCost,
    total: itemsTotal + shippingCost,
  };
};
```

## Refactoring - The Critical Third Step

Evaluating refactoring opportunities is not optional - it's the third step in the TDD cycle. After achieving a green state and committing your work, you MUST assess whether the code can be improved. However, only refactor if there's clear value.

### Refactoring Priority Classification

**Critical (Fix Now Before Commit):**
- Immutability violations (mutations)
- Semantic knowledge duplication (same business rule in multiple places)
- Deeply nested code (>3 levels)
- Security issues or data leak risks

**High Value (Should Fix This Session):**
- Unclear names affecting comprehension
- Magic numbers/strings used multiple times
- Long functions (>30 lines) with multiple responsibilities
- Missing constants for important business rules

**Nice to Have (Consider Later):**
- Minor naming improvements
- Extraction of single-use helper functions
- Structural reorganisation that doesn't improve clarity

**Skip Refactoring:**
- Code that's already clean and expressive
- Structural similarity without semantic relationship
- Changes that would make code less clear
- Abstractions that aren't yet proven necessary

### Refactoring Guidelines

1. **Commit before refactoring** - safe rollback point
2. **Abstract based on semantic meaning** - not structural similarity
3. **DRY is about knowledge, not code** - duplicate code is cheaper than wrong abstraction
4. **Maintain external APIs** - refactoring must never break consumers
5. **Verify and commit after** - all tests pass, then separate commit

### Decision Framework: Should I Abstract This Duplication?

1. **Semantic Check**: Same business concept or just similar structure?
2. **Evolution Check**: If rules change for one, should others change too?
3. **Comprehension Check**: Would a developer understand the grouping?
4. **Coupling Check**: Abstracting based on meaning or structure?

**Remember:** Duplicate code is far cheaper than the wrong abstraction. When in doubt, wait for a third instance to confirm the pattern.

### Refactoring Assessment Pattern

After every green test, explicitly assess:

1. **Naming**: Are variable/function names clear?
2. **Magic values**: Are constants extracted where needed?
3. **Structure**: Is complexity manageable (nesting <=2, function <30 lines)?
4. **Duplication**: Is knowledge (not just code) repeated?
5. **Purity**: Are functions pure where possible?

If all satisfied: **No refactoring needed, commit and move on**
If issues found: Classify priority and refactor if high value
