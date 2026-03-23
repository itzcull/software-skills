---
title: "Move Field"
description: "Move a field from one class to another when it's used more by another class"
category: "Moving Features"
tags: ["move", "field", "organization", "cohesion", "coupling", "data"]
related: ["move-function", "extract-class", "inline-class"]
---

# Move Field

Move a field from one class to another when it's used more by another class than the class it's currently in.

## Motivation

As systems evolve, data and behavior that initially made sense in one class may become more closely related to another class. Signs that a field should move:

- The field is used more by methods in another class
- The field logically belongs with other data in another class
- Moving the field would reduce coupling between classes
- The field represents a concept that fits better elsewhere

Moving fields helps maintain proper encapsulation and keeps related data together.

## Example

### Basic Example
```javascript
// Before - Discount rate in Customer but used by Plan
class Customer {
  constructor(name, discountRate) {
    this._name = name;
    this._discountRate = discountRate;
    this._plan = new Plan();
  }
  
  get name() { return this._name; }
  get discountRate() { return this._discountRate; }
  get plan() { return this._plan; }
  
  applyDiscount(amount) {
    return amount * (1 - this._discountRate);
  }
}

class Plan {
  constructor() {
    this._name = 'Basic';
    this._monthlyFee = 20;
  }
  
  get name() { return this._name; }
  get monthlyFee() { return this._monthlyFee; }
}

// Usage shows discount is really plan-related
const customer = new Customer('Alice', 0.1);
const discountedFee = customer.applyDiscount(customer.plan.monthlyFee);

// After - Discount rate moved to Plan
class Customer {
  constructor(name, plan) {
    this._name = name;
    this._plan = plan;
  }
  
  get name() { return this._name; }
  get plan() { return this._plan; }
  get discountRate() { return this._plan.discountRate; }
  
  applyDiscount(amount) {
    return amount * (1 - this.discountRate);
  }
}

class Plan {
  constructor(name, monthlyFee, discountRate) {
    this._name = name;
    this._monthlyFee = monthlyFee;
    this._discountRate = discountRate;
  }
  
  get name() { return this._name; }
  get monthlyFee() { return this._monthlyFee; }
  get discountRate() { return this._discountRate; }
  
  get discountedMonthlyFee() {
    return this._monthlyFee * (1 - this._discountRate);
  }
}

// Usage is cleaner
const plan = new Plan('Basic', 20, 0.1);
const customer = new Customer('Alice', plan);
const discountedFee = plan.discountedMonthlyFee;
```

### Complex Example - Moving Related Fields Together
```javascript
// Before - Address fields in Order but logically belong together
class Order {
  constructor(customer, items) {
    this._customer = customer;
    this._items = items;
    this._shippingStreet = '';
    this._shippingCity = '';
    this._shippingState = '';
    this._shippingZip = '';
    this._shippingCountry = 'US';
  }
  
  setShippingAddress(street, city, state, zip, country) {
    this._shippingStreet = street;
    this._shippingCity = city;
    this._shippingState = state;
    this._shippingZip = zip;
    this._shippingCountry = country;
  }
  
  get shippingCost() {
    // Complex calculation using address fields
    if (this._shippingCountry !== 'US') {
      return 25;
    }
    
    if (['AK', 'HI'].includes(this._shippingState)) {
      return 15;
    }
    
    return 10;
  }
  
  get formattedShippingAddress() {
    return `${this._shippingStreet}
${this._shippingCity}, ${this._shippingState} ${this._shippingZip}
${this._shippingCountry}`;
  }
  
  validateShippingAddress() {
    if (!this._shippingStreet || !this._shippingCity || 
        !this._shippingState || !this._shippingZip) {
      throw new Error('Incomplete shipping address');
    }
  }
}

// After - Address fields moved to Address class
class Order {
  constructor(customer, items) {
    this._customer = customer;
    this._items = items;
    this._shippingAddress = null;
  }
  
  setShippingAddress(address) {
    this._shippingAddress = address;
  }
  
  get shippingAddress() { return this._shippingAddress; }
  
  get shippingCost() {
    if (!this._shippingAddress) {
      throw new Error('No shipping address set');
    }
    
    return this._shippingAddress.calculateShippingCost();
  }
  
  get formattedShippingAddress() {
    return this._shippingAddress ? this._shippingAddress.format() : 'No address';
  }
  
  validateShippingAddress() {
    if (!this._shippingAddress) {
      throw new Error('No shipping address set');
    }
    this._shippingAddress.validate();
  }
}

class Address {
  constructor(street, city, state, zip, country = 'US') {
    this._street = street;
    this._city = city;
    this._state = state;
    this._zip = zip;
    this._country = country;
  }
  
  calculateShippingCost() {
    if (this._country !== 'US') {
      return 25;
    }
    
    if (['AK', 'HI'].includes(this._state)) {
      return 15;
    }
    
    return 10;
  }
  
  format() {
    return `${this._street}
${this._city}, ${this._state} ${this._zip}
${this._country}`;
  }
  
  validate() {
    if (!this._street || !this._city || !this._state || !this._zip) {
      throw new Error('Incomplete address');
    }
    
    if (this._country === 'US' && !/^\d{5}(-\d{4})?$/.test(this._zip)) {
      throw new Error('Invalid US ZIP code');
    }
  }
}
```

### Moving Fields Between Inheritance Hierarchies
```javascript
// Before - Field in subclasses but could be in superclass
class Party {
  constructor(name) {
    this._name = name;
  }
  
  get name() { return this._name; }
}

class Person extends Party {
  constructor(name, id, email) {
    super(name);
    this._id = id;
    this._email = email;
    this._lastContacted = null;
  }
  
  get email() { return this._email; }
  get lastContacted() { return this._lastContacted; }
  
  recordContact(date) {
    this._lastContacted = date;
  }
}

class Organization extends Party {
  constructor(name, registrationNumber, email) {
    super(name);
    this._registrationNumber = registrationNumber;
    this._email = email;
    this._lastContacted = null;
  }
  
  get email() { return this._email; }
  get lastContacted() { return this._lastContacted; }
  
  recordContact(date) {
    this._lastContacted = date;
  }
}

// After - Common fields moved to superclass
class Party {
  constructor(name, email) {
    this._name = name;
    this._email = email;
    this._lastContacted = null;
  }
  
  get name() { return this._name; }
  get email() { return this._email; }
  get lastContacted() { return this._lastContacted; }
  
  recordContact(date) {
    this._lastContacted = date;
  }
}

class Person extends Party {
  constructor(name, id, email) {
    super(name, email);
    this._id = id;
  }
  
  get id() { return this._id; }
}

class Organization extends Party {
  constructor(name, registrationNumber, email) {
    super(name, email);
    this._registrationNumber = registrationNumber;
  }
  
  get registrationNumber() { return this._registrationNumber; }
}
```

## Mechanics

1. **Ensure the field is encapsulated**
   - If public, create getter/setter methods first
   - Update all direct field access to use accessors

2. **Create field and accessors in target class**
   - Add the field to the target class
   - Create appropriate getter/setter methods

3. **Redirect source class accessors**
   - Change the source class getter/setter to delegate to target
   - This maintains the existing interface temporarily

4. **Update references**
   - Find all uses of the source class accessors
   - Update to use the target class directly when appropriate

5. **Remove the field from source class**
   - Delete the field
   - Remove or simplify the redirecting accessors

6. **Test after each step**
   - Ensure behavior is preserved
   - Watch for any broken references

## Patterns for Moving Fields

### Moving to a New Class
```javascript
// When multiple fields should move together
class Employee {
  // Before
  constructor() {
    this._street = '';
    this._city = '';
    this._state = '';
    this._zip = '';
    // Other employee fields
  }
}

// After - Extract Address class and move fields
class Employee {
  constructor() {
    this._address = new Address();
    // Other employee fields
  }
  
  get address() { return this._address; }
}
```

### Moving Along Associations
```javascript
// Before - Field in wrong end of association
class Order {
  constructor(customer) {
    this._customer = customer;
    this._customerDiscount = 0.1; // Really about the customer
  }
}

// After - Field moved to associated class
class Order {
  constructor(customer) {
    this._customer = customer;
  }
  
  get customerDiscount() {
    return this._customer.discount;
  }
}

class Customer {
  constructor() {
    this._discount = 0.1;
  }
  
  get discount() { return this._discount; }
}
```

### Temporary Delegation Pattern
```javascript
// Step 1: Add delegation (keeps interface stable)
class Source {
  get field() { return this._target.field; }
  set field(value) { this._target.field = value; }
}

// Step 2: Update clients gradually
// Step 3: Remove delegation when all clients updated
```

## When to Use

- **Feature envy**: Field is used more by another class
- **Data clumps**: Field belongs with related fields in another class
- **Inappropriate intimacy**: Classes too tightly coupled through field access
- **Logical cohesion**: Field represents concept that belongs elsewhere
- **Inheritance issues**: Field should be in superclass or subclass

## Trade-offs

### Benefits
- **Better encapsulation**: Related data stays together
- **Reduced coupling**: Less cross-class field access
- **Clearer design**: Fields are where they logically belong
- **Easier maintenance**: Related changes happen in one place

### Drawbacks
- **Breaking changes**: May affect many client classes
- **Complex refactoring**: Can require many steps
- **Performance**: May add indirection
- **Temporary complexity**: Delegation phase can be confusing

## Common Scenarios

### Configuration Fields
```javascript
// Before - Configuration scattered
class Application {
  constructor() {
    this._dbHost = 'localhost';
    this._dbPort = 5432;
    this._apiKey = '';
    this._apiEndpoint = '';
  }
}

// After - Configuration grouped
class Application {
  constructor() {
    this._dbConfig = new DatabaseConfig();
    this._apiConfig = new APIConfig();
  }
}
```

### State Fields
```javascript
// Before - State fields in controller
class GameController {
  constructor() {
    this._score = 0;
    this._level = 1;
    this._lives = 3;
  }
}

// After - State fields in state object
class GameController {
  constructor() {
    this._gameState = new GameState();
  }
}

class GameState {
  constructor() {
    this._score = 0;
    this._level = 1;
    this._lives = 3;
  }
}
```

### Calculated Fields
```javascript
// Before - Calculated field stored separately
class Order {
  constructor() {
    this._items = [];
    this._total = 0; // Calculated from items
  }
  
  addItem(item) {
    this._items.push(item);
    this._total += item.price; // Maintain total
  }
}

// After - Calculation moved to source of truth
class Order {
  constructor() {
    this._items = [];
  }
  
  get total() {
    return this._items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

## Related Refactorings

- [Move Function](move-function.md) - Often done together with Move Field
- [Extract Class](extract-class.md) - Create target class for the field
- [Inline Class](inline-class.md) - Opposite direction, absorbing fields
- [Encapsulate Field](encapsulate-variable.md) - Preparation step
- [Pull Up Field](pull-up-field.md) - Specific case moving to superclass
- [Push Down Field](push-down-field.md) - Specific case moving to subclass