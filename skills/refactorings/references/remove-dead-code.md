---
title: "Remove Dead Code"
description: "Delete code that is never executed or used to reduce clutter and maintenance burden"
category: "Organization"
tags: ["remove", "dead-code", "cleanup", "maintenance", "unused"]
related: ["inline-function", "inline-variable", "remove-setting-method"]
---

# Remove Dead Code

Delete code that is never executed or used. Dead code clutters the codebase, increases maintenance burden, and can confuse developers.

## Motivation

Dead code serves no purpose and creates several problems:

- **Increases complexity**: More code to read and understand
- **Maintenance burden**: Code that needs to be maintained but provides no value
- **Confusion**: Developers waste time understanding unused code
- **Security risks**: Unused code may contain vulnerabilities
- **Build time**: Dead code still needs to be compiled/processed
- **Code coverage**: Can artificially inflate coverage metrics

## Example

### Basic Example
```javascript
// Before - Unused functions and variables
function calculateTax(amount) {
  const TAX_RATE = 0.08;
  const LUXURY_TAX_RATE = 0.15; // Never used
  
  return amount * TAX_RATE;
}

function formatCurrency(amount) {
  return `$${amount.toFixed(2)}`;
}

// This function is never called anywhere
function calculateLuxuryTax(amount) {
  const LUXURY_THRESHOLD = 1000;
  if (amount > LUXURY_THRESHOLD) {
    return amount * 0.15;
  }
  return 0;
}

// Unused variable
const DEPRECATED_API_URL = 'https://old-api.example.com';

// After - Dead code removed
function calculateTax(amount) {
  const TAX_RATE = 0.08;
  return amount * TAX_RATE;
}

function formatCurrency(amount) {
  return `$${amount.toFixed(2)}`;
}
```

### Unreachable Code Example
```javascript
// Before - Code after return statement
function processOrder(order) {
  if (!order) {
    return null;
  }
  
  if (order.status === 'cancelled') {
    return { error: 'Order cancelled' };
    
    // This code is never reached
    console.log('Processing cancelled order');
    order.status = 'processing';
  }
  
  if (order.items.length === 0) {
    throw new Error('No items in order');
    
    // This is also unreachable
    return { error: 'Empty order' };
  }
  
  return processValidOrder(order);
}

// After - Unreachable code removed
function processOrder(order) {
  if (!order) {
    return null;
  }
  
  if (order.status === 'cancelled') {
    return { error: 'Order cancelled' };
  }
  
  if (order.items.length === 0) {
    throw new Error('No items in order');
  }
  
  return processValidOrder(order);
}
```

### Complex Example - Refactoring Remnants
```javascript
// Before - Code left over from refactoring
class UserService {
  constructor(database, cache, logger) {
    this._database = database;
    this._cache = cache;
    this._logger = logger;
    
    // Old configuration that's no longer used
    this._enableLegacyMode = false;
    this._maxRetries = 3;
  }
  
  async getUser(id) {
    const cacheKey = `user:${id}`;
    
    // Check cache first
    let user = await this._cache.get(cacheKey);
    if (user) {
      return user;
    }
    
    // Fetch from database
    user = await this._database.findById(id);
    
    if (user) {
      await this._cache.set(cacheKey, user, 300);
    }
    
    return user;
  }
  
  async createUser(userData) {
    const user = await this._database.create(userData);
    
    // Clear relevant cache entries
    await this._cache.delete(`users:all`);
    
    return user;
  }
  
  // This method was replaced by a more efficient implementation
  // but never removed
  async _legacyGetUser(id) {
    this._logger.info(`Legacy fetch for user ${id}`);
    
    let retries = 0;
    while (retries < this._maxRetries) {
      try {
        const user = await this._database.findById(id);
        if (user) {
          return this._transformLegacyUser(user);
        }
        break;
      } catch (error) {
        retries++;
        if (retries >= this._maxRetries) {
          throw error;
        }
        await this._delay(1000 * retries);
      }
    }
    
    return null;
  }
  
  // Helper method only used by legacy method
  _transformLegacyUser(user) {
    return {
      ...user,
      legacy: true,
      transformedAt: new Date()
    };
  }
  
  // Utility method that's no longer needed
  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  // Old debugging method
  _debugUserCache() {
    console.log('Cache state:', this._cache.getStats());
  }
}

// After - Dead code removed
class UserService {
  constructor(database, cache, logger) {
    this._database = database;
    this._cache = cache;
    this._logger = logger;
  }
  
  async getUser(id) {
    const cacheKey = `user:${id}`;
    
    // Check cache first
    let user = await this._cache.get(cacheKey);
    if (user) {
      return user;
    }
    
    // Fetch from database
    user = await this._database.findById(id);
    
    if (user) {
      await this._cache.set(cacheKey, user, 300);
    }
    
    return user;
  }
  
  async createUser(userData) {
    const user = await this._database.create(userData);
    
    // Clear relevant cache entries
    await this._cache.delete(`users:all`);
    
    return user;
  }
}
```

### Conditional Dead Code Example
```javascript
// Before - Feature flags with dead branches
class PaymentProcessor {
  constructor(config) {
    this._config = config;
    this._enableNewProcessor = config.enableNewProcessor || false;
  }
  
  async processPayment(payment) {
    // Feature flag that's always false in production
    if (this._config.enableExperimentalFeature) {
      return this._processWithExperimentalMethod(payment);
    }
    
    if (this._enableNewProcessor) {
      return this._processWithNewMethod(payment);
    } else {
      return this._processWithOldMethod(payment);
    }
  }
  
  // This method was never actually implemented
  async _processWithExperimentalMethod(payment) {
    throw new Error('Experimental method not implemented');
  }
  
  async _processWithNewMethod(payment) {
    // Current implementation
    const result = await this._chargeCard(payment);
    return {
      success: true,
      transactionId: result.id,
      amount: payment.amount
    };
  }
  
  // Old method that's no longer used
  async _processWithOldMethod(payment) {
    console.log('Using legacy payment processing');
    
    // Complex legacy logic
    const validation = await this._validatePaymentLegacy(payment);
    if (!validation.valid) {
      throw new Error(validation.error);
    }
    
    const transaction = await this._createLegacyTransaction(payment);
    const result = await this._executeLegacyPayment(transaction);
    
    return {
      success: result.status === 'completed',
      transactionId: result.legacyId,
      amount: payment.amount,
      legacy: true
    };
  }
  
  async _validatePaymentLegacy(payment) {
    // Old validation logic
    return { valid: true };
  }
  
  async _createLegacyTransaction(payment) {
    // Legacy transaction creation
    return { id: Date.now() };
  }
  
  async _executeLegacyPayment(transaction) {
    // Legacy payment execution
    return { status: 'completed', legacyId: transaction.id };
  }
}

// After - Dead branches and methods removed
class PaymentProcessor {
  constructor(config) {
    this._config = config;
  }
  
  async processPayment(payment) {
    return this._processWithNewMethod(payment);
  }
  
  async _processWithNewMethod(payment) {
    const result = await this._chargeCard(payment);
    return {
      success: true,
      transactionId: result.id,
      amount: payment.amount
    };
  }
  
  async _chargeCard(payment) {
    // Card charging implementation
    return { id: generateTransactionId() };
  }
}
```

### Import/Export Dead Code Example
```javascript
// Before - Unused imports and exports
// utils.js
export function formatDate(date) {
  return date.toISOString().split('T')[0];
}

export function formatTime(date) {
  return date.toTimeString().split(' ')[0];
}

// This function is exported but never used anywhere
export function formatDateTime(date) {
  return `${formatDate(date)} ${formatTime(date)}`;
}

// Also unused
export function parseDate(dateString) {
  return new Date(dateString);
}

export function isWeekend(date) {
  const day = date.getDay();
  return day === 0 || day === 6;
}

// main.js
import { 
  formatDate, 
  formatTime, 
  formatDateTime,  // Imported but never used
  parseDate,       // Imported but never used
  isWeekend 
} from './utils.js';

function displayEvent(event) {
  console.log(`Event: ${event.name}`);
  console.log(`Date: ${formatDate(event.date)}`);
  console.log(`Time: ${formatTime(event.date)}`);
  
  if (isWeekend(event.date)) {
    console.log('Weekend event!');
  }
}

// After - Unused imports and exports removed
// utils.js
export function formatDate(date) {
  return date.toISOString().split('T')[0];
}

export function formatTime(date) {
  return date.toTimeString().split(' ')[0];
}

export function isWeekend(date) {
  const day = date.getDay();
  return day === 0 || day === 6;
}

// main.js
import { formatDate, formatTime, isWeekend } from './utils.js';

function displayEvent(event) {
  console.log(`Event: ${event.name}`);
  console.log(`Date: ${formatDate(event.date)}`);
  console.log(`Time: ${formatTime(event.date)}`);
  
  if (isWeekend(event.date)) {
    console.log('Weekend event!');
  }
}
```

## Mechanics

1. **Identify dead code**
   - Use static analysis tools to find unused code
   - Look for unreachable code after return/throw statements
   - Check for unused variables, functions, and imports
   - Find conditional branches that are never executed

2. **Verify code is truly unused**
   - Search the entire codebase for references
   - Check for dynamic usage (reflection, eval, etc.)
   - Consider external consumers (APIs, libraries)
   - Review version control history for context

3. **Remove gradually**
   - Start with obviously unused code
   - Remove unreachable code first
   - Clean up unused imports and variables
   - Remove unused functions and classes

4. **Update related code**
   - Remove unused parameters from function calls
   - Clean up related comments and documentation
   - Update build configurations if needed

5. **Test thoroughly**
   - Run all tests to ensure functionality is preserved
   - Check that build processes still work
   - Verify no runtime errors are introduced

## Detection Techniques

### Static Analysis Tools
```bash
# JavaScript/TypeScript
npx eslint --rule 'no-unused-vars: error'
npx tsc --noUnusedLocals --noUnusedParameters

# Find unused exports
npx ts-unused-exports tsconfig.json

# Dead code elimination
npx webpack --mode=production # Tree shaking
```

### Manual Inspection
```javascript
// Look for these patterns:

// 1. Code after return/throw
function example() {
  return value;
  console.log('This is dead'); // Dead code
}

// 2. Unreachable conditions
if (true) {
  return 'always';
} else {
  return 'never'; // Dead code
}

// 3. Unused variables
function process() {
  const unused = 'value'; // Dead code if never referenced
  const used = 'value';
  return used;
}

// 4. Commented out code
// function oldImplementation() {
//   // This should be removed
// }
```

### Runtime Analysis
```javascript
// Add logging to identify unused code paths
class Analytics {
  static trackFunctionCall(functionName) {
    console.log(`Function called: ${functionName}`);
  }
}

// Temporarily add tracking
function suspiciousFunction() {
  Analytics.trackFunctionCall('suspiciousFunction');
  // ... function body
}
```

## When to Use

- **Code reviews**: Remove dead code as part of regular reviews
- **Refactoring**: Clean up after major refactoring efforts
- **Feature removal**: Remove code when features are deprecated
- **Performance optimization**: Reduce bundle size and compilation time
- **Security audits**: Remove potentially vulnerable unused code
- **Maintenance**: Regular cleanup to keep codebase healthy

## Trade-offs

### Benefits
- **Reduced complexity**: Less code to understand and maintain
- **Improved performance**: Smaller bundles, faster builds
- **Better security**: Fewer potential attack vectors
- **Cleaner codebase**: Easier to navigate and understand
- **Accurate metrics**: Better code coverage and analysis

### Risks
- **Lost functionality**: Accidentally removing needed code
- **Breaking changes**: External dependencies on "unused" code
- **Historical value**: Losing reference implementations
- **Time investment**: Effort to identify and verify dead code

## Best Practices

### Safe Removal Process
```javascript
// 1. Mark as deprecated first
/**
 * @deprecated This function is no longer used and will be removed
 */
function oldFunction() {
  console.warn('oldFunction is deprecated');
  // ... implementation
}

// 2. Add removal date
/**
 * @deprecated Since v2.1.0, remove in v3.0.0
 */

// 3. Use feature flags for gradual removal
if (config.enableLegacyFeature) {
  // Legacy code that can be removed when flag is retired
}
```

### Documentation
```javascript
// Document why code was removed
// Removed calculateLuxuryTax() - luxury tax feature was cancelled
// See issue #123 for context
// Last used in commit abc123 (2023-01-15)
```

### Version Control
```bash
# Create dedicated commits for dead code removal
git commit -m "Remove dead code: unused utility functions"

# Tag commits that remove significant functionality
git tag -a "removal/legacy-api" -m "Removed legacy API code"
```

## Tools and Automation

### Linting Rules
```javascript
// .eslintrc.js
module.exports = {
  rules: {
    'no-unused-vars': 'error',
    'no-unreachable': 'error',
    'no-dead-code': 'error'
  }
};
```

### Build Tools
```javascript
// webpack.config.js - Enable tree shaking
module.exports = {
  mode: 'production',
  optimization: {
    usedExports: true,
    sideEffects: false
  }
};
```

### CI/CD Integration
```yaml
# .github/workflows/dead-code.yml
name: Dead Code Detection
on: [push, pull_request]

jobs:
  detect-dead-code:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Find unused exports
        run: npx ts-unused-exports tsconfig.json
      - name: Lint for unused variables
        run: npx eslint --rule 'no-unused-vars: error' .
```

## Related Refactorings

- [Extract Function](extract-function.md) - May reveal dead code
- [Inline Function](inline-function.md) - May create dead code
- [Remove Flag Argument](remove-flag-argument.md) - May eliminate dead branches
- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Alternative to conditional dead code
- [Collapse Hierarchy](collapse-hierarchy.md) - May reveal unused inheritance code