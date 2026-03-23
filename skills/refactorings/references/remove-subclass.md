---
title: "Remove Subclass"
description: "Eliminate a subclass that no longer provides enough value to justify its existence"
category: "Dealing with Inheritance"
tags: ["remove", "subclass", "simplification", "hierarchy"]
related: ["collapse-hierarchy", "inline-class", "push-down-method"]
---

# Remove Subclass

Eliminate a subclass that no longer provides enough value to justify its existence. Move any useful functionality to the superclass or other appropriate classes.

## Motivation

Subclasses can become unnecessary over time due to:

- **Minimal functionality**: Subclass adds little or no unique behavior
- **Complexity without benefit**: Extra inheritance layer that doesn't justify its existence
- **Code evolution**: Changes that make the subclass distinction unnecessary
- **Over-engineering**: Premature abstraction that wasn't needed
- **Maintenance burden**: More classes to maintain without proportional value

## Example

### Basic Example
```javascript
// Before - Subclass with minimal differentiation
class Employee {
  constructor(name, id, salary) {
    this._name = name;
    this._id = id;
    this._salary = salary;
  }
  
  get name() { return this._name; }
  get id() { return this._id; }
  get salary() { return this._salary; }
  
  getAnnualSalary() {
    return this._salary * 12;
  }
  
  getPayrollInfo() {
    return {
      id: this._id,
      name: this._name,
      monthlySalary: this._salary,
      annualSalary: this.getAnnualSalary()
    };
  }
}

class Manager extends Employee {
  constructor(name, id, salary) {
    super(name, id, salary);
  }
  
  // Only difference is a slightly higher salary calculation
  getAnnualSalary() {
    return this._salary * 12 * 1.1; // 10% bonus
  }
}

class Developer extends Employee {
  constructor(name, id, salary) {
    super(name, id, salary);
  }
  
  // No additional functionality - just a type distinction
}

// Usage
const dev = new Developer('Alice', 1, 5000);
const mgr = new Manager('Bob', 2, 7000);

// After - Remove unnecessary subclasses, use composition or flags
class Employee {
  constructor(name, id, salary, type = 'employee', bonusMultiplier = 1.0) {
    this._name = name;
    this._id = id;
    this._salary = salary;
    this._type = type;
    this._bonusMultiplier = bonusMultiplier;
  }
  
  get name() { return this._name; }
  get id() { return this._id; }
  get salary() { return this._salary; }
  get type() { return this._type; }
  
  getAnnualSalary() {
    return this._salary * 12 * this._bonusMultiplier;
  }
  
  getPayrollInfo() {
    return {
      id: this._id,
      name: this._name,
      type: this._type,
      monthlySalary: this._salary,
      annualSalary: this.getAnnualSalary()
    };
  }
  
  // Factory methods for common types
  static createDeveloper(name, id, salary) {
    return new Employee(name, id, salary, 'developer');
  }
  
  static createManager(name, id, salary) {
    return new Employee(name, id, salary, 'manager', 1.1);
  }
}

// Usage
const dev = Employee.createDeveloper('Alice', 1, 5000);
const mgr = Employee.createManager('Bob', 2, 7000);
```

### Complex Example - Shape Hierarchy
```javascript
// Before - Over-engineered shape hierarchy
class Shape {
  constructor(x, y) {
    this._x = x;
    this._y = y;
  }
  
  get x() { return this._x; }
  get y() { return this._y; }
  
  move(dx, dy) {
    this._x += dx;
    this._y += dy;
  }
  
  getArea() {
    throw new Error('Subclasses must implement getArea');
  }
  
  draw(context) {
    throw new Error('Subclasses must implement draw');
  }
}

class Rectangle extends Shape {
  constructor(x, y, width, height) {
    super(x, y);
    this._width = width;
    this._height = height;
  }
  
  get width() { return this._width; }
  get height() { return this._height; }
  
  getArea() {
    return this._width * this._height;
  }
  
  draw(context) {
    context.fillRect(this._x, this._y, this._width, this._height);
  }
}

class Square extends Rectangle {
  constructor(x, y, size) {
    super(x, y, size, size);
  }
  
  get size() { return this._width; }
  
  // Square doesn't add any unique behavior
  // It's just a rectangle with equal width and height
}

class Circle extends Shape {
  constructor(x, y, radius) {
    super(x, y);
    this._radius = radius;
  }
  
  get radius() { return this._radius; }
  
  getArea() {
    return Math.PI * this._radius * this._radius;
  }
  
  draw(context) {
    context.beginPath();
    context.arc(this._x, this._y, this._radius, 0, 2 * Math.PI);
    context.fill();
  }
}

// Triangle was added but barely used
class Triangle extends Shape {
  constructor(x, y, base, height) {
    super(x, y);
    this._base = base;
    this._height = height;
  }
  
  get base() { return this._base; }
  get height() { return this._height; }
  
  getArea() {
    return 0.5 * this._base * this._height;
  }
  
  draw(context) {
    // Complex triangle drawing logic that's rarely used
    context.beginPath();
    context.moveTo(this._x, this._y);
    context.lineTo(this._x + this._base, this._y);
    context.lineTo(this._x + this._base / 2, this._y - this._height);
    context.closePath();
    context.fill();
  }
}

// After - Simplified structure with removed Triangle and Square
class Shape {
  constructor(type, x, y, properties) {
    this._type = type;
    this._x = x;
    this._y = y;
    this._properties = properties;
  }
  
  get type() { return this._type; }
  get x() { return this._x; }
  get y() { return this._y; }
  get properties() { return this._properties; }
  
  move(dx, dy) {
    this._x += dx;
    this._y += dy;
  }
  
  getArea() {
    switch (this._type) {
      case 'rectangle':
        return this._properties.width * this._properties.height;
      case 'circle':
        return Math.PI * this._properties.radius * this._properties.radius;
      default:
        throw new Error(`Unknown shape type: ${this._type}`);
    }
  }
  
  draw(context) {
    switch (this._type) {
      case 'rectangle':
        context.fillRect(this._x, this._y, this._properties.width, this._properties.height);
        break;
      case 'circle':
        context.beginPath();
        context.arc(this._x, this._y, this._properties.radius, 0, 2 * Math.PI);
        context.fill();
        break;
      default:
        throw new Error(`Cannot draw shape type: ${this._type}`);
    }
  }
  
  // Factory methods for common shapes
  static createRectangle(x, y, width, height) {
    return new Shape('rectangle', x, y, { width, height });
  }
  
  static createSquare(x, y, size) {
    return new Shape('rectangle', x, y, { width: size, height: size });
  }
  
  static createCircle(x, y, radius) {
    return new Shape('circle', x, y, { radius });
  }
  
  // Helper methods
  isSquare() {
    return this._type === 'rectangle' && 
           this._properties.width === this._properties.height;
  }
}

// Usage
const rect = Shape.createRectangle(10, 20, 100, 50);
const square = Shape.createSquare(0, 0, 30);
const circle = Shape.createCircle(50, 50, 25);

console.log(square.isSquare()); // true
console.log(rect.isSquare());   // false
```

### Service Layer Example
```javascript
// Before - Unnecessary service subclasses
class BaseService {
  constructor(repository, logger) {
    this._repository = repository;
    this._logger = logger;
  }
  
  async findById(id) {
    this._logger.info(`Finding entity by id: ${id}`);
    return this._repository.findById(id);
  }
  
  async create(data) {
    this._logger.info('Creating new entity');
    return this._repository.create(data);
  }
  
  async update(id, data) {
    this._logger.info(`Updating entity: ${id}`);
    return this._repository.update(id, data);
  }
  
  async delete(id) {
    this._logger.info(`Deleting entity: ${id}`);
    return this._repository.delete(id);
  }
}

// These subclasses add no value
class UserService extends BaseService {
  constructor(userRepository, logger) {
    super(userRepository, logger);
  }
  
  // Just inherits everything from BaseService
}

class ProductService extends BaseService {
  constructor(productRepository, logger) {
    super(productRepository, logger);
  }
  
  // Also just inherits everything
}

class OrderService extends BaseService {
  constructor(orderRepository, logger) {
    super(orderRepository, logger);
  }
  
  // Same here - no additional functionality
}

// After - Remove unnecessary subclasses, use generic service
class GenericService {
  constructor(repository, logger, entityType) {
    this._repository = repository;
    this._logger = logger;
    this._entityType = entityType;
  }
  
  async findById(id) {
    this._logger.info(`Finding ${this._entityType} by id: ${id}`);
    return this._repository.findById(id);
  }
  
  async create(data) {
    this._logger.info(`Creating new ${this._entityType}`);
    return this._repository.create(data);
  }
  
  async update(id, data) {
    this._logger.info(`Updating ${this._entityType}: ${id}`);
    return this._repository.update(id, data);
  }
  
  async delete(id) {
    this._logger.info(`Deleting ${this._entityType}: ${id}`);
    return this._repository.delete(id);
  }
  
  // Factory methods for specific entity types
  static createUserService(userRepository, logger) {
    return new GenericService(userRepository, logger, 'user');
  }
  
  static createProductService(productRepository, logger) {
    return new GenericService(productRepository, logger, 'product');
  }
  
  static createOrderService(orderRepository, logger) {
    return new GenericService(orderRepository, logger, 'order');
  }
}

// Usage
const userService = GenericService.createUserService(userRepo, logger);
const productService = GenericService.createProductService(productRepo, logger);
const orderService = GenericService.createOrderService(orderRepo, logger);
```

### Error Hierarchy Example
```javascript
// Before - Over-specific error hierarchy
class ApplicationError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'ApplicationError';
    this.code = code;
  }
}

class ValidationError extends ApplicationError {
  constructor(message, field) {
    super(message, 'VALIDATION_ERROR');
    this.name = 'ValidationError';
    this.field = field;
  }
}

class EmailValidationError extends ValidationError {
  constructor(email) {
    super(`Invalid email: ${email}`, 'email');
    this.name = 'EmailValidationError';
  }
}

class PasswordValidationError extends ValidationError {
  constructor(reason) {
    super(`Password validation failed: ${reason}`, 'password');
    this.name = 'PasswordValidationError';
  }
}

class DatabaseError extends ApplicationError {
  constructor(message, operation) {
    super(message, 'DATABASE_ERROR');
    this.name = 'DatabaseError';
    this.operation = operation;
  }
}

class ConnectionError extends DatabaseError {
  constructor() {
    super('Database connection failed', 'connect');
    this.name = 'ConnectionError';
  }
}

class QueryError extends DatabaseError {
  constructor(query) {
    super(`Query failed: ${query}`, 'query');
    this.name = 'QueryError';
    this.query = query;
  }
}

// After - Simplified error handling with metadata
class ApplicationError extends Error {
  constructor(message, type, metadata = {}) {
    super(message);
    this.name = 'ApplicationError';
    this.type = type;
    this.metadata = metadata;
    this.timestamp = new Date();
  }
  
  // Factory methods for common error types
  static validation(message, field, value) {
    return new ApplicationError(message, 'VALIDATION_ERROR', { field, value });
  }
  
  static database(message, operation, query = null) {
    return new ApplicationError(message, 'DATABASE_ERROR', { operation, query });
  }
  
  static authentication(message) {
    return new ApplicationError(message, 'AUTH_ERROR');
  }
  
  static notFound(resource, id) {
    return new ApplicationError(`${resource} not found`, 'NOT_FOUND', { resource, id });
  }
  
  // Helper methods
  isValidationError() {
    return this.type === 'VALIDATION_ERROR';
  }
  
  isDatabaseError() {
    return this.type === 'DATABASE_ERROR';
  }
  
  getField() {
    return this.metadata.field;
  }
  
  getOperation() {
    return this.metadata.operation;
  }
}

// Usage
try {
  throw ApplicationError.validation('Invalid email format', 'email', 'bad-email');
} catch (error) {
  if (error.isValidationError()) {
    console.log(`Validation failed for field: ${error.getField()}`);
  }
}

try {
  throw ApplicationError.database('Connection timeout', 'connect');
} catch (error) {
  if (error.isDatabaseError()) {
    console.log(`Database operation failed: ${error.getOperation()}`);
  }
}
```

## Mechanics

1. **Identify candidates for removal**
   - Look for subclasses with minimal functionality
   - Find subclasses that are rarely used or extended
   - Check for subclasses that only differ in data, not behavior

2. **Analyze subclass functionality**
   - List all methods and properties unique to the subclass
   - Determine if unique functionality can be moved elsewhere
   - Check if the subclass is just a type marker

3. **Choose replacement strategy**
   - Use composition for complex behavior
   - Use parameters or flags for simple variations
   - Use factory methods for common configurations
   - Use strategy pattern for varying algorithms

4. **Move useful functionality**
   - Move unique methods to superclass with appropriate parameters
   - Extract useful logic to separate classes
   - Preserve important behavior through other mechanisms

5. **Update client code**
   - Replace subclass instantiation with superclass + configuration
   - Update type checks to use properties or methods
   - Modify polymorphic code to handle the new structure

6. **Remove the subclass**
   - Delete the subclass definition
   - Remove related imports and references
   - Clean up any subclass-specific tests

7. **Test thoroughly**
   - Ensure all functionality is preserved
   - Verify that client code works correctly
   - Check that polymorphism still works as expected

## When to Use

- **Minimal differentiation**: Subclass adds little unique value
- **Type-only inheritance**: Subclass is just a type marker
- **Rarely used**: Subclass has few instances or use cases
- **Maintenance burden**: Cost of maintaining subclass exceeds benefits
- **Over-engineering**: Inheritance was premature optimization
- **Simple variations**: Differences can be handled with parameters

## Trade-offs

### Benefits
- **Reduced complexity**: Fewer classes to understand and maintain
- **Simpler hierarchy**: Less inheritance depth
- **Easier testing**: Fewer classes to test
- **Better performance**: Less virtual method dispatch
- **Clearer design**: Focus on essential abstractions

### Drawbacks
- **Lost type safety**: Can't distinguish types at compile time
- **Larger classes**: Superclass may become more complex
- **Lost polymorphism**: May need conditional logic instead
- **Breaking changes**: Existing code may depend on subclass types

## Alternative Patterns

### Strategy Pattern
```javascript
// Instead of subclasses, use strategies
class PaymentProcessor {
  constructor(strategy) {
    this._strategy = strategy;
  }
  
  process(amount) {
    return this._strategy.process(amount);
  }
}

class CreditCardStrategy {
  process(amount) {
    // Credit card processing
  }
}

class PayPalStrategy {
  process(amount) {
    // PayPal processing
  }
}
```

### Factory Pattern
```javascript
// Use factory instead of inheritance
class ShapeFactory {
  static create(type, ...args) {
    switch (type) {
      case 'rectangle':
        return new Shape('rectangle', ...args);
      case 'circle':
        return new Shape('circle', ...args);
      default:
        throw new Error(`Unknown shape type: ${type}`);
    }
  }
}
```

### Composition
```javascript
// Use composition instead of inheritance
class Vehicle {
  constructor(engine, wheels, body) {
    this._engine = engine;
    this._wheels = wheels;
    this._body = body;
  }
  
  start() {
    return this._engine.start();
  }
  
  move() {
    return this._wheels.rotate();
  }
}
```

## Related Refactorings

- [Collapse Hierarchy](collapse-hierarchy.md) - Merge subclass into superclass
- [Replace Inheritance with Delegation](replace-superclass-with-delegate.md) - Use composition instead
- [Extract Class](extract-class.md) - Move functionality to separate class
- [Inline Class](inline-class.md) - Merge classes together
- [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md) - The inverse operation