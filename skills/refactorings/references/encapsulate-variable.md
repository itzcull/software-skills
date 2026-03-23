---
title: "Encapsulate Variable"
description: "Provide controlled access to a variable by creating getter and setter methods for better data control"
category: "Encapsulation"
tags: ["encapsulation", "variable", "getter", "setter", "data-hiding", "access-control"]
related: ["encapsulate-field", "encapsulate-collection", "self-encapsulate-field"]
---

# Encapsulate Variable

Provide controlled access to a variable by creating getter and setter methods. This allows for future modification of variable access without changing client code.

## Also Known As

- Self-Encapsulate Field
- Encapsulate Field

## Motivation

When data is accessed widely throughout the codebase, it becomes difficult to change how that data is managed. By encapsulating variable access behind functions, we gain:
- **Control**: Can add validation, logging, or other behavior
- **Flexibility**: Can change internal representation without affecting clients
- **Tracking**: Can monitor when and how data is accessed
- **Thread safety**: Can add synchronization if needed

This is especially important for global variables or widely shared data.

## Example

### Global Variable Encapsulation
```javascript
// Before - Direct access to global variable
let defaultOwner = {firstName: "Martin", lastName: "Fowler"};

// Client code accesses directly
console.log(`${defaultOwner.firstName} ${defaultOwner.lastName}`);
defaultOwner = {firstName: "Rebecca", lastName: "Parsons"};

// After - Encapsulated access
let defaultOwnerData = {firstName: "Martin", lastName: "Fowler"};

export function defaultOwner() {
  return defaultOwnerData;
}

export function setDefaultOwner(arg) {
  defaultOwnerData = arg;
}

// Client code uses accessor functions
console.log(`${defaultOwner().firstName} ${defaultOwner().lastName}`);
setDefaultOwner({firstName: "Rebecca", lastName: "Parsons"});
```

### Class Field Encapsulation
```javascript
// Before - Direct field access
class Product {
  constructor(name, price) {
    this.name = name;
    this.price = price;
  }
  
  applyDiscount(percentage) {
    this.price = this.price * (1 - percentage); // Direct access
  }
  
  toString() {
    return `${this.name}: $${this.price}`; // Direct access
  }
}

// After - Encapsulated field access
class Product {
  constructor(name, price) {
    this._name = name;
    this._price = price;
  }
  
  get name() { return this._name; }
  set name(value) {
    if (!value || value.trim() === '') {
      throw new Error('Name cannot be empty');
    }
    this._name = value;
  }
  
  get price() { return this._price; }
  set price(value) {
    if (value < 0) {
      throw new Error('Price cannot be negative');
    }
    this._price = value;
  }
  
  applyDiscount(percentage) {
    this.price = this.price * (1 - percentage); // Uses setter
  }
  
  toString() {
    return `${this.name}: $${this.price}`; // Uses getters
  }
}
```

### With Validation and Logging
```javascript
// Configuration variable with tracking
let currentConfig = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
  retries: 3
};

const configHistory = [];

export function getConfig() {
  console.log('Config accessed at:', new Date().toISOString());
  return {...currentConfig}; // Return copy to prevent modification
}

export function setConfig(newConfig) {
  // Validation
  if (!newConfig.apiUrl) {
    throw new Error('API URL is required');
  }
  if (newConfig.timeout < 1000) {
    throw new Error('Timeout must be at least 1000ms');
  }
  
  // Track changes
  configHistory.push({
    timestamp: new Date(),
    oldConfig: {...currentConfig},
    newConfig: {...newConfig}
  });
  
  currentConfig = {...newConfig};
  console.log('Config updated:', newConfig);
}

export function getConfigHistory() {
  return [...configHistory];
}
```

## Mechanics

1. **Create a getter function**
   - Return the variable value
   - Consider returning a copy if the variable is mutable

2. **Create a setter function (if needed)**
   - Accept the new value as a parameter
   - Add any validation logic
   - Update the variable

3. **Replace all direct variable access**
   - Find all references to the variable
   - Replace reads with calls to the getter
   - Replace writes with calls to the setter

4. **Make the variable private**
   - Move to module scope or rename to indicate privacy
   - Ensure only the accessor functions can reach it

5. **Test after each change**
   - Verify behavior remains the same
   - Test any new validation logic

## Implementation Patterns

### Read-Only Access
```javascript
// For constants or computed values
let _instanceCount = 0;

export function getInstanceCount() {
  return _instanceCount;
}

// Internal function to modify (not exported)
function incrementInstanceCount() {
  _instanceCount++;
}
```

### Lazy Initialization
```javascript
let _expensiveResource = null;

export function getExpensiveResource() {
  if (_expensiveResource === null) {
    console.log('Initializing expensive resource...');
    _expensiveResource = createExpensiveResource();
  }
  return _expensiveResource;
}
```

### Cached Computation
```javascript
let _data = [];
let _cachedSum = null;
let _isDirty = false;

export function getData() {
  return [..._data]; // Return copy
}

export function addData(item) {
  _data.push(item);
  _isDirty = true;
}

export function getSum() {
  if (_isDirty || _cachedSum === null) {
    _cachedSum = _data.reduce((sum, item) => sum + item, 0);
    _isDirty = false;
  }
  return _cachedSum;
}
```

### Thread-Safe Access (Node.js)
```javascript
const { Worker, isMainThread, parentPort } = require('worker_threads');

let _sharedCounter = 0;
const _lock = new Set();

export async function getCounter() {
  return _sharedCounter;
}

export async function incrementCounter() {
  // Simple lock mechanism
  while (_lock.has('counter')) {
    await new Promise(resolve => setTimeout(resolve, 1));
  }
  
  _lock.add('counter');
  try {
    _sharedCounter++;
  } finally {
    _lock.delete('counter');
  }
}
```

## When to Use

- **Global state**: Any variable accessed from multiple modules
- **Configuration**: Application settings that might change
- **Caching**: When you need to control cache invalidation
- **Validation**: When data needs to be validated on changes
- **Monitoring**: When you need to track access patterns
- **Future flexibility**: When you anticipate needing more control

## Trade-offs

### Benefits
- **Encapsulation**: Hide implementation details
- **Validation**: Ensure data integrity
- **Flexibility**: Easy to modify behavior later
- **Debugging**: Can add logging and breakpoints
- **Testing**: Can mock or stub the accessors

### Drawbacks
- **Verbosity**: More code than direct access
- **Performance**: Function call overhead
- **Breaking changes**: Clients must update their code
- **Complexity**: Additional layer of indirection

## Common Mistakes

### Exposing Mutable Objects
```javascript
// Bad - Returns reference to internal object
function getUsers() {
  return users; // Clients can modify the array
}

// Good - Returns copy
function getUsers() {
  return [...users];
}
```

### Forgetting to Update All Access Points
```javascript
// Some code still accesses the variable directly
console.log(oldVariableName); // Missed during refactoring
```

### Over-Encapsulation
```javascript
// Overkill for simple local variables
function processData() {
  let _localCounter = 0;
  
  function getLocalCounter() { return _localCounter; }
  function incrementLocalCounter() { _localCounter++; }
  
  // Just use localCounter directly!
}
```

## Related Refactorings

- [Extract Variable](extract-variable.md) - May create variables that need encapsulation
- [Replace Global with Query](replace-temp-with-query.md) - Alternative to global variables
- [Encapsulate Collection](encapsulate-collection.md) - Specific case for collections
- [Encapsulate Record](encapsulate-record.md) - For structured data
- [Introduce Parameter Object](introduce-parameter-object.md) - Alternative for grouped data