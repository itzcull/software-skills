---
title: "Extract Class"
description: "Break down a class that has too many responsibilities by moving some fields and methods to a separate class"
category: "Organization"
tags: ["extract", "class", "organization", "single-responsibility", "cohesion", "refactoring"]
related: ["inline-class", "move-function", "move-field", "extract-superclass"]
---

# Extract Class

Break down a class that has too many responsibilities by moving some fields and methods to a separate class. This helps improve code organization and reduces the complexity of existing classes.

## Inverse

[Inline Class](inline-class.md)

## Motivation

Classes grow over time as features are added. Eventually, a class may become responsible for too many things, making it:
- Hard to understand
- Difficult to test
- Prone to bugs when changes are made
- Likely to change for multiple reasons

Extracting a class helps by:
- **Single Responsibility**: Each class has one clear purpose
- **Cohesion**: Related data and behavior stay together
- **Testability**: Smaller classes are easier to test
- **Reusability**: Extracted classes can be used elsewhere

## Example

### Basic Example
```javascript
// Before - Person class handling too many concerns
class Person {
  constructor(name, officeAreaCode, officeNumber) {
    this._name = name;
    this._officeAreaCode = officeAreaCode;
    this._officeNumber = officeNumber;
  }
  
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  
  get telephoneNumber() {
    return `(${this._officeAreaCode}) ${this._officeNumber}`;
  }
  
  get officeAreaCode() { return this._officeAreaCode; }
  set officeAreaCode(arg) { this._officeAreaCode = arg; }
  
  get officeNumber() { return this._officeNumber; }
  set officeNumber(arg) { this._officeNumber = arg; }
}

// After - Extracted TelephoneNumber class
class Person {
  constructor(name, areaCode, number) {
    this._name = name;
    this._telephoneNumber = new TelephoneNumber(areaCode, number);
  }
  
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  
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
```

### Complex Example - Order Management
```javascript
// Before - Order class doing too much
class Order {
  constructor(customer) {
    this._customer = customer;
    this._items = [];
    this._shippingAddress = '';
    this._shippingCity = '';
    this._shippingState = '';
    this._shippingZip = '';
    this._shippingCountry = '';
    this._expedited = false;
    this._trackingNumber = '';
  }
  
  addItem(product, quantity) {
    this._items.push({product, quantity});
  }
  
  get subtotal() {
    return this._items.reduce(
      (sum, item) => sum + item.product.price * item.quantity, 0
    );
  }
  
  get shippingCost() {
    const baseShipping = this._expedited ? 25 : 10;
    const weight = this._items.reduce(
      (sum, item) => sum + item.product.weight * item.quantity, 0
    );
    return baseShipping + weight * 0.5;
  }
  
  get total() {
    return this.subtotal + this.shippingCost;
  }
  
  get fullShippingAddress() {
    return `${this._shippingAddress}\n${this._shippingCity}, ${this._shippingState} ${this._shippingZip}\n${this._shippingCountry}`;
  }
  
  setShippingAddress(address, city, state, zip, country) {
    this._shippingAddress = address;
    this._shippingCity = city;
    this._shippingState = state;
    this._shippingZip = zip;
    this._shippingCountry = country;
  }
  
  ship() {
    this._trackingNumber = this.generateTrackingNumber();
    console.log(`Order shipped to: ${this.fullShippingAddress}`);
    console.log(`Tracking: ${this._trackingNumber}`);
  }
  
  generateTrackingNumber() {
    return Math.random().toString(36).substr(2, 9).toUpperCase();
  }
}

// After - Extracted Address and Shipping classes
class Order {
  constructor(customer) {
    this._customer = customer;
    this._items = [];
    this._shipping = new Shipping();
  }
  
  addItem(product, quantity) {
    this._items.push({product, quantity});
  }
  
  get subtotal() {
    return this._items.reduce(
      (sum, item) => sum + item.product.price * item.quantity, 0
    );
  }
  
  get shippingCost() {
    const weight = this._items.reduce(
      (sum, item) => sum + item.product.weight * item.quantity, 0
    );
    return this._shipping.calculateCost(weight);
  }
  
  get total() {
    return this.subtotal + this.shippingCost;
  }
  
  setShippingAddress(address, city, state, zip, country) {
    this._shipping.setAddress(new Address(address, city, state, zip, country));
  }
  
  ship() {
    this._shipping.ship();
  }
}

class Address {
  constructor(street, city, state, zip, country) {
    this._street = street;
    this._city = city;
    this._state = state;
    this._zip = zip;
    this._country = country;
  }
  
  get street() { return this._street; }
  get city() { return this._city; }
  get state() { return this._state; }
  get zip() { return this._zip; }
  get country() { return this._country; }
  
  toString() {
    return `${this._street}\n${this._city}, ${this._state} ${this._zip}\n${this._country}`;
  }
  
  isInternational() {
    return this._country !== 'USA';
  }
}

class Shipping {
  constructor() {
    this._address = null;
    this._expedited = false;
    this._trackingNumber = null;
  }
  
  setAddress(address) {
    this._address = address;
  }
  
  setExpedited(expedited) {
    this._expedited = expedited;
  }
  
  calculateCost(weight) {
    let baseShipping = this._expedited ? 25 : 10;
    
    if (this._address && this._address.isInternational()) {
      baseShipping *= 2;
    }
    
    return baseShipping + weight * 0.5;
  }
  
  ship() {
    if (!this._address) {
      throw new Error('Shipping address not set');
    }
    
    this._trackingNumber = this._generateTrackingNumber();
    console.log(`Order shipped to: ${this._address}`);
    console.log(`Tracking: ${this._trackingNumber}`);
  }
  
  _generateTrackingNumber() {
    return Math.random().toString(36).substr(2, 9).toUpperCase();
  }
  
  get trackingNumber() {
    return this._trackingNumber;
  }
}
```

## Mechanics

1. **Identify cohesive groups**
   - Look for fields and methods that work together
   - Find data that's always used together
   - Identify methods that operate on the same subset of fields

2. **Create the new class**
   - Choose a meaningful name
   - Add a constructor for the extracted data

3. **Create a link from the original class**
   - Add a field to hold an instance of the new class
   - Initialize it in the constructor

4. **Move fields using Move Field**
   - Move related fields one at a time
   - Test after each move

5. **Move methods using Move Function**
   - Move methods that primarily use the moved fields
   - Update any remaining references

6. **Review and simplify interfaces**
   - Look for ways to simplify the interactions
   - Consider whether some methods can be delegated

## Signs a Class Needs Extraction

### Too Many Fields
```javascript
// Class with 15+ fields probably doing too much
class Employee {
  constructor() {
    this.name = '';
    this.email = '';
    this.phone = '';
    this.address = '';
    this.city = '';
    this.state = '';
    this.zip = '';
    this.salary = 0;
    this.bonus = 0;
    this.benefits = 0;
    this.department = '';
    this.manager = '';
    this.startDate = null;
    this.performance = '';
    this.skills = [];
    // ... even more fields
  }
}
```

### Divergent Change
```javascript
// Different types of changes affect different parts
class Product {
  // Pricing-related (changes for pricing team)
  updatePrice() { /* ... */ }
  applyDiscount() { /* ... */ }
  calculateTax() { /* ... */ }
  
  // Inventory-related (changes for warehouse team)
  updateStock() { /* ... */ }
  reserveItems() { /* ... */ }
  trackLocation() { /* ... */ }
  
  // Shipping-related (changes for logistics team)
  calculateShipping() { /* ... */ }
  packItems() { /* ... */ }
  generateLabel() { /* ... */ }
}
```

### Shotgun Surgery
```javascript
// Adding a new field requires changes in many methods
class Customer {
  // Adding 'preferredLanguage' requires updating all these:
  sendEmail() { /* needs language */ }
  generateInvoice() { /* needs language */ }
  formatAddress() { /* needs language */ }
  createStatement() { /* needs language */ }
}
```

## When to Use

- **Large classes**: Classes with many fields and methods
- **Multiple responsibilities**: Class changes for different reasons
- **Subset usage**: Some methods only use a subset of fields
- **Testing difficulty**: Hard to test due to complex setup
- **Code duplication**: Similar groups of fields in multiple classes

## Trade-offs

### Benefits
- **Single Responsibility**: Each class has one clear purpose
- **Easier testing**: Smaller classes are simpler to test
- **Better reusability**: Extracted classes can be used elsewhere
- **Reduced coupling**: Dependencies become more explicit
- **Improved maintainability**: Changes affect fewer methods

### Drawbacks
- **More classes**: Increases the number of classes
- **Indirection**: May need to navigate through multiple objects
- **Interface complexity**: Need to design interactions between classes
- **Potential over-engineering**: Can create unnecessary complexity

## Guidelines

### Good Extraction
- Extracted class has a clear, single responsibility
- Fields and methods in the new class are highly cohesive
- The original class becomes simpler and more focused
- The new class could potentially be reused elsewhere

### Avoid Over-Extraction
```javascript
// Don't extract every single field
// Bad - over-extraction
class Person {
  constructor(nameWrapper, ageWrapper) {
    this._name = nameWrapper;
    this._age = ageWrapper;
  }
}

class NameWrapper {
  constructor(name) { this._name = name; }
  get name() { return this._name; }
}

class AgeWrapper {
  constructor(age) { this._age = age; }
  get age() { return this._age; }
}
```

## Related Refactorings

- [Inline Class](inline-class.md) - The inverse operation
- [Move Field](move-field.md) - Used during extraction
- [Move Function](move-function.md) - Used during extraction
- [Extract Superclass](extract-superclass.md) - When multiple classes need common behavior
- [Replace Data Value with Object](replace-primitive-with-object.md) - Similar concept for simple values