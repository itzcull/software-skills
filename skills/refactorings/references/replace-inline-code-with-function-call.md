---
title: "Replace Inline Code with Function Call"
description: "Replace duplicated inline code with a call to an existing function"
category: "Organization"
tags: ["inline", "function-call", "duplication", "centralization"]
related: ["extract-function", "inline-function", "substitute-algorithm"]
---

# Replace Inline Code with Function Call

Replace duplicated inline code with a call to an existing function. This eliminates code duplication and centralizes common logic in one place.

## Motivation

Duplicated inline code creates several problems:

- **Code duplication**: Same logic repeated in multiple places
- **Maintenance burden**: Changes must be made in multiple locations
- **Inconsistency**: Duplicated code can diverge over time
- **Increased bugs**: More places where errors can occur
- **Larger codebase**: Unnecessary code bloat
- **Poor readability**: Repeated code obscures the main logic

## Example

### Basic Example
```javascript
// Before - Duplicated validation logic
class UserRegistration {
  validateEmail(email) {
    // Email validation logic
    if (!email || typeof email !== 'string') {
      return false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email.toLowerCase().trim());
  }
  
  registerUser(userData) {
    // Inline email validation - duplicates validateEmail logic
    if (!userData.email || typeof userData.email !== 'string') {
      throw new Error('Invalid email format');
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(userData.email.toLowerCase().trim())) {
      throw new Error('Invalid email format');
    }
    
    // Registration logic...
    return this._createUser(userData);
  }
  
  updateEmail(userId, newEmail) {
    // Inline email validation again - third copy!
    if (!newEmail || typeof newEmail !== 'string') {
      throw new Error('Invalid email format');
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(newEmail.toLowerCase().trim())) {
      throw new Error('Invalid email format');
    }
    
    // Update logic...
    return this._updateUserEmail(userId, newEmail);
  }
}

// After - Use existing function
class UserRegistration {
  validateEmail(email) {
    if (!email || typeof email !== 'string') {
      return false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email.toLowerCase().trim());
  }
  
  registerUser(userData) {
    // Use existing validation function
    if (!this.validateEmail(userData.email)) {
      throw new Error('Invalid email format');
    }
    
    // Registration logic...
    return this._createUser(userData);
  }
  
  updateEmail(userId, newEmail) {
    // Use existing validation function
    if (!this.validateEmail(newEmail)) {
      throw new Error('Invalid email format');
    }
    
    // Update logic...
    return this._updateUserEmail(userId, newEmail);
  }
}
```

### Complex Example - Data Processing
```javascript
// Before - Repeated data transformation logic
class DataProcessor {
  normalizeData(data) {
    // Complex normalization logic
    let normalized = data.map(item => ({
      ...item,
      name: item.name ? item.name.trim().toLowerCase() : '',
      email: item.email ? item.email.trim().toLowerCase() : '',
      createdAt: item.createdAt ? new Date(item.createdAt) : new Date()
    }));
    
    // Remove duplicates based on email
    const emailMap = new Map();
    normalized = normalized.filter(item => {
      if (emailMap.has(item.email)) {
        return false;
      }
      emailMap.set(item.email, true);
      return true;
    });
    
    return normalized;
  }
  
  processUserImport(importData) {
    // Inline normalization - duplicates normalizeData logic
    let processedData = importData.map(item => ({
      ...item,
      name: item.name ? item.name.trim().toLowerCase() : '',
      email: item.email ? item.email.trim().toLowerCase() : '',
      createdAt: item.createdAt ? new Date(item.createdAt) : new Date()
    }));
    
    // Remove duplicates - same logic as above
    const emailMap = new Map();
    processedData = processedData.filter(item => {
      if (emailMap.has(item.email)) {
        return false;
      }
      emailMap.set(item.email, true);
      return true;
    });
    
    // Additional import-specific processing
    return processedData.map(user => ({
      ...user,
      source: 'import',
      importedAt: new Date()
    }));
  }
  
  syncUserData(externalData) {
    // Inline normalization again - third copy!
    let syncedData = externalData.map(item => ({
      ...item,
      name: item.name ? item.name.trim().toLowerCase() : '',
      email: item.email ? item.email.trim().toLowerCase() : '',
      createdAt: item.createdAt ? new Date(item.createdAt) : new Date()
    }));
    
    // Remove duplicates - same logic repeated
    const emailMap = new Map();
    syncedData = syncedData.filter(item => {
      if (emailMap.has(item.email)) {
        return false;
      }
      emailMap.set(item.email, true);
      return true;
    });
    
    // Sync-specific processing
    return syncedData.map(user => ({
      ...user,
      lastSyncAt: new Date(),
      source: 'external_sync'
    }));
  }
  
  mergeUserData(primaryData, secondaryData) {
    // Normalize both datasets - inline duplication
    let normalizedPrimary = primaryData.map(item => ({
      ...item,
      name: item.name ? item.name.trim().toLowerCase() : '',
      email: item.email ? item.email.trim().toLowerCase() : '',
      createdAt: item.createdAt ? new Date(item.createdAt) : new Date()
    }));
    
    let normalizedSecondary = secondaryData.map(item => ({
      ...item,
      name: item.name ? item.name.trim().toLowerCase() : '',
      email: item.email ? item.email.trim().toLowerCase() : '',
      createdAt: item.createdAt ? new Date(item.createdAt) : new Date()
    }));
    
    // Remove duplicates from each dataset
    const primaryEmailMap = new Map();
    normalizedPrimary = normalizedPrimary.filter(item => {
      if (primaryEmailMap.has(item.email)) {
        return false;
      }
      primaryEmailMap.set(item.email, true);
      return true;
    });
    
    const secondaryEmailMap = new Map();
    normalizedSecondary = normalizedSecondary.filter(item => {
      if (secondaryEmailMap.has(item.email)) {
        return false;
      }
      secondaryEmailMap.set(item.email, true);
      return true;
    });
    
    // Merge logic...
    return [...normalizedPrimary, ...normalizedSecondary];
  }
}

// After - Use existing normalization function
class DataProcessor {
  normalizeData(data) {
    // Complex normalization logic in one place
    let normalized = data.map(item => ({
      ...item,
      name: item.name ? item.name.trim().toLowerCase() : '',
      email: item.email ? item.email.trim().toLowerCase() : '',
      createdAt: item.createdAt ? new Date(item.createdAt) : new Date()
    }));
    
    // Remove duplicates based on email
    const emailMap = new Map();
    normalized = normalized.filter(item => {
      if (emailMap.has(item.email)) {
        return false;
      }
      emailMap.set(item.email, true);
      return true;
    });
    
    return normalized;
  }
  
  processUserImport(importData) {
    // Use existing normalization function
    const normalizedData = this.normalizeData(importData);
    
    // Additional import-specific processing
    return normalizedData.map(user => ({
      ...user,
      source: 'import',
      importedAt: new Date()
    }));
  }
  
  syncUserData(externalData) {
    // Use existing normalization function
    const normalizedData = this.normalizeData(externalData);
    
    // Sync-specific processing
    return normalizedData.map(user => ({
      ...user,
      lastSyncAt: new Date(),
      source: 'external_sync'
    }));
  }
  
  mergeUserData(primaryData, secondaryData) {
    // Use existing normalization function for both datasets
    const normalizedPrimary = this.normalizeData(primaryData);
    const normalizedSecondary = this.normalizeData(secondaryData);
    
    // Merge logic...
    return [...normalizedPrimary, ...normalizedSecondary];
  }
}
```

### Utility Functions Example
```javascript
// Before - Repeated utility logic
class OrderProcessor {
  formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(amount);
  }
  
  calculateOrderTotal(order) {
    const subtotal = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const tax = subtotal * 0.08;
    const shipping = order.shippingMethod === 'express' ? 15.00 : 5.00;
    const total = subtotal + tax + shipping;
    
    return {
      subtotal: subtotal,
      tax: tax,
      shipping: shipping,
      total: total,
      // Inline currency formatting - duplicates formatCurrency
      formatted: {
        subtotal: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 2
        }).format(subtotal),
        tax: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 2
        }).format(tax),
        shipping: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 2
        }).format(shipping),
        total: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 2
        }).format(total)
      }
    };
  }
  
  generateInvoice(order) {
    const orderTotals = this.calculateOrderTotal(order);
    
    return {
      orderNumber: order.id,
      customerName: order.customer.name,
      items: order.items.map(item => ({
        name: item.name,
        quantity: item.quantity,
        unitPrice: item.price,
        // Inline currency formatting again
        formattedUnitPrice: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 2
        }).format(item.price),
        lineTotal: item.price * item.quantity,
        formattedLineTotal: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 2
        }).format(item.price * item.quantity)
      })),
      totals: orderTotals
    };
  }
  
  generateReceipt(order, payment) {
    const orderTotals = this.calculateOrderTotal(order);
    
    return {
      receiptNumber: `R-${Date.now()}`,
      orderNumber: order.id,
      paymentMethod: payment.method,
      // Inline currency formatting yet again
      amountPaid: new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
      }).format(payment.amount),
      change: new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
      }).format(payment.amount - orderTotals.total),
      timestamp: new Date().toISOString()
    };
  }
}

// After - Use existing utility function
class OrderProcessor {
  formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(amount);
  }
  
  calculateOrderTotal(order) {
    const subtotal = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const tax = subtotal * 0.08;
    const shipping = order.shippingMethod === 'express' ? 15.00 : 5.00;
    const total = subtotal + tax + shipping;
    
    return {
      subtotal: subtotal,
      tax: tax,
      shipping: shipping,
      total: total,
      // Use existing currency formatting function
      formatted: {
        subtotal: this.formatCurrency(subtotal),
        tax: this.formatCurrency(tax),
        shipping: this.formatCurrency(shipping),
        total: this.formatCurrency(total)
      }
    };
  }
  
  generateInvoice(order) {
    const orderTotals = this.calculateOrderTotal(order);
    
    return {
      orderNumber: order.id,
      customerName: order.customer.name,
      items: order.items.map(item => ({
        name: item.name,
        quantity: item.quantity,
        unitPrice: item.price,
        // Use existing currency formatting function
        formattedUnitPrice: this.formatCurrency(item.price),
        lineTotal: item.price * item.quantity,
        formattedLineTotal: this.formatCurrency(item.price * item.quantity)
      })),
      totals: orderTotals
    };
  }
  
  generateReceipt(order, payment) {
    const orderTotals = this.calculateOrderTotal(order);
    
    return {
      receiptNumber: `R-${Date.now()}`,
      orderNumber: order.id,
      paymentMethod: payment.method,
      // Use existing currency formatting function
      amountPaid: this.formatCurrency(payment.amount),
      change: this.formatCurrency(payment.amount - orderTotals.total),
      timestamp: new Date().toISOString()
    };
  }
}
```

### Error Handling Example
```javascript
// Before - Duplicated error handling logic
class ApiClient {
  logError(error, context) {
    console.error(`[${new Date().toISOString()}] ${context}:`, {
      message: error.message,
      stack: error.stack,
      context: context
    });
  }
  
  async fetchUsers() {
    try {
      const response = await fetch('/api/users');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      // Inline error logging - duplicates logError
      console.error(`[${new Date().toISOString()}] fetchUsers:`, {
        message: error.message,
        stack: error.stack,
        context: 'fetchUsers'
      });
      throw error;
    }
  }
  
  async createUser(userData) {
    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      // Inline error logging again
      console.error(`[${new Date().toISOString()}] createUser:`, {
        message: error.message,
        stack: error.stack,
        context: 'createUser'
      });
      throw error;
    }
  }
  
  async updateUser(id, userData) {
    try {
      const response = await fetch(`/api/users/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      // Inline error logging third time
      console.error(`[${new Date().toISOString()}] updateUser:`, {
        message: error.message,
        stack: error.stack,
        context: 'updateUser'
      });
      throw error;
    }
  }
}

// After - Use existing error logging function
class ApiClient {
  logError(error, context) {
    console.error(`[${new Date().toISOString()}] ${context}:`, {
      message: error.message,
      stack: error.stack,
      context: context
    });
  }
  
  async fetchUsers() {
    try {
      const response = await fetch('/api/users');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      // Use existing error logging function
      this.logError(error, 'fetchUsers');
      throw error;
    }
  }
  
  async createUser(userData) {
    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      // Use existing error logging function
      this.logError(error, 'createUser');
      throw error;
    }
  }
  
  async updateUser(id, userData) {
    try {
      const response = await fetch(`/api/users/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      // Use existing error logging function
      this.logError(error, 'updateUser');
      throw error;
    }
  }
}
```

## Mechanics

1. **Identify duplicated code**
   - Look for identical or very similar code blocks
   - Find repeated patterns across methods
   - Check for inline logic that matches existing functions

2. **Locate existing function**
   - Find the function that already implements the needed logic
   - Ensure the function is accessible from the duplication site
   - Verify that the function signature matches the inline code needs

3. **Replace inline code with function call**
   - Remove the duplicated inline code
   - Add a call to the existing function
   - Pass appropriate parameters to the function

4. **Handle parameter differences**
   - If parameters don't match exactly, consider adapting the call
   - Extract variables for complex parameter expressions
   - Consider whether the existing function needs modification

5. **Test thoroughly**
   - Verify that the function call produces the same results
   - Check that all edge cases are handled correctly
   - Ensure no regressions are introduced

6. **Update related code**
   - Look for other instances of the same duplication
   - Consider extracting functions if no suitable function exists
   - Update comments and documentation

## When to Use

- **Exact duplication**: Code is identical or nearly identical
- **Existing function**: A suitable function already exists
- **Accessible scope**: The function can be called from the duplication site
- **Same purpose**: The duplicated code serves the same logical purpose
- **Stable function**: The existing function is stable and well-tested
- **Maintenance burden**: Duplication is causing maintenance issues

## When NOT to Use

- **Different contexts**: Code looks similar but serves different purposes
- **Performance critical**: Function call overhead is unacceptable
- **Temporary duplication**: Planning to refactor both copies soon
- **Unstable function**: Existing function is likely to change
- **Complex adaptation**: Would require significant changes to make it work

## Trade-offs

### Benefits
- **Eliminates duplication**: Reduces code repetition
- **Centralized logic**: Changes happen in one place
- **Consistency**: All usages follow the same implementation
- **Reduced bugs**: Fewer places where errors can occur
- **Smaller codebase**: Less code to maintain
- **Improved readability**: Less noise in the main logic

### Drawbacks
- **Function dependency**: Creates coupling to the existing function
- **Performance overhead**: Function call may be slower than inline code
- **Reduced flexibility**: All usages must work with the same function
- **Debugging complexity**: May need to step through additional function calls

## Detection Strategies

### Manual Review
```javascript
// Look for repeated patterns like this:

// Pattern 1: Repeated validation
if (!email || typeof email !== 'string' || !email.includes('@')) {
  throw new Error('Invalid email');
}

// Pattern 2: Repeated formatting
const formatted = value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');

// Pattern 3: Repeated error handling
catch (error) {
  console.error('Operation failed:', error.message);
  throw error;
}
```

### Code Analysis Tools
```bash
# Use tools to find duplicated code
npx jscpd src/
npx duplicate-code-detection-tool
```

### IDE Features
```javascript
// Many IDEs can detect and highlight duplicated code blocks
// Look for gray highlighting or duplicate code warnings
```

## Best Practices

### Verify Function Compatibility
```javascript
// Before replacing, ensure the function does exactly what you need
function existingFunction(param) {
  // Check: Does this handle all the cases your inline code handled?
  // Check: Does this return the same type/format?
  // Check: Does this have the same error handling?
}
```

### Handle Parameter Differences
```javascript
// If parameters don't match exactly, adapt the call

// Inline code used:
const result = data.map(item => item.value * 2).filter(val => val > 10);

// Existing function expects different format:
function processValues(values, multiplier, threshold) {
  return values.map(val => val * multiplier).filter(val => val > threshold);
}

// Adapt the call:
const values = data.map(item => item.value);
const result = processValues(values, 2, 10);
```

### Consider Function Location
```javascript
// Ensure the function is accessible

// Option 1: Move function to shared utility
const utils = {
  formatCurrency: (amount) => { /* implementation */ }
};

// Option 2: Make function a class method
class BaseProcessor {
  formatCurrency(amount) { /* implementation */ }
}

// Option 3: Import from module
import { formatCurrency } from './utils';
```

## Related Refactorings

- [Extract Function](extract-function.md) - Create a function if none exists
- [Move Method](move-method.md) - Move function to better location
- [Inline Function](inline-function.md) - The reverse operation
- [Pull Up Method](pull-up-method.md) - Move function to superclass
- [Extract Variable](extract-variable.md) - Simplify function call parameters