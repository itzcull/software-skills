---
title: "Inline Function"
description: "Simplify code by removing unnecessary function abstraction by directly incorporating function logic into calling code"
category: "Inline"
tags: ["inline", "function", "method", "simplification", "abstraction", "complexity"]
related: ["extract-function", "inline-variable", "remove-dead-code"]
---

# Inline Function

Simplify code by removing unnecessary function abstraction. Reduce complexity by directly incorporating function logic into calling code.

## Also Known As

- Inline Method

## Inverse

[Extract Function](extract-function.md)

## Motivation

Sometimes functions become too small or lose their purpose. When a function's body is as clear as its name, or when a layer of indirection isn't helping, it's time to inline it. This happens when:

- The function body is self-explanatory
- The function is poorly named and its body is clearer
- You have too many small functions that don't add value
- Refactoring has left a function with minimal logic
- Performance is critical and function calls add overhead

## Example

### Basic Example
```javascript
// Before - Unnecessary abstraction
function getRating(driver) {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver) {
  return driver.numberOfLateDeliveries > 5;
}

// After - Inlined for clarity
function getRating(driver) {
  return (driver.numberOfLateDeliveries > 5) ? 2 : 1;
}
```

### Over-Abstracted Example
```javascript
// Before - Too many tiny functions
class Order {
  constructor(customer, items) {
    this._customer = customer;
    this._items = items;
  }
  
  getDiscountRate() {
    return getCustomerDiscountRate(this._customer);
  }
  
  calculateSubtotal() {
    return calculateItemsTotal(this._items);
  }
  
  calculateTotal() {
    const subtotal = this.calculateSubtotal();
    const discount = subtotal * this.getDiscountRate();
    return subtotal - discount;
  }
}

function getCustomerDiscountRate(customer) {
  return isVIPCustomer(customer) ? 0.1 : 0.05;
}

function isVIPCustomer(customer) {
  return customer.type === 'VIP';
}

function calculateItemsTotal(items) {
  return sumItemPrices(items);
}

function sumItemPrices(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// After - Inlined unnecessary abstractions
class Order {
  constructor(customer, items) {
    this._customer = customer;
    this._items = items;
  }
  
  getDiscountRate() {
    return this._customer.type === 'VIP' ? 0.1 : 0.05;
  }
  
  calculateSubtotal() {
    return this._items.reduce((sum, item) => sum + item.price, 0);
  }
  
  calculateTotal() {
    const subtotal = this.calculateSubtotal();
    const discount = subtotal * this.getDiscountRate();
    return subtotal - discount;
  }
}
```

### Dead Code After Refactoring
```javascript
// Before - Function left over from old requirements
class PayrollCalculator {
  calculatePay(employee) {
    const basePay = this.calculateBasePay(employee);
    const overtime = this.calculateOvertime(employee);
    const deductions = this.calculateDeductions(employee);
    
    return basePay + overtime - deductions;
  }
  
  calculateBasePay(employee) {
    return employee.hoursWorked * employee.hourlyRate;
  }
  
  calculateOvertime(employee) {
    // This used to be complex, but requirements simplified
    return 0; // No overtime in new system
  }
  
  calculateDeductions(employee) {
    const taxRate = this.getTaxRate(employee);
    return this.calculateBasePay(employee) * taxRate;
  }
  
  getTaxRate(employee) {
    // Used to be complex calculation, now it's simple
    return 0.25;
  }
}

// After - Inlined simplified functions
class PayrollCalculator {
  calculatePay(employee) {
    const basePay = employee.hoursWorked * employee.hourlyRate;
    const deductions = basePay * 0.25; // 25% tax rate
    
    return basePay - deductions;
  }
}
```

### Complex Example with Multiple Inlinings
```javascript
// Before - Over-engineered validation
class UserValidator {
  validateUser(user) {
    if (!this.hasRequiredFields(user)) {
      throw new Error(this.getMissingFieldsError(user));
    }
    
    if (!this.isValidEmail(user)) {
      throw new Error(this.getInvalidEmailError());
    }
    
    if (!this.isValidAge(user)) {
      throw new Error(this.getInvalidAgeError());
    }
    
    return true;
  }
  
  hasRequiredFields(user) {
    return this.hasName(user) && this.hasEmail(user) && this.hasAge(user);
  }
  
  hasName(user) {
    return user.name && user.name.trim().length > 0;
  }
  
  hasEmail(user) {
    return user.email && user.email.trim().length > 0;
  }
  
  hasAge(user) {
    return user.age !== undefined && user.age !== null;
  }
  
  isValidEmail(user) {
    return this.emailMatchesPattern(user.email);
  }
  
  emailMatchesPattern(email) {
    const pattern = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return pattern.test(email);
  }
  
  isValidAge(user) {
    return this.ageInValidRange(user.age);
  }
  
  ageInValidRange(age) {
    return age >= 0 && age <= 150;
  }
  
  getMissingFieldsError(user) {
    return 'User must have name, email, and age';
  }
  
  getInvalidEmailError() {
    return 'Invalid email format';
  }
  
  getInvalidAgeError() {
    return 'Age must be between 0 and 150';
  }
}

// After - Inlined to appropriate level
class UserValidator {
  validateUser(user) {
    // Inline simple field checks
    if (!user.name?.trim() || !user.email?.trim() || user.age == null) {
      throw new Error('User must have name, email, and age');
    }
    
    // Inline simple email validation
    const emailPattern = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    if (!emailPattern.test(user.email)) {
      throw new Error('Invalid email format');
    }
    
    // Inline simple age validation
    if (user.age < 0 || user.age > 150) {
      throw new Error('Age must be between 0 and 150');
    }
    
    return true;
  }
}
```

## Mechanics

1. **Check that the function is not polymorphic**
   - Ensure it's not overridden in subclasses
   - Make sure it's not part of an interface implementation
   - Verify it's not used as a callback or higher-order function

2. **Find all calls to the function**
   - Use IDE search or grep to find all references
   - Note any recursive calls (handle these carefully)

3. **Replace each call with the function body**
   - Copy the function body to each call site
   - Replace function parameters with actual arguments
   - Handle any local variables in the function

4. **Test after each replacement**
   - Run tests after each inline to catch issues early
   - Don't inline everything at once

5. **Remove the function definition**
   - Delete the function once all calls are replaced
   - Remove any imports or references

## When to Inline

### Clear and Simple Logic
```javascript
// Function name doesn't add clarity
function isAdult(person) {
  return person.age >= 18;
}

// Inline when the code is self-explanatory
if (person.age >= 18) {
  // adult logic
}
```

### One-Line Functions That Don't Abstract Anything
```javascript
// These don't add value
function getFirst(array) {
  return array[0];
}

function isEmpty(array) {
  return array.length === 0;
}

// Better to use directly
const first = items[0];
const empty = items.length === 0;
```

### Functions Used Only Once
```javascript
// Single-use function
function calculateTaxAmount(price) {
  return price * 0.08;
}

const total = basePrice + calculateTaxAmount(basePrice);

// Inline it
const total = basePrice + (basePrice * 0.08);
```

### Dead Abstractions After Refactoring
```javascript
// Function that became trivial after business changes
function getPriority(order) {
  return 'normal'; // Used to be complex logic
}

// Just use the value directly
const priority = 'normal';
```

## When NOT to Inline

### Functions That Provide Meaningful Abstraction
```javascript
// Keep these - they represent domain concepts
function calculateInterest(principal, rate, time) {
  return principal * rate * time;
}

function isEligibleForLoan(applicant) {
  return applicant.creditScore > 600 && 
         applicant.income > 30000 && 
         applicant.debtRatio < 0.4;
}
```

### Functions Used Multiple Times
```javascript
// Don't inline if used in many places
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}
```

### Functions That May Grow
```javascript
// Keep if you expect it to become more complex
function validateInput(data) {
  return data !== null; // Simple now, but may need more validation
}
```

### Polymorphic Functions
```javascript
// Don't inline if overridden in subclasses
class Shape {
  area() {
    throw new Error('Must implement area');
  }
}

class Rectangle extends Shape {
  area() {
    return this.width * this.height; // Don't inline - polymorphic
  }
}
```

## Trade-offs

### Benefits
- **Simplicity**: Fewer functions to understand
- **Performance**: Eliminates function call overhead
- **Clarity**: May make code more direct and readable
- **Reduced maintenance**: Fewer functions to maintain
- **Less navigation**: Don't need to jump to function definitions

### Drawbacks
- **Code duplication**: Logic may be repeated
- **Reduced testability**: Can't test the function in isolation
- **Loss of naming**: Lose descriptive function names
- **Larger functions**: May make functions longer and more complex
- **Reduced reusability**: Can't reuse the extracted logic

## Guidelines

### Good Candidates for Inlining
```javascript
// Trivial wrappers
function setName(person, name) {
  person.name = name;
}

// Obvious calculations
function double(x) {
  return x * 2;
}

// Single-use helpers
function getRandomId() {
  return Math.random().toString(36);
}
```

### Keep These Functions
```javascript
// Complex algorithms
function quicksort(array) {
  // Complex sorting logic
}

// Domain-specific operations
function calculateMortgagePayment(principal, rate, years) {
  // Financial calculation
}

// Reusable utilities
function debounce(func, delay) {
  // Utility function used in many places
}
```

### Balance Abstraction Levels
```javascript
// Good balance - meaningful abstractions
class OrderProcessor {
  processOrder(order) {
    this.validateOrder(order);
    this.calculatePricing(order);
    this.reserveInventory(order);
    this.chargePayment(order);
    this.scheduleShipping(order);
  }
  
  // These methods contain substantial logic worth abstracting
  validateOrder(order) { /* meaningful validation logic */ }
  calculatePricing(order) { /* complex pricing rules */ }
  // etc.
}
```

## Related Refactorings

- [Extract Function](extract-function.md) - The inverse operation
- [Replace Function with Inline](inline-variable.md) - Similar concept for variables
- [Collapse Hierarchy](collapse-hierarchy.md) - Similar concept for classes
- [Remove Dead Code](remove-dead-code.md) - Often follows inlining
- [Substitute Algorithm](substitute-algorithm.md) - Alternative to inlining complex functions