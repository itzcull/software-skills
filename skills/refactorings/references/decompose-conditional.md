---
title: "Decompose Conditional"
description: "Simplify complex conditional logic by extracting the condition and actions into separate methods"
category: "Simplifying Conditional Logic"
tags: ["conditional", "decompose", "extract", "readability", "clarity"]
related: ["consolidate-conditional-expression", "extract-function", "replace-conditional-with-polymorphism"]
---

# Decompose Conditional

Simplify complex conditional logic by extracting the condition and its corresponding actions into separate, more readable methods. This makes the code's intent clearer.

## Motivation

Conditional logic can quickly become complex and hard to understand. Long conditions mixed with complex consequences obscure the intent of the code. By extracting both the conditional check and its actions into well-named functions, we make the code self-documenting and easier to understand.

## Example

### Basic Example
```javascript
// Before - Complex conditional with unclear intent
function calculateCharge(date, plan) {
  let charge;
  if (!date.isBefore(plan.summerStart) && !date.isAfter(plan.summerEnd)) {
    charge = quantity * plan.summerRate;
  } else {
    charge = quantity * plan.regularRate + plan.regularServiceCharge;
  }
  return charge;
}

// After - Clear intent through decomposition
function calculateCharge(date, plan) {
  return isSummer(date, plan) 
    ? summerCharge(plan) 
    : regularCharge(plan);
}

function isSummer(date, plan) {
  return !date.isBefore(plan.summerStart) && !date.isAfter(plan.summerEnd);
}

function summerCharge(plan) {
  return quantity * plan.summerRate;
}

function regularCharge(plan) {
  return quantity * plan.regularRate + plan.regularServiceCharge;
}
```

### Complex Business Logic Example
```javascript
// Before - Multiple conditions and complex calculations
function calculatePayAmount(employee) {
  let result;
  if (employee.isSeparated) {
    result = {amount: 0, reason: "SEP"};
  } else if (employee.isRetired) {
    result = {amount: 0, reason: "RET"};
  } else if (employee.seniority < 2 || employee.monthsDisabled > 12 || employee.isPartTime) {
    result = {amount: 0, reason: "INELIGIBLE"};
  } else {
    // complex calculation
    const basePay = employee.rate * employee.hours;
    const overtime = Math.max(0, employee.hours - 40) * employee.rate * 0.5;
    const benefits = employee.seniority > 10 ? basePay * 0.1 : basePay * 0.05;
    result = {
      amount: basePay + overtime + benefits,
      reason: "NORMAL"
    };
  }
  return result;
}

// After - Decomposed into clear, focused functions
function calculatePayAmount(employee) {
  if (isNotPayable(employee)) {
    return createZeroPayment(employee);
  }
  return createNormalPayment(employee);
}

function isNotPayable(employee) {
  return employee.isSeparated || 
         employee.isRetired || 
         isNotEligibleForPayment(employee);
}

function isNotEligibleForPayment(employee) {
  return employee.seniority < 2 || 
         employee.monthsDisabled > 12 || 
         employee.isPartTime;
}

function createZeroPayment(employee) {
  const reason = determineZeroPaymentReason(employee);
  return {amount: 0, reason};
}

function determineZeroPaymentReason(employee) {
  if (employee.isSeparated) return "SEP";
  if (employee.isRetired) return "RET";
  return "INELIGIBLE";
}

function createNormalPayment(employee) {
  return {
    amount: calculateTotalPay(employee),
    reason: "NORMAL"
  };
}

function calculateTotalPay(employee) {
  const basePay = calculateBasePay(employee);
  const overtime = calculateOvertime(employee);
  const benefits = calculateBenefits(employee, basePay);
  return basePay + overtime + benefits;
}

function calculateBasePay(employee) {
  return employee.rate * employee.hours;
}

function calculateOvertime(employee) {
  const overtimeHours = Math.max(0, employee.hours - 40);
  return overtimeHours * employee.rate * 0.5;
}

function calculateBenefits(employee, basePay) {
  const benefitRate = employee.seniority > 10 ? 0.1 : 0.05;
  return basePay * benefitRate;
}
```

## Mechanics

1. **Extract the conditional into its own function**
   - Use [Extract Function](extract-function.md)
   - Give it a name that expresses the intent of the condition

2. **Extract the then-branch**
   - Extract the code in the then-branch to a function
   - Name it to express what happens when the condition is true

3. **Extract the else-branch**
   - Extract the code in the else-branch to a function
   - Name it to express the alternative action

4. **Replace the original conditional**
   - Call the extracted functions
   - Use a ternary operator if appropriate

5. **Test after each extraction**
   - Ensure behavior remains the same
   - Check edge cases

## Patterns and Variations

### Nested Conditionals
```javascript
// Before
function getPayRate(employee) {
  if (employee.type === 'commissioned') {
    if (employee.sales > 10000) {
      return employee.baseSalary + (employee.sales * 0.1);
    } else {
      return employee.baseSalary + (employee.sales * 0.05);
    }
  } else if (employee.type === 'hourly') {
    if (employee.overtime > 0) {
      return employee.rate * 40 + (employee.overtime * employee.rate * 1.5);
    } else {
      return employee.rate * employee.hours;
    }
  } else {
    return employee.salary;
  }
}

// After
function getPayRate(employee) {
  switch (employee.type) {
    case 'commissioned': return getCommissionedPay(employee);
    case 'hourly': return getHourlyPay(employee);
    default: return employee.salary;
  }
}

function getCommissionedPay(employee) {
  const commissionRate = employee.sales > 10000 ? 0.1 : 0.05;
  return employee.baseSalary + (employee.sales * commissionRate);
}

function getHourlyPay(employee) {
  return hasOvertime(employee)
    ? calculatePayWithOvertime(employee)
    : calculateRegularPay(employee);
}

function hasOvertime(employee) {
  return employee.overtime > 0;
}

function calculatePayWithOvertime(employee) {
  const regularPay = employee.rate * 40;
  const overtimePay = employee.overtime * employee.rate * 1.5;
  return regularPay + overtimePay;
}

function calculateRegularPay(employee) {
  return employee.rate * employee.hours;
}
```

### Complex Conditions
```javascript
// Before
if ((customer.type === 'vip' && order.total > 1000) || 
    (customer.loyaltyYears > 5 && order.total > 500) ||
    (promotion.isActive && promotion.applies(order))) {
  applyDiscount(order, 0.2);
}

// After
if (isEligibleForDiscount(customer, order, promotion)) {
  applyDiscount(order, 0.2);
}

function isEligibleForDiscount(customer, order, promotion) {
  return isVipLargeOrder(customer, order) ||
         isLoyalCustomerOrder(customer, order) ||
         isPromotionApplicable(promotion, order);
}

function isVipLargeOrder(customer, order) {
  return customer.type === 'vip' && order.total > 1000;
}

function isLoyalCustomerOrder(customer, order) {
  return customer.loyaltyYears > 5 && order.total > 500;
}

function isPromotionApplicable(promotion, order) {
  return promotion.isActive && promotion.applies(order);
}
```

## When to Use

- **Complex conditions**: When the conditional expression is hard to understand
- **Long branches**: When then/else blocks contain multiple statements
- **Business rules**: When conditions represent important business logic
- **Repeated logic**: When similar conditions appear in multiple places
- **Comments needed**: When you feel the need to comment what a condition does

## Trade-offs

### Benefits
- **Readability**: Code intent is immediately clear
- **Testability**: Each function can be tested independently
- **Reusability**: Extracted functions can be used elsewhere
- **Documentation**: Function names serve as documentation
- **Debugging**: Easier to set breakpoints and understand flow

### Drawbacks
- **More code**: Can increase total lines of code
- **Indirection**: May need to navigate to multiple functions
- **Over-extraction**: Can make simple logic harder to follow
- **Performance**: Minimal overhead from function calls

## Guidelines

### Good Decomposition
- Each function has a single, clear purpose
- Function names express intent, not implementation
- Functions are at the same level of abstraction
- The main function reads like a story

### Avoid Over-Decomposition
```javascript
// Too much decomposition for simple logic
// Bad
function isAdult(person) {
  return isAgeGreaterThanOrEqual(person.age, getAdultAge());
}

function isAgeGreaterThanOrEqual(age, threshold) {
  return age >= threshold;
}

function getAdultAge() {
  return 18;
}

// Good - Keep simple logic inline
function isAdult(person) {
  return person.age >= 18;
}
```

## Related Refactorings

- [Extract Function](extract-function.md) - The primary tool for this refactoring
- [Consolidate Conditional Expression](consolidate-conditional-expression.md) - Combine related conditions
- [Replace Nested Conditional with Guard Clauses](replace-nested-conditional-with-guard-clauses.md) - Simplify nested logic
- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Use objects instead of conditions
- [Introduce Explaining Variable](extract-variable.md) - For complex expressions within conditions