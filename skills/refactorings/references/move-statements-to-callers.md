---
title: "Move Statements to Callers"
description: "Move specific statements from a function to its call locations for more flexibility"
category: "Moving Features"
tags: ["move", "statements", "callers", "flexibility", "single-responsibility"]
related: ["move-statements-into-function", "extract-function", "split-phase"]
---

# Move Statements to Callers

Move specific statements from a function to the locations where the function is called, typically to give more flexibility or control to the callers or when the function is doing too many things.

## Inverse

[Move Statements into Function](move-statements-into-function.md)

## Motivation

Sometimes functions accumulate responsibilities that don't belong in all calling contexts. Moving statements out to callers helps when:

- Different callers need different behavior for part of the function
- The function is violating single responsibility principle
- Some callers don't need all the functionality
- You want to make the function more focused and reusable
- The statements are cross-cutting concerns that belong with specific callers

## Example

### Basic Example
```javascript
// Before - Function does too much
function emitPhotoData(outStream, photo) {
  outStream.write(`<p>title: ${photo.title}</p>\\n`);
  outStream.write(`<p>location: ${photo.location}</p>\\n`);
  outStream.write(`<p>date: ${photo.date.toDateString()}</p>\\n`);
}

function listRecentPhotos(photos) {
  photos.filter(p => p.date > lastWeek).forEach(photo => {
    emitPhotoData(outStream, photo);
  });
}

function listPhotoDetails(photo) {
  emitPhotoData(outStream, photo);
}

// After - Location moved to callers for more control
function emitPhotoData(outStream, photo) {
  outStream.write(`<p>title: ${photo.title}</p>\\n`);
  outStream.write(`<p>date: ${photo.date.toDateString()}</p>\\n`);
}

function listRecentPhotos(photos) {
  photos.filter(p => p.date > lastWeek).forEach(photo => {
    emitPhotoData(outStream, photo);
    outStream.write(`<p>location: ${photo.location}</p>\\n`); // Moved out
  });
}

function listPhotoDetails(photo) {
  emitPhotoData(outStream, photo);
  outStream.write(`<p>location: ${photo.location}</p>\\n`); // Moved out
  outStream.write(`<p>GPS: ${photo.gpsCoordinates}</p>\\n`); // Additional detail
}
```

### Complex Example - Different Validation Needs
```javascript
// Before - Validation function tries to handle all cases
function validateAndSaveUser(userData) {
  // Basic validation
  if (!userData.email || !userData.name) {
    throw new Error('Email and name are required');
  }
  
  // Email format validation
  const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  if (!emailRegex.test(userData.email)) {
    throw new Error('Invalid email format');
  }
  
  // Age validation
  if (userData.age && (userData.age < 0 || userData.age > 150)) {
    throw new Error('Invalid age');
  }
  
  // Password strength validation
  if (userData.password && userData.password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  
  // Save user
  const user = database.save('users', userData);
  
  // Send welcome email
  emailService.sendWelcomeEmail(user.email, user.name);
  
  return user;
}

// Different calling contexts
function registerNewUser(registrationData) {
  // New users need full validation
  return validateAndSaveUser(registrationData);
}

function importUsersFromCSV(userRecords) {
  return userRecords.map(userData => {
    // Imported users might not have passwords, different email rules
    return validateAndSaveUser(userData);
  });
}

function updateUserProfile(userId, updates) {
  // Updates don't need password validation or welcome emails
  const existingUser = database.findById('users', userId);
  const updatedData = { ...existingUser, ...updates };
  return validateAndSaveUser(updatedData);
}

// After - Validation moved to callers for flexibility
function saveUser(userData) {
  // Basic validation that applies to all cases
  if (!userData.email || !userData.name) {
    throw new Error('Email and name are required');
  }
  
  // Save user
  return database.save('users', userData);
}

function registerNewUser(registrationData) {
  // Full validation for new registrations
  validateEmailFormat(registrationData.email);
  validateAge(registrationData.age);
  validatePasswordStrength(registrationData.password);
  
  const user = saveUser(registrationData);
  
  // Send welcome email for new registrations
  emailService.sendWelcomeEmail(user.email, user.name);
  
  return user;
}

function importUsersFromCSV(userRecords) {
  return userRecords.map(userData => {
    // Different validation rules for imports
    validateEmailFormat(userData.email);
    if (userData.age) {
      validateAge(userData.age);
    }
    // No password validation for imports
    
    return saveUser(userData);
    // No welcome email for imports
  });
}

function updateUserProfile(userId, updates) {
  const existingUser = database.findById('users', userId);
  const updatedData = { ...existingUser, ...updates };
  
  // Only validate email if it's being changed
  if (updates.email && updates.email !== existingUser.email) {
    validateEmailFormat(updates.email);
  }
  
  // Only validate age if it's being changed
  if (updates.age !== undefined) {
    validateAge(updates.age);
  }
  
  return saveUser(updatedData);
  // No welcome email for updates
}

// Helper functions for validation
function validateEmailFormat(email) {
  const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  if (!emailRegex.test(email)) {
    throw new Error('Invalid email format');
  }
}

function validateAge(age) {
  if (age < 0 || age > 150) {
    throw new Error('Invalid age');
  }
}

function validatePasswordStrength(password) {
  if (password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
}
```

### Logging Example
```javascript
// Before - Function always logs the same way
function processOrder(orderData) {
  console.log(`Processing order: ${orderData.id}`);
  
  const validatedOrder = validateOrder(orderData);
  const pricedOrder = calculatePricing(validatedOrder);
  const savedOrder = saveOrder(pricedOrder);
  
  console.log(`Order processed successfully: ${savedOrder.id}`);
  
  return savedOrder;
}

function handleWebOrder(orderData) {
  return processOrder(orderData);
}

function handleBatchOrders(orders) {
  return orders.map(order => processOrder(order));
}

function handleAPIOrder(orderData) {
  return processOrder(orderData);
}

// After - Logging moved to callers for context-appropriate messages
function processOrder(orderData) {
  const validatedOrder = validateOrder(orderData);
  const pricedOrder = calculatePricing(validatedOrder);
  return saveOrder(pricedOrder);
}

function handleWebOrder(orderData) {
  console.log(`Processing web order: ${orderData.id} from user ${orderData.userId}`);
  
  const order = processOrder(orderData);
  
  console.log(`Web order completed: ${order.id}, total: $${order.total}`);
  auditLog.record('web_order_completed', { orderId: order.id, userId: orderData.userId });
  
  return order;
}

function handleBatchOrders(orders) {
  console.log(`Processing batch of ${orders.length} orders`);
  
  const results = orders.map((orderData, index) => {
    try {
      return processOrder(orderData);
    } catch (error) {
      console.error(`Failed to process order ${index + 1}: ${error.message}`);
      return null;
    }
  });
  
  const successful = results.filter(r => r !== null);
  console.log(`Batch processing complete: ${successful.length}/${orders.length} successful`);
  
  return results;
}

function handleAPIOrder(orderData) {
  const startTime = Date.now();
  console.log(`API order request: ${orderData.id}`);
  
  const order = processOrder(orderData);
  
  const duration = Date.now() - startTime;
  console.log(`API order response: ${order.id} (${duration}ms)`);
  metrics.recordAPICall('order.create', duration);
  
  return order;
}
```

### Error Handling Example
```javascript
// Before - Function handles errors the same way for all callers
function fetchUserData(userId) {
  try {
    const user = database.findUser(userId);
    if (!user) {
      throw new Error('User not found');
    }
    
    const profile = profileService.getProfile(userId);
    const preferences = preferenceService.getPreferences(userId);
    
    return {
      user,
      profile,
      preferences
    };
  } catch (error) {
    // Always logs and rethrows
    logger.error(`Failed to fetch user data for ${userId}: ${error.message}`);
    throw error;
  }
}

// Different calling contexts need different error handling
function getUserForAPI(userId) {
  return fetchUserData(userId); // Wants the exception to bubble up
}

function getUserForUI(userId) {
  return fetchUserData(userId); // Wants to show error message to user
}

function getUserForBatch(userId) {
  return fetchUserData(userId); // Wants to continue processing other users
}

// After - Error handling moved to callers
function fetchUserData(userId) {
  const user = database.findUser(userId);
  if (!user) {
    throw new Error('User not found');
  }
  
  const profile = profileService.getProfile(userId);
  const preferences = preferenceService.getPreferences(userId);
  
  return {
    user,
    profile,
    preferences
  };
}

function getUserForAPI(userId) {
  try {
    return fetchUserData(userId);
  } catch (error) {
    logger.error(`API request failed for user ${userId}: ${error.message}`);
    throw new APIError(error.message, 404);
  }
}

function getUserForUI(userId) {
  try {
    return fetchUserData(userId);
  } catch (error) {
    logger.warn(`UI request failed for user ${userId}: ${error.message}`);
    return {
      error: 'Unable to load user profile. Please try again.',
      user: null,
      profile: null,
      preferences: getDefaultPreferences()
    };
  }
}

function getUserForBatch(userIds) {
  return userIds.map(userId => {
    try {
      return fetchUserData(userId);
    } catch (error) {
      // Log but don't stop processing
      logger.debug(`Batch processing: skipping user ${userId}: ${error.message}`);
      return null;
    }
  }).filter(result => result !== null);
}
```

## Mechanics

1. **Identify statements that don't belong in all contexts**
   - Look for conditional logic based on calling context
   - Find statements that only some callers need
   - Note cross-cutting concerns that vary by caller

2. **Choose which statements to move**
   - Start with statements that clearly belong to specific callers
   - Consider moving all instances or just some

3. **Copy statements to callers**
   - Add the statements before or after the function call
   - Adjust for any local variables or context

4. **Remove statements from the function**
   - Delete the moved statements
   - Test that all callers still work

5. **Consider extracting helper functions**
   - If multiple callers need the same moved logic
   - Create shared utilities for common patterns

## When to Use

- **Different caller needs**: Callers need different behavior for part of the function
- **Cross-cutting concerns**: Logging, monitoring, caching varies by context
- **Over-responsible function**: Function is doing too many things
- **Conditional complexity**: Function has many conditionals based on caller type
- **Reusability**: Want to make function more focused and reusable

## Trade-offs

### Benefits
- **Flexibility**: Callers can customize behavior
- **Single responsibility**: Functions become more focused
- **Testability**: Easier to test smaller, focused functions
- **Reusability**: Core function can be used in more contexts
- **Clarity**: Each caller shows exactly what it's doing

### Drawbacks
- **Duplication**: Same code may appear in multiple callers
- **Complexity**: More places to maintain the same logic
- **Consistency**: Harder to ensure all callers behave consistently
- **Forgetting**: Easy to forget important steps in new callers

## Patterns and Techniques

### Extract Template Method
```javascript
// When callers have similar but slightly different patterns
class OrderProcessor {
  processOrder(order) {
    this.beforeProcessing(order);
    const result = this.doProcessing(order);
    this.afterProcessing(order, result);
    return result;
  }
  
  // Subclasses override these
  beforeProcessing(order) { }
  doProcessing(order) { throw new Error('Must implement'); }
  afterProcessing(order, result) { }
}
```

### Strategy Pattern
```javascript
// When behavior varies significantly by caller
class OrderService {
  constructor(validationStrategy, loggingStrategy) {
    this._validationStrategy = validationStrategy;
    this._loggingStrategy = loggingStrategy;
  }
  
  processOrder(order) {
    this._validationStrategy.validate(order);
    const result = this._doProcessing(order);
    this._loggingStrategy.log(order, result);
    return result;
  }
}
```

### Configuration Objects
```javascript
// When callers need different options
function processOrder(order, options = {}) {
  if (options.validate !== false) {
    validateOrder(order);
  }
  
  const result = doProcessing(order);
  
  if (options.sendEmail) {
    sendNotificationEmail(result);
  }
  
  if (options.logLevel) {
    log(options.logLevel, `Order processed: ${result.id}`);
  }
  
  return result;
}
```

## Common Scenarios

### Caching Strategies
```javascript
// Before - Function always caches
function getUser(id) {
  const cached = cache.get(`user:${id}`);
  if (cached) return cached;
  
  const user = database.findUser(id);
  cache.set(`user:${id}`, user, 3600);
  return user;
}

// After - Callers decide caching
function getUser(id) {
  return database.findUser(id);
}

// Callers handle caching as needed
function getUserFromAPI(id) {
  const cached = cache.get(`user:${id}`);
  if (cached) return cached;
  
  const user = getUser(id);
  cache.set(`user:${id}`, user, 3600);
  return user;
}

function getUserForBatch(id) {
  // No caching for batch operations
  return getUser(id);
}
```

### Response Formatting
```javascript
// Before - Always formats the same way
function searchProducts(query) {
  const results = database.search('products', query);
  return {
    data: results,
    count: results.length,
    timestamp: new Date()
  };
}

// After - Callers format as needed
function searchProducts(query) {
  return database.search('products', query);
}

function searchAPI(query) {
  const results = searchProducts(query);
  return {
    data: results,
    meta: {
      count: results.length,
      timestamp: new Date(),
      query: query
    }
  };
}

function searchInternal(query) {
  // Just return raw results for internal use
  return searchProducts(query);
}
```

## Related Refactorings

- [Move Statements into Function](move-statements-into-function.md) - The inverse operation
- [Extract Function](extract-function.md) - May create functions to move statements to
- [Parameterize Function](parameterize-function.md) - Alternative to moving statements
- [Replace Function with Command](replace-function-with-command.md) - When configuration becomes complex
- [Form Template Method](extract-superclass.md) - Pattern for similar caller variations