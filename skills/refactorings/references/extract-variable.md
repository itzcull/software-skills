---
title: "Extract Variable"
description: "Break down complex expressions into more readable and understandable variables that explain their purpose"
category: "Extract"
tags: ["extract", "variable", "expression", "readability", "clarity", "naming"]
related: ["inline-variable", "extract-function", "introduce-explaining-variable"]
---

# Extract Variable

Break down complex expressions into more readable and understandable variables that explain their purpose.

## Also Known As

- Introduce Explaining Variable

## Inverse

[Inline Variable](inline-variable.md)

## Motivation

Complex expressions can be hard to understand, especially when they:
- Contain multiple operations
- Use unclear intermediate calculations
- Repeat the same sub-expressions
- Mix different levels of abstraction

By extracting parts of these expressions into well-named variables, we make the code self-documenting and easier to understand.

## Example

### Basic Example
```javascript
// Before - Complex expression
return order.quantity * order.itemPrice -
  Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
  Math.min(order.quantity * order.itemPrice * 0.1, 100);

// After - Extracted variables explain the calculation
const basePrice = order.quantity * order.itemPrice;
const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
const shipping = Math.min(basePrice * 0.1, 100);
return basePrice - quantityDiscount + shipping;
```

### Complex Conditional Example
```javascript
// Before - Hard to understand condition
if ((platform.toUpperCase().indexOf('MAC') > -1) &&
    (browser.toUpperCase().indexOf('IE') > -1) &&
    wasInitialized() && resize > 0) {
  // do something
}

// After - Clear intent through variables
const isMacOS = platform.toUpperCase().indexOf('MAC') > -1;
const isInternetExplorer = browser.toUpperCase().indexOf('IE') > -1;
const isReady = wasInitialized() && resize > 0;

if (isMacOS && isInternetExplorer && isReady) {
  // do something
}
```

### Calculation with Business Logic
```javascript
// Before - Mixed calculation and business rules
function calculateEmployeeBonus(employee) {
  return employee.salary * 
         (employee.performanceRating > 4 ? 0.15 : 
          employee.performanceRating > 3 ? 0.10 : 
          employee.performanceRating > 2 ? 0.05 : 0) *
         (employee.yearsOfService > 10 ? 1.2 : 
          employee.yearsOfService > 5 ? 1.1 : 1.0) *
         (employee.department === 'sales' && employee.salesTarget > employee.actualSales ? 0.8 : 1.0);
}

// After - Clear business rules
function calculateEmployeeBonus(employee) {
  const performanceMultiplier = getPerformanceMultiplier(employee.performanceRating);
  const loyaltyMultiplier = getLoyaltyMultiplier(employee.yearsOfService);
  const salesPenalty = getSalesPenalty(employee);
  
  return employee.salary * performanceMultiplier * loyaltyMultiplier * salesPenalty;
}

function getPerformanceMultiplier(rating) {
  if (rating > 4) return 0.15;
  if (rating > 3) return 0.10;
  if (rating > 2) return 0.05;
  return 0;
}

function getLoyaltyMultiplier(yearsOfService) {
  if (yearsOfService > 10) return 1.2;
  if (yearsOfService > 5) return 1.1;
  return 1.0;
}

function getSalesPenalty(employee) {
  const missedTarget = employee.department === 'sales' && 
                      employee.salesTarget > employee.actualSales;
  return missedTarget ? 0.8 : 1.0;
}
```

### Data Processing Example
```javascript
// Before - Complex data transformation
function processUserData(users) {
  return users
    .filter(u => u.isActive && u.lastLogin && 
            (Date.now() - new Date(u.lastLogin).getTime()) < 30 * 24 * 60 * 60 * 1000)
    .map(u => ({
      id: u.id,
      name: u.firstName + ' ' + (u.middleName ? u.middleName + ' ' : '') + u.lastName,
      email: u.email.toLowerCase().trim(),
      daysActive: Math.floor((Date.now() - new Date(u.createdAt).getTime()) / (24 * 60 * 60 * 1000))
    }))
    .sort((a, b) => b.daysActive - a.daysActive);
}

// After - Clear step-by-step processing
function processUserData(users) {
  const activeUsers = filterActiveUsers(users);
  const enrichedUsers = enrichUserData(activeUsers);
  const sortedUsers = sortByActivityDuration(enrichedUsers);
  return sortedUsers;
}

function filterActiveUsers(users) {
  const thirtyDaysInMs = 30 * 24 * 60 * 60 * 1000;
  
  return users.filter(user => {
    const isActive = user.isActive;
    const hasRecentLogin = user.lastLogin && 
      (Date.now() - new Date(user.lastLogin).getTime()) < thirtyDaysInMs;
    
    return isActive && hasRecentLogin;
  });
}

function enrichUserData(users) {
  return users.map(user => {
    const fullName = buildFullName(user);
    const normalizedEmail = user.email.toLowerCase().trim();
    const daysActive = calculateDaysActive(user.createdAt);
    
    return {
      id: user.id,
      name: fullName,
      email: normalizedEmail,
      daysActive: daysActive
    };
  });
}

function buildFullName(user) {
  const firstName = user.firstName;
  const middleName = user.middleName ? user.middleName + ' ' : '';
  const lastName = user.lastName;
  return `${firstName} ${middleName}${lastName}`;
}

function calculateDaysActive(createdAt) {
  const msPerDay = 24 * 60 * 60 * 1000;
  const timeDiff = Date.now() - new Date(createdAt).getTime();
  return Math.floor(timeDiff / msPerDay);
}

function sortByActivityDuration(users) {
  return users.sort((a, b) => b.daysActive - a.daysActive);
}
```

## Mechanics

1. **Identify the sub-expression to extract**
   - Look for complex parts of larger expressions
   - Find repeated calculations
   - Spot unclear or commented code

2. **Ensure the expression is side-effect free**
   - The expression should always return the same result
   - No modifications to external state
   - Safe to evaluate multiple times

3. **Create a variable with a descriptive name**
   - Name should explain what the value represents
   - Use business terminology when appropriate
   - Avoid implementation details in the name

4. **Assign the expression to the variable**
   - Use const if the value won't change
   - Place declaration close to where it's used

5. **Replace the original expression**
   - Substitute with the variable name
   - Test to ensure behavior is preserved

6. **Consider extracting to a function**
   - If the variable is used in multiple places
   - If the calculation is complex enough to warrant reuse

## When to Extract

### Expression Complexity
```javascript
// Extract when expressions are hard to read
const isEligible = user.age >= 18 && 
                  user.hasValidLicense && 
                  user.creditScore > 650;
```

### Repeated Sub-expressions
```javascript
// Before - repeated calculation
const tax = income * 0.25;
const afterTax = income - (income * 0.25);

// After - extract the repeated part
const taxAmount = income * 0.25;
const tax = taxAmount;
const afterTax = income - taxAmount;
```

### Magic Numbers
```javascript
// Before - unclear constants
if (days > 30) { /* ... */ }

// After - meaningful names
const monthlyThreshold = 30;
if (days > monthlyThreshold) { /* ... */ }
```

### Complex Conditions
```javascript
// Before - complex boolean logic
if ((status === 'active' || status === 'pending') && 
    amount > 1000 && 
    customer.tier === 'premium') {
  // ...
}

// After - extracted conditions
const isValidStatus = status === 'active' || status === 'pending';
const isLargeAmount = amount > 1000;
const isPremiumCustomer = customer.tier === 'premium';

if (isValidStatus && isLargeAmount && isPremiumCustomer) {
  // ...
}
```

## Variable Naming Guidelines

### Good Names
```javascript
// Business-focused names
const totalPrice = basePrice + tax + shipping;
const isEligibleForDiscount = customer.loyaltyYears > 5;
const monthlyPayment = loanAmount / numberOfMonths;
```

### Avoid Implementation Details
```javascript
// Bad - focuses on how it's calculated
const arrayLength = users.length;
const stringConcatenation = firstName + ' ' + lastName;

// Good - focuses on what it represents
const userCount = users.length;
const fullName = firstName + ' ' + lastName;
```

### Be Specific
```javascript
// Bad - too vague
const data = response.users;
const result = calculate(input);

// Good - specific and clear
const activeUsers = response.users;
const totalCost = calculate(orderItems);
```

## Trade-offs

### Benefits
- **Readability**: Code becomes self-documenting
- **Debugging**: Easier to inspect intermediate values
- **Reuse**: Can reference the same calculation multiple times
- **Understanding**: Break complex logic into digestible parts
- **Maintenance**: Changes to calculations are localized

### Drawbacks
- **Verbosity**: More lines of code
- **Performance**: Additional variable assignments (usually negligible)
- **Scope pollution**: More variables in scope
- **Over-extraction**: Can make simple code unnecessarily complex

## Common Patterns

### Guard Clauses
```javascript
// Extract complex conditions for early returns
const isInvalidInput = !data || !data.items || data.items.length === 0;
if (isInvalidInput) {
  throw new Error('Invalid input data');
}
```

### Configuration Values
```javascript
// Extract configuration and thresholds
const maxRetries = 3;
const timeoutMs = 5000;
const batchSize = 100;
```

### Intermediate Results
```javascript
// Extract steps in multi-step calculations
const grossPay = hoursWorked * hourlyRate;
const overtimePay = calculateOvertime(hoursWorked, hourlyRate);
const totalPay = grossPay + overtimePay;
```

## Avoid Over-Extraction

```javascript
// Too much extraction for simple cases
// Bad
const two = 2;
const result = value * two;

// Good - keep simple expressions inline
const result = value * 2;

// Extract only when it adds clarity
const doubledValue = value * 2;
const quadrupledValue = doubledValue * 2;
```

## Related Refactorings

- [Inline Variable](inline-variable.md) - The inverse operation
- [Extract Function](extract-function.md) - When extracted logic becomes reusable
- [Replace Temp with Query](replace-temp-with-query.md) - Convert variables to functions
- [Split Variable](split-variable.md) - When variables are used for multiple purposes
- [Introduce Parameter Object](introduce-parameter-object.md) - When multiple related variables emerge