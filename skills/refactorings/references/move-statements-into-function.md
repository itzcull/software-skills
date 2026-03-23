---
title: "Move Statements into Function"
description: "Consolidate repeated or related statements into a function to improve organization and reduce duplication"
category: "Moving Features"
tags: ["move", "statements", "function", "consolidation", "duplication"]
related: ["move-statements-to-callers", "extract-function", "slide-statements"]
---

# Move Statements into Function

Consolidate repeated or related statements into a function to improve code organization and reduce duplication. When you see the same code pattern appearing before or after function calls, it's often a sign that those statements belong inside the function.

## Inverse

[Move Statements to Callers](move-statements-to-callers.md)

## Motivation

Code often evolves to have repeated patterns around function calls. These patterns might be:
- Setup code that prepares data for the function
- Cleanup code that processes results
- Logging or debugging statements
- Error handling patterns

Moving these statements into the function reduces duplication and ensures consistency.

## Example

### Basic Example
```javascript
// Before - Repeated pattern around function calls
function renderPerson(person) {
  const result = [];
  result.push(`<p>${person.name}</p>`);
  result.push(`<p>title: ${person.photo.title}</p>`);
  result.concat(photoData(person.photo));
  return result;
}

function photoData(photo) {
  return [
    `<p>location: ${photo.location}</p>`,
    `<p>date: ${photo.date.toDateString()}</p>`
  ];
}

function renderPhoto(photo) {
  const result = [];
  result.push(`<p>title: ${photo.title}</p>`);
  result.concat(photoData(photo));
  return result;
}

// After - Title rendering moved into photoData
function renderPerson(person) {
  const result = [];
  result.push(`<p>${person.name}</p>`);
  result.concat(photoData(person.photo));
  return result;
}

function photoData(photo) {
  return [
    `<p>title: ${photo.title}</p>`,
    `<p>location: ${photo.location}</p>`,
    `<p>date: ${photo.date.toDateString()}</p>`
  ];
}

function renderPhoto(photo) {
  return photoData(photo);
}
```

### Complex Example - Database Operations
```javascript
// Before - Repeated transaction pattern
class UserRepository {
  createUser(userData) {
    const connection = database.getConnection();
    connection.beginTransaction();
    
    try {
      const user = connection.insert('users', userData);
      connection.commit();
      logger.info(`User created: ${user.id}`);
      cache.invalidate('users');
      return user;
    } catch (error) {
      connection.rollback();
      logger.error(`Failed to create user: ${error.message}`);
      throw error;
    } finally {
      connection.release();
    }
  }
  
  updateUser(id, updates) {
    const connection = database.getConnection();
    connection.beginTransaction();
    
    try {
      const user = connection.update('users', id, updates);
      connection.commit();
      logger.info(`User updated: ${id}`);
      cache.invalidate('users');
      cache.invalidate(`user:${id}`);
      return user;
    } catch (error) {
      connection.rollback();
      logger.error(`Failed to update user ${id}: ${error.message}`);
      throw error;
    } finally {
      connection.release();
    }
  }
  
  deleteUser(id) {
    const connection = database.getConnection();
    connection.beginTransaction();
    
    try {
      connection.delete('users', id);
      connection.commit();
      logger.info(`User deleted: ${id}`);
      cache.invalidate('users');
      cache.invalidate(`user:${id}`);
      return true;
    } catch (error) {
      connection.rollback();
      logger.error(`Failed to delete user ${id}: ${error.message}`);
      throw error;
    } finally {
      connection.release();
    }
  }
}

// After - Transaction pattern moved into helper function
class UserRepository {
  createUser(userData) {
    return this._executeInTransaction('create', (connection) => {
      return connection.insert('users', userData);
    }, (result) => {
      logger.info(`User created: ${result.id}`);
      cache.invalidate('users');
    });
  }
  
  updateUser(id, updates) {
    return this._executeInTransaction('update', (connection) => {
      return connection.update('users', id, updates);
    }, (result) => {
      logger.info(`User updated: ${id}`);
      cache.invalidate('users');
      cache.invalidate(`user:${id}`);
    });
  }
  
  deleteUser(id) {
    return this._executeInTransaction('delete', (connection) => {
      connection.delete('users', id);
      return true;
    }, () => {
      logger.info(`User deleted: ${id}`);
      cache.invalidate('users');
      cache.invalidate(`user:${id}`);
    });
  }
  
  _executeInTransaction(operation, work, onSuccess) {
    const connection = database.getConnection();
    connection.beginTransaction();
    
    try {
      const result = work(connection);
      connection.commit();
      if (onSuccess) {
        onSuccess(result);
      }
      return result;
    } catch (error) {
      connection.rollback();
      logger.error(`Failed to ${operation} user: ${error.message}`);
      throw error;
    } finally {
      connection.release();
    }
  }
}
```

### API Response Pattern
```javascript
// Before - Repeated response handling
class APIController {
  getUser(req, res) {
    try {
      const user = userService.findById(req.params.id);
      
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('X-Response-Time', Date.now() - req.startTime);
      
      if (!user) {
        res.status(404);
        res.json({ error: 'User not found' });
        return;
      }
      
      res.status(200);
      res.json({ data: user });
    } catch (error) {
      handleError(error, res);
    }
  }
  
  getUsers(req, res) {
    try {
      const users = userService.findAll(req.query);
      
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('X-Response-Time', Date.now() - req.startTime);
      
      res.status(200);
      res.json({ data: users, count: users.length });
    } catch (error) {
      handleError(error, res);
    }
  }
  
  createUser(req, res) {
    try {
      const user = userService.create(req.body);
      
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('X-Response-Time', Date.now() - req.startTime);
      
      res.status(201);
      res.json({ data: user });
    } catch (error) {
      handleError(error, res);
    }
  }
}

// After - Response handling moved into helper
class APIController {
  getUser(req, res) {
    this._handleRequest(req, res, async () => {
      const user = userService.findById(req.params.id);
      
      if (!user) {
        return { status: 404, body: { error: 'User not found' } };
      }
      
      return { status: 200, body: { data: user } };
    });
  }
  
  getUsers(req, res) {
    this._handleRequest(req, res, async () => {
      const users = userService.findAll(req.query);
      return { status: 200, body: { data: users, count: users.length } };
    });
  }
  
  createUser(req, res) {
    this._handleRequest(req, res, async () => {
      const user = userService.create(req.body);
      return { status: 201, body: { data: user } };
    });
  }
  
  _handleRequest(req, res, handler) {
    try {
      const result = handler();
      
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('X-Response-Time', Date.now() - req.startTime);
      
      res.status(result.status);
      res.json(result.body);
    } catch (error) {
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('X-Response-Time', Date.now() - req.startTime);
      
      handleError(error, res);
    }
  }
}
```

### Validation Pattern
```javascript
// Before - Repeated validation
function processOrder(orderData) {
  if (!orderData) {
    throw new Error('Order data is required');
  }
  
  if (!orderData.customerId) {
    throw new Error('Customer ID is required');
  }
  
  if (!orderData.items || orderData.items.length === 0) {
    throw new Error('Order must have items');
  }
  
  const order = createOrder(orderData);
  return order;
}

function updateOrder(id, updates) {
  if (!updates) {
    throw new Error('Update data is required');
  }
  
  if (updates.items !== undefined) {
    if (!Array.isArray(updates.items) || updates.items.length === 0) {
      throw new Error('Order must have items');
    }
  }
  
  const order = applyUpdates(id, updates);
  return order;
}

// After - Validation moved into functions
function processOrder(orderData) {
  const order = createOrder(orderData);
  return order;
}

function updateOrder(id, updates) {
  const order = applyUpdates(id, updates);
  return order;
}

function createOrder(orderData) {
  validateOrderData(orderData, true);
  // Create order logic
}

function applyUpdates(id, updates) {
  validateOrderData(updates, false);
  // Update logic
}

function validateOrderData(data, isNew) {
  if (!data) {
    throw new Error('Order data is required');
  }
  
  if (isNew && !data.customerId) {
    throw new Error('Customer ID is required');
  }
  
  if (isNew || data.items !== undefined) {
    if (!data.items || !Array.isArray(data.items) || data.items.length === 0) {
      throw new Error('Order must have items');
    }
  }
}
```

## Mechanics

1. **Identify the repeated pattern**
   - Look for similar code before/after function calls
   - Find common setup or cleanup code
   - Note any variations in the pattern

2. **Choose where to move the statements**
   - Into the existing function if it makes sense
   - Into a new wrapper function if needed
   - Into a template method if using inheritance

3. **Move statements one at a time**
   - Start with statements that are identical
   - Test after each move
   - Handle variations carefully

4. **Update all call sites**
   - Remove the moved statements
   - Adjust any code that depended on those statements

5. **Consider parameterizing variations**
   - If some call sites have slight differences
   - Add parameters to handle the variations

## When to Use

- **Repeated patterns**: Same code appears around function calls
- **Setup/teardown**: Common initialization or cleanup
- **Cross-cutting concerns**: Logging, timing, error handling
- **Missing abstraction**: Pattern indicates a higher-level operation
- **API consistency**: Ensure all calls follow same pattern

## Trade-offs

### Benefits
- **DRY principle**: Eliminates code duplication
- **Consistency**: Ensures pattern is always followed
- **Maintenance**: Changes happen in one place
- **Abstraction**: Can hide complexity from callers
- **Safety**: Can't forget important steps

### Drawbacks
- **Flexibility**: Harder to customize individual calls
- **Complexity**: May make simple operations more complex
- **Coupling**: Ties behavior together that might change separately
- **Performance**: May do unnecessary work in some cases

## Patterns and Variations

### Template Method Pattern
```javascript
class DataProcessor {
  process(data) {
    this.validate(data);
    const prepared = this.prepare(data);
    const result = this.execute(prepared);
    this.cleanup(result);
    return result;
  }
  
  // Subclasses override these
  validate(data) { }
  prepare(data) { return data; }
  execute(data) { throw new Error('Must implement execute'); }
  cleanup(result) { }
}
```

### Decorator Pattern
```javascript
function withLogging(fn, operationName) {
  return function(...args) {
    console.log(`Starting ${operationName}`);
    const start = Date.now();
    
    try {
      const result = fn.apply(this, args);
      console.log(`Completed ${operationName} in ${Date.now() - start}ms`);
      return result;
    } catch (error) {
      console.error(`Failed ${operationName}: ${error.message}`);
      throw error;
    }
  };
}

// Usage
const saveUser = withLogging(originalSaveUser, 'saveUser');
```

### Command Pattern
```javascript
class DatabaseCommand {
  constructor(operation) {
    this._operation = operation;
  }
  
  execute() {
    const connection = this.getConnection();
    this.beginTransaction(connection);
    
    try {
      const result = this._operation(connection);
      this.commit(connection);
      this.logSuccess(result);
      return result;
    } catch (error) {
      this.rollback(connection);
      this.logError(error);
      throw error;
    } finally {
      this.release(connection);
    }
  }
}
```

## Common Scenarios

### Resource Management
```javascript
// Before
const file = fs.openSync(path, 'r');
const data = processFile(file);
fs.closeSync(file);

// After - Statements moved into function
function processFile(path) {
  const file = fs.openSync(path, 'r');
  try {
    // Original processFile logic here
    return data;
  } finally {
    fs.closeSync(file);
  }
}
```

### Performance Monitoring
```javascript
// Before
const start = performance.now();
const result = complexCalculation(data);
metrics.record('calculation.time', performance.now() - start);

// After
function complexCalculation(data) {
  const start = performance.now();
  try {
    // Original calculation logic
    return result;
  } finally {
    metrics.record('calculation.time', performance.now() - start);
  }
}
```

### Caching Pattern
```javascript
// Before
const cacheKey = `user:${id}`;
let user = cache.get(cacheKey);
if (!user) {
  user = loadUser(id);
  cache.set(cacheKey, user);
}

// After
function loadUser(id) {
  const cacheKey = `user:${id}`;
  let user = cache.get(cacheKey);
  if (user) {
    return user;
  }
  
  // Original loadUser logic
  user = database.findUser(id);
  cache.set(cacheKey, user);
  return user;
}
```

## Related Refactorings

- [Move Statements to Callers](move-statements-to-callers.md) - The inverse operation
- [Extract Function](extract-function.md) - Create function for the statements
- [Consolidate Duplicate Conditional Fragments](consolidate-conditional-expression.md) - Similar concept for conditionals
- [Form Template Method](extract-superclass.md) - For inheritance hierarchies
- [Replace Loop with Pipeline](replace-loop-with-pipeline.md) - Similar consolidation concept