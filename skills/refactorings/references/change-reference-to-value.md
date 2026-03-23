---
title: "Change Reference to Value"
description: "Transform a reference object into an immutable value object for predictable manipulation"
category: "Organizing Data"
tags: ["reference", "value", "immutable", "predictability", "thread-safety"]
related: ["change-value-to-reference", "remove-setting-method", "replace-primitive-with-object"]
---

# Change Reference to Value

Transform a reference object into an immutable value object. This allows for more predictable and safer object manipulation by creating new instances rather than modifying existing ones.

## Inverse

[Change Value to Reference](change-value-to-reference.md)

## Motivation

When objects are shared and mutable, changes in one place can have unexpected effects elsewhere in the system. By converting reference objects to value objects, we gain:
- **Immutability**: Objects cannot be changed after creation
- **Predictability**: No unexpected side effects from modifications
- **Thread safety**: Immutable objects are inherently thread-safe
- **Simplicity**: Easier to reason about code behavior

Value objects are particularly useful for representing concepts like money, dates, or coordinates where identity isn't important, only the values matter.

## Example

### Basic Example
```java
// Before
class Product {
  private Money price;
  
  applyDiscount(amount) {
    this.price.amount -= amount; // Modifying the existing object
  }
}

// After
class Product {
  private Money price;
  
  applyDiscount(amount) {
    this.price = new Money(this.price.amount - amount, this.price.currency);
  }
}
```

### JavaScript Example
```javascript
// Before
class Person {
  constructor(name, phoneNumber) {
    this.name = name;
    this.phoneNumber = phoneNumber;
  }
  
  updateAreaCode(newCode) {
    this.phoneNumber.areaCode = newCode; // Mutating shared object
  }
}

// After
class Person {
  constructor(name, phoneNumber) {
    this.name = name;
    this.phoneNumber = phoneNumber;
  }
  
  updateAreaCode(newCode) {
    this.phoneNumber = new PhoneNumber(
      newCode,
      this.phoneNumber.number
    );
  }
}

class PhoneNumber {
  constructor(areaCode, number) {
    this.areaCode = areaCode;
    this.number = number;
  }
  
  equals(other) {
    return this.areaCode === other.areaCode && 
           this.number === other.number;
  }
}
```

## Mechanics

1. **Check that the candidate is immutable or can become immutable**
   - Remove any setters
   - Ensure all fields are set only in the constructor

2. **Remove any setters on the object**
   - If setters exist, replace them with methods that return new instances

3. **Provide an equals method based on the object's fields**
   - Value objects should be compared by their values, not identity
   - Implement proper equality comparison

4. **Replace mutations with creating new objects**
   - Find all places where the object is modified
   - Replace with creation of new instances

5. **Test after each change**
   - Ensure behavior remains consistent
   - Verify immutability is maintained

## When to Use

- **Small objects**: Objects that represent simple values or measurements
- **No meaningful identity**: When you care about what the object contains, not which object it is
- **Frequent comparisons**: When objects are often compared for equality
- **Thread safety needed**: In concurrent environments where shared mutable state is problematic
- **Functional programming**: When adopting functional programming principles

## Trade-offs

### Benefits
- **Predictability**: No unexpected mutations
- **Thread safety**: Immutable objects are inherently thread-safe
- **Easier testing**: No need to worry about state changes
- **Simpler equality**: Can use value-based equality
- **Better for caching**: Immutable objects can be safely cached

### Drawbacks
- **Performance**: Creating new objects can be slower than mutation
- **Memory usage**: More objects may be created
- **Learning curve**: Requires different thinking about object updates
- **Framework compatibility**: Some frameworks expect mutable objects

## Example: Complex Value Object

```javascript
// Complete example with Address as a value object
class Address {
  constructor(street, city, postalCode, country) {
    // Make fields truly private and immutable
    Object.freeze(Object.assign(this, {
      street,
      city,
      postalCode,
      country
    }));
  }
  
  // Return new instance for any "change"
  withStreet(newStreet) {
    return new Address(newStreet, this.city, this.postalCode, this.country);
  }
  
  withCity(newCity) {
    return new Address(this.street, newCity, this.postalCode, this.country);
  }
  
  equals(other) {
    if (!(other instanceof Address)) return false;
    return this.street === other.street &&
           this.city === other.city &&
           this.postalCode === other.postalCode &&
           this.country === other.country;
  }
  
  toString() {
    return `${this.street}, ${this.city}, ${this.postalCode}, ${this.country}`;
  }
}
```

## Related Refactorings

- [Change Value to Reference](change-value-to-reference.md) - The inverse operation
- [Replace Primitive with Object](replace-primitive-with-object.md) - Creating value objects from primitives
- [Introduce Parameter Object](introduce-parameter-object.md) - Often creates value objects
- [Extract Class](extract-class.md) - May be needed to separate value object logic