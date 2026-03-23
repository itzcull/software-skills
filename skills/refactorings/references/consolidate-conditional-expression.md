---
title: "Consolidate Conditional Expression"
description: "Simplify multiple conditional checks that share similar logic or return the same result"
category: "Simplifying Conditional Logic"
tags: ["conditional", "consolidate", "simplify", "boolean-logic", "extract"]
related: ["decompose-conditional", "replace-conditional-with-polymorphism", "extract-function"]
---

# Consolidate Conditional Expression

When multiple conditional checks share similar logic or return the same result, this refactoring helps simplify and extract the shared condition into a single, clear method.

## Motivation

Code often contains multiple conditional statements that:
- Check different conditions but produce the same result
- Represent parts of a single conceptual check
- Make the code's intent unclear through repetition

Consolidating these conditionals makes the code more readable and reveals the underlying business logic.

## Example

### Basic OR Consolidation
```javascript
// Before - Multiple conditions with same result
function disabilityAmount(anEmployee) {
  if (anEmployee.seniority < 2) return 0;
  if (anEmployee.monthsDisabled > 12) return 0;
  if (anEmployee.isPartTime) return 0;
  
  // calculate disability amount
  return anEmployee.salary * 0.6;
}

// After - Consolidated with OR
function disabilityAmount(anEmployee) {
  if (isNotEligibleForDisability(anEmployee)) return 0;
  
  // calculate disability amount
  return anEmployee.salary * 0.6;
}

function isNotEligibleForDisability(anEmployee) {
  return (anEmployee.seniority < 2)
      || (anEmployee.monthsDisabled > 12)
      || (anEmployee.isPartTime);
}
```

### AND Consolidation
```javascript
// Before - Nested conditions
function rate(anEmployee) {
  if (anEmployee.onVacation) {
    if (anEmployee.seniority > 10) {
      return 1;
    }
  }
  return 0.5;
}

// After - Consolidated with AND
function rate(anEmployee) {
  if (anEmployee.onVacation && anEmployee.seniority > 10) {
    return 1;
  }
  return 0.5;
}

// Or with extracted function
function rate(anEmployee) {
  return isEligibleForSpecialRate(anEmployee) ? 1 : 0.5;
}

function isEligibleForSpecialRate(anEmployee) {
  return anEmployee.onVacation && anEmployee.seniority > 10;
}
```

### Complex Business Rule
```javascript
// Before - Multiple related checks scattered
function calculateCharge(usage, provider) {
  let charge = 0;
  
  if (provider.type === 'premium') {
    charge = usage * 0.05;
  }
  if (provider.type === 'standard' && usage > 100) {
    charge = usage * 0.07;
  }
  if (provider.type === 'basic' && usage > 200) {
    charge = usage * 0.09;
  }
  
  // Additional charges
  if (usage > 1000 && provider.region === 'international') {
    charge += 50;
  }
  if (usage > 1000 && provider.type === 'premium') {
    charge += 30;
  }
  
  return charge;
}

// After - Consolidated conditions
function calculateCharge(usage, provider) {
  const baseCharge = calculateBaseCharge(usage, provider);
  const additionalCharge = calculateAdditionalCharge(usage, provider);
  return baseCharge + additionalCharge;
}

function calculateBaseCharge(usage, provider) {
  if (provider.type === 'premium') return usage * 0.05;
  if (provider.type === 'standard' && usage > 100) return usage * 0.07;
  if (provider.type === 'basic' && usage > 200) return usage * 0.09;
  return 0;
}

function calculateAdditionalCharge(usage, provider) {
  if (!isHighUsage(usage)) return 0;
  
  let charge = 0;
  if (provider.region === 'international') charge += 50;
  if (provider.type === 'premium') charge += 30;
  return charge;
}

function isHighUsage(usage) {
  return usage > 1000;
}
```

## Mechanics

1. **Identify conditions with identical outcomes**
   - Look for if statements that return/do the same thing
   - Check for patterns in conditional logic

2. **Combine conditions using logical operators**
   - Use OR (||) when any condition triggers the outcome
   - Use AND (&&) when all conditions must be true

3. **Extract the combined condition**
   - Create a well-named function
   - Move the combined conditional expression

4. **Replace original conditions**
   - Call the new function
   - Remove the redundant checks

5. **Test**
   - Ensure all edge cases still work
   - Verify the logic is preserved

## Patterns and Variations

### Guard Clause Consolidation
```javascript
// Before
function processOrder(order) {
  if (!order) return null;
  if (!order.customer) return null;
  if (!order.items) return null;
  if (order.items.length === 0) return null;
  
  // process order
}

// After
function processOrder(order) {
  if (!isValidOrder(order)) return null;
  
  // process order
}

function isValidOrder(order) {
  return order 
      && order.customer 
      && order.items 
      && order.items.length > 0;
}
```

### State Machine Conditions
```javascript
// Before
function getTransitionAction(state, event) {
  if (state === 'idle' && event === 'start') return 'initialize';
  if (state === 'running' && event === 'pause') return 'suspend';
  if (state === 'paused' && event === 'resume') return 'restart';
  if (state === 'running' && event === 'stop') return 'terminate';
  if (state === 'paused' && event === 'stop') return 'terminate';
  return 'invalid';
}

// After
function getTransitionAction(state, event) {
  if (isStartTransition(state, event)) return 'initialize';
  if (isPauseTransition(state, event)) return 'suspend';
  if (isResumeTransition(state, event)) return 'restart';
  if (isStopTransition(state, event)) return 'terminate';
  return 'invalid';
}

function isStopTransition(state, event) {
  return event === 'stop' && (state === 'running' || state === 'paused');
}
```

### Complex Boolean Logic
```javascript
// Before - Hard to understand
if ((a && b) || (a && c) || (b && !c && d)) {
  doSomething();
}

// After - Clear intent
if (shouldProcess(a, b, c, d)) {
  doSomething();
}

function shouldProcess(a, b, c, d) {
  const basicCondition = a && (b || c);
  const specialCondition = b && !c && d;
  return basicCondition || specialCondition;
}
```

## When to Use

- **Repeated outcomes**: Multiple conditions lead to the same action
- **Complex boolean logic**: Conditions are hard to understand
- **Business rules**: Multiple checks represent a single business concept
- **Guard clauses**: Multiple validation checks at the start of a function
- **State machines**: Complex state transition logic

## Trade-offs

### Benefits
- **Clarity**: Makes the intent of conditions clearer
- **DRY**: Eliminates duplicate code
- **Testability**: Extracted functions are easier to test
- **Maintainability**: Business rules are centralized
- **Documentation**: Function names document the logic

### Drawbacks
- **Indirection**: Adds a layer of abstraction
- **Over-extraction**: Can make simple logic harder to follow
- **Performance**: Function calls have minimal overhead
- **Debugging**: May need to step into functions

## Common Mistakes

### Over-consolidation
```javascript
// Don't consolidate unrelated conditions
// Bad
function shouldSkipProcessing(order, user, system) {
  return !order.isValid || !user.isActive || system.isMaintenanceMode;
}

// Good - Keep unrelated checks separate
if (!order.isValid) return 'Invalid order';
if (!user.isActive) return 'User not active';
if (system.isMaintenanceMode) return 'System maintenance';
```

### Losing Error Context
```javascript
// Bad - Lost specific error information
if (!isValid(data)) {
  throw new Error('Invalid data');
}

// Good - Preserve specific validation failures
const validationError = validateData(data);
if (validationError) {
  throw new Error(validationError);
}
```

## Related Refactorings

- [Decompose Conditional](decompose-conditional.md) - Break down complex conditions
- [Replace Nested Conditional with Guard Clauses](replace-nested-conditional-with-guard-clauses.md) - Simplify nested logic
- [Extract Function](extract-function.md) - Used to create the consolidated function
- [Introduce Explaining Variable](extract-variable.md) - For complex boolean expressions