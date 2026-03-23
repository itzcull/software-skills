---
title: "Inline Class"
description: "Merge a class that no longer provides significant value into another class to simplify the design"
category: "Inline"
tags: ["inline", "class", "simplification", "merge", "design"]
related: ["extract-class", "collapse-hierarchy", "move-function", "move-field"]
---

# Inline Class

When a class is no longer providing significant value or functionality, merge its responsibilities into another class to simplify the design.

## Inverse

[Extract Class](extract-class.md)

## Motivation

Classes should earn their keep. Sometimes a class becomes too small or loses its purpose:
- Features get moved to other classes through refactoring
- Requirements change and the class is no longer needed
- The class was over-engineered from the start
- The class has become a simple data holder

When a class isn't pulling its weight, it's often better to merge it into another class where its remaining responsibilities make sense.

## Example

### Basic Example
```javascript
// Before - TelephoneNumber class is too simple
class Person {
  constructor(name, areaCode, number) {
    this._name = name;
    this._telephoneNumber = new TelephoneNumber(areaCode, number);
  }
  
  get name() { return this._name; }
  
  get telephoneNumber() {
    return this._telephoneNumber.toString();
  }
  
  get officeAreaCode() { return this._telephoneNumber.areaCode; }
  set officeAreaCode(arg) { this._telephoneNumber.areaCode = arg; }
  
  get officeNumber() { return this._telephoneNumber.number; }
  set officeNumber(arg) { this._telephoneNumber.number = arg; }
}

class TelephoneNumber {
  constructor(areaCode, number) {
    this._areaCode = areaCode;
    this._number = number;
  }
  
  get areaCode() { return this._areaCode; }
  set areaCode(arg) { this._areaCode = arg; }
  
  get number() { return this._number; }
  set number(arg) { this._number = arg; }
  
  toString() {
    return `(${this._areaCode}) ${this._number}`;
  }
}

// After - TelephoneNumber functionality moved to Person
class Person {
  constructor(name, areaCode, number) {
    this._name = name;
    this._officeAreaCode = areaCode;
    this._officeNumber = number;
  }
  
  get name() { return this._name; }
  
  get telephoneNumber() {
    return `(${this._officeAreaCode}) ${this._officeNumber}`;
  }
  
  get officeAreaCode() { return this._officeAreaCode; }
  set officeAreaCode(arg) { this._officeAreaCode = arg; }
  
  get officeNumber() { return this._officeNumber; }
  set officeNumber(arg) { this._officeNumber = arg; }
}
```

### Complex Example - Merging Configuration Classes
```javascript
// Before - Overly granular configuration classes
class DatabaseConfig {
  constructor() {
    this._host = 'localhost';
    this._port = 5432;
    this._database = 'myapp';
  }
  
  get host() { return this._host; }
  set host(value) { this._host = value; }
  
  get port() { return this._port; }
  set port(value) { this._port = value; }
  
  get database() { return this._database; }
  set database(value) { this._database = value; }
  
  getConnectionString() {
    return `postgresql://${this._host}:${this._port}/${this._database}`;
  }
}

class CacheConfig {
  constructor() {
    this._enabled = true;
    this._ttl = 3600;
  }
  
  get enabled() { return this._enabled; }
  set enabled(value) { this._enabled = value; }
  
  get ttl() { return this._ttl; }
  set ttl(value) { this._ttl = value; }
}

class ApplicationConfig {
  constructor() {
    this._database = new DatabaseConfig();\n    this._cache = new CacheConfig();
    this._port = 3000;
    this._env = 'development';
  }
  
  get database() { return this._database; }
  get cache() { return this._cache; }
  get port() { return this._port; }
  get env() { return this._env; }
  
  // Most methods just delegate to sub-configs
  getDatabaseUrl() {
    return this._database.getConnectionString();
  }
  
  isCacheEnabled() {
    return this._cache.enabled;
  }
  
  getCacheTtl() {
    return this._cache.ttl;
  }
}

// After - Simplified single configuration class
class ApplicationConfig {
  constructor() {
    // Database configuration
    this._dbHost = 'localhost';
    this._dbPort = 5432;
    this._dbDatabase = 'myapp';
    
    // Cache configuration
    this._cacheEnabled = true;
    this._cacheTtl = 3600;
    
    // Application configuration
    this._port = 3000;
    this._env = 'development';
  }
  
  // Database accessors
  get dbHost() { return this._dbHost; }
  set dbHost(value) { this._dbHost = value; }
  
  get dbPort() { return this._dbPort; }
  set dbPort(value) { this._dbPort = value; }
  
  get dbDatabase() { return this._dbDatabase; }
  set dbDatabase(value) { this._dbDatabase = value; }
  
  getDatabaseUrl() {
    return `postgresql://${this._dbHost}:${this._dbPort}/${this._dbDatabase}`;
  }
  
  // Cache accessors
  get cacheEnabled() { return this._cacheEnabled; }
  set cacheEnabled(value) { this._cacheEnabled = value; }
  
  get cacheTtl() { return this._cacheTtl; }
  set cacheTtl(value) { this._cacheTtl = value; }
  
  // Application accessors
  get port() { return this._port; }
  set port(value) { this._port = value; }
  
  get env() { return this._env; }
  set env(value) { this._env = value; }
  
  // Configuration validation
  isValid() {
    return this._dbHost && this._dbPort > 0 && this._dbDatabase &&
           this._port > 0 && this._cacheTtl > 0;
  }
  
  // Load from environment
  loadFromEnv() {
    this._dbHost = process.env.DB_HOST || this._dbHost;
    this._dbPort = parseInt(process.env.DB_PORT) || this._dbPort;
    this._dbDatabase = process.env.DB_NAME || this._dbDatabase;
    this._cacheEnabled = process.env.CACHE_ENABLED === 'true';
    this._cacheTtl = parseInt(process.env.CACHE_TTL) || this._cacheTtl;
    this._port = parseInt(process.env.PORT) || this._port;
    this._env = process.env.NODE_ENV || this._env;
  }
}
```

### When Requirements Change
```javascript
// Before - ShippingCalculator became too simple after business rules changed
class Order {
  constructor(items, customer) {
    this._items = items;
    this._customer = customer;
    this._shippingCalculator = new ShippingCalculator();
  }
  
  getShippingCost() {
    return this._shippingCalculator.calculate(this._items, this._customer);
  }
  
  getTotal() {
    const subtotal = this._items.reduce((sum, item) => sum + item.price, 0);
    const shipping = this.getShippingCost();
    return subtotal + shipping;
  }
}

class ShippingCalculator {
  calculate(items, customer) {
    // Business simplified: flat rate for everyone now
    return 10;
  }
}

// After - ShippingCalculator inlined since it's too simple
class Order {
  constructor(items, customer) {
    this._items = items;
    this._customer = customer;
  }
  
  getShippingCost() {
    // Simplified business rule: flat rate
    return 10;
  }
  
  getTotal() {
    const subtotal = this._items.reduce((sum, item) => sum + item.price, 0);
    const shipping = this.getShippingCost();
    return subtotal + shipping;
  }
}
```

## Mechanics

1. **Choose which class to keep**
   - Usually keep the class that has more responsibilities
   - Consider which class name better represents the combined concept
   - Think about which class is more central to the domain

2. **Move all features from the class being removed**
   - Use [Move Field](move-field.md) to move fields
   - Use [Move Method](move-function.md) to move methods
   - Move one feature at a time and test after each move

3. **Update all references to the removed class**
   - Change object creation sites
   - Update variable declarations and type annotations
   - Modify method parameters and return types

4. **Remove the empty class**
   - Delete the class definition
   - Remove any import/require statements
   - Clean up any related configuration or documentation

5. **Test thoroughly**
   - Ensure all functionality still works
   - Check that no references to the old class remain

## Signs a Class Should Be Inlined

### Too Few Responsibilities
```javascript
// Class that only holds data
class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}

// Could be inlined into the class that uses it
class Rectangle {
  constructor(topLeft, bottomRight) {
    this._topLeft = topLeft;    // Point
    this._bottomRight = bottomRight; // Point
  }
  
  // Inline the Point data
  constructor(x1, y1, x2, y2) {
    this._topLeftX = x1;
    this._topLeftY = y1;
    this._bottomRightX = x2;
    this._bottomRightY = y2;
  }
}
```

### Delegating Everything
```javascript
// Class that just delegates to another class
class PersonWrapper {
  constructor(person) {
    this._person = person;
  }
  
  getName() { return this._person.getName(); }
  getAge() { return this._person.getAge(); }
  getEmail() { return this._person.getEmail(); }
  
  // Just use Person directly!
}
```

### Lost Its Purpose
```javascript
// Class that was useful before but not anymore
class UserValidator {
  validate(user) {
    // Used to have complex validation logic
    // Now requirements changed and it's simple
    return user.email && user.name;
  }
}

// Can be inlined into the calling code
function createUser(userData) {
  if (!userData.email || !userData.name) {
    throw new Error('Email and name are required');
  }
  return new User(userData);
}
```

## When to Use

- **Single responsibility lost**: Class no longer has a clear, single purpose
- **Too simple**: Class has very few methods or fields
- **Over-engineering**: Abstraction adds no value
- **Changed requirements**: Business rules simplified the need for the class
- **Delegation only**: Class just forwards calls to another class
- **Testing difficulty**: Class is hard to test in isolation

## Trade-offs

### Benefits
- **Simplicity**: Fewer classes to understand and maintain
- **Reduced complexity**: Less abstraction overhead
- **Better performance**: Eliminates object creation and method call overhead
- **Easier navigation**: Fewer files and classes to navigate
- **Clear ownership**: Functionality has obvious location

### Drawbacks
- **Larger classes**: Remaining class becomes bigger
- **Mixed responsibilities**: May violate single responsibility principle
- **Harder to test**: Fewer isolated units to test
- **Reduced reusability**: Functionality is now tied to specific class
- **Future flexibility**: Harder to separate concerns later

## Guidelines

### When to Inline vs Extract
```javascript
// Inline when class is too simple
class Color {
  constructor(hex) {
    this.hex = hex;
  }
}

// Better as a simple property
class Button {
  constructor(text, colorHex) {
    this.text = text;
    this.color = colorHex; // Just store the hex string
  }
}

// Keep separate when there's real behavior
class Color {
  constructor(hex) {
    this.hex = hex;
  }
  
  toRgb() { /* conversion logic */ }
  getLuminance() { /* calculation */ }
  getContrastRatio(other) { /* comparison */ }
  darken(percentage) { /* modification */ }
}
```

### Avoid Creating God Classes
```javascript
// Bad - inlining everything into one massive class
class Application {
  // Database stuff
  connectToDatabase() { }
  executeQuery() { }
  
  // UI stuff
  renderHTML() { }
  handleClick() { }
  
  // Business logic
  calculatePrice() { }
  processOrder() { }
  
  // ... 50 more methods
}

// Better - inline only related functionality
class OrderService {
  // Order-related functionality only
  calculatePrice() { }
  processOrder() { }
  validateOrder() { }
}
```

### Consider the Domain Model
```javascript
// Don't inline if it represents an important domain concept
class Money {
  constructor(amount, currency) {
    this.amount = amount;
    this.currency = currency;
  }
  
  // Even if simple, Money is an important domain concept
  // Keep it separate for clarity and future enhancement
}
```

## Related Refactorings

- [Extract Class](extract-class.md) - The inverse operation
- [Move Field](move-field.md) - Used during inlining process
- [Move Method](move-function.md) - Used during inlining process
- [Collapse Hierarchy](collapse-hierarchy.md) - Similar concept for inheritance
- [Replace Class with Function](replace-command-with-function.md) - When class becomes too simple