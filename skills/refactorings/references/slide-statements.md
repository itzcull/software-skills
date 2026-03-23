---
title: "Slide Statements"
description: "Move related statements together to improve code organization and readability"
category: "Organization"
tags: ["slide", "statements", "organization", "readability", "grouping"]
related: ["extract-function", "move-statements-into-function", "split-phase"]
---

# Slide Statements

Move related statements together to improve code organization and readability. This refactoring groups statements that work on the same data or accomplish related tasks.

## Motivation

Scattered statements create several problems:

- **Poor readability**: Related logic is spread throughout a method
- **Hard to understand**: Code flow is difficult to follow
- **Maintenance issues**: Changes require hunting through the method
- **Extract opportunities missed**: Related statements could be extracted as a group
- **Cognitive overhead**: Mental context switching between unrelated operations
- **Bug hiding**: Errors can hide between unrelated statements

## Example

### Basic Example
```javascript
// Before - Scattered statements
function processOrder(orderData) {
  const orderId = generateOrderId();
  
  // Validate customer
  if (!orderData.customerId) {
    throw new Error('Customer ID is required');
  }
  const customer = getCustomer(orderData.customerId);
  if (!customer.isActive) {
    throw new Error('Customer is not active');
  }
  
  // Calculate totals
  let subtotal = 0;
  for (const item of orderData.items) {
    subtotal += item.price * item.quantity;
  }
  
  // More validation
  if (orderData.items.length === 0) {
    throw new Error('Order must have at least one item');
  }
  
  // More total calculations
  const tax = subtotal * 0.08;
  const total = subtotal + tax;
  
  // More customer checks
  if (customer.creditLimit < total) {
    throw new Error('Order exceeds customer credit limit');
  }
  
  // Create order
  const order = {
    id: orderId,
    customerId: orderData.customerId,
    items: orderData.items,
    subtotal,
    tax,
    total,
    createdAt: new Date()
  };
  
  return saveOrder(order);
}

// After - Related statements grouped together
function processOrder(orderData) {
  const orderId = generateOrderId();
  
  // All validation together
  if (!orderData.customerId) {
    throw new Error('Customer ID is required');
  }
  if (orderData.items.length === 0) {
    throw new Error('Order must have at least one item');
  }
  
  // All customer operations together
  const customer = getCustomer(orderData.customerId);
  if (!customer.isActive) {
    throw new Error('Customer is not active');
  }
  
  // All calculation operations together
  let subtotal = 0;
  for (const item of orderData.items) {
    subtotal += item.price * item.quantity;
  }
  const tax = subtotal * 0.08;
  const total = subtotal + tax;
  
  // Credit check after we have the total
  if (customer.creditLimit < total) {
    throw new Error('Order exceeds customer credit limit');
  }
  
  // Order creation
  const order = {
    id: orderId,
    customerId: orderData.customerId,
    items: orderData.items,
    subtotal,
    tax,
    total,
    createdAt: new Date()
  };
  
  return saveOrder(order);
}
```

### Complex Example - User Registration
```javascript
// Before - Mixed concerns throughout method
function registerUser(userData) {
  const userId = generateUserId();
  
  // Email validation
  if (!userData.email) {
    throw new Error('Email is required');
  }
  
  // Password setup
  const salt = generateSalt();
  
  // More email validation
  if (!isValidEmail(userData.email)) {
    throw new Error('Invalid email format');
  }
  
  // More password setup
  const hashedPassword = hashPassword(userData.password, salt);
  
  // Email uniqueness check
  const existingUser = findUserByEmail(userData.email);
  if (existingUser) {
    throw new Error('Email already registered');
  }
  
  // Profile setup
  const profileData = {
    firstName: userData.firstName,
    lastName: userData.lastName,
    dateOfBirth: userData.dateOfBirth
  };
  
  // Password validation
  if (!userData.password || userData.password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  
  // More profile setup
  const profileId = generateProfileId();
  const profile = { ...profileData, id: profileId };
  
  // Audit logging
  const timestamp = new Date();
  logUserAction('user_registration_started', userId, timestamp);
  
  // Settings setup
  const defaultSettings = getDefaultUserSettings();
  
  // User creation
  const user = {
    id: userId,
    email: userData.email.toLowerCase(),
    passwordHash: hashedPassword,
    salt: salt,
    profileId: profileId,
    isActive: true,
    createdAt: timestamp
  };
  
  // More audit logging
  logUserAction('user_created', userId, timestamp);
  
  // Save everything
  const savedProfile = saveProfile(profile);
  const savedUser = saveUser(user);
  const savedSettings = saveUserSettings(userId, defaultSettings);
  
  // Final audit log
  logUserAction('user_registration_completed', userId, new Date());
  
  return {
    user: savedUser,
    profile: savedProfile,
    settings: savedSettings
  };
}

// After - Related statements grouped logically
function registerUser(userData) {
  const userId = generateUserId();
  const timestamp = new Date();
  
  // All input validation together
  if (!userData.email) {
    throw new Error('Email is required');
  }
  if (!isValidEmail(userData.email)) {
    throw new Error('Invalid email format');
  }
  if (!userData.password || userData.password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  
  // Email uniqueness check
  const existingUser = findUserByEmail(userData.email);
  if (existingUser) {
    throw new Error('Email already registered');
  }
  
  // All password-related operations together
  const salt = generateSalt();
  const hashedPassword = hashPassword(userData.password, salt);
  
  // All profile-related operations together
  const profileId = generateProfileId();
  const profileData = {
    firstName: userData.firstName,
    lastName: userData.lastName,
    dateOfBirth: userData.dateOfBirth
  };
  const profile = { ...profileData, id: profileId };
  
  // User object creation
  const user = {
    id: userId,
    email: userData.email.toLowerCase(),
    passwordHash: hashedPassword,
    salt: salt,
    profileId: profileId,
    isActive: true,
    createdAt: timestamp
  };
  
  // Default settings setup
  const defaultSettings = getDefaultUserSettings();
  
  // All audit logging together
  logUserAction('user_registration_started', userId, timestamp);
  logUserAction('user_created', userId, timestamp);
  
  // All save operations together
  const savedProfile = saveProfile(profile);
  const savedUser = saveUser(user);
  const savedSettings = saveUserSettings(userId, defaultSettings);
  
  // Final audit log
  logUserAction('user_registration_completed', userId, new Date());
  
  return {
    user: savedUser,
    profile: savedProfile,
    settings: savedSettings
  };
}
```

### Data Processing Example
```javascript
// Before - Data transformations scattered throughout
function processAnalyticsData(rawData) {
  const results = [];
  
  // Some filtering
  const activeUsers = rawData.users.filter(user => user.isActive);
  
  // Some aggregation
  let totalRevenue = 0;
  
  // More filtering
  const paidOrders = rawData.orders.filter(order => order.status === 'paid');
  
  // Continue aggregation
  for (const order of paidOrders) {
    totalRevenue += order.amount;
  }
  
  // User metrics calculation
  const userMetrics = {
    totalUsers: activeUsers.length,
    newUsersThisMonth: activeUsers.filter(user => 
      isThisMonth(user.createdAt)
    ).length
  };
  
  // More order filtering
  const recentOrders = paidOrders.filter(order => 
    isThisMonth(order.createdAt)
  );
  
  // More user metrics
  userMetrics.averageOrderValue = totalRevenue / paidOrders.length;
  
  // Product analysis
  const productSales = {};
  for (const order of paidOrders) {
    for (const item of order.items) {
      if (!productSales[item.productId]) {
        productSales[item.productId] = {
          quantity: 0,
          revenue: 0,
          productName: item.name
        };
      }
      productSales[item.productId].quantity += item.quantity;
      productSales[item.productId].revenue += item.price * item.quantity;
    }
  }
  
  // More user analysis
  const usersByRegion = activeUsers.reduce((regions, user) => {
    regions[user.region] = (regions[user.region] || 0) + 1;
    return regions;
  }, {});
  
  // Finalize product analysis
  const topProducts = Object.values(productSales)
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 10);
  
  return {
    userMetrics,
    totalRevenue,
    recentOrders: recentOrders.length,
    topProducts,
    usersByRegion
  };
}

// After - Related operations grouped together
function processAnalyticsData(rawData) {
  // All user filtering and analysis together
  const activeUsers = rawData.users.filter(user => user.isActive);
  const newUsersThisMonth = activeUsers.filter(user => 
    isThisMonth(user.createdAt)
  );
  const usersByRegion = activeUsers.reduce((regions, user) => {
    regions[user.region] = (regions[user.region] || 0) + 1;
    return regions;
  }, {});
  
  // All order filtering together
  const paidOrders = rawData.orders.filter(order => order.status === 'paid');
  const recentOrders = paidOrders.filter(order => 
    isThisMonth(order.createdAt)
  );
  
  // All revenue calculations together
  let totalRevenue = 0;
  for (const order of paidOrders) {
    totalRevenue += order.amount;
  }
  const averageOrderValue = totalRevenue / paidOrders.length;
  
  // All product analysis together
  const productSales = {};
  for (const order of paidOrders) {
    for (const item of order.items) {
      if (!productSales[item.productId]) {
        productSales[item.productId] = {
          quantity: 0,
          revenue: 0,
          productName: item.name
        };
      }
      productSales[item.productId].quantity += item.quantity;
      productSales[item.productId].revenue += item.price * item.quantity;
    }
  }
  const topProducts = Object.values(productSales)
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 10);
  
  // All metrics assembly together
  const userMetrics = {
    totalUsers: activeUsers.length,
    newUsersThisMonth: newUsersThisMonth.length,
    averageOrderValue
  };
  
  return {
    userMetrics,
    totalRevenue,
    recentOrders: recentOrders.length,
    topProducts,
    usersByRegion
  };
}
```

### Configuration and Setup Example
```javascript
// Before - Setup operations scattered
function initializeApplication(config) {
  // Logger setup
  const logger = createLogger(config.logging);
  
  // Database connection
  const dbConnection = connectToDatabase(config.database);
  
  // More logger setup
  logger.setLevel(config.logging.level);
  logger.addTransport(new FileTransport(config.logging.file));
  
  // Cache setup
  const cache = new MemoryCache();
  
  // More database setup
  dbConnection.setPoolSize(config.database.poolSize);
  dbConnection.enableQueryLogging(config.database.logQueries);
  
  // More cache setup
  cache.setMaxSize(config.cache.maxSize);
  cache.setTTL(config.cache.defaultTTL);
  
  // Server setup
  const server = createServer();
  
  // Middleware registration
  server.use(requestLogger(logger));
  server.use(errorHandler(logger));
  
  // More server setup
  server.setPort(config.server.port);
  server.setHost(config.server.host);
  
  // Route registration
  server.get('/health', healthCheckHandler);
  server.post('/api/users', createUserHandler);
  
  // Security setup
  server.use(helmet());
  server.use(cors(config.security.cors));
  
  return {
    server,
    database: dbConnection,
    logger,
    cache
  };
}

// After - Related setup operations grouped
function initializeApplication(config) {
  // All logger setup together
  const logger = createLogger(config.logging);
  logger.setLevel(config.logging.level);
  logger.addTransport(new FileTransport(config.logging.file));
  
  // All database setup together
  const dbConnection = connectToDatabase(config.database);
  dbConnection.setPoolSize(config.database.poolSize);
  dbConnection.enableQueryLogging(config.database.logQueries);
  
  // All cache setup together
  const cache = new MemoryCache();
  cache.setMaxSize(config.cache.maxSize);
  cache.setTTL(config.cache.defaultTTL);
  
  // All server setup together
  const server = createServer();
  server.setPort(config.server.port);
  server.setHost(config.server.host);
  
  // All middleware registration together
  server.use(requestLogger(logger));
  server.use(errorHandler(logger));
  server.use(helmet());
  server.use(cors(config.security.cors));
  
  // All route registration together
  server.get('/health', healthCheckHandler);
  server.post('/api/users', createUserHandler);
  
  return {
    server,
    database: dbConnection,
    logger,
    cache
  };
}
```

## Mechanics

1. **Identify related statements**
   - Look for statements that work on the same data
   - Find statements that accomplish similar tasks
   - Check for statements with dependencies between them

2. **Check for dependencies**
   - Ensure moved statements don't break data dependencies
   - Verify that variables are defined before use
   - Check that side effects occur in the correct order

3. **Move statements gradually**
   - Move one statement at a time
   - Test after each move to ensure correctness
   - Use temporary variables if needed to maintain dependencies

4. **Group logically**
   - Group by data being manipulated
   - Group by functional concern
   - Group by temporal requirements

5. **Consider extraction opportunities**
   - Look for groups that could become methods
   - Identify reusable patterns
   - Consider creating helper functions

6. **Test thoroughly**
   - Verify behavior is unchanged
   - Test all code paths
   - Check error conditions

## When to Use

- **Scattered logic**: Related statements are separated by unrelated code
- **Hard to follow**: Code jumps between different concerns
- **Extract preparation**: Before extracting methods from grouped statements
- **Maintenance difficulty**: Changes require hunting through long methods
- **Code review issues**: Reviewers struggle to understand the flow
- **Refactoring preparation**: Before other refactoring operations

## Trade-offs

### Benefits
- **Improved readability**: Related code is together
- **Easier maintenance**: Changes are localized
- **Better understanding**: Code flow is clearer
- **Extract opportunities**: Reveals extraction possibilities
- **Reduced cognitive load**: Less context switching
- **Better organization**: Logical structure is more apparent

### Drawbacks
- **Temporary complexity**: May temporarily disrupt existing patterns
- **Dependency challenges**: Need to be careful about data dependencies
- **Variable scope**: May require adjusting variable declarations
- **Testing overhead**: Need to verify behavior after each move

## Patterns and Guidelines

### Group by Data
```javascript
// Group statements that work on the same data structure
const user = createUser();
user.setName(userData.name);
user.setEmail(userData.email);
user.setRole(userData.role);

const profile = createProfile();
profile.setBio(userData.bio);
profile.setAvatar(userData.avatar);
```

### Group by Phase
```javascript
// Group by operation phase
// Validation phase
validateInput(data);
checkPermissions(user);
verifyConstraints(data);

// Processing phase
const result = processData(data);
const enriched = enrichResult(result);
const formatted = formatOutput(enriched);

// Persistence phase
saveResult(formatted);
updateIndex(formatted);
logOperation(user, formatted);
```

### Group by Error Handling
```javascript
// Group error conditions together
if (!user) throw new Error('User required');
if (!user.isActive) throw new Error('User not active');
if (!user.hasPermission('write')) throw new Error('Insufficient permissions');

// Continue with normal processing
```

### Temporal Grouping
```javascript
// Group operations that must happen in sequence
const transaction = beginTransaction();
const savedUser = saveUser(user);
const savedProfile = saveProfile(profile, savedUser.id);
const result = commitTransaction(transaction);
```

## Related Refactorings

- [Extract Function](extract-function.md) - Extract grouped statements into methods
- [Extract Variable](extract-variable.md) - Extract complex expressions before sliding
- [Split Variable](split-variable.md) - Separate variables with different purposes
- [Remove Dead Code](remove-dead-code.md) - Remove unused statements that clutter code
- [Consolidate Conditional Expression](consolidate-conditional-expression.md) - Group related conditions
- [Split Loop](split-loop.md) - Separate different concerns in loops