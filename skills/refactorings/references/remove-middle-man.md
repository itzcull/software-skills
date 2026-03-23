---
title: "Remove Middle Man"
description: "Remove a class that simply delegates to another class and have clients call the delegate directly"
category: "Encapsulation"
tags: ["middle-man", "delegation", "indirection", "simplification"]
related: ["hide-delegate", "inline-class", "move-function"]
---

# Remove Middle Man

Remove a class that is simply delegating to another class, and have clients call the delegate directly. This eliminates unnecessary indirection when a class provides little value beyond simple delegation.

## Inverse

[Hide Delegate](hide-delegate.md)

## Motivation

Middle man classes that do nothing but delegate can create problems:

- **Unnecessary indirection**: Extra layer that adds no value
- **Performance overhead**: Additional method calls without benefit
- **Maintenance burden**: More classes to maintain without purpose
- **Hidden functionality**: Delegate features are not accessible to clients
- **Code complexity**: More moving parts for no functional gain
- **Interface bloat**: Middle man grows methods just to expose delegate features

## Example

### Basic Example
```javascript
// Before - Unnecessary middle man
class PersonManager {
  constructor(person) {
    this._person = person;
  }
  
  // All methods just delegate to person
  getName() {
    return this._person.getName();
  }
  
  setName(name) {
    this._person.setName(name);
  }
  
  getAge() {
    return this._person.getAge();
  }
  
  setAge(age) {
    this._person.setAge(age);
  }
  
  getEmail() {
    return this._person.getEmail();
  }
  
  setEmail(email) {
    this._person.setEmail(email);
  }
  
  // PersonManager adds no value - just forwards everything
}

// After - Remove middle man, use delegate directly
class Person {
  constructor(name, age, email) {
    this._name = name;
    this._age = age;
    this._email = email;
  }
  
  getName() { return this._name; }
  setName(name) { this._name = name; }
  
  getAge() { return this._age; }
  setAge(age) { this._age = age; }
  
  getEmail() { return this._email; }
  setEmail(email) { this._email = email; }
  
  getFullContact() {
    return `${this._name} <${this._email}>`;
  }
  
  isAdult() {
    return this._age >= 18;
  }
}

// Client uses Person directly - simpler and more powerful
const person = new Person('John Doe', 30, 'john@example.com');

// Direct access - no unnecessary indirection
const name = person.getName();
const age = person.getAge();
person.setEmail('newemail@example.com');

// Can access all Person functionality
const fullContact = person.getFullContact();
const isAdult = person.isAdult();
```

## Mechanics

1. **Analyze the middle man**
   - Identify what value the middle man provides
   - Check if it's just simple delegation
   - Look for delegate features that aren't exposed

2. **Assess client needs**
   - Find all clients using the middle man
   - Determine if they need delegate features directly
   - Check for any middle man specific functionality

3. **Replace middle man usage**
   - Update clients to use the delegate directly
   - Replace middle man method calls with delegate calls
   - Provide helper methods on delegate if needed

4. **Add convenience methods to delegate**
   - Move any useful middle man methods to the delegate
   - Add domain-specific helper methods
   - Maintain any valuable abstractions

5. **Remove the middle man class**
   - Delete the middle man class
   - Update any factories or configuration
   - Clean up any unused imports

6. **Test thoroughly**
   - Verify all functionality is preserved
   - Check that performance is improved
   - Ensure no functionality is lost

## When to Use

- **Simple delegation**: Middle man just forwards calls to delegate
- **No added value**: Middle man provides no significant abstraction
- **Performance issues**: Extra layer is causing performance problems
- **Hidden functionality**: Delegate has useful features not exposed
- **Interface bloat**: Middle man keeps growing to expose delegate features
- **Maintenance burden**: Extra class with no clear benefit

## Trade-offs

### Benefits
- **Reduced complexity**: Fewer classes to maintain
- **Better performance**: Eliminates unnecessary method calls
- **Direct access**: Clients can use full delegate functionality
- **Simpler code**: Less indirection to understand
- **Exposed features**: Previously hidden delegate features become available

### Drawbacks
- **Increased coupling**: Clients become coupled to delegate
- **Lost abstraction**: May lose valuable simplification
- **Interface instability**: Delegate interface may be less stable
- **Breaking changes**: Clients need to be updated
- **Feature exposure**: May expose internal implementation details

## Related Refactorings

- [Hide Delegate](hide-delegate.md) - The inverse operation when encapsulation is needed
- [Move Method](move-method.md) - Move useful methods from middle man to delegate
- [Inline Class](inline-class.md) - Merge middle man into another class
- [Extract Superclass](extract-superclass.md) - Create common interface for delegate and middle man