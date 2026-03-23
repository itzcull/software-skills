---
title: "Encapsulate Collection"
description: "Replace direct access to a collection with methods that control access and modification"
category: "Encapsulation"
tags: ["encapsulation", "collection", "access-control", "invariants", "data-hiding"]
related: ["encapsulate-variable", "encapsulate-record", "hide-delegate"]
---

# Encapsulate Collection

Replace direct access to a collection with methods that control how the collection is accessed and modified. This prevents unwanted modifications and maintains collection invariants.

## Motivation

Direct access to collections creates several problems:

- **Uncontrolled modification**: Clients can modify collections in unexpected ways
- **Broken invariants**: Direct access can violate business rules
- **Poor encapsulation**: Internal data structure is exposed
- **Hard to track changes**: No way to monitor collection modifications
- **Difficult validation**: Can't validate items being added/removed
- **Coupling issues**: Clients depend on specific collection implementation

## Example

### Basic Example
```javascript
// Before - Direct collection access
class Course {
  constructor(name, level) {
    this._name = name;
    this._level = level;
    this._students = []; // Direct access to array
  }
  
  get name() { return this._name; }
  get level() { return this._level; }
  
  // Dangerous: returns direct reference to internal array
  get students() {
    return this._students;
  }
  
  set students(studentList) {
    this._students = studentList; // No validation
  }
}

// Client code can break the course
const course = new Course('JavaScript Basics', 'beginner');
const students = course.students;

// These operations bypass any business logic
students.push(null); // Invalid student
students.push({ name: 'John' }); // Missing required fields
students.splice(0, students.length); // Removes all students

// Can replace entire collection
course.students = 'invalid'; // Not even an array!

// After - Proper encapsulation
class Course {
  constructor(name, level) {
    this._name = name;
    this._level = level;
    this._students = [];
    this._maxStudents = 30;
  }
  
  get name() { return this._name; }
  get level() { return this._level; }
  get studentCount() { return this._students.length; }
  get maxStudents() { return this._maxStudents; }
  
  // Return defensive copy, not direct reference
  getStudents() {
    return [...this._students];
  }
  
  // Controlled access to individual students
  getStudent(index) {
    if (index < 0 || index >= this._students.length) {
      throw new Error(`Invalid student index: ${index}`);
    }
    return this._students[index];
  }
  
  // Controlled addition with validation
  addStudent(student) {
    this._validateStudent(student);
    
    if (this._students.length >= this._maxStudents) {
      throw new Error('Course is full');
    }
    
    if (this._students.some(s => s.id === student.id)) {
      throw new Error(`Student ${student.id} is already enrolled`);
    }
    
    this._students.push(student);
  }
  
  // Controlled removal
  removeStudent(studentId) {
    const index = this._students.findIndex(s => s.id === studentId);
    
    if (index === -1) {
      throw new Error(`Student ${studentId} not found in course`);
    }
    
    return this._students.splice(index, 1)[0];
  }
  
  // Check if student is enrolled
  hasStudent(studentId) {
    return this._students.some(s => s.id === studentId);
  }
  
  // Safe iteration
  forEachStudent(callback) {
    this._students.forEach(callback);
  }
  
  // Find students with criteria
  findStudents(predicate) {
    return this._students.filter(predicate);
  }
  
  _validateStudent(student) {
    if (!student || typeof student !== 'object') {
      throw new Error('Student must be an object');
    }
    
    if (!student.id || !student.name || !student.email) {
      throw new Error('Student must have id, name, and email');
    }
    
    if (this._level === 'advanced' && !student.hasPrerequisites) {
      throw new Error('Advanced course requires prerequisites');
    }
  }
}

// Usage - safe and controlled
const course = new Course('JavaScript Basics', 'beginner');

// Can only add valid students
course.addStudent({
  id: 'S001',
  name: 'John Doe',
  email: 'john@example.com'
});

// Can't directly modify the collection
const students = course.getStudents(); // Gets a copy
students.push(null); // This doesn't affect the course

// All modifications go through controlled methods
course.removeStudent('S001');
console.log(course.studentCount); // 0
```

## Mechanics

1. **Identify collection exposure**
   - Find fields that return collections directly
   - Look for setters that accept entire collections
   - Check for direct array/object manipulation by clients

2. **Create access methods**
   - Add methods to get individual items
   - Add methods to check if items exist
   - Create iteration methods for safe traversal

3. **Create modification methods**
   - Add methods to add items with validation
   - Add methods to remove items
   - Add methods to update items

4. **Add defensive copying**
   - Return copies of collections, not direct references
   - Return copies of individual items if they're mutable
   - Consider deep copying for complex objects

5. **Implement validation**
   - Validate items being added to the collection
   - Enforce business rules and invariants
   - Check collection size limits and constraints

6. **Remove direct access**
   - Replace getter/setter with appropriate methods
   - Update client code to use new methods
   - Make collection field private

7. **Test thoroughly**
   - Test that clients can't modify internal collections
   - Test all validation rules
   - Verify business logic is enforced

## When to Use

- **Public collections**: Collections exposed through public APIs
- **Business rules**: Collections with business constraints
- **Validation needed**: Items need validation before addition
- **Invariants**: Collection must maintain certain properties
- **Tracking changes**: Need to monitor collection modifications
- **Complex operations**: Collections support complex business operations

## Trade-offs

### Benefits
- **Data integrity**: Prevents invalid modifications
- **Business rule enforcement**: Maintains collection invariants
- **Better encapsulation**: Hides internal implementation details
- **Controlled access**: Can monitor and log changes
- **Validation**: Ensures only valid items are added
- **Flexibility**: Can change internal representation without affecting clients

### Drawbacks
- **More methods**: Increases class interface size
- **Performance overhead**: Defensive copying and validation
- **Complexity**: More code to maintain
- **Learning curve**: Clients need to learn new methods
- **Memory usage**: Defensive copying uses more memory

## Related Refactorings

- [Extract Class](extract-class.md) - Extract collection into its own class
- [Move Method](move-method.md) - Move collection operations to appropriate classes
- [Replace Primitive with Object](replace-primitive-with-object.md) - Replace primitive collections with rich objects