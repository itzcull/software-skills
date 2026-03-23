---
title: "Introduce Assertion"
description: "Add assertions to make code assumptions explicit and catch bugs early"
category: "Organization"
tags: ["assertion", "assumptions", "debugging", "documentation", "fail-fast"]
related: ["introduce-special-case", "decompose-conditional", "extract-function"]
---

# Introduce Assertion

Add assertions to make assumptions in the code explicit. This helps catch bugs early, documents expectations, and makes code more robust by failing fast when assumptions are violated.

## Motivation

Code often contains implicit assumptions that can cause subtle bugs:

- **Hidden assumptions**: Code assumes certain conditions without stating them
- **Silent failures**: Invalid states go undetected until they cause problems
- **Debugging difficulty**: Hard to identify where invalid states originate
- **Documentation gaps**: Assumptions aren't communicated to other developers
- **Regression risks**: Changes can violate assumptions without immediate feedback
- **Production mysteries**: Crashes happen with unclear root causes

## Example

### Basic Example
```javascript
// Before - Hidden assumptions
function calculateDiscount(customer, order) {
  // Hidden assumption: customer is not null
  // Hidden assumption: order has positive total
  // Hidden assumption: customer has loyalty level
  
  let discountRate = 0;
  
  if (customer.loyaltyLevel === 'gold') {
    discountRate = 0.15;
  } else if (customer.loyaltyLevel === 'silver') {
    discountRate = 0.10;
  } else if (customer.loyaltyLevel === 'bronze') {
    discountRate = 0.05;
  }
  
  return order.total * discountRate;
}

// After - Explicit assertions
function calculateDiscount(customer, order) {
  // Make assumptions explicit with assertions
  assert(customer !== null && customer !== undefined, 'Customer cannot be null or undefined');
  assert(order !== null && order !== undefined, 'Order cannot be null or undefined');
  assert(typeof order.total === 'number', 'Order total must be a number');
  assert(order.total >= 0, 'Order total cannot be negative');
  assert(customer.loyaltyLevel, 'Customer must have a loyalty level');
  assert(['gold', 'silver', 'bronze'].includes(customer.loyaltyLevel), 
         `Invalid loyalty level: ${customer.loyaltyLevel}`);
  
  let discountRate = 0;
  
  if (customer.loyaltyLevel === 'gold') {
    discountRate = 0.15;
  } else if (customer.loyaltyLevel === 'silver') {
    discountRate = 0.10;
  } else if (customer.loyaltyLevel === 'bronze') {
    discountRate = 0.05;
  }
  
  const discount = order.total * discountRate;
  
  // Assert post-conditions
  assert(discount >= 0, 'Discount cannot be negative');
  assert(discount <= order.total, 'Discount cannot exceed order total');
  
  return discount;
}

// Helper assertion function
function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}
```

## Mechanics

1. **Identify implicit assumptions**
   - Look for code that assumes certain conditions without checking
   - Find places where null/undefined checks are missing
   - Check for assumptions about data types, ranges, or formats

2. **Add pre-condition assertions**
   - Assert that parameters meet expected conditions
   - Check that object state is valid before operations
   - Validate input data format and ranges

3. **Add post-condition assertions**
   - Assert that results meet expected conditions
   - Check that object state remains valid after operations
   - Validate output data format and ranges

4. **Add invariant assertions**
   - Assert that class invariants are maintained
   - Check that object state is always consistent
   - Validate that business rules are not violated

5. **Create assertion utilities**
   - Build helper functions for common assertion patterns
   - Create domain-specific validation functions
   - Add logging and debugging support to assertions

6. **Test assertion behavior**
   - Verify that assertions catch invalid conditions
   - Test that valid conditions pass assertions
   - Ensure assertion messages are clear and helpful

## When to Use

- **Critical algorithms**: Code that must be correct for system stability
- **Public APIs**: Methods that accept external input
- **Data processing**: Code that transforms or validates data
- **Financial calculations**: Operations involving money or sensitive data
- **State machines**: Code that manages complex state transitions
- **Boundary conditions**: Operations near limits or edge cases

## Trade-offs

### Benefits
- **Early bug detection**: Catch problems immediately when they occur
- **Self-documenting code**: Assertions express assumptions clearly
- **Debugging aid**: Failed assertions provide clear failure points
- **Regression prevention**: Catch broken assumptions during changes
- **Code confidence**: Increased confidence in code correctness
- **Contract documentation**: Express method contracts explicitly

### Drawbacks
- **Performance overhead**: Runtime checks slow down execution
- **Code verbosity**: Assertions add lines of code to maintain
- **False positives**: Overly strict assertions may fail on valid edge cases
- **Maintenance burden**: Assertions need to be updated with code changes
- **Production concerns**: Failed assertions can crash production systems

## Related Refactorings

- [Introduce Guard Clause](introduce-guard-clause.md) - Add early returns for invalid conditions
- [Extract Function](extract-function.md) - Extract assertion logic into reusable methods
- [Add Parameter](change-function-declaration.md) - Add parameters to make dependencies explicit