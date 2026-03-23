---
title: "Replace Type Code with Subclasses"
description: "Replace a type code field with subclasses for better type safety and polymorphism"
category: "Dealing with Inheritance"
tags: ["type-code", "subclasses", "polymorphism", "type-safety"]
related: ["replace-conditional-with-polymorphism", "extract-superclass", "replace-primitive-with-object"]
---

# Replace Type Code with Subclasses

Replace a type code field with subclasses where each subclass represents a specific type. This provides better type safety, polymorphism, and eliminates conditional logic based on type codes.

## Motivation

Using type codes (enums, strings, or numbers) to differentiate behavior creates several problems:

- **Scattered conditionals**: Type-based logic spreads throughout the codebase
- **No type safety**: Easy to pass invalid type codes
- **Hard to extend**: Adding new types requires modifying existing code
- **Poor encapsulation**: Type-specific behavior isn't contained
- **Switch statement smell**: Repeated switch/if statements on type codes
- **Maintenance burden**: Changes to types affect multiple places

## Example

### Basic Example
```javascript
// Before - Type code with scattered conditionals
class Employee {
  static ENGINEER = 'engineer';
  static MANAGER = 'manager';
  static SALESPERSON = 'salesperson';
  
  constructor(name, type) {
    this._name = name;
    this._type = type;
  }
  
  get name() { return this._name; }
  get type() { return this._type; }
  
  getPayAmount() {
    switch (this._type) {
      case Employee.ENGINEER:
        return this._monthlySalary;
      case Employee.MANAGER:
        return this._monthlySalary + this._bonus;
      case Employee.SALESPERSON:
        return this._commission;
      default:
        throw new Error(`Unknown employee type: ${this._type}`);
    }
  }
  
  getWorkingHours() {
    switch (this._type) {
      case Employee.ENGINEER:
        return 40;
      case Employee.MANAGER:
        return 45;
      case Employee.SALESPERSON:
        return 35;
      default:
        throw new Error(`Unknown employee type: ${this._type}`);
    }
  }
  
  getVacationDays() {
    switch (this._type) {
      case Employee.ENGINEER:
        return 20;
      case Employee.MANAGER:
        return 25;
      case Employee.SALESPERSON:
        return 15;
      default:
        throw new Error(`Unknown employee type: ${this._type}`);
    }
  }
  
  set monthlySalary(value) { this._monthlySalary = value; }
  set bonus(value) { this._bonus = value; }
  set commission(value) { this._commission = value; }
}

// After - Subclasses with polymorphism
class Employee {
  constructor(name) {
    this._name = name;
  }
  
  get name() { return this._name; }
  
  // Abstract methods to be implemented by subclasses
  getPayAmount() {
    throw new Error('Subclass must implement getPayAmount');
  }
  
  getWorkingHours() {
    throw new Error('Subclass must implement getWorkingHours');
  }
  
  getVacationDays() {
    throw new Error('Subclass must implement getVacationDays');
  }
  
  // Factory method to create appropriate subclass
  static create(name, type, options = {}) {
    switch (type) {
      case 'engineer':
        return new Engineer(name, options.monthlySalary);
      case 'manager':
        return new Manager(name, options.monthlySalary, options.bonus);
      case 'salesperson':
        return new Salesperson(name, options.commission);
      default:
        throw new Error(`Unknown employee type: ${type}`);
    }
  }
}

class Engineer extends Employee {
  constructor(name, monthlySalary) {
    super(name);
    this._monthlySalary = monthlySalary;
  }
  
  getPayAmount() {
    return this._monthlySalary;
  }
  
  getWorkingHours() {
    return 40;
  }
  
  getVacationDays() {
    return 20;
  }
  
  set monthlySalary(value) { this._monthlySalary = value; }
}

class Manager extends Employee {
  constructor(name, monthlySalary, bonus = 0) {
    super(name);
    this._monthlySalary = monthlySalary;
    this._bonus = bonus;
  }
  
  getPayAmount() {
    return this._monthlySalary + this._bonus;
  }
  
  getWorkingHours() {
    return 45;
  }
  
  getVacationDays() {
    return 25;
  }
  
  set monthlySalary(value) { this._monthlySalary = value; }
  set bonus(value) { this._bonus = value; }
}

class Salesperson extends Employee {
  constructor(name, commission) {
    super(name);
    this._commission = commission;
  }
  
  getPayAmount() {
    return this._commission;
  }
  
  getWorkingHours() {
    return 35;
  }
  
  getVacationDays() {
    return 15;
  }
  
  set commission(value) { this._commission = value; }
}

// Usage - type safety and polymorphism
const engineer = Employee.create('John', 'engineer', { monthlySalary: 5000 });
const manager = Employee.create('Sarah', 'manager', { monthlySalary: 6000, bonus: 1000 });
const salesperson = Employee.create('Mike', 'salesperson', { commission: 3000 });

// Polymorphic behavior - no conditionals needed
console.log(engineer.getPayAmount()); // 5000
console.log(manager.getPayAmount());  // 7000
console.log(salesperson.getPayAmount()); // 3000
```

### Complex Example - Shape Hierarchy
```javascript
// Before - Shape with type code
class Shape {
  static CIRCLE = 'circle';
  static RECTANGLE = 'rectangle';
  static TRIANGLE = 'triangle';
  
  constructor(type, ...args) {
    this._type = type;
    
    switch (type) {
      case Shape.CIRCLE:
        this._radius = args[0];
        break;
      case Shape.RECTANGLE:
        this._width = args[0];
        this._height = args[1];
        break;
      case Shape.TRIANGLE:
        this._base = args[0];
        this._height = args[1];
        break;
      default:
        throw new Error(`Unknown shape type: ${type}`);
    }
  }
  
  get type() { return this._type; }
  
  getArea() {
    switch (this._type) {
      case Shape.CIRCLE:
        return Math.PI * this._radius * this._radius;
      case Shape.RECTANGLE:
        return this._width * this._height;
      case Shape.TRIANGLE:
        return 0.5 * this._base * this._height;
      default:
        throw new Error(`Unknown shape type: ${this._type}`);
    }
  }
  
  getPerimeter() {
    switch (this._type) {
      case Shape.CIRCLE:
        return 2 * Math.PI * this._radius;
      case Shape.RECTANGLE:
        return 2 * (this._width + this._height);
      case Shape.TRIANGLE:
        // Simplified: assuming equilateral triangle
        return 3 * this._base;
      default:
        throw new Error(`Unknown shape type: ${this._type}`);
    }
  }
  
  draw(context) {
    switch (this._type) {
      case Shape.CIRCLE:
        context.beginPath();
        context.arc(0, 0, this._radius, 0, 2 * Math.PI);
        context.stroke();
        break;
      case Shape.RECTANGLE:
        context.strokeRect(0, 0, this._width, this._height);
        break;
      case Shape.TRIANGLE:
        context.beginPath();
        context.moveTo(0, 0);
        context.lineTo(this._base, 0);
        context.lineTo(this._base / 2, this._height);
        context.closePath();
        context.stroke();
        break;
      default:
        throw new Error(`Unknown shape type: ${this._type}`);
    }
  }
  
  getBoundingBox() {
    switch (this._type) {
      case Shape.CIRCLE:
        return {
          x: -this._radius,
          y: -this._radius,
          width: 2 * this._radius,
          height: 2 * this._radius
        };
      case Shape.RECTANGLE:
        return {
          x: 0,
          y: 0,
          width: this._width,
          height: this._height
        };
      case Shape.TRIANGLE:
        return {
          x: 0,
          y: 0,
          width: this._base,
          height: this._height
        };
      default:
        throw new Error(`Unknown shape type: ${this._type}`);
    }
  }
}

// After - Shape hierarchy with subclasses
class Shape {
  getArea() {
    throw new Error('Subclass must implement getArea');
  }
  
  getPerimeter() {
    throw new Error('Subclass must implement getPerimeter');
  }
  
  draw(context) {
    throw new Error('Subclass must implement draw');
  }
  
  getBoundingBox() {
    throw new Error('Subclass must implement getBoundingBox');
  }
  
  // Template method for common operations
  describe() {
    return `${this.constructor.name}: Area=${this.getArea().toFixed(2)}, Perimeter=${this.getPerimeter().toFixed(2)}`;
  }
  
  // Factory method
  static create(type, ...args) {
    switch (type) {
      case 'circle':
        return new Circle(args[0]);
      case 'rectangle':
        return new Rectangle(args[0], args[1]);
      case 'triangle':
        return new Triangle(args[0], args[1]);
      default:
        throw new Error(`Unknown shape type: ${type}`);
    }
  }
}

class Circle extends Shape {
  constructor(radius) {
    super();
    this._radius = radius;
  }
  
  get radius() { return this._radius; }
  set radius(value) { this._radius = value; }
  
  getArea() {
    return Math.PI * this._radius * this._radius;
  }
  
  getPerimeter() {
    return 2 * Math.PI * this._radius;
  }
  
  draw(context) {
    context.beginPath();
    context.arc(0, 0, this._radius, 0, 2 * Math.PI);
    context.stroke();
  }
  
  getBoundingBox() {
    return {
      x: -this._radius,
      y: -this._radius,
      width: 2 * this._radius,
      height: 2 * this._radius
    };
  }
  
  // Circle-specific methods
  getDiameter() {
    return 2 * this._radius;
  }
  
  getCircumference() {
    return this.getPerimeter();
  }
}

class Rectangle extends Shape {
  constructor(width, height) {
    super();
    this._width = width;
    this._height = height;
  }
  
  get width() { return this._width; }
  get height() { return this._height; }
  set width(value) { this._width = value; }
  set height(value) { this._height = value; }
  
  getArea() {
    return this._width * this._height;
  }
  
  getPerimeter() {
    return 2 * (this._width + this._height);
  }
  
  draw(context) {
    context.strokeRect(0, 0, this._width, this._height);
  }
  
  getBoundingBox() {
    return {
      x: 0,
      y: 0,
      width: this._width,
      height: this._height
    };
  }
  
  // Rectangle-specific methods
  isSquare() {
    return this._width === this._height;
  }
  
  getAspectRatio() {
    return this._width / this._height;
  }
}

class Triangle extends Shape {
  constructor(base, height) {
    super();
    this._base = base;
    this._height = height;
  }
  
  get base() { return this._base; }
  get height() { return this._height; }
  set base(value) { this._base = value; }
  set height(value) { this._height = value; }
  
  getArea() {
    return 0.5 * this._base * this._height;
  }
  
  getPerimeter() {
    // Simplified: assuming equilateral triangle
    return 3 * this._base;
  }
  
  draw(context) {
    context.beginPath();
    context.moveTo(0, 0);
    context.lineTo(this._base, 0);
    context.lineTo(this._base / 2, this._height);
    context.closePath();
    context.stroke();
  }
  
  getBoundingBox() {
    return {
      x: 0,
      y: 0,
      width: this._base,
      height: this._height
    };
  }
  
  // Triangle-specific methods
  isRightTriangle() {
    // Simplified check for right triangle
    const hypotenuse = Math.sqrt(this._base * this._base + this._height * this._height);
    return Math.abs(this._base * this._base + this._height * this._height - hypotenuse * hypotenuse) < 0.001;
  }
}

// Usage - clean polymorphism
const shapes = [
  Shape.create('circle', 5),
  Shape.create('rectangle', 4, 6),
  Shape.create('triangle', 3, 4)
];

shapes.forEach(shape => {
  console.log(shape.describe());
  shape.draw(context); // Polymorphic drawing
});

// Type-specific operations without conditionals
const circle = new Circle(10);
console.log(circle.getDiameter()); // 20

const rectangle = new Rectangle(4, 4);
console.log(rectangle.isSquare()); // true
```

### State Machine Example
```javascript
// Before - State machine with type codes
class Order {
  static PENDING = 'pending';
  static CONFIRMED = 'confirmed';
  static SHIPPED = 'shipped';
  static DELIVERED = 'delivered';
  static CANCELLED = 'cancelled';
  
  constructor(id, items) {
    this._id = id;
    this._items = items;
    this._state = Order.PENDING;
    this._createdAt = new Date();
  }
  
  get state() { return this._state; }
  get id() { return this._id; }
  get items() { return this._items; }
  
  confirm() {
    switch (this._state) {
      case Order.PENDING:
        this._state = Order.CONFIRMED;
        this._confirmedAt = new Date();
        break;
      default:
        throw new Error(`Cannot confirm order in state: ${this._state}`);
    }
  }
  
  ship() {
    switch (this._state) {
      case Order.CONFIRMED:
        this._state = Order.SHIPPED;
        this._shippedAt = new Date();
        break;
      default:
        throw new Error(`Cannot ship order in state: ${this._state}`);
    }
  }
  
  deliver() {
    switch (this._state) {
      case Order.SHIPPED:
        this._state = Order.DELIVERED;
        this._deliveredAt = new Date();
        break;
      default:
        throw new Error(`Cannot deliver order in state: ${this._state}`);
    }
  }
  
  cancel() {
    switch (this._state) {
      case Order.PENDING:
      case Order.CONFIRMED:
        this._state = Order.CANCELLED;
        this._cancelledAt = new Date();
        break;
      default:
        throw new Error(`Cannot cancel order in state: ${this._state}`);
    }
  }
  
  canModifyItems() {
    switch (this._state) {
      case Order.PENDING:
        return true;
      case Order.CONFIRMED:
      case Order.SHIPPED:
      case Order.DELIVERED:
      case Order.CANCELLED:
        return false;
      default:
        throw new Error(`Unknown state: ${this._state}`);
    }
  }
  
  getEstimatedDelivery() {
    switch (this._state) {
      case Order.PENDING:
        return null;
      case Order.CONFIRMED:
        return new Date(Date.now() + 7 * 24 * 60 * 60 * 1000); // 7 days
      case Order.SHIPPED:
        return new Date(Date.now() + 3 * 24 * 60 * 60 * 1000); // 3 days
      case Order.DELIVERED:
        return this._deliveredAt;
      case Order.CANCELLED:
        return null;
      default:
        throw new Error(`Unknown state: ${this._state}`);
    }
  }
}

// After - State pattern with subclasses
class Order {
  constructor(id, items) {
    this._id = id;
    this._items = items;
    this._createdAt = new Date();
    this._state = new PendingState(this);
  }
  
  get state() { return this._state; }
  get id() { return this._id; }
  get items() { return this._items; }
  get createdAt() { return this._createdAt; }
  
  setState(state) {
    this._state = state;
  }
  
  // Delegate to current state
  confirm() { this._state.confirm(); }
  ship() { this._state.ship(); }
  deliver() { this._state.deliver(); }
  cancel() { this._state.cancel(); }
  canModifyItems() { return this._state.canModifyItems(); }
  getEstimatedDelivery() { return this._state.getEstimatedDelivery(); }
  
  getStateName() { return this._state.constructor.name.replace('State', '').toLowerCase(); }
  
  // State transition helpers
  setConfirmedAt(date) { this._confirmedAt = date; }
  setShippedAt(date) { this._shippedAt = date; }
  setDeliveredAt(date) { this._deliveredAt = date; }
  setCancelledAt(date) { this._cancelledAt = date; }
  
  get confirmedAt() { return this._confirmedAt; }
  get shippedAt() { return this._shippedAt; }
  get deliveredAt() { return this._deliveredAt; }
  get cancelledAt() { return this._cancelledAt; }
}

class OrderState {
  constructor(order) {
    this._order = order;
  }
  
  confirm() { throw new Error(`Cannot confirm order in ${this.constructor.name}`); }
  ship() { throw new Error(`Cannot ship order in ${this.constructor.name}`); }
  deliver() { throw new Error(`Cannot deliver order in ${this.constructor.name}`); }
  cancel() { throw new Error(`Cannot cancel order in ${this.constructor.name}`); }
  canModifyItems() { return false; }
  getEstimatedDelivery() { return null; }
}

class PendingState extends OrderState {
  confirm() {
    this._order.setConfirmedAt(new Date());
    this._order.setState(new ConfirmedState(this._order));
  }
  
  cancel() {
    this._order.setCancelledAt(new Date());
    this._order.setState(new CancelledState(this._order));
  }
  
  canModifyItems() {
    return true;
  }
  
  getEstimatedDelivery() {
    return null; // No estimate until confirmed
  }
}

class ConfirmedState extends OrderState {
  ship() {
    this._order.setShippedAt(new Date());
    this._order.setState(new ShippedState(this._order));
  }
  
  cancel() {
    this._order.setCancelledAt(new Date());
    this._order.setState(new CancelledState(this._order));
  }
  
  getEstimatedDelivery() {
    return new Date(Date.now() + 7 * 24 * 60 * 60 * 1000); // 7 days
  }
}

class ShippedState extends OrderState {
  deliver() {
    this._order.setDeliveredAt(new Date());
    this._order.setState(new DeliveredState(this._order));
  }
  
  getEstimatedDelivery() {
    return new Date(Date.now() + 3 * 24 * 60 * 60 * 1000); // 3 days
  }
}

class DeliveredState extends OrderState {
  getEstimatedDelivery() {
    return this._order.deliveredAt;
  }
}

class CancelledState extends OrderState {
  // All operations throw errors by default from base class
}

// Usage - clean state management
const order = new Order('ORD-001', ['item1', 'item2']);
console.log(order.getStateName()); // pending

order.confirm();
console.log(order.getStateName()); // confirmed
console.log(order.canModifyItems()); // false

order.ship();
console.log(order.getStateName()); // shipped

order.deliver();
console.log(order.getStateName()); // delivered
```

## Mechanics

1. **Identify type codes and conditionals**
   - Find fields that represent types (enums, constants, strings)
   - Locate switch statements or if-else chains based on type codes
   - Check for type-specific behavior scattered across methods

2. **Create the hierarchy**
   - Create a base class or interface
   - Create subclasses for each type code value
   - Move type-specific behavior to appropriate subclasses

3. **Replace conditionals with polymorphism**
   - Convert switch statements to polymorphic method calls
   - Move type-specific logic to subclass methods
   - Use template methods for common behavior

4. **Add factory methods**
   - Create factory methods to instantiate appropriate subclasses
   - Replace direct constructor calls with factory calls
   - Consider using abstract factory for complex hierarchies

5. **Remove type code field**
   - Delete the type code field from the base class
   - Remove type-related constants
   - Update any remaining code that checked the type

6. **Test thoroughly**
   - Verify all behavior is preserved
   - Test that new types can be added easily
   - Check that invalid operations are properly prevented

## When to Use

- **Scattered conditionals**: Many switch statements on the same type code
- **Type-specific behavior**: Different behavior for different types
- **Frequent type additions**: Need to add new types regularly
- **Complex type logic**: Type-specific behavior is substantial
- **Polymorphism opportunity**: Behavior varies by type in predictable ways
- **State machines**: Type code represents states with different behaviors

## Trade-offs

### Benefits
- **Eliminates conditionals**: No more switch statements on type codes
- **Better extensibility**: Easy to add new types without modifying existing code
- **Type safety**: Compiler can catch type-related errors
- **Encapsulation**: Type-specific behavior is contained in appropriate classes
- **Polymorphism**: Leverage object-oriented design principles
- **Open/Closed Principle**: Open for extension, closed for modification

### Drawbacks
- **More classes**: Increases the number of classes in the system
- **Indirection**: May be harder to follow code flow
- **Overkill for simple cases**: Too much for simple type codes with minimal behavior
- **Memory overhead**: Objects instead of simple values
- **Initial complexity**: Requires more upfront design

## Common Patterns

### Abstract Factory
```javascript
class ShapeFactory {
  static create(config) {
    switch (config.type) {
      case 'circle':
        return new Circle(config.radius);
      case 'rectangle':
        return new Rectangle(config.width, config.height);
      default:
        throw new Error(`Unknown shape type: ${config.type}`);
    }
  }
}
```

### Template Method
```javascript
class Animal {
  makeSound() {
    return this.getSound();
  }
  
  getSound() {
    throw new Error('Subclass must implement getSound');
  }
}

class Dog extends Animal {
  getSound() { return 'Woof!'; }
}
```

### Strategy Pattern
```javascript
class PaymentProcessor {
  constructor(strategy) {
    this._strategy = strategy;
  }
  
  process(amount) {
    return this._strategy.process(amount);
  }
}

class CreditCardStrategy {
  process(amount) { /* credit card logic */ }
}

class PayPalStrategy {
  process(amount) { /* PayPal logic */ }
}
```

## Related Refactorings

- [Replace Type Code with State/Strategy](replace-type-code-with-state-strategy.md) - Alternative approach using composition
- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Remove conditionals after creating hierarchy
- [Extract Subclass](extract-subclass.md) - Create subclasses for specialization
- [Pull Up Method](pull-up-method.md) - Move common behavior to base class
- [Push Down Method](push-down-method.md) - Move specific behavior to subclasses