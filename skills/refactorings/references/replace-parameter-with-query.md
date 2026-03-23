---
title: "Replace Parameter with Query"
description: "Remove a parameter from a method and make it get the value through a query or field access"
category: "Simplifying Function Calls"
tags: ["parameter", "query", "simplify", "self-contained", "coupling"]
related: ["replace-query-with-parameter", "preserve-whole-object", "remove-flag-argument"]
---

# Replace Parameter with Query

Remove a parameter from a method and make the method get the value by calling another method or accessing a field. This reduces the parameter list and makes the method more self-contained.

## Motivation

Long parameter lists create several problems:

- **Complexity**: Methods become harder to call and understand
- **Coupling**: Callers must know how to obtain parameter values
- **Duplication**: Same parameter values computed in multiple places
- **Inconsistency**: Different callers may compute parameters differently
- **Maintenance**: Changes to parameter calculation affect all callers

## Example

### Basic Example
```javascript
// Before - Temperature conversion with redundant parameter
class TemperatureCalculator {
  constructor(location) {
    this._location = location;
  }
  
  get location() {
    return this._location;
  }
  
  getCurrentTemperature() {
    // Get temperature from weather service
    return weatherService.getTemperature(this._location);
  }
  
  // Parameter is redundant - location is already available
  convertToFahrenheit(celsius, location) {
    const adjustment = this._getLocationAdjustment(location);
    return (celsius * 9/5) + 32 + adjustment;
  }
  
  convertToCelsius(fahrenheit, location) {
    const adjustment = this._getLocationAdjustment(location);
    return ((fahrenheit - 32) * 5/9) - adjustment;
  }
  
  _getLocationAdjustment(location) {
    // Some locations have calibration adjustments
    const adjustments = {
      'desert': 2,
      'coastal': -1,
      'mountain': 0
    };
    return adjustments[location.type] || 0;
  }
}

// Usage - callers must pass redundant location
const calculator = new TemperatureCalculator({ type: 'coastal', name: 'San Francisco' });
const currentTemp = calculator.getCurrentTemperature();
const fahrenheit = calculator.convertToFahrenheit(currentTemp, calculator.location); // Redundant!

// After - Method gets location itself
class TemperatureCalculator {
  constructor(location) {
    this._location = location;
  }
  
  get location() {
    return this._location;
  }
  
  getCurrentTemperature() {
    return weatherService.getTemperature(this._location);
  }
  
  // Method gets location from instance state
  convertToFahrenheit(celsius) {
    const adjustment = this._getLocationAdjustment();
    return (celsius * 9/5) + 32 + adjustment;
  }
  
  convertToCelsius(fahrenheit) {
    const adjustment = this._getLocationAdjustment();
    return ((fahrenheit - 32) * 5/9) - adjustment;
  }
  
  _getLocationAdjustment() {
    const adjustments = {
      'desert': 2,
      'coastal': -1,
      'mountain': 0
    };
    return adjustments[this._location.type] || 0;
  }
}

// Usage - simpler method calls
const calculator = new TemperatureCalculator({ type: 'coastal', name: 'San Francisco' });
const currentTemp = calculator.getCurrentTemperature();
const fahrenheit = calculator.convertToFahrenheit(currentTemp); // Cleaner!
```

### Complex Example - Order Processing
```javascript
// Before - Multiple redundant parameters
class OrderProcessor {
  constructor(customer, shippingRules, taxRates) {
    this._customer = customer;
    this._shippingRules = shippingRules;
    this._taxRates = taxRates;
  }
  
  // All these parameters can be derived from the order or instance state
  calculateShipping(order, customer, shippingRules) {
    const baseRate = shippingRules.getBaseRate(customer.tier);
    const distance = this._calculateDistance(customer.address, order.destination);
    const weight = order.items.reduce((sum, item) => sum + item.weight, 0);
    
    let cost = baseRate + (distance * 0.01) + (weight * 0.05);
    
    if (customer.isPremium) {
      cost *= 0.9; // 10% discount
    }
    
    return Math.max(cost, 5.00);
  }
  
  calculateTax(order, customer, taxRates) {
    const rate = taxRates.getRate(customer.address.state);
    const taxableAmount = order.items
      .filter(item => item.isTaxable)
      .reduce((sum, item) => sum + item.price * item.quantity, 0);
    
    let tax = taxableAmount * rate;
    
    if (customer.isExempt) {
      tax = 0;
    }
    
    return tax;
  }
  
  calculateDiscount(order, customer) {
    let discount = 0;
    
    // Volume discount
    if (order.total > 100) {
      discount += order.total * 0.05;
    }
    
    // Loyalty discount
    if (customer.loyaltyPoints > 1000) {
      discount += order.total * 0.1;
    }
    
    // First-time customer
    if (customer.isFirstTime) {
      discount += 10;
    }
    
    return Math.min(discount, order.total * 0.5); // Max 50% discount
  }
  
  processOrder(order, customer, shippingRules, taxRates) {
    const shipping = this.calculateShipping(order, customer, shippingRules);
    const tax = this.calculateTax(order, customer, taxRates);
    const discount = this.calculateDiscount(order, customer);
    
    const total = order.subtotal + shipping + tax - discount;
    
    return {
      order,
      shipping,
      tax,
      discount,
      total
    };
  }
}

// Usage - many redundant parameters
const processor = new OrderProcessor(customer, shippingRules, taxRates);
const result = processor.processOrder(order, customer, shippingRules, taxRates);

// After - Methods get what they need from instance state
class OrderProcessor {
  constructor(customer, shippingRules, taxRates) {
    this._customer = customer;
    this._shippingRules = shippingRules;
    this._taxRates = taxRates;
  }
  
  // Methods get customer and rules from instance state
  calculateShipping(order) {
    const baseRate = this._shippingRules.getBaseRate(this._customer.tier);
    const distance = this._calculateDistance(this._customer.address, order.destination);
    const weight = order.items.reduce((sum, item) => sum + item.weight, 0);
    
    let cost = baseRate + (distance * 0.01) + (weight * 0.05);
    
    if (this._customer.isPremium) {
      cost *= 0.9; // 10% discount
    }
    
    return Math.max(cost, 5.00);
  }
  
  calculateTax(order) {
    const rate = this._taxRates.getRate(this._customer.address.state);
    const taxableAmount = order.items
      .filter(item => item.isTaxable)
      .reduce((sum, item) => sum + item.price * item.quantity, 0);
    
    let tax = taxableAmount * rate;
    
    if (this._customer.isExempt) {
      tax = 0;
    }
    
    return tax;
  }
  
  calculateDiscount(order) {
    let discount = 0;
    
    // Volume discount
    if (order.total > 100) {
      discount += order.total * 0.05;
    }
    
    // Loyalty discount
    if (this._customer.loyaltyPoints > 1000) {
      discount += order.total * 0.1;
    }
    
    // First-time customer
    if (this._customer.isFirstTime) {
      discount += 10;
    }
    
    return Math.min(discount, order.total * 0.5); // Max 50% discount
  }
  
  processOrder(order) {
    const shipping = this.calculateShipping(order);
    const tax = this.calculateTax(order);
    const discount = this.calculateDiscount(order);
    
    const total = order.subtotal + shipping + tax - discount;
    
    return {
      order,
      shipping,
      tax,
      discount,
      total
    };
  }
  
  _calculateDistance(from, to) {
    // Simplified distance calculation
    return Math.sqrt(
      Math.pow(from.lat - to.lat, 2) + Math.pow(from.lng - to.lng, 2)
    ) * 111; // Convert to km
  }
}

// Usage - cleaner method calls
const processor = new OrderProcessor(customer, shippingRules, taxRates);
const result = processor.processOrder(order); // Much cleaner!
```

### Global State Example
```javascript
// Before - Passing current user everywhere
class DocumentService {
  createDocument(title, content, currentUser) {
    this._validatePermissions(currentUser, 'create');
    
    const document = {
      id: generateId(),
      title,
      content,
      author: currentUser.id,
      createdAt: new Date(),
      permissions: this._getDefaultPermissions(currentUser)
    };
    
    this._auditLog('document_created', currentUser, { documentId: document.id });
    return this._saveDocument(document);
  }
  
  updateDocument(documentId, updates, currentUser) {
    const document = this._getDocument(documentId);
    this._validatePermissions(currentUser, 'edit', document);
    
    const updatedDocument = {
      ...document,
      ...updates,
      modifiedBy: currentUser.id,
      modifiedAt: new Date()
    };
    
    this._auditLog('document_updated', currentUser, { documentId });
    return this._saveDocument(updatedDocument);
  }
  
  deleteDocument(documentId, currentUser) {
    const document = this._getDocument(documentId);
    this._validatePermissions(currentUser, 'delete', document);
    
    this._auditLog('document_deleted', currentUser, { documentId });
    return this._removeDocument(documentId);
  }
  
  shareDocument(documentId, userId, permissions, currentUser) {
    const document = this._getDocument(documentId);
    this._validatePermissions(currentUser, 'share', document);
    
    const shareRecord = {
      documentId,
      userId,
      permissions,
      sharedBy: currentUser.id,
      sharedAt: new Date()
    };
    
    this._auditLog('document_shared', currentUser, { documentId, sharedWith: userId });
    return this._saveShare(shareRecord);
  }
  
  _validatePermissions(user, action, document = null) {
    // Permission validation logic
  }
  
  _getDefaultPermissions(user) {
    // Get default permissions based on user role
  }
  
  _auditLog(action, user, metadata) {
    // Log user actions
  }
}

// After - Get current user from context
class DocumentService {
  constructor(userContext) {
    this._userContext = userContext;
  }
  
  getCurrentUser() {
    return this._userContext.getCurrentUser();
  }
  
  createDocument(title, content) {
    const currentUser = this.getCurrentUser();
    this._validatePermissions('create');
    
    const document = {
      id: generateId(),
      title,
      content,
      author: currentUser.id,
      createdAt: new Date(),
      permissions: this._getDefaultPermissions()
    };
    
    this._auditLog('document_created', { documentId: document.id });
    return this._saveDocument(document);
  }
  
  updateDocument(documentId, updates) {
    const document = this._getDocument(documentId);
    const currentUser = this.getCurrentUser();
    this._validatePermissions('edit', document);
    
    const updatedDocument = {
      ...document,
      ...updates,
      modifiedBy: currentUser.id,
      modifiedAt: new Date()
    };
    
    this._auditLog('document_updated', { documentId });
    return this._saveDocument(updatedDocument);
  }
  
  deleteDocument(documentId) {
    const document = this._getDocument(documentId);
    this._validatePermissions('delete', document);
    
    this._auditLog('document_deleted', { documentId });
    return this._removeDocument(documentId);
  }
  
  shareDocument(documentId, userId, permissions) {
    const document = this._getDocument(documentId);
    const currentUser = this.getCurrentUser();
    this._validatePermissions('share', document);
    
    const shareRecord = {
      documentId,
      userId,
      permissions,
      sharedBy: currentUser.id,
      sharedAt: new Date()
    };
    
    this._auditLog('document_shared', { documentId, sharedWith: userId });
    return this._saveShare(shareRecord);
  }
  
  _validatePermissions(action, document = null) {
    const currentUser = this.getCurrentUser();
    // Permission validation logic using currentUser
  }
  
  _getDefaultPermissions() {
    const currentUser = this.getCurrentUser();
    // Get default permissions based on user role
  }
  
  _auditLog(action, metadata) {
    const currentUser = this.getCurrentUser();
    // Log user actions
  }
}

// Usage - no need to pass current user
const documentService = new DocumentService(userContext);
const document = documentService.createDocument('My Document', 'Content here');
documentService.shareDocument(document.id, 'user123', ['read', 'comment']);
```

### Computed Parameter Example
```javascript
// Before - Callers compute parameters that method could derive
class ReportGenerator {
  generateSalesReport(startDate, endDate, dateRange, totalDays) {
    console.log(`Generating report for ${dateRange} (${totalDays} days)`);
    
    const salesData = this._getSalesData(startDate, endDate);
    const dailyAverage = salesData.total / totalDays;
    
    return {
      period: dateRange,
      totalDays,
      totalSales: salesData.total,
      dailyAverage,
      breakdown: salesData.breakdown
    };
  }
  
  generateInventoryReport(categoryId, categoryName, productCount) {
    console.log(`Generating inventory report for ${categoryName} (${productCount} products)`);
    
    const inventoryData = this._getInventoryData(categoryId);
    const averageStock = inventoryData.totalStock / productCount;
    
    return {
      category: categoryName,
      productCount,
      totalStock: inventoryData.totalStock,
      averageStock,
      lowStockItems: inventoryData.lowStock
    };
  }
}

// Usage - callers must compute redundant parameters
const generator = new ReportGenerator();

const startDate = new Date('2023-01-01');
const endDate = new Date('2023-01-31');
const dateRange = `${startDate.toISOString().slice(0, 10)} to ${endDate.toISOString().slice(0, 10)}`;
const totalDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));

const salesReport = generator.generateSalesReport(startDate, endDate, dateRange, totalDays);

const categoryId = 'electronics';
const category = getCategoryById(categoryId);
const categoryName = category.name;
const productCount = category.products.length;

const inventoryReport = generator.generateInventoryReport(categoryId, categoryName, productCount);

// After - Methods compute derived values themselves
class ReportGenerator {
  constructor(categoryService) {
    this._categoryService = categoryService;
  }
  
  generateSalesReport(startDate, endDate) {
    const dateRange = this._formatDateRange(startDate, endDate);
    const totalDays = this._calculateDaysBetween(startDate, endDate);
    
    console.log(`Generating report for ${dateRange} (${totalDays} days)`);
    
    const salesData = this._getSalesData(startDate, endDate);
    const dailyAverage = salesData.total / totalDays;
    
    return {
      period: dateRange,
      totalDays,
      totalSales: salesData.total,
      dailyAverage,
      breakdown: salesData.breakdown
    };
  }
  
  generateInventoryReport(categoryId) {
    const category = this._categoryService.getById(categoryId);
    const categoryName = category.name;
    const productCount = category.products.length;
    
    console.log(`Generating inventory report for ${categoryName} (${productCount} products)`);
    
    const inventoryData = this._getInventoryData(categoryId);
    const averageStock = inventoryData.totalStock / productCount;
    
    return {
      category: categoryName,
      productCount,
      totalStock: inventoryData.totalStock,
      averageStock,
      lowStockItems: inventoryData.lowStock
    };
  }
  
  _formatDateRange(startDate, endDate) {
    return `${startDate.toISOString().slice(0, 10)} to ${endDate.toISOString().slice(0, 10)}`;
  }
  
  _calculateDaysBetween(startDate, endDate) {
    return Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
  }
}

// Usage - much simpler
const generator = new ReportGenerator(categoryService);

const salesReport = generator.generateSalesReport(
  new Date('2023-01-01'),
  new Date('2023-01-31')
);

const inventoryReport = generator.generateInventoryReport('electronics');
```

## Mechanics

1. **Identify derivable parameters**
   - Look for parameters that can be computed from other available data
   - Find parameters that are instance fields or accessible through fields
   - Check for parameters that are derived from other parameters

2. **Ensure the method can access the data**
   - Verify the method can reach the data source
   - Add fields or method parameters if necessary
   - Consider dependency injection for external data sources

3. **Remove the parameter**
   - Delete the parameter from the method signature
   - Update the method body to get the value instead
   - Add helper methods if the computation is complex

4. **Update all callers**
   - Remove the parameter from all method calls
   - Delete any code that was computing the parameter value
   - Test that all callers work correctly

5. **Consider performance**
   - If the computation is expensive, consider caching
   - Evaluate whether the parameter removal impacts performance
   - Profile if performance is critical

6. **Test thoroughly**
   - Verify the method produces the same results
   - Test all code paths and edge cases
   - Ensure no regressions in functionality

## When to Use

- **Redundant parameters**: Parameter can be derived from available data
- **Long parameter lists**: Too many parameters make methods hard to use
- **Coupling issues**: Callers shouldn't need to know how to compute parameters
- **Duplication**: Same parameter computation repeated in multiple places
- **Instance data**: Parameter is always the same as an instance field
- **Global context**: Parameter is available through global state or context

## When NOT to Use

- **External data**: Method can't easily access the required data
- **Performance critical**: Computing the value is expensive
- **Flexibility needed**: Different callers need to pass different values
- **Pure functions**: Method should remain pure and stateless
- **Testing**: Parameter makes the method easier to test

## Trade-offs

### Benefits
- **Simpler interface**: Fewer parameters to pass
- **Less coupling**: Callers don't need to compute parameter values
- **Reduced duplication**: Parameter computation happens in one place
- **Self-contained**: Method takes care of its own data needs
- **Easier to call**: Less chance of passing wrong values

### Drawbacks
- **Hidden dependencies**: Method's data requirements are less visible
- **Reduced flexibility**: All callers get the same computed value
- **Performance impact**: May compute values more often than needed
- **Testing difficulty**: Harder to test with different parameter values
- **Coupling to state**: Method becomes dependent on instance or global state

## Alternative Approaches

### Default Parameters
```javascript
// Provide default parameter that computes the value
function processOrder(order, customer = getCurrentUser()) {
  // Use customer parameter or computed default
}
```

### Method Overloading Pattern
```javascript
// Provide both versions of the method
class Calculator {
  // Version that takes all parameters
  calculate(value, rate, period) {
    return value * Math.pow(1 + rate, period);
  }
  
  // Convenience version that uses defaults
  calculateWithDefaults(value) {
    return this.calculate(value, this.getDefaultRate(), this.getDefaultPeriod());
  }
}
```

### Builder Pattern
```javascript
// Use builder for complex parameter setup
class ReportBuilder {
  constructor() {
    this._startDate = null;
    this._endDate = null;
  }
  
  setDateRange(start, end) {
    this._startDate = start;
    this._endDate = end;
    return this;
  }
  
  build() {
    const dateRange = this._formatDateRange();
    const totalDays = this._calculateDays();
    return new Report(this._startDate, this._endDate, dateRange, totalDays);
  }
}
```

## Related Refactorings

- [Add Parameter](change-function-declaration.md) - The inverse operation
- [Introduce Parameter Object](introduce-parameter-object.md) - Group remaining parameters
- [Extract Variable](extract-variable.md) - Extract parameter computation
- [Move Method](move-method.md) - Move method closer to data source
- [Preserve Whole Object](preserve-whole-object.md) - Pass object instead of derived values