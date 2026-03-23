---
title: "Change Value to Reference"
description: "Transform a value object into a reference object for managing a single shared instance"
category: "Organizing Data"
tags: ["value", "reference", "shared-state", "identity", "consistency"]
related: ["change-reference-to-value", "encapsulate-variable", "extract-class"]
---

# Change Value to Reference

Transform an object that is currently created as a value object into a reference object. This allows managing a single shared instance of an object across the system instead of creating multiple copies.

## Inverse

[Change Reference to Value](change-reference-to-value.md)

## Motivation

Sometimes we start with value objects but later discover we need:
- **Shared state**: When changes to an object should be visible everywhere
- **Identity**: When we need to track specific instances
- **Performance**: When creating many copies becomes expensive
- **Consistency**: When we need a single source of truth

For example, customer objects might start as value objects, but as the system grows, we need to ensure all references to a customer reflect the same data.

## Example

### Basic Example
```javascript
// Before - Value objects created each time
class Order {
  constructor(data) {
    this._customer = new Customer(data.customer);
  }
  
  get customer() {
    return this._customer;
  }
}

// Multiple orders create multiple customer instances
const order1 = new Order({customer: {id: 123, name: "Alice"}});
const order2 = new Order({customer: {id: 123, name: "Alice"}});
// order1.customer !== order2.customer (different instances)

// After - Reference objects from repository
class Order {
  constructor(data) {
    this._customer = customerRepository.get(data.customerId);
  }
  
  get customer() {
    return this._customer;
  }
}

// Repository ensures single instance per customer
const order1 = new Order({customerId: 123});
const order2 = new Order({customerId: 123});
// order1.customer === order2.customer (same instance)
```

### Repository Implementation
```javascript
class CustomerRepository {
  constructor() {
    this._customers = new Map();
  }
  
  get(id) {
    if (!this._customers.has(id)) {
      // Load from database or create new instance
      this._customers.set(id, this._loadCustomer(id));
    }
    return this._customers.get(id);
  }
  
  _loadCustomer(id) {
    // In real implementation, load from database
    const data = database.customers.find(id);
    return new Customer(data);
  }
  
  save(customer) {
    this._customers.set(customer.id, customer);
    // Also persist to database
    database.customers.update(customer.id, customer);
  }
}

const customerRepository = new CustomerRepository();
```

## Mechanics

1. **Create a repository for storing the instances of the reference object**
   - Use a Map, dictionary, or similar structure
   - Ensure the repository is accessible where needed

2. **Ensure the object has a unique identifier**
   - Add an ID field if it doesn't exist
   - This ID will be the key in the repository

3. **Modify the constructor to register instances with the repository**
   - Alternative: Use a factory method that manages registration

4. **Replace direct instantiation with repository lookups**
   - Find all places where the object is created
   - Replace with repository.get() calls

5. **Test**
   - Verify that identity is preserved
   - Ensure updates are reflected everywhere

## Extended Example: Factory Pattern

```javascript
// Using factory pattern for controlled instantiation
class Customer {
  constructor(id, name, data) {
    this.id = id;
    this.name = name;
    Object.assign(this, data);
  }
  
  // Private constructor simulation
  static _create(id, name, data) {
    return new Customer(id, name, data);
  }
}

class CustomerFactory {
  constructor() {
    this._instances = new Map();
  }
  
  createCustomer(id, name, data) {
    if (!this._instances.has(id)) {
      const customer = Customer._create(id, name, data);
      this._instances.set(id, customer);
    }
    return this._instances.get(id);
  }
  
  getCustomer(id) {
    if (!this._instances.has(id)) {
      throw new Error(`Customer ${id} not found`);
    }
    return this._instances.get(id);
  }
  
  registerCustomer(customer) {
    if (this._instances.has(customer.id)) {
      throw new Error(`Customer ${customer.id} already exists`);
    }
    this._instances.set(customer.id, customer);
  }
}
```

## When to Use

- **Shared mutable state**: When multiple parts of the system need to see the same changes
- **Identity matters**: When you need to distinguish between instances with the same data
- **Performance**: When creating many copies is expensive
- **Bidirectional relationships**: When objects need to reference each other
- **Event systems**: When objects need to notify observers of changes

## Trade-offs

### Benefits
- **Consistency**: Single source of truth for each entity
- **Memory efficiency**: Avoid duplicate instances
- **Shared updates**: Changes visible everywhere immediately
- **Identity preservation**: Can compare objects with ===

### Drawbacks
- **Complexity**: Need to manage repositories or factories
- **Coupling**: Shared state can create hidden dependencies
- **Thread safety**: Shared mutable state requires synchronization
- **Testing**: Harder to test with shared state
- **Memory leaks**: Need to manage object lifecycle

## Common Patterns

### Singleton Repository
```javascript
class CustomerRepository {
  static instance = new CustomerRepository();
  
  static getInstance() {
    return CustomerRepository.instance;
  }
  
  // ... repository implementation
}
```

### Dependency Injection
```javascript
class OrderService {
  constructor(customerRepository) {
    this._customerRepository = customerRepository;
  }
  
  createOrder(customerId, items) {
    const customer = this._customerRepository.get(customerId);
    return new Order(customer, items);
  }
}
```

## Related Refactorings

- [Change Reference to Value](change-reference-to-value.md) - The inverse operation
- [Replace Constructor with Factory Method](replace-constructor-with-factory-function.md) - Often used to control instantiation
- [Introduce Parameter Object](introduce-parameter-object.md) - May create objects needing reference semantics
- [Extract Class](extract-class.md) - May create new reference objects