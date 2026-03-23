---
title: "Parameterize Function"
description: "Eliminate duplicate functions with similar logic by introducing a parameter for variations"
category: "Simplifying Function Calls"
tags: ["parameterize", "function", "duplication", "consolidation", "parameter"]
related: ["remove-flag-argument", "replace-parameter-with-query", "introduce-parameter-object"]
---

# Parameterize Function

Eliminate duplicate functions with similar logic by introducing a parameter that allows a single function to handle multiple variations.

## Also Known As

- Parameterize Method

## Motivation

When you have multiple functions that do nearly the same thing but differ only in a few literal values, you can consolidate them by replacing the literals with parameters. This:

- **Reduces duplication**: One function instead of many similar ones
- **Improves maintainability**: Changes happen in one place
- **Increases flexibility**: Easy to add new variations
- **Simplifies testing**: Fewer functions to test

## Example

### Basic Example
```javascript
// Before - Multiple similar functions
function tenPercentRaise(person) {
  person.salary = person.salary.multiply(1.1);
}

function fivePercentRaise(person) {
  person.salary = person.salary.multiply(1.05);
}

function fifteenPercentRaise(person) {
  person.salary = person.salary.multiply(1.15);
}

// Usage
tenPercentRaise(employee);
fivePercentRaise(contractor);

// After - Single parameterized function
function raise(person, factor) {
  person.salary = person.salary.multiply(1 + factor);
}

// Usage
raise(employee, 0.10);
raise(contractor, 0.05);
raise(executive, 0.15);
```

### Complex Example - Discount Calculations
```javascript
// Before - Multiple discount functions
function calculateStudentDiscount(amount) {
  if (amount > 100) {
    return amount * 0.15; // 15% for students on orders over $100
  }
  return amount * 0.10; // 10% for students
}

function calculateSeniorDiscount(amount) {
  if (amount > 100) {
    return amount * 0.12; // 12% for seniors on orders over $100
  }
  return amount * 0.08; // 8% for seniors
}

function calculateMilitaryDiscount(amount) {
  if (amount > 100) {
    return amount * 0.20; // 20% for military on orders over $100
  }
  return amount * 0.15; // 15% for military
}

function calculateEmployeeDiscount(amount) {
  if (amount > 100) {
    return amount * 0.25; // 25% for employees on orders over $100
  }
  return amount * 0.20; // 20% for employees
}

// After - Single parameterized function
function calculateDiscount(amount, baseRate, bonusRate, threshold = 100) {
  const rate = amount > threshold ? bonusRate : baseRate;
  return amount * rate;
}

// Usage with clear parameters
function calculateStudentDiscount(amount) {
  return calculateDiscount(amount, 0.10, 0.15);
}

function calculateSeniorDiscount(amount) {
  return calculateDiscount(amount, 0.08, 0.12);
}

function calculateMilitaryDiscount(amount) {
  return calculateDiscount(amount, 0.15, 0.20);
}

function calculateEmployeeDiscount(amount) {
  return calculateDiscount(amount, 0.20, 0.25);
}

// Or direct usage
const studentDiscount = calculateDiscount(150, 0.10, 0.15);
const seniorDiscount = calculateDiscount(75, 0.08, 0.12);
```

### String Formatting Example
```javascript
// Before - Multiple formatting functions
function formatSuccessMessage(action, item) {
  return `${action} ${item} completed successfully`;
}

function formatErrorMessage(action, item) {
  return `Failed to ${action.toLowerCase()} ${item}`;
}

function formatWarningMessage(action, item) {
  return `Warning: ${action} ${item} may have issues`;
}

function formatInfoMessage(action, item) {
  return `Info: ${action} ${item} in progress`;
}

// After - Parameterized with message type
function formatMessage(level, action, item) {
  const templates = {
    success: `${action} ${item} completed successfully`,
    error: `Failed to ${action.toLowerCase()} ${item}`,
    warning: `Warning: ${action} ${item} may have issues`,
    info: `Info: ${action} ${item} in progress`
  };
  
  return templates[level] || `${action} ${item}`;
}

// Usage
const message1 = formatMessage('success', 'Create', 'user');
const message2 = formatMessage('error', 'Delete', 'file');
const message3 = formatMessage('warning', 'Update', 'profile');
```

### Validation Example
```javascript
// Before - Multiple validation functions
function isValidEmail(email) {
  const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  return emailRegex.test(email);
}

function isValidPhone(phone) {
  const phoneRegex = /^\\+?[1-9]\\d{1,14}$/;
  return phoneRegex.test(phone);
}

function isValidZipCode(zip) {
  const zipRegex = /^\\d{5}(-\\d{4})?$/;
  return zipRegex.test(zip);
}

function isValidCreditCard(card) {
  const cardRegex = /^\\d{13,19}$/;
  return cardRegex.test(card);
}

// After - Parameterized validation
function validateFormat(value, type) {
  const patterns = {
    email: /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/,
    phone: /^\\+?[1-9]\\d{1,14}$/,
    zipCode: /^\\d{5}(-\\d{4})?$/,
    creditCard: /^\\d{13,19}$/,
    ssn: /^\\d{3}-\\d{2}-\\d{4}$/,
    url: /^https?:\\/\\/[^\\s]+$/
  };
  
  const pattern = patterns[type];
  if (!pattern) {
    throw new Error(`Unknown validation type: ${type}`);
  }
  
  return pattern.test(value);
}

// Usage
const isValidEmail = validateFormat(email, 'email');
const isValidPhone = validateFormat(phone, 'phone');
const isValidZip = validateFormat(zipCode, 'zipCode');

// Can still provide wrapper functions if needed
function isValidEmail(email) {
  return validateFormat(email, 'email');
}
```

### HTTP Status Response Example
```javascript
// Before - Multiple response functions
function respondOK(res, data) {
  res.status(200).json({
    success: true,
    data: data,
    timestamp: new Date().toISOString()
  });
}

function respondCreated(res, data) {
  res.status(201).json({
    success: true,
    data: data,
    timestamp: new Date().toISOString()
  });
}

function respondBadRequest(res, message) {
  res.status(400).json({
    success: false,
    error: message,
    timestamp: new Date().toISOString()
  });
}

function respondNotFound(res, message) {
  res.status(404).json({
    success: false,
    error: message,
    timestamp: new Date().toISOString()
  });
}

function respondServerError(res, message) {
  res.status(500).json({
    success: false,
    error: message,
    timestamp: new Date().toISOString()
  });
}

// After - Parameterized response function
function respond(res, statusCode, payload) {
  const isSuccess = statusCode >= 200 && statusCode < 300;
  
  const response = {
    success: isSuccess,
    timestamp: new Date().toISOString()
  };
  
  if (isSuccess) {
    response.data = payload;
  } else {
    response.error = payload;
  }
  
  res.status(statusCode).json(response);
}

// Usage
respond(res, 200, userData);
respond(res, 201, newUser);
respond(res, 400, 'Invalid email format');
respond(res, 404, 'User not found');
respond(res, 500, 'Database connection failed');

// Can still provide convenience functions
function respondOK(res, data) {
  respond(res, 200, data);
}

function respondError(res, statusCode, message) {
  respond(res, statusCode, message);
}
```

## Mechanics

1. **Identify the varying elements**
   - Find the literal values that differ between functions
   - Note any conditional logic based on these values

2. **Choose appropriate parameter names**
   - Use descriptive names that explain the parameter's purpose
   - Consider using enums or constants for discrete values

3. **Create the parameterized function**
   - Replace literals with parameters
   - Ensure all variations are handled

4. **Replace original functions**
   - Update call sites to use the new function
   - Consider keeping wrapper functions for backward compatibility

5. **Test thoroughly**
   - Verify all original behaviors are preserved
   - Test edge cases and new parameter combinations

## When to Use

- **Similar functions**: Multiple functions with nearly identical logic
- **Literal differences**: Functions differ only in constant values
- **Growing variations**: Need to support new variations frequently
- **Template patterns**: Code follows a template with variable parts
- **Configuration-driven behavior**: Behavior varies based on settings

## Trade-offs

### Benefits
- **DRY principle**: Eliminates code duplication
- **Maintainability**: Changes happen in one place
- **Flexibility**: Easy to add new variations
- **Consistency**: All variations follow same logic
- **Testing**: Fewer functions to test

### Drawbacks
- **Complexity**: May make simple cases more complex
- **Performance**: Additional parameter passing
- **Type safety**: May weaken compile-time checking
- **Readability**: May be less clear than specific functions

## Implementation Patterns

### Enum Parameters
```javascript
const DiscountType = {
  STUDENT: 'student',
  SENIOR: 'senior',
  MILITARY: 'military',
  EMPLOYEE: 'employee'
};

function calculateDiscount(amount, discountType) {
  const rates = {
    [DiscountType.STUDENT]: { base: 0.10, bonus: 0.15 },
    [DiscountType.SENIOR]: { base: 0.08, bonus: 0.12 },
    [DiscountType.MILITARY]: { base: 0.15, bonus: 0.20 },
    [DiscountType.EMPLOYEE]: { base: 0.20, bonus: 0.25 }
  };
  
  const rate = rates[discountType];
  return amount > 100 ? amount * rate.bonus : amount * rate.base;
}
```

### Configuration Objects
```javascript
function processPayment(amount, options) {
  const config = {
    currency: 'USD',
    processingFee: 0,
    taxRate: 0,
    sendReceipt: true,
    ...options
  };
  
  let total = amount;
  total += config.processingFee;
  total += total * config.taxRate;
  
  const result = chargeCard(total, config.currency);
  
  if (config.sendReceipt) {
    sendReceipt(result, config.currency);
  }
  
  return result;
}
```

### Strategy Pattern Alternative
```javascript
// When parameterization becomes complex, consider strategy pattern
class DiscountCalculator {
  constructor(strategy) {
    this._strategy = strategy;
  }
  
  calculate(amount) {
    return this._strategy.calculate(amount);
  }
}

class StudentDiscountStrategy {
  calculate(amount) {
    return amount > 100 ? amount * 0.15 : amount * 0.10;
  }
}

class SeniorDiscountStrategy {
  calculate(amount) {
    return amount > 100 ? amount * 0.12 : amount * 0.08;
  }
}
```

### Functional Approach
```javascript
// Using higher-order functions
function createRaiseFunction(factor) {
  return function(person) {
    person.salary = person.salary.multiply(1 + factor);
  };
}

const tenPercentRaise = createRaiseFunction(0.10);
const fivePercentRaise = createRaiseFunction(0.05);
const fifteenPercentRaise = createRaiseFunction(0.15);
```

## Common Mistakes

### Over-Parameterization
```javascript
// Bad - too many parameters make it hard to use
function processOrder(id, type, priority, sendEmail, calculateTax, 
                     discountType, shippingMethod, paymentType) {
  // Too complex
}

// Better - use configuration object
function processOrder(id, options) {
  const config = {
    type: 'standard',
    priority: 'normal',
    sendEmail: true,
    calculateTax: true,
    discountType: null,
    shippingMethod: 'standard',
    paymentType: 'card',
    ...options
  };
  // Much cleaner
}
```

### Wrong Abstraction
```javascript
// Bad - parameterizing unrelated functions
function handleUserAction(action, user, data) {
  if (action === 'login') {
    return loginUser(user, data.password);
  } else if (action === 'logout') {
    return logoutUser(user);
  } else if (action === 'updateProfile') {
    return updateProfile(user, data.profile);
  }
  // These are really different operations
}

// Better - keep them separate
function loginUser(user, password) { }
function logoutUser(user) { }
function updateProfile(user, profile) { }
```

## Related Refactorings

- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Alternative for complex variations
- [Introduce Parameter Object](introduce-parameter-object.md) - When many parameters are needed
- [Extract Function](extract-function.md) - Often done before parameterizing
- [Substitute Algorithm](substitute-algorithm.md) - Alternative approach
- [Replace Function with Command](replace-function-with-command.md) - For complex parameterization