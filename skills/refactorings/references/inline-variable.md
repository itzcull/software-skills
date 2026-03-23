---
title: "Inline Variable"
description: "Simplify code by removing unnecessary temporary variables and directly using the expression they represent"
category: "Inline"
tags: ["inline", "variable", "simplification", "unnecessary-variables", "readability"]
related: ["extract-variable", "inline-function", "remove-dead-code"]
---

# Inline Variable

Simplify code by removing unnecessary temporary variables and directly using the expression they represent.

## Also Known As

- Inline Temp

## Inverse

[Extract Variable](extract-variable.md)

## Motivation

Variables are generally good for making code clearer, but sometimes they don't add value:
- The variable name doesn't communicate more than the expression itself
- The variable is assigned once and never modified
- The variable gets in the way of refactoring
- The expression is simple enough to be self-explanatory

Removing these variables can make the code simpler and more direct.

## Example

### Basic Example
```javascript
// Before - Unnecessary variable
function getPrice(order) {
  let basePrice = order.basePrice;\n  return (basePrice > 1000);\n}\n\n// After - Direct expression\nfunction getPrice(order) {\n  return order.basePrice > 1000;\n}
```

### Multiple Unnecessary Variables
```javascript
// Before - Variables that don't add clarity
function calculateTotal(items) {
  let count = items.length;
  let isEmpty = count === 0;
  let hasItems = !isEmpty;
  
  if (hasItems) {
    let sum = 0;
    for (let i = 0; i < count; i++) {
      let item = items[i];
      let price = item.price;
      sum += price;
    }
    let total = sum;
    return total;
  }
  
  let defaultValue = 0;
  return defaultValue;
}

// After - Inlined unnecessary variables
function calculateTotal(items) {
  if (items.length === 0) {
    return 0;
  }
  
  let sum = 0;
  for (let i = 0; i < items.length; i++) {
    sum += items[i].price;
  }
  return sum;
}

// Even better - using array methods
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Variables That Hinder Refactoring
```javascript
// Before - Temporary variable prevents extract method
function processOrder(order) {
  // ... some setup code
  
  let discount = order.customer.isVIP() ? order.total * 0.1 : 0;
  let finalAmount = order.total - discount;
  
  if (finalAmount > 1000) {
    // VIP processing
    processVIPOrder(order, finalAmount);
  } else {
    // Regular processing
    processRegularOrder(order, finalAmount);
  }
}

// After - Inlined to enable better abstraction
function processOrder(order) {\n  // ... some setup code\n  \n  if (calculateFinalAmount(order) > 1000) {\n    processVIPOrder(order);\n  } else {\n    processRegularOrder(order);\n  }\n}\n\nfunction calculateFinalAmount(order) {\n  const discount = order.customer.isVIP() ? order.total * 0.1 : 0;\n  return order.total - discount;\n}
```

### Overly Granular Variables
```javascript
// Before - Too many intermediate variables
function formatUserName(user) {
  let firstName = user.firstName;
  let lastName = user.lastName;
  let hasFirstName = firstName !== null && firstName !== undefined;
  let hasLastName = lastName !== null && lastName !== undefined;
  let firstNamePart = hasFirstName ? firstName : '';
  let lastNamePart = hasLastName ? lastName : '';
  let space = hasFirstName && hasLastName ? ' ' : '';
  let fullName = firstNamePart + space + lastNamePart;
  let trimmed = fullName.trim();
  return trimmed;
}

// After - Inlined unnecessary variables
function formatUserName(user) {
  const firstName = user.firstName || '';
  const lastName = user.lastName || '';
  return `${firstName} ${lastName}`.trim();
}
```

### Variables in Conditional Logic
```javascript
// Before - Variables that obscure logic
function canProcessPayment(user, amount) {\n  let hasAccount = user.account !== null;\n  let hasBalance = user.account.balance >= amount;\n  let isVerified = user.isVerified === true;\n  let isActive = user.status === 'active';\n  \n  let accountIsReady = hasAccount && hasBalance;\n  let userIsValid = isVerified && isActive;\n  \n  return accountIsReady && userIsValid;\n}\n\n// After - Direct conditional expressions\nfunction canProcessPayment(user, amount) {\n  return user.account !== null &&\n         user.account.balance >= amount &&\n         user.isVerified &&\n         user.status === 'active';\n}
```

### Loop Variables
```javascript
// Before - Unnecessary loop variables
function findMostExpensiveItem(items) {
  let maxPrice = 0;
  let maxItem = null;
  
  for (let i = 0; i < items.length; i++) {
    let currentItem = items[i];
    let currentPrice = currentItem.price;
    let isMoreExpensive = currentPrice > maxPrice;
    
    if (isMoreExpensive) {
      maxPrice = currentPrice;
      maxItem = currentItem;
    }\n  }\n  \n  return maxItem;\n}\n\n// After - Inlined obvious variables\nfunction findMostExpensiveItem(items) {\n  let maxPrice = 0;\n  let maxItem = null;\n  \n  for (let i = 0; i < items.length; i++) {\n    if (items[i].price > maxPrice) {\n      maxPrice = items[i].price;\n      maxItem = items[i];\n    }\n  }\n  \n  return maxItem;\n}\n\n// Even better - using reduce\nfunction findMostExpensiveItem(items) {\n  return items.reduce((max, item) => \n    item.price > max.price ? item : max, \n    items[0] || null\n  );\n}
```

## Mechanics

1. **Check that the variable is assigned only once**
   - The variable should not be modified after assignment
   - Look for any mutations or reassignments

2. **Check that the expression is side-effect free**
   - The expression should not modify global state
   - Should not call functions with side effects
   - Should be safe to evaluate multiple times

3. **Find all references to the variable**
   - Use IDE search to find all usages
   - Note where the variable is used

4. **Replace references with the expression**
   - Substitute each use of the variable with its assigned expression
   - Add parentheses if needed to preserve operator precedence

5. **Remove the variable declaration**
   - Delete the variable declaration and assignment
   - Test to ensure behavior is preserved

6. **Consider extracting to a function if used multiple times**
   - If the expression is used in multiple places after inlining

## When to Inline

### Obvious Assignments
```javascript
// Variable name doesn't add information
const result = calculate();
return result;

// Better
return calculate();
```

### Single-Use Variables
```javascript
// Used only once
const user = getCurrentUser();
if (user.isAdmin) { /* ... */ }

// Inline it
if (getCurrentUser().isAdmin) { /* ... */ }
```

### Variables That Break Flow
```javascript
// Interrupts the logical flow
function processData(data) {
  const processed = transform(data);
  return validate(processed);\n}\n\n// More direct\nfunction processData(data) {\n  return validate(transform(data));\n}
```

### Intermediate Variables in Calculations
```javascript
// Breaking up simple calculations unnecessarily
const subtotal = price * quantity;
const total = subtotal + tax;
return total;

// More direct
return price * quantity + tax;
```

## When NOT to Inline

### Complex Expressions
```javascript
// Keep variable for complex calculations
const monthlyPayment = principal * 
  (monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) /
  (Math.pow(1 + monthlyRate, numberOfPayments) - 1);

return monthlyPayment > maxAffordablePayment;
```

### Expressions Used Multiple Times
```javascript
// Don't inline if used multiple times
const currentUser = getCurrentUser();
log(`User ${currentUser.name} logged in`);
updateLastSeen(currentUser);
return currentUser.preferences;
```

### Debugging Aid
```javascript
// Keep for debugging purposes
function complexCalculation(data) {
  const intermediate1 = step1(data);  // Useful for debugging
  const intermediate2 = step2(intermediate1);  // Useful for debugging
  const result = step3(intermediate2);  // Useful for debugging
  return result;
}
```

### Performance-Critical Code
```javascript
// Don't inline expensive operations used multiple times
function processItems(items) {
  const sortedItems = expensiveSort(items);  // Don't inline if expensive
  
  displayItems(sortedItems);
  logStatistics(sortedItems);
  saveToCache(sortedItems);
}
```

## Trade-offs

### Benefits
- **Simplicity**: Fewer variables to track
- **Directness**: More straightforward code flow
- **Readability**: Can improve readability when variables don't add clarity
- **Reduced scope pollution**: Fewer variables in scope
- **Better for refactoring**: Easier to extract functions

### Drawbacks
- **Loss of intermediate values**: Harder to inspect during debugging
- **Repeated evaluation**: Expression may be evaluated multiple times
- **Reduced testability**: Can't test intermediate values
- **Complexity**: May make expressions more complex

## Guidelines

### Good Candidates for Inlining
```javascript
// Trivial assignments
const name = person.name;
console.log(name);

// Better
console.log(person.name);

// Obvious boolean expressions
const isValid = user !== null;
if (isValid) { /* ... */ }

// Better
if (user !== null) { /* ... */ }
```

### Keep These Variables
```javascript
// Complex business calculations
const taxableIncome = calculateTaxableIncome(salary, deductions, exemptions);

// Multiple usage
const config = getConfiguration();
validateConfig(config);
applyConfig(config);
logConfig(config);

// Aid for understanding
const userHasPermission = user.role === 'admin' || user.permissions.includes('write');
const resourceIsAvailable = resource.status === 'available' && !resource.locked;
if (userHasPermission && resourceIsAvailable) {
  // Complex condition broken down for clarity
}
```

### Balance Readability
```javascript
// Sometimes variables help readability even if simple
function calculateShipping(order) {
  const isInternational = order.country !== 'US';
  const isExpedited = order.shippingType === 'expedited';
  const baseRate = isInternational ? 25 : 10;
  
  return isExpedited ? baseRate * 2 : baseRate;
}

// This is clearer than:
function calculateShipping(order) {
  return order.shippingType === 'expedited' 
    ? (order.country !== 'US' ? 25 : 10) * 2 
    : (order.country !== 'US' ? 25 : 10);
}
```

## Related Refactorings

- [Extract Variable](extract-variable.md) - The inverse operation
- [Inline Function](inline-function.md) - Similar concept for functions  
- [Replace Temp with Query](replace-temp-with-query.md) - Alternative to inlining
- [Split Variable](split-variable.md) - When variables serve multiple purposes
- [Remove Dead Code](remove-dead-code.md) - May follow from inlining