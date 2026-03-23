---
title: "Hide Delegate"
description: "Create methods on the server class to hide the delegate from the client and reduce coupling"
category: "Encapsulation"
tags: ["delegate", "encapsulation", "coupling", "navigation", "structure"]
related: ["remove-middle-man", "encapsulate-collection", "move-function"]
---

# Hide Delegate

Create methods on the server class to hide the delegate from the client. This reduces coupling between clients and the object's internal structure.

## Motivation

When clients need to navigate through multiple objects to get what they need, they become coupled to the navigation structure:

- **Exposed structure**: Clients depend on internal object relationships
- **Tight coupling**: Changes to object structure require client updates
- **Fragile code**: Navigation chains are prone to null reference errors
- **Poor encapsulation**: Internal organization is exposed to clients
- **Difficult maintenance**: Changes propagate through many client classes
- **Knowledge burden**: Clients must understand complex object hierarchies

## Example

### Basic Example
```javascript
// Before - Client must navigate through delegates
class Department {
  constructor(name, manager) {
    this._name = name;
    this._manager = manager;
  }
  
  get name() { return this._name; }
  get manager() { return this._manager; } // Exposes delegate
}

class Person {
  constructor(name, department) {
    this._name = name;
    this._department = department;
  }
  
  get name() { return this._name; }
  get department() { return this._department; } // Exposes delegate
}

class Manager {
  constructor(name, title) {
    this._name = name;
    this._title = title;
  }
  
  get name() { return this._name; }
  get title() { return this._title; }
}

// Client code is coupled to object structure
const manager = new Manager('Sarah Johnson', 'Engineering Manager');
const department = new Department('Engineering', manager);
const person = new Person('John Doe', department);

// Client must know the navigation path
const managerName = person.department.manager.name; // Fragile chain
const managerTitle = person.department.manager.title; // Another fragile chain
const departmentName = person.department.name;

// After - Hide delegates behind convenience methods
class Person {
  constructor(name, department) {
    this._name = name;
    this._department = department;
  }
  
  get name() { return this._name; }
  
  // Hide department delegate navigation
  getDepartmentName() {
    return this._department ? this._department.name : null;
  }
  
  getManagerName() {
    return this._department && this._department.manager 
      ? this._department.manager.name 
      : null;
  }
  
  getManagerTitle() {
    return this._department && this._department.manager 
      ? this._department.manager.title 
      : null;
  }
  
  hasManager() {
    return this._department && this._department.manager !== null;
  }
}

// Client code is now simpler and more robust
const manager = new Manager('Sarah Johnson', 'Engineering Manager');
const department = new Department('Engineering', manager);
const person = new Person('John Doe', department);

// Clean, safe access without navigation chains
const managerName = person.getManagerName();
const managerTitle = person.getManagerTitle();
const departmentName = person.getDepartmentName();
```

## Mechanics

1. **Identify navigation chains**
   - Find code that accesses delegates through chains
   - Look for repeated navigation patterns
   - Check for fragile navigation that could break

2. **Create delegating methods**
   - Add methods that hide the navigation
   - Choose meaningful names that express intent
   - Include null checking and error handling

3. **Replace client navigation**
   - Update clients to use new delegating methods
   - Remove direct access to delegates where possible
   - Keep delegate access for internal use if needed

4. **Add convenience methods**
   - Create methods that combine multiple delegate calls
   - Add business logic methods that use delegates internally
   - Provide meaningful abstractions over complex structures

5. **Consider removing delegate access**
   - Evaluate if public delegate access is still needed
   - Make delegate getters private/protected if possible
   - Document which methods are for internal use

6. **Test thoroughly**
   - Verify all navigation still works
   - Test null/error scenarios
   - Check that encapsulation is improved

## When to Use

- **Complex navigation**: Clients navigate through multiple object levels
- **Fragile chains**: Navigation chains are prone to null reference errors
- **Repeated patterns**: Same navigation appears in multiple places
- **Tight coupling**: Clients depend on internal object structure
- **API design**: Want to provide clean, simple interfaces
- **Encapsulation**: Need to hide internal object relationships

## Trade-offs

### Benefits
- **Reduced coupling**: Clients don't depend on internal structure
- **Improved encapsulation**: Internal organization is hidden
- **Easier maintenance**: Structure changes don't break clients
- **Better null safety**: Delegating methods can handle null cases
- **Cleaner client code**: Simpler method calls instead of navigation
- **Intent revelation**: Method names express what clients actually want

### Drawbacks
- **More methods**: Increases the interface size
- **Potential duplication**: May duplicate delegate functionality
- **Maintenance overhead**: Need to maintain delegating methods
- **Performance cost**: Additional method calls
- **Less flexibility**: Clients can't access delegate features directly

## Related Refactorings

- [Remove Middle Man](remove-middle-man.md) - The inverse operation when hiding becomes excessive
- [Move Method](move-method.md) - Move methods to eliminate delegation
- [Extract Class](extract-class.md) - Extract delegate handling into separate class