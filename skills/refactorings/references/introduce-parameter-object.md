---
title: "Introduce Parameter Object"
description: "Replace a group of parameters with an object that groups related data together"
category: "Simplifying Function Calls"
tags: ["parameter-object", "function", "parameters", "data-grouping", "simplification"]
related: ["preserve-whole-object", "extract-class", "remove-flag-argument"]
---

# Introduce Parameter Object

Replace a group of parameters with an object that groups related data together. This reduces parameter lists, makes function calls clearer, and creates opportunities for additional behavior.

## Motivation

Long parameter lists and groups of related parameters cause several problems:

- **Long parameter lists**: Functions become hard to understand and use
- **Parameter ordering errors**: Easy to pass parameters in wrong order
- **Repeated parameter groups**: Same group of parameters used in multiple functions
- **Missing cohesion**: Related data is scattered across separate parameters
- **Difficult evolution**: Adding new related data requires changing many function signatures
- **Poor readability**: Function calls become hard to read and understand

## Example

### Basic Example
```javascript
// Before - Long parameter list with related data
class PriceCalculator {
  calculatePrice(quantity, unitPrice, taxRate, discountRate, shippingCost, currency) {
    const subtotal = quantity * unitPrice;
    const discount = subtotal * discountRate;
    const tax = (subtotal - discount) * taxRate;
    const total = subtotal - discount + tax + shippingCost;
    
    return {
      subtotal,
      discount,
      tax,
      shippingCost,
      total,
      currency
    };
  }
  
  formatPrice(quantity, unitPrice, taxRate, discountRate, shippingCost, currency) {
    const result = this.calculatePrice(quantity, unitPrice, taxRate, discountRate, shippingCost, currency);
    return `${result.total.toFixed(2)} ${result.currency}`;
  }
  
  validatePricing(quantity, unitPrice, taxRate, discountRate, shippingCost, currency) {
    return quantity > 0 && 
           unitPrice >= 0 && 
           taxRate >= 0 && 
           discountRate >= 0 && 
           shippingCost >= 0 &&
           currency.length === 3;
  }
}

// Usage - error-prone parameter ordering
const calculator = new PriceCalculator();
const price1 = calculator.calculatePrice(2, 10.99, 0.08, 0.10, 5.99, 'USD');
const price2 = calculator.calculatePrice(1, 25.50, 0.08, 0.15, 'USD', 7.50); // Wrong order!

// After - Parameter object groups related data
class PricingInfo {
  constructor(quantity, unitPrice, taxRate, discountRate, shippingCost, currency) {
    this._quantity = quantity;
    this._unitPrice = unitPrice;
    this._taxRate = taxRate;
    this._discountRate = discountRate;
    this._shippingCost = shippingCost;
    this._currency = currency;
  }
  
  // Getters for encapsulation
  get quantity() { return this._quantity; }
  get unitPrice() { return this._unitPrice; }
  get taxRate() { return this._taxRate; }
  get discountRate() { return this._discountRate; }
  get shippingCost() { return this._shippingCost; }
  get currency() { return this._currency; }
  
  // Parameter object can have its own behavior
  getSubtotal() {
    return this._quantity * this._unitPrice;
  }
  
  getDiscount() {
    return this.getSubtotal() * this._discountRate;
  }
  
  isValid() {
    return this._quantity > 0 && 
           this._unitPrice >= 0 && 
           this._taxRate >= 0 && 
           this._discountRate >= 0 && 
           this._shippingCost >= 0 &&
           this._currency.length === 3;
  }
  
  // Factory method for common scenarios
  static createStandardPricing(quantity, unitPrice, currency) {
    return new PricingInfo(quantity, unitPrice, 0.08, 0.0, 5.99, currency);
  }
}

class PriceCalculator {
  calculatePrice(pricingInfo) {
    if (!pricingInfo.isValid()) {
      throw new Error('Invalid pricing information');
    }
    
    const subtotal = pricingInfo.getSubtotal();
    const discount = pricingInfo.getDiscount();
    const tax = (subtotal - discount) * pricingInfo.taxRate;
    const total = subtotal - discount + tax + pricingInfo.shippingCost;
    
    return {
      subtotal,
      discount,
      tax,
      shippingCost: pricingInfo.shippingCost,
      total,
      currency: pricingInfo.currency
    };
  }
  
  formatPrice(pricingInfo) {
    const result = this.calculatePrice(pricingInfo);
    return `${result.total.toFixed(2)} ${result.currency}`;
  }
  
  validatePricing(pricingInfo) {
    return pricingInfo.isValid();
  }
}

// Usage - clearer and less error-prone
const calculator = new PriceCalculator();

const pricing1 = new PricingInfo(2, 10.99, 0.08, 0.10, 5.99, 'USD');
const price1 = calculator.calculatePrice(pricing1);

const pricing2 = PricingInfo.createStandardPricing(1, 25.50, 'USD');
const price2 = calculator.calculatePrice(pricing2);
```

### Advanced Example - Configuration Object
```javascript
// Before - Complex function with many configuration parameters
class DatabaseConnection {
  connect(host, port, database, username, password, ssl, timeout, retryAttempts, poolSize, maxConnections) {
    console.log(`Connecting to ${host}:${port}/${database}`);
    console.log(`SSL: ${ssl}, Timeout: ${timeout}ms`);
    console.log(`Pool: ${poolSize}, Max: ${maxConnections}, Retries: ${retryAttempts}`);
    
    // Connection logic here
    return { status: 'connected', host, database };
  }
  
  createBackup(host, port, database, username, password, ssl, timeout, retryAttempts, poolSize, maxConnections, backupPath) {
    const connection = this.connect(host, port, database, username, password, ssl, timeout, retryAttempts, poolSize, maxConnections);
    console.log(`Creating backup to ${backupPath}`);
    return { status: 'backup_created', path: backupPath };
  }
}

// After - Configuration object with intelligent defaults
class DatabaseConfig {
  constructor(options = {}) {
    this._host = options.host || 'localhost';
    this._port = options.port || 5432;
    this._database = options.database || 'defaultdb';
    this._username = options.username || 'user';
    this._password = options.password || '';
    this._ssl = options.ssl !== undefined ? options.ssl : true;
    this._timeout = options.timeout || 30000;
    this._retryAttempts = options.retryAttempts || 3;
    this._poolSize = options.poolSize || 10;
    this._maxConnections = options.maxConnections || 100;
  }
  
  // Getters
  get host() { return this._host; }
  get port() { return this._port; }
  get database() { return this._database; }
  get username() { return this._username; }
  get password() { return this._password; }
  get ssl() { return this._ssl; }
  get timeout() { return this._timeout; }
  get retryAttempts() { return this._retryAttempts; }
  get poolSize() { return this._poolSize; }
  get maxConnections() { return this._maxConnections; }
  
  // Configuration object behavior
  getConnectionString() {
    const protocol = this._ssl ? 'postgresql' : 'postgres';
    return `${protocol}://${this._username}:${this._password}@${this._host}:${this._port}/${this._database}`;
  }
  
  isValid() {
    return this._host && 
           this._port > 0 && 
           this._database && 
           this._username &&
           this._timeout > 0 &&
           this._retryAttempts >= 0 &&
           this._poolSize > 0 &&
           this._maxConnections > 0;
  }
  
  // Factory methods for common configurations
  static createLocal(database, username = 'admin') {
    return new DatabaseConfig({
      host: 'localhost',
      database,
      username,
      ssl: false,
      timeout: 5000
    });
  }
  
  static createProduction(host, database, username, password) {
    return new DatabaseConfig({
      host,
      database,
      username,
      password,
      ssl: true,
      timeout: 30000,
      retryAttempts: 5,
      poolSize: 20,
      maxConnections: 200
    });
  }
}

class DatabaseConnection {
  connect(config) {
    if (!config.isValid()) {
      throw new Error('Invalid database configuration');
    }
    
    console.log(`Connecting to ${config.host}:${config.port}/${config.database}`);
    console.log(`SSL: ${config.ssl}, Timeout: ${config.timeout}ms`);
    console.log(`Pool: ${config.poolSize}, Max: ${config.maxConnections}, Retries: ${config.retryAttempts}`);
    
    // Connection logic here
    return { status: 'connected', host: config.host, database: config.database };
  }
  
  createBackup(config, backupPath) {
    const connection = this.connect(config);
    console.log(`Creating backup to ${backupPath}`);
    return { status: 'backup_created', path: backupPath };
  }
}

// Usage - much cleaner and more flexible
const db = new DatabaseConnection();

// Local development
const localConfig = DatabaseConfig.createLocal('myapp_dev', 'developer');
const localConnection = db.connect(localConfig);

// Production with specific settings
const prodConfig = DatabaseConfig.createProduction(
  'prod-db.company.com', 
  'myapp_prod', 
  'produser', 
  'securepassword'
);
const prodConnection = db.connect(prodConfig);

// Custom configuration
const customConfig = new DatabaseConfig({
  host: 'test-db.company.com',
  database: 'test_db',
  username: 'testuser',
  password: 'testpass',
  ssl: false,
  timeout: 10000,
  poolSize: 5
});
const testConnection = db.connect(customConfig);
```

## Mechanics

1. **Identify parameter groups**
   - Find functions with long parameter lists
   - Look for related parameters that appear together
   - Check for repeated parameter patterns across functions

2. **Create parameter object class**
   - Create a class to hold the related parameters
   - Add constructor with appropriate parameters
   - Provide getters for accessing the data

3. **Add object behavior**
   - Move related logic into the parameter object
   - Add validation methods
   - Create factory methods for common scenarios

4. **Update function signatures**
   - Replace parameter list with parameter object
   - Update function implementations to use object properties
   - Maintain backward compatibility if needed

5. **Update callers**
   - Create parameter objects at call sites
   - Use factory methods where appropriate
   - Simplify parameter passing

6. **Test thoroughly**
   - Verify all functions work with new parameter object
   - Test parameter object behavior and validation
   - Check that no functionality is lost

## When to Use

- **Long parameter lists**: Functions with 4+ parameters
- **Related parameters**: Groups of parameters that belong together
- **Repeated patterns**: Same parameters used across multiple functions
- **Configuration data**: Functions that accept configuration options
- **Data transfer objects**: Need to pass data between layers
- **Complex constructors**: Classes with many initialization parameters

## Trade-offs

### Benefits
- **Reduced complexity**: Shorter, clearer parameter lists
- **Better organization**: Related data grouped together
- **Easier evolution**: Can add new fields without changing signatures
- **Reduced errors**: Less chance of parameter ordering mistakes
- **Reusability**: Parameter objects can be reused across functions
- **Enhanced behavior**: Objects can have their own methods and validation

### Drawbacks
- **More classes**: Additional classes to maintain
- **Indirection**: Extra layer between callers and functions
- **Object creation overhead**: Need to create objects for simple calls
- **Breaking changes**: Existing code needs to be updated
- **Potential over-engineering**: May be overkill for simple parameter groups

## Related Refactorings

- [Extract Class](extract-class.md) - Extract parameter object behavior into separate class
- [Preserve Whole Object](preserve-whole-object.md) - Pass entire object instead of individual fields
- [Replace Parameter with Query](replace-parameter-with-query.md) - Remove parameters by getting data from other sources