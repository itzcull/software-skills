---
title: "Extract Function"
description: "Improve code readability and modularity by breaking down complex functions into smaller, more focused functions"
category: "Extract"
tags: ["extract", "function", "method", "modularity", "readability", "complexity"]
related: ["inline-function", "extract-variable", "split-phase"]
---

# Extract Function

Improve code readability and modularity by breaking down complex functions into smaller, more focused functions.

## Also Known As

- Extract Method

## Inverse

[Inline Function](inline-function.md)

## Motivation

Long functions are hard to understand, debug, and maintain. By extracting smaller functions, we:
- **Improve readability**: Functions become self-documenting
- **Enable reuse**: Extracted logic can be used elsewhere
- **Simplify testing**: Smaller functions are easier to test
- **Reduce duplication**: Common patterns can be extracted
- **Clarify intent**: Function names explain what the code does

## Example

### Basic Example
```javascript
// Before - Complex function with mixed concerns
function printOwing(invoice) {
  printBanner();
  let outstanding = calculateOutstanding();

  // print details
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}

// After - Extracted detail printing
function printOwing(invoice) {
  printBanner();
  let outstanding = calculateOutstanding();
  printDetails(invoice, outstanding);
}

function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

### Complex Example with Local Variables
```javascript
// Before - Long function with complex logic
function processOrder(order) {
  // Validate order
  if (!order.customer) {
    throw new Error('Customer is required');
  }
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must have items');
  }
  for (let item of order.items) {
    if (item.quantity <= 0) {
      throw new Error('Item quantity must be positive');
    }
    if (!item.product || !item.product.price) {
      throw new Error('Item must have valid product with price');
    }
  }
  
  // Calculate totals
  let subtotal = 0;
  for (let item of order.items) {
    subtotal += item.product.price * item.quantity;
  }
  
  let discountRate = 0;
  if (order.customer.isVIP) {
    discountRate = 0.1;
  } else if (order.customer.loyaltyYears > 5) {
    discountRate = 0.05;
  }
  
  let discount = subtotal * discountRate;
  let taxRate = getTaxRate(order.customer.state);
  let tax = (subtotal - discount) * taxRate;
  let shipping = calculateShipping(order);
  let total = subtotal - discount + tax + shipping;
  
  // Create invoice
  let invoice = {
    orderId: order.id,
    customer: order.customer,
    subtotal: subtotal,
    discount: discount,
    tax: tax,
    shipping: shipping,
    total: total,
    items: order.items
  };
  
  // Save and notify
  saveInvoice(invoice);
  sendConfirmationEmail(order.customer, invoice);
  updateInventory(order.items);
  
  return invoice;
}

// After - Extracted into focused functions
function processOrder(order) {
  validateOrder(order);
  const invoice = createInvoice(order);
  finalizeOrder(order, invoice);
  return invoice;
}

function validateOrder(order) {
  validateCustomer(order.customer);
  validateItems(order.items);
}

function validateCustomer(customer) {
  if (!customer) {
    throw new Error('Customer is required');
  }
}

function validateItems(items) {
  if (!items || items.length === 0) {
    throw new Error('Order must have items');
  }
  
  for (let item of items) {
    validateItem(item);
  }
}

function validateItem(item) {
  if (item.quantity <= 0) {
    throw new Error('Item quantity must be positive');
  }
  if (!item.product || !item.product.price) {
    throw new Error('Item must have valid product with price');
  }
}

function createInvoice(order) {
  const subtotal = calculateSubtotal(order.items);
  const discount = calculateDiscount(order.customer, subtotal);
  const tax = calculateTax(order.customer, subtotal - discount);
  const shipping = calculateShipping(order);
  const total = subtotal - discount + tax + shipping;
  
  return {
    orderId: order.id,
    customer: order.customer,
    subtotal,
    discount,
    tax,
    shipping,
    total,
    items: order.items
  };
}

function calculateSubtotal(items) {
  return items.reduce((sum, item) => {
    return sum + item.product.price * item.quantity;
  }, 0);
}

function calculateDiscount(customer, subtotal) {
  const discountRate = getDiscountRate(customer);
  return subtotal * discountRate;
}

function getDiscountRate(customer) {
  if (customer.isVIP) return 0.1;
  if (customer.loyaltyYears > 5) return 0.05;
  return 0;
}

function calculateTax(customer, taxableAmount) {
  const taxRate = getTaxRate(customer.state);
  return taxableAmount * taxRate;
}

function finalizeOrder(order, invoice) {
  saveInvoice(invoice);
  sendConfirmationEmail(order.customer, invoice);
  updateInventory(order.items);
}
```

## Mechanics

1. **Create a new function**
   - Give it a name that explains its purpose
   - Make it as descriptive as possible

2. **Copy the extracted code**
   - Copy the code fragment to the new function
   - Don't remove it from the original yet

3. **Scan for local variables**
   - Variables used but not modified: pass as parameters
   - Variables modified: consider return values or reference parameters
   - Variables declared: can usually stay in the extracted function

4. **Deal with variables**
   - Pass required data as parameters
   - Return modified values
   - Consider extracting variable assignments

5. **Replace extracted code with call**
   - Call the new function from the original location
   - Pass necessary arguments
   - Handle return values

6. **Test**
   - Run tests to ensure behavior is preserved
   - Debug any issues with variable handling

## Handling Variables

### No Local Variables
```javascript
// Simple case - no variables to worry about
function printBanner() {
  console.log('***********************');
  console.log('***** Customer Owes *****');
  console.log('***********************');
}
```

### Using Local Variables
```javascript
// Variables used but not modified
function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

### Modifying Local Variables
```javascript
// Before
function calculateTotal() {
  let total = 0;
  for (let item of items) {
    total += item.price * item.quantity;
    if (item.discount) {
      total -= item.discount;
    }
  }
  return total;
}

// After
function calculateTotal() {
  let total = 0;
  for (let item of items) {
    total += calculateItemTotal(item);
  }
  return total;
}

function calculateItemTotal(item) {
  let itemTotal = item.price * item.quantity;
  if (item.discount) {
    itemTotal -= item.discount;
  }
  return itemTotal;
}
```

### Multiple Return Values
```javascript
// When you need to return multiple values
function calculateOrderTotals(items) {
  const subtotal = calculateSubtotal(items);
  const tax = calculateTax(subtotal);
  const shipping = calculateShipping(items);
  
  return {
    subtotal,
    tax,
    shipping,
    total: subtotal + tax + shipping
  };
}
```

## When to Extract

### Length-Based Rules
- Functions longer than 20-30 lines
- Nested blocks that could stand alone
- Loops with complex bodies

### Intent-Based Rules
- Code that needs a comment to explain it
- Repetitive patterns
- Complex conditional logic
- Mixed levels of abstraction

### Code Smells
```javascript
// Long parameter lists
function processPayment(amount, currency, cardNumber, cardExpiry, 
                      cardCvv, billingAddress, customerEmail, 
                      merchantId, transactionId) {
  // Extract into objects or smaller functions
}

// Deeply nested conditionals
if (customer.isVIP) {
  if (order.total > 1000) {
    if (customer.region === 'US') {
      // Extract this logic
    }
  }
}

// Comments indicating separate concerns
function processOrder(order) {
  // Validate order
  if (!order.customer) { /* ... */ }
  
  // Calculate pricing
  let total = 0;
  /* ... */
  
  // Update inventory
  for (let item of order.items) { /* ... */ }
  
  // Send notifications
  sendEmail(order.customer);
}
```

## Trade-offs

### Benefits
- **Readability**: Code becomes self-documenting
- **Reusability**: Extracted functions can be used elsewhere
- **Testability**: Smaller functions are easier to test
- **Debugging**: Easier to isolate and fix problems
- **Maintainability**: Changes are localized

### Drawbacks
- **Performance**: Function call overhead (usually negligible)
- **Complexity**: Can create too many small functions
- **Navigation**: May need to jump between functions
- **Context**: Losing the "big picture" view

## Guidelines

### Good Function Names
```javascript
// Good - describes what the function does
function calculateTotalWithTax(subtotal, taxRate) { }
function isEligibleForDiscount(customer) { }
function formatCurrency(amount, currency) { }

// Bad - vague or implementation-focused
function doStuff() { }
function processData() { }
function handleInput() { }
```

### Function Size
- **Single responsibility**: Each function should do one thing
- **Reasonable length**: 5-20 lines is often ideal
- **Consistent abstraction level**: Don't mix high and low-level operations

### Parameter Guidelines
- **Minimize parameters**: More than 3-4 parameters suggests need for an object
- **Logical grouping**: Related parameters should be grouped
- **Avoid flag parameters**: Use separate functions instead

```javascript
// Bad - flag parameter
function processOrder(order, isUrgent) {
  if (isUrgent) {
    // urgent processing
  } else {
    // normal processing
  }
}

// Good - separate functions
function processOrder(order) { /* normal processing */ }
function processUrgentOrder(order) { /* urgent processing */ }
```

## Related Refactorings

- [Inline Function](inline-function.md) - The inverse operation
- [Extract Variable](extract-variable.md) - Extract complex expressions first
- [Introduce Parameter Object](introduce-parameter-object.md) - For functions with many parameters
- [Replace Temp with Query](replace-temp-with-query.md) - Extract calculations into functions
- [Split Phase](split-phase.md) - For functions doing multiple distinct tasks