---
title: "Replace Superclass with Delegate"
description: "Replace inheritance with composition by turning the superclass into a delegate"
category: "Dealing with Inheritance"
tags: ["inheritance", "composition", "delegate", "flexibility"]
related: ["extract-class", "hide-delegate", "replace-conditional-with-polymorphism"]
---

# Replace Superclass with Delegate

Replace inheritance with composition by turning the superclass into a delegate. This provides more flexibility and avoids the problems that come with inappropriate inheritance.

## Motivation

Inheritance can create problems when:

- **Inappropriate relationship**: Subclass doesn't truly "is-a" the superclass
- **Interface pollution**: Subclass inherits methods it doesn't need or want
- **Tight coupling**: Changes to superclass can break subclasses
- **Single inheritance limitation**: Can't inherit from multiple classes
- **Forced interface**: Can't control which methods are exposed
- **Liskov Substitution violations**: Subclass can't properly substitute for superclass

## Example

### Basic Example
```javascript
// Before - Stack inappropriately inherits from List
class List {
  constructor() {
    this._items = [];
  }
  
  add(item) {
    this._items.push(item);
  }
  
  remove(index) {
    if (index >= 0 && index < this._items.length) {
      return this._items.splice(index, 1)[0];
    }
    return null;
  }
  
  get(index) {
    return this._items[index];
  }
  
  set(index, item) {
    this._items[index] = item;
  }
  
  size() {
    return this._items.length;
  }
  
  isEmpty() {
    return this._items.length === 0;
  }
  
  indexOf(item) {
    return this._items.indexOf(item);
  }
  
  clear() {
    this._items = [];
  }
}

class Stack extends List {
  // Stack should only expose stack operations
  push(item) {
    this.add(item); // Uses inherited method
  }
  
  pop() {
    if (this.isEmpty()) {
      return null;
    }
    return this.remove(this.size() - 1); // Uses inherited method
  }
  
  peek() {
    if (this.isEmpty()) {
      return null;
    }
    return this.get(this.size() - 1); // Uses inherited method
  }
}

// Problem: Stack exposes List methods that break stack semantics
const stack = new Stack();
stack.push(1);
stack.push(2);
stack.push(3);

// These operations violate stack semantics but are allowed!
stack.remove(1); // Removes middle element
stack.set(0, 99); // Modifies arbitrary element
console.log(stack.indexOf(2)); // Exposes internal structure

// After - Stack uses List as a delegate
class Stack {
  constructor() {
    this._list = new List(); // Composition instead of inheritance
  }
  
  push(item) {
    this._list.add(item);
  }
  
  pop() {
    if (this._list.isEmpty()) {
      return null;
    }
    return this._list.remove(this._list.size() - 1);
  }
  
  peek() {
    if (this._list.isEmpty()) {
      return null;
    }
    return this._list.get(this._list.size() - 1);
  }
  
  size() {
    return this._list.size();
  }
  
  isEmpty() {
    return this._list.isEmpty();
  }
  
  clear() {
    this._list.clear();
  }
}

// Now Stack only exposes appropriate stack operations
const stack = new Stack();
stack.push(1);
stack.push(2);
stack.push(3);

// These operations are no longer available - compilation/runtime error
// stack.remove(1);     // Error: method doesn't exist
// stack.set(0, 99);    // Error: method doesn't exist
// stack.indexOf(2);    // Error: method doesn't exist

console.log(stack.pop()); // 3 - proper stack behavior
```

### Complex Example - Employee and Person
```javascript
// Before - Employee inherits from Person but the relationship is problematic
class Person {
  constructor(name, age, address) {
    this._name = name;
    this._age = age;
    this._address = address;
    this._relationships = [];
  }
  
  get name() { return this._name; }
  get age() { return this._age; }
  get address() { return this._address; }
  
  setAddress(address) {
    this._address = address;
  }
  
  addRelationship(person, type) {
    this._relationships.push({ person, type });
  }
  
  getRelationships() {
    return [...this._relationships];
  }
  
  introduceTo(otherPerson) {
    return `Hi ${otherPerson.name}, I'm ${this._name}`;
  }
  
  celebrateBirthday() {
    this._age++;
    return `${this._name} is now ${this._age} years old!`;
  }
  
  // Personal methods that don't make sense for employees in work context
  getMaritalStatus() {
    const spouse = this._relationships.find(r => r.type === 'spouse');
    return spouse ? 'married' : 'single';
  }
  
  getChildren() {
    return this._relationships.filter(r => r.type === 'child').map(r => r.person);
  }
}

class Employee extends Person {
  constructor(name, age, address, employeeId, department, salary) {
    super(name, age, address);
    this._employeeId = employeeId;
    this._department = department;
    this._salary = salary;
    this._manager = null;
    this._reports = [];
  }
  
  get employeeId() { return this._employeeId; }
  get department() { return this._department; }
  get salary() { return this._salary; }
  
  setManager(manager) {
    this._manager = manager;
  }
  
  addReport(employee) {
    this._reports.push(employee);
  }
  
  getReports() {
    return [...this._reports];
  }
  
  introduceTo(otherPerson) {
    // Override to be work-appropriate
    if (otherPerson instanceof Employee) {
      return `Hello, I'm ${this._name} from ${this._department}`;
    }
    return super.introduceTo(otherPerson);
  }
  
  // Problem: Employee inherits personal methods that don't belong in work context
  // celebrateBirthday() - might be inappropriate in work system
  // getMaritalStatus() - privacy concerns in HR system
  // getChildren() - not relevant for work
}

// Problems with inheritance:
// 1. Employee exposes personal relationship methods in work context
// 2. Changes to Person affect Employee
// 3. Can't easily make Employee extend something else (like User)
// 4. Violates single responsibility - Employee handles both work and personal data

const employee = new Employee('John', 30, '123 Main St', 'E001', 'Engineering', 75000);

// These personal methods are available but inappropriate in work context:
console.log(employee.getMaritalStatus()); // Should this be available in HR system?
console.log(employee.getChildren());      // Privacy concerns

// After - Employee delegates to Person for personal information
class Employee {
  constructor(name, age, address, employeeId, department, salary) {
    this._person = new Person(name, age, address); // Delegate
    this._employeeId = employeeId;
    this._department = department;
    this._salary = salary;
    this._manager = null;
    this._reports = [];
  }
  
  // Expose only relevant Person methods
  get name() { return this._person.name; }
  get age() { return this._person.age; }
  get address() { return this._person.address; }
  
  setAddress(address) {
    this._person.setAddress(address);
  }
  
  // Work-specific properties
  get employeeId() { return this._employeeId; }
  get department() { return this._department; }
  get salary() { return this._salary; }
  
  setManager(manager) {
    this._manager = manager;
  }
  
  addReport(employee) {
    this._reports.push(employee);
  }
  
  getReports() {
    return [...this._reports];
  }
  
  // Work-appropriate introduction
  introduceTo(otherEmployee) {
    return `Hello, I'm ${this.name} from ${this._department}`;
  }
  
  // Only expose birthday celebration if appropriate for work context
  celebrateWorkAnniversary() {
    return `${this.name} is celebrating another year at the company!`;
  }
  
  // If personal information is needed, provide controlled access
  getPersonalInformation() {
    // Only return if user has permission
    return this._person;
  }
}

// Now Employee only exposes work-appropriate methods
const employee = new Employee('John', 30, '123 Main St', 'E001', 'Engineering', 75000);

// Work-related operations are clear and appropriate
console.log(employee.name);           // OK - needed for work
console.log(employee.department);     // OK - work-related
console.log(employee.introduceTo(otherEmployee)); // OK - work context

// Personal methods are no longer directly available
// employee.getMaritalStatus();  // Error - method doesn't exist
// employee.getChildren();       // Error - method doesn't exist
// employee.celebrateBirthday(); // Error - use celebrateWorkAnniversary instead

// Can still access personal info when appropriate
const personalInfo = employee.getPersonalInformation();
console.log(personalInfo.getMaritalStatus()); // Controlled access
```

### UI Component Example
```javascript
// Before - Window inherits from Rectangle but needs different behavior
class Rectangle {
  constructor(x, y, width, height) {
    this._x = x;
    this._y = y;
    this._width = width;
    this._height = height;
  }
  
  get x() { return this._x; }
  get y() { return this._y; }
  get width() { return this._width; }
  get height() { return this._height; }
  
  setPosition(x, y) {
    this._x = x;
    this._y = y;
  }
  
  setSize(width, height) {
    this._width = width;
    this._height = height;
  }
  
  getArea() {
    return this._width * this._height;
  }
  
  contains(pointX, pointY) {
    return pointX >= this._x && pointX <= this._x + this._width &&
           pointY >= this._y && pointY <= this._y + this._height;
  }
  
  intersects(other) {
    return !(other._x > this._x + this._width ||
             other._x + other._width < this._x ||
             other._y > this._y + this._height ||
             other._y + other._height < this._y);
  }
}

class Window extends Rectangle {
  constructor(x, y, width, height, title) {
    super(x, y, width, height);
    this._title = title;
    this._isVisible = true;
    this._isMinimized = false;
    this._minWidth = 200;
    this._minHeight = 100;
    this._components = [];
  }
  
  get title() { return this._title; }
  
  setSize(width, height) {
    // Window has constraints that Rectangle doesn't
    const constrainedWidth = Math.max(width, this._minWidth);
    const constrainedHeight = Math.max(height, this._minHeight);
    super.setSize(constrainedWidth, constrainedHeight);
  }
  
  show() {
    this._isVisible = true;
  }
  
  hide() {
    this._isVisible = false;
  }
  
  minimize() {
    this._isMinimized = true;
  }
  
  restore() {
    this._isMinimized = false;
  }
  
  addComponent(component) {
    this._components.push(component);
  }
  
  // Problem: Window inherits geometric methods that may not make sense
  // getArea() - not really relevant for windows
  // intersects() - complex for windows with decorations
}

// Window is forced to override methods or accept inappropriate behavior
const window = new Window(100, 100, 400, 300, 'My App');
console.log(window.getArea()); // 120000 - is this meaningful for a window?

// After - Window delegates to Rectangle for geometric operations
class Window {
  constructor(x, y, width, height, title) {
    this._bounds = new Rectangle(x, y, width, height); // Delegate
    this._title = title;
    this._isVisible = true;
    this._isMinimized = false;
    this._minWidth = 200;
    this._minHeight = 100;
    this._components = [];
  }
  
  get title() { return this._title; }
  get x() { return this._bounds.x; }
  get y() { return this._bounds.y; }
  get width() { return this._bounds.width; }
  get height() { return this._bounds.height; }
  
  setPosition(x, y) {
    this._bounds.setPosition(x, y);
  }
  
  setSize(width, height) {
    // Apply window-specific constraints
    const constrainedWidth = Math.max(width, this._minWidth);
    const constrainedHeight = Math.max(height, this._minHeight);
    this._bounds.setSize(constrainedWidth, constrainedHeight);
  }
  
  getBounds() {
    return this._bounds;
  }
  
  contains(pointX, pointY) {
    // Only check if visible and not minimized
    if (!this._isVisible || this._isMinimized) {
      return false;
    }
    return this._bounds.contains(pointX, pointY);
  }
  
  intersectsWindow(otherWindow) {
    // Window-specific intersection logic
    if (!this._isVisible || !otherWindow._isVisible) {
      return false;
    }
    return this._bounds.intersects(otherWindow._bounds);
  }
  
  show() {
    this._isVisible = true;
  }
  
  hide() {
    this._isVisible = false;
  }
  
  minimize() {
    this._isMinimized = true;
  }
  
  restore() {
    this._isMinimized = false;
  }
  
  addComponent(component) {
    this._components.push(component);
  }
  
  // Window-specific methods
  getVisibleArea() {
    if (!this._isVisible || this._isMinimized) {
      return 0;
    }
    return this._bounds.getArea();
  }
}

// Now Window has appropriate interface and behavior
const window = new Window(100, 100, 400, 300, 'My App');
console.log(window.getVisibleArea()); // 120000 - meaningful for windows
window.minimize();
console.log(window.getVisibleArea()); // 0 - makes sense for minimized window

// Geometric operations are available when needed
const bounds = window.getBounds();
console.log(bounds.getArea()); // Direct access to Rectangle functionality
```

### Database Connection Example
```javascript
// Before - FileBasedCache inappropriately inherits from File
class File {
  constructor(path) {
    this._path = path;
    this._content = '';
    this._isOpen = false;
  }
  
  open() {
    this._isOpen = true;
    // Read file content
  }
  
  close() {
    this._isOpen = false;
  }
  
  read() {
    if (!this._isOpen) {
      throw new Error('File is not open');
    }
    return this._content;
  }
  
  write(content) {
    if (!this._isOpen) {
      throw new Error('File is not open');
    }
    this._content = content;
  }
  
  append(content) {
    if (!this._isOpen) {
      throw new Error('File is not open');
    }
    this._content += content;
  }
  
  truncate() {
    if (!this._isOpen) {
      throw new Error('File is not open');
    }
    this._content = '';
  }
  
  getSize() {
    return this._content.length;
  }
}

class FileBasedCache extends File {
  constructor(cachePath) {
    super(cachePath);
    this._cache = new Map();
    this.open(); // Auto-open for cache
  }
  
  set(key, value) {
    this._cache.set(key, value);
    this._persistCache();
  }
  
  get(key) {
    return this._cache.get(key);
  }
  
  delete(key) {
    this._cache.delete(key);
    this._persistCache();
  }
  
  clear() {
    this._cache.clear();
    this._persistCache();
  }
  
  _persistCache() {
    const cacheData = JSON.stringify([...this._cache.entries()]);
    this.write(cacheData); // Uses inherited method
  }
  
  _loadCache() {
    try {
      const data = this.read(); // Uses inherited method
      const entries = JSON.parse(data);
      this._cache = new Map(entries);
    } catch (error) {
      this._cache = new Map();
    }
  }
}

// Problem: Cache exposes file methods that don't make sense for cache
const cache = new FileBasedCache('/tmp/cache.json');
cache.set('key1', 'value1');

// These file operations don't make sense for a cache:
cache.append('random data'); // Corrupts cache format!
cache.truncate();           // Destroys cache!
console.log(cache.getSize()); // Not meaningful for cache

// After - Cache delegates to File for persistence
class FileBasedCache {
  constructor(cachePath) {
    this._file = new File(cachePath); // Delegate
    this._cache = new Map();
    this._isDirty = false;
    this._loadCache();
  }
  
  set(key, value) {
    this._cache.set(key, value);
    this._isDirty = true;
    this._scheduleFlush();
  }
  
  get(key) {
    return this._cache.get(key);
  }
  
  has(key) {
    return this._cache.has(key);
  }
  
  delete(key) {
    const result = this._cache.delete(key);
    if (result) {
      this._isDirty = true;
      this._scheduleFlush();
    }
    return result;
  }
  
  clear() {
    this._cache.clear();
    this._isDirty = true;
    this._scheduleFlush();
  }
  
  size() {
    return this._cache.size;
  }
  
  keys() {
    return this._cache.keys();
  }
  
  values() {
    return this._cache.values();
  }
  
  flush() {
    if (this._isDirty) {
      this._persistCache();
      this._isDirty = false;
    }
  }
  
  _persistCache() {
    try {
      this._file.open();
      const cacheData = JSON.stringify([...this._cache.entries()]);
      this._file.write(cacheData);
      this._file.close();
    } catch (error) {
      console.error('Failed to persist cache:', error);
    }
  }
  
  _loadCache() {
    try {
      this._file.open();
      const data = this._file.read();
      this._file.close();
      
      if (data) {
        const entries = JSON.parse(data);
        this._cache = new Map(entries);
      }
    } catch (error) {
      this._cache = new Map();
    }
  }
  
  _scheduleFlush() {
    // Debounce flush operations
    if (this._flushTimeout) {
      clearTimeout(this._flushTimeout);
    }
    this._flushTimeout = setTimeout(() => this.flush(), 1000);
  }
}

// Now Cache only exposes cache-appropriate methods
const cache = new FileBasedCache('/tmp/cache.json');
cache.set('key1', 'value1');
cache.set('key2', 'value2');

// Only cache operations are available:
console.log(cache.size());     // 2 - meaningful for cache
console.log(cache.has('key1')); // true - cache operation

// File operations are no longer directly available:
// cache.append('data');  // Error - method doesn't exist
// cache.truncate();      // Error - method doesn't exist
// cache.getSize();       // Error - use size() instead

cache.flush(); // Controlled file access
```

## Mechanics

1. **Identify inappropriate inheritance**
   - Look for "has-a" relationships modeled as "is-a"
   - Find subclasses that override many superclass methods
   - Check for interface pollution (unwanted inherited methods)

2. **Create delegate field**
   - Add a field to hold an instance of the former superclass
   - Initialize the delegate in the constructor
   - Choose a descriptive name for the delegate field

3. **Replace inheritance with delegation**
   - Remove the extends clause
   - For each inherited method that's still needed, create a delegating method
   - Remove or replace methods that shouldn't be exposed

4. **Update method implementations**
   - Change method calls from `super.method()` to `this._delegate.method()`
   - Modify methods that need different behavior
   - Add new methods that provide appropriate abstractions

5. **Control the interface**
   - Only expose methods that make sense for the class
   - Add new methods that provide better abstractions
   - Consider providing access to the delegate when needed

6. **Test thoroughly**
   - Verify that all functionality is preserved
   - Test that unwanted methods are no longer accessible
   - Check that the new interface makes sense

## When to Use

- **Inappropriate "is-a" relationship**: Subclass doesn't truly "is-a" the superclass
- **Interface pollution**: Subclass inherits methods it doesn't need
- **Liskov Substitution violations**: Subclass can't properly substitute for superclass
- **Need multiple inheritance**: Want to delegate to multiple objects
- **Complex overriding**: Subclass overrides many superclass methods
- **Tight coupling**: Inheritance creates unwanted dependencies

## Trade-offs

### Benefits
- **Better encapsulation**: Control which methods are exposed
- **Flexibility**: Can delegate to multiple objects
- **Loose coupling**: Less dependent on superclass changes
- **Appropriate interface**: Only expose relevant methods
- **Composition benefits**: Runtime flexibility and testing advantages

### Drawbacks
- **More verbose**: Need to write delegating methods
- **Lost polymorphism**: Can't use subclass where superclass is expected
- **Performance overhead**: Additional method calls through delegate
- **Code duplication**: May need to duplicate some delegating methods

## Design Patterns

### Adapter Pattern
```javascript
// Use composition to adapt interfaces
class LegacySystem {
  oldMethod(data) {
    return `Legacy: ${data}`;
  }
}

class ModernAdapter {
  constructor(legacySystem) {
    this._legacy = legacySystem;
  }
  
  newMethod(data) {
    return this._legacy.oldMethod(data);
  }
}
```

### Strategy Pattern
```javascript
// Use composition for varying algorithms
class Context {
  constructor(strategy) {
    this._strategy = strategy;
  }
  
  execute() {
    return this._strategy.algorithm();
  }
}
```

### Decorator Pattern
```javascript
// Use composition to add behavior
class BasicService {
  operation() {
    return 'basic';
  }
}

class LoggingDecorator {
  constructor(service) {
    this._service = service;
  }
  
  operation() {
    console.log('Logging operation');
    return this._service.operation();
  }
}
```

## Related Refactorings

- [Replace Inheritance with Delegation](replace-superclass-with-delegate.md) - This refactoring
- [Extract Class](extract-class.md) - Create the delegate class
- [Move Method](move-method.md) - Move methods to appropriate classes
- [Hide Delegate](hide-delegate.md) - Hide the delegation relationship
- [Remove Middle Man](remove-middle-man.md) - Expose delegate when appropriate