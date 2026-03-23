---
title: "Remove Setting Method"
description: "Remove a setter method when a field should not be changed after object creation"
category: "Encapsulation"
tags: ["setter", "immutability", "encapsulation", "state-change"]
related: ["encapsulate-variable", "remove-dead-code", "change-reference-to-value"]
---

# Remove Setting Method

Remove a method that sets the value of a field when that field should not be changed after object creation. This improves immutability and prevents unwanted state changes.

## Motivation

Setting methods (setters) can cause problems when they exist for fields that shouldn't be modified:

- **Broken immutability**: Objects become mutable when they should be immutable
- **Invalid state changes**: Allows objects to be put into inconsistent states
- **Temporal coupling**: Object behavior depends on when setters are called
- **Thread safety issues**: Concurrent modifications can cause race conditions
- **Violated invariants**: Setters can break object invariants
- **Confusion about lifecycle**: Unclear when objects are "complete" or "ready"

## Example

### Basic Example
```javascript
// Before - Unnecessary setter for immutable data
class PersonId {
  constructor(value) {
    this._value = value;
  }
  
  get value() {
    return this._value;
  }
  
  // This setter shouldn't exist - PersonId should be immutable
  set value(newValue) {
    this._value = newValue;
  }
  
  toString() {
    return this._value;
  }
  
  equals(other) {
    return other instanceof PersonId && this._value === other._value;
  }
}

// After - Immutable PersonId
class PersonId {
  constructor(value) {
    if (!value || typeof value !== 'string') {
      throw new Error('PersonId value must be a non-empty string');
    }
    this._value = value;
    Object.freeze(this); // Make the object immutable
  }
  
  get value() {
    return this._value;
  }
  
  // No setter - PersonId is immutable
  
  toString() {
    return this._value;
  }
  
  equals(other) {
    return other instanceof PersonId && this._value === other._value;
  }
  
  // If you need a different value, create a new instance
  withNewValue(newValue) {
    return new PersonId(newValue);
  }
}
```

## Mechanics

1. **Identify problematic setters**
   - Find setters for fields that should be immutable
   - Look for setters that can put objects in invalid states
   - Check for setters that break business rules

2. **Analyze dependencies**
   - Find all code that uses the setter
   - Determine if the setter is actually needed
   - Check if the field should be set only during construction

3. **Provide alternatives if needed**
   - Create factory methods for different configurations
   - Add `withX()` methods for creating modified copies
   - Provide controlled state transition methods

4. **Remove the setter**
   - Delete the setter method
   - Make the field read-only if appropriate
   - Update any code that was using the setter

5. **Enforce immutability**
   - Use `Object.freeze()` for complete immutability
   - Use `Object.defineProperty()` with `writable: false`
   - Consider using TypeScript `readonly` modifier

6. **Update client code**
   - Replace setter calls with constructor parameters
   - Use factory methods or builder pattern
   - Use controlled methods for state changes

7. **Test thoroughly**
   - Verify that objects maintain valid state
   - Test that immutability is enforced
   - Check that all functionality still works

## When to Use

- **Immutable value objects**: Objects that should never change after creation
- **Identity fields**: IDs, keys, or other identifying information
- **Calculated properties**: Values derived from other properties
- **Invalid state prevention**: Setters that can break object invariants
- **Controlled state transitions**: Complex state that needs managed changes
- **Thread safety**: Objects that need to be thread-safe

## Trade-offs

### Benefits
- **Immutability**: Objects cannot be accidentally modified
- **Thread safety**: Immutable objects are inherently thread-safe
- **Predictability**: Object state cannot change unexpectedly
- **Hash stability**: Objects can be safely used as hash keys
- **Simplified reasoning**: Easier to understand object lifecycle
- **Prevented bugs**: Cannot put objects into invalid states

### Drawbacks
- **Less flexibility**: Cannot modify objects after creation
- **Memory usage**: May need to create new instances for changes
- **API changes**: Clients need to adapt to new patterns
- **Learning curve**: Team needs to understand immutability concepts
- **Verbose patterns**: Builder or factory patterns can be more complex

## Related Refactorings

- [Extract Class](extract-class.md) - Extract mutable parts into separate class
- [Replace Primitive with Object](replace-primitive-with-object.md) - Create proper value objects
- [Encapsulate Field](encapsulate-field.md) - Add proper encapsulation before removing setters