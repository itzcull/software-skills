---
title: "Collapse Hierarchy"
description: "Merge a superclass and subclass when the distinction is no longer meaningful or necessary"
category: "Dealing with Inheritance"
tags: ["collapse", "hierarchy", "inheritance", "merge", "simplification"]
related: ["inline-class", "pull-up-method", "pull-up-field", "remove-subclass"]
---

# Collapse Hierarchy

Merge a superclass and subclass when the distinction between them is no longer meaningful or necessary. This simplifies the inheritance hierarchy when a subclass adds little or no value.

## Motivation

Class hierarchies evolve over time. What started as a meaningful distinction between classes may become unnecessary as:
- Features get refactored and moved around
- Requirements change and specializations are no longer needed
- The subclass becomes too similar to its parent
- The hierarchy becomes overly complex for the problem it solves

When a subclass isn't pulling its weight, it's time to merge it back into its parent.

## Example

### Simple Example
```javascript
// Before - Unnecessary subclass
class Employee {
  constructor(name, id, annualCost) {
    this._name = name;
    this._id = id;
    this._annualCost = annualCost;
  }
  
  get name() { return this._name; }
  get id() { return this._id; }
  get annualCost() { return this._annualCost; }
}

class Salesman extends Employee {
  // No additional behavior or fields
}

// After - Single class
class Employee {
  constructor(name, id, annualCost) {
    this._name = name;
    this._id = id;
    this._annualCost = annualCost;
  }
  
  get name() { return this._name; }
  get id() { return this._id; }
  get annualCost() { return this._annualCost; }
}
```

### Example with Minor Differences
```javascript
// Before - Subclass with minimal differences
class Party {
  constructor(name) {
    this._name = name;
  }
  
  get name() { return this._name; }
  get annualCost() {
    return this.monthlyCost * 12;
  }
}

class Department extends Party {
  constructor(name, staff) {
    super(name);
    this._staff = staff;
  }
  
  get staff() { return this._staff; }
  get monthlyCost() {
    return this._staff.reduce(
      (sum, emp) => sum + emp.monthlyCost, 0
    );
  }
  
  get headCount() {
    return this._staff.length;
  }
}

// After - Merged into single class
class Party {
  constructor(name, staff = []) {
    this._name = name;
    this._staff = staff;
  }
  
  get name() { return this._name; }
  get staff() { return this._staff; }
  
  get monthlyCost() {
    return this._staff.reduce(
      (sum, emp) => sum + emp.monthlyCost, 0
    );
  }
  
  get annualCost() {
    return this.monthlyCost * 12;
  }
  
  get headCount() {
    return this._staff.length;
  }
  
  get isDepartment() {
    return this._staff.length > 0;
  }
}
```

## Mechanics

1. **Choose which class to remove**
   - Usually remove the one with fewer features
   - Consider which name better represents the combined concept

2. **Pull up or push down all features**
   - Use [Pull Up Field](pull-up-field.md) and [Pull Up Method](pull-up-method.md)
   - Or use [Push Down Field](push-down-field.md) and [Push Down Method](push-down-method.md)
   - Move all fields, methods, and constructors

3. **Adjust constructors**
   - Ensure the remaining class can handle all creation scenarios
   - May need to add parameters or provide defaults

4. **Update all references**
   - Change all type declarations
   - Update instanceof checks
   - Modify any code that depends on the hierarchy

5. **Remove the empty class**
   - Delete the now-empty class
   - Remove any import/require statements

6. **Test**
   - Ensure all functionality still works
   - Check that no type-dependent code breaks

## When to Use

- **Empty subclass**: The subclass adds no fields or methods
- **Minimal differences**: The subclass has very few unique features
- **Lost purpose**: The original reason for the subclass no longer exists
- **Over-engineering**: The hierarchy is more complex than the problem requires
- **Single instance**: Only one subclass exists and no more are expected

## Trade-offs

### Benefits
- **Simplicity**: Reduces unnecessary complexity
- **Maintainability**: Fewer classes to understand and maintain
- **Performance**: Slight improvement from avoiding inheritance overhead
- **Clarity**: Makes it clear that the distinction isn't important

### Drawbacks
- **Future flexibility**: Harder to re-introduce the distinction later
- **Type safety**: May lose some compile-time type checking
- **Breaking changes**: Can break code that depends on the specific types
- **Conceptual clarity**: Sometimes separate classes better express domain concepts

## Example: Collapsing with Type Codes

```javascript
// When subclasses only differ by type
// Before
class Employee {
  constructor(name) {
    this._name = name;
  }
  get name() { return this._name; }
}

class Manager extends Employee {
  get type() { return "manager"; }
}

class Engineer extends Employee {
  get type() { return "engineer"; }
}

class Salesman extends Employee {
  get type() { return "salesman"; }
}

// After - Using type codes instead
class Employee {
  constructor(name, type) {
    this._name = name;
    this._type = type;
  }
  
  get name() { return this._name; }
  get type() { return this._type; }
  
  static createManager(name) {
    return new Employee(name, "manager");
  }
  
  static createEngineer(name) {
    return new Employee(name, "engineer");
  }
  
  static createSalesman(name) {
    return new Employee(name, "salesman");
  }
}
```

## Related Refactorings

- [Pull Up Method](pull-up-method.md) - Used to move methods to parent
- [Pull Up Field](pull-up-field.md) - Used to move fields to parent
- [Push Down Method](push-down-method.md) - Alternative direction for moving methods
- [Push Down Field](push-down-field.md) - Alternative direction for moving fields
- [Extract Superclass](extract-superclass.md) - Opposite refactoring
- [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md) - Opposite approach
- [Replace Subclass with Delegate](replace-subclass-with-delegate.md) - Alternative to collapsing