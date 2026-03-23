---
title: "Encapsulate Record"
description: "Transform a raw data record/object into a class with controlled access to its properties"
category: "Encapsulation"
tags: ["encapsulation", "record", "data-class", "getter", "setter", "validation"]
related: ["encapsulate-variable", "replace-primitive-with-object", "extract-class"]
---

# Encapsulate Record

Transform a raw data record/object into a class with controlled access to its properties. This provides getter and setter methods for better data management and potential future validation.

## Also Known As

- Replace Record with Data Class

## Motivation

Raw data structures (objects, dictionaries, records) are common in programming, but they have limitations:
- No place to add behavior
- No validation of data
- Direct field access makes changes difficult
- No encapsulation of derived values

By converting records to classes, we gain a proper home for methods and validation while maintaining clean interfaces.

## Example

### Basic Example
```javascript
// Before - Plain object
const organization = {name: "Acme Gooseberries", country: "GB"};

// Direct access and modification
console.log(organization.name);
organization.name = "New Name";

// After - Encapsulated class
class Organization {
  constructor(data) {
    this._name = data.name;
    this._country = data.country;
  }
  
  get name() { return this._name; }
  set name(aString) { this._name = aString; }
  
  get country() { return this._country; }
  set country(aCountryCode) { this._country = aCountryCode; }
}

const organization = new Organization({name: "Acme Gooseberries", country: "GB"});
console.log(organization.name);
organization.name = "New Name";
```

### With Validation
```javascript
// Before - No validation possible
const employee = {
  name: "John",
  age: 25,
  email: "john@example.com",
  salary: 50000
};

employee.age = -5; // Invalid but allowed
employee.email = "not-an-email"; // Invalid but allowed

// After - With validation
class Employee {
  constructor(data) {
    this._name = data.name;
    this._age = data.age;
    this._email = data.email;
    this._salary = data.salary;
    this._validate();
  }
  
  get name() { return this._name; }
  set name(value) {
    if (!value || value.trim() === '') {
      throw new Error('Name cannot be empty');
    }
    this._name = value;
  }
  
  get age() { return this._age; }
  set age(value) {
    if (value < 0 || value > 150) {
      throw new Error('Invalid age');
    }
    this._age = value;
  }
  
  get email() { return this._email; }
  set email(value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      throw new Error('Invalid email format');
    }
    this._email = value;
  }
  
  get salary() { return this._salary; }
  set salary(value) {
    if (value < 0) {
      throw new Error('Salary cannot be negative');
    }
    this._salary = value;
  }
  
  _validate() {
    // Trigger setters to validate initial data
    this.name = this._name;
    this.age = this._age;
    this.email = this._email;
    this.salary = this._salary;
  }
  
  // Derived value
  get monthlySalary() {
    return this._salary / 12;
  }
}
```

### Nested Records
```javascript
// Before - Nested plain objects
const person = {
  name: "Alice",
  address: {
    street: "123 Main St",
    city: "Boston",
    postalCode: "02101"
  }
};

// After - Nested classes
class Address {
  constructor(data) {
    this._street = data.street;
    this._city = data.city;
    this._postalCode = data.postalCode;
  }
  
  get street() { return this._street; }
  set street(value) { this._street = value; }
  
  get city() { return this._city; }
  set city(value) { this._city = value; }
  
  get postalCode() { return this._postalCode; }
  set postalCode(value) {
    if (!/^\d{5}(-\d{4})?$/.test(value)) {
      throw new Error('Invalid postal code');
    }
    this._postalCode = value;
  }
  
  toString() {
    return `${this._street}, ${this._city} ${this._postalCode}`;
  }
}

class Person {
  constructor(data) {
    this._name = data.name;
    this._address = new Address(data.address);
  }
  
  get name() { return this._name; }
  set name(value) { this._name = value; }
  
  get address() { return this._address; }
  set address(anAddress) {
    if (!(anAddress instanceof Address)) {
      throw new Error('Address must be an Address instance');
    }
    this._address = anAddress;
  }
}
```

## Mechanics

1. **Create a class for the record**
   - Use a meaningful name for the class
   - Add a constructor that takes the record data

2. **Create private fields for each property**
   - Prefix with underscore or use private field syntax
   - Initialize from constructor parameter

3. **Create getters and setters**
   - Add getter for each field
   - Add setter for each mutable field
   - Consider making some fields read-only

4. **Replace record creation with class instantiation**
   - Find all places records are created
   - Replace with new ClassName(data)

5. **Replace property access with getter/setter calls**
   - Update all direct field access
   - Use the new accessor methods

6. **Test incrementally**
   - Test after each property migration
   - Ensure behavior remains consistent

## Advanced Patterns

### Immutable Records
```javascript
class ImmutablePoint {
  constructor(x, y) {
    this._x = x;
    this._y = y;
    Object.freeze(this);
  }
  
  get x() { return this._x; }
  get y() { return this._y; }
  
  // No setters - create new instances instead
  withX(newX) {
    return new ImmutablePoint(newX, this._y);
  }
  
  withY(newY) {
    return new ImmutablePoint(this._x, newY);
  }
  
  distanceTo(other) {
    const dx = this._x - other.x;
    const dy = this._y - other.y;
    return Math.sqrt(dx * dx + dy * dy);
  }
}
```

### Builder Pattern
```javascript
class CustomerBuilder {
  constructor() {
    this._data = {};
  }
  
  withName(name) {
    this._data.name = name;
    return this;
  }
  
  withEmail(email) {
    this._data.email = email;
    return this;
  }
  
  withPhone(phone) {
    this._data.phone = phone;
    return this;
  }
  
  build() {
    return new Customer(this._data);
  }
}

// Usage
const customer = new CustomerBuilder()
  .withName("John Doe")
  .withEmail("john@example.com")
  .withPhone("555-1234")
  .build();
```

### Factory Methods
```javascript
class Temperature {
  constructor(celsius) {
    this._celsius = celsius;
  }
  
  static fromCelsius(celsius) {
    return new Temperature(celsius);
  }
  
  static fromFahrenheit(fahrenheit) {
    return new Temperature((fahrenheit - 32) * 5/9);
  }
  
  static fromKelvin(kelvin) {
    return new Temperature(kelvin - 273.15);
  }
  
  get celsius() { return this._celsius; }
  get fahrenheit() { return this._celsius * 9/5 + 32; }
  get kelvin() { return this._celsius + 273.15; }
}

// Usage
const temp1 = Temperature.fromCelsius(25);
const temp2 = Temperature.fromFahrenheit(77);
```

## When to Use

- **Complex validation**: When data needs validation rules
- **Derived values**: When you have calculated properties
- **Future behavior**: When you might add methods later
- **API boundaries**: At system interfaces for stability
- **Type safety**: In typed languages for better checking

## Trade-offs

### Benefits
- **Encapsulation**: Hides internal representation
- **Validation**: Can enforce data integrity
- **Flexibility**: Easy to add behavior later
- **Debugging**: Can add logging to setters
- **Refactoring**: Easier to change internals

### Drawbacks
- **Verbosity**: More code than plain objects
- **Performance**: Slight overhead from method calls
- **Serialization**: May complicate JSON conversion
- **Learning curve**: More complex than plain data

## Common Pitfalls

### Over-Engineering
```javascript
// Too much for simple data
class Color {
  constructor(r, g, b) {
    this.setRed(r);
    this.setGreen(g);
    this.setBlue(b);
  }
  
  getRed() { return this._r; }
  setRed(value) { 
    this._validateColorValue(value);
    this._r = value;
  }
  // ... etc
}

// Better for simple cases
class Color {
  constructor(r, g, b) {
    this.r = r;
    this.g = g;
    this.b = b;
  }
}
```

### Anemic Domain Model
```javascript
// Bad - Just getters and setters
class Order {
  get items() { return this._items; }
  set items(value) { this._items = value; }
  get total() { return this._total; }
  set total(value) { this._total = value; }
}

// Good - Rich behavior
class Order {
  constructor() {
    this._items = [];
  }
  
  addItem(product, quantity) {
    this._items.push({product, quantity});
  }
  
  get total() {
    return this._items.reduce(
      (sum, item) => sum + item.product.price * item.quantity, 
      0
    );
  }
}
```

## Related Refactorings

- [Replace Primitive with Object](replace-primitive-with-object.md) - Similar concept for primitives
- [Extract Class](extract-class.md) - When record logic grows complex
- [Encapsulate Variable](encapsulate-variable.md) - General encapsulation
- [Encapsulate Collection](encapsulate-collection.md) - For collection properties
- [Change Value to Reference](change-value-to-reference.md) - When identity matters