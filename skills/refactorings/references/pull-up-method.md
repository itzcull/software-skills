---
title: "Pull Up Method"
description: "Move a method from subclasses to the superclass when it has identical implementations"
category: "Dealing with Inheritance"
tags: ["pull-up", "method", "inheritance", "duplication", "superclass"]
related: ["push-down-method", "extract-superclass", "pull-up-field"]
---

# Pull Up Method

Move a method from subclasses to the superclass when the method has identical implementations across multiple subclasses.

## Inverse

[Push Down Method](push-down-method.md)

## Motivation

When you find identical methods in multiple subclasses, it's a clear sign that the method belongs in the superclass. Moving shared methods up the hierarchy:

- **Eliminates duplication**: Method implemented once instead of multiple times
- **Simplifies maintenance**: Changes to the method happen in one place
- **Enables polymorphism**: Superclass references can call the method
- **Clarifies design**: Shows that the behavior is a common concept
- **Reduces testing**: Fewer identical methods to test

## Example

### Basic Example
```javascript
// Before - Identical methods in subclasses
class Employee {
  constructor(name, id) {
    this._name = name;
    this._id = id;
  }
}

class Salesman extends Employee {
  constructor(name, id, salesQuota) {
    super(name, id);
    this._salesQuota = salesQuota;
  }
  
  getName() {
    return this._name;
  }
  
  getId() {
    return this._id;
  }
  
  getSalesQuota() {
    return this._salesQuota;
  }
}

class Engineer extends Employee {
  constructor(name, id, specialization) {
    super(name, id);
    this._specialization = specialization;
  }
  
  getName() {
    return this._name;  // Identical to Salesman
  }
  
  getId() {
    return this._id;    // Identical to Salesman
  }
  
  getSpecialization() {
    return this._specialization;
  }
}

// After - Common methods moved to superclass
class Employee {
  constructor(name, id) {
    this._name = name;
    this._id = id;
  }
  
  getName() {
    return this._name;
  }
  
  getId() {
    return this._id;
  }
}

class Salesman extends Employee {
  constructor(name, id, salesQuota) {
    super(name, id);
    this._salesQuota = salesQuota;
  }
  
  getSalesQuota() {
    return this._salesQuota;
  }
}

class Engineer extends Employee {
  constructor(name, id, specialization) {
    super(name, id);
    this._specialization = specialization;
  }
  
  getSpecialization() {
    return this._specialization;
  }
}
```

### Complex Example - Document Types
```javascript
// Before - Repeated validation logic
class Document {
  constructor(title, author) {
    this._title = title;
    this._author = author;
    this._createdAt = new Date();
  }
}

class TextDocument extends Document {
  constructor(title, author, content) {
    super(title, author);
    this._content = content;
  }
  
  validate() {
    const errors = [];
    
    if (!this._title || this._title.trim().length === 0) {
      errors.push('Title is required');
    }
    
    if (!this._author || this._author.trim().length === 0) {
      errors.push('Author is required');
    }
    
    if (this._title && this._title.length > 200) {
      errors.push('Title too long');
    }
    
    return errors;
  }
  
  getMetadata() {
    return {
      title: this._title,
      author: this._author,
      createdAt: this._createdAt,
      type: 'text'
    };
  }
}

class ImageDocument extends Document {
  constructor(title, author, imageUrl) {
    super(title, author);
    this._imageUrl = imageUrl;
  }
  
  validate() {
    const errors = [];
    
    // Identical validation logic
    if (!this._title || this._title.trim().length === 0) {
      errors.push('Title is required');
    }
    
    if (!this._author || this._author.trim().length === 0) {
      errors.push('Author is required');
    }
    
    if (this._title && this._title.length > 200) {
      errors.push('Title too long');
    }
    
    return errors;
  }
  
  getMetadata() {
    return {
      title: this._title,
      author: this._author,
      createdAt: this._createdAt,
      type: 'image'
    };
  }
}

class VideoDocument extends Document {
  constructor(title, author, videoUrl, duration) {
    super(title, author);
    this._videoUrl = videoUrl;
    this._duration = duration;
  }
  
  validate() {
    const errors = [];
    
    // Same validation logic again
    if (!this._title || this._title.trim().length === 0) {
      errors.push('Title is required');
    }
    
    if (!this._author || this._author.trim().length === 0) {
      errors.push('Author is required');
    }
    
    if (this._title && this._title.length > 200) {
      errors.push('Title too long');
    }
    
    return errors;
  }
  
  getMetadata() {
    return {
      title: this._title,
      author: this._author,
      createdAt: this._createdAt,
      type: 'video'
    };
  }
}

// After - Common methods moved to superclass
class Document {
  constructor(title, author) {
    this._title = title;
    this._author = author;
    this._createdAt = new Date();
  }
  
  validate() {
    const errors = [];
    
    if (!this._title || this._title.trim().length === 0) {
      errors.push('Title is required');
    }
    
    if (!this._author || this._author.trim().length === 0) {
      errors.push('Author is required');
    }
    
    if (this._title && this._title.length > 200) {
      errors.push('Title too long');
    }
    
    // Allow subclasses to add their own validation
    const subclassErrors = this._validateSpecific();
    return errors.concat(subclassErrors);
  }
  
  getMetadata() {
    return {
      title: this._title,
      author: this._author,
      createdAt: this._createdAt,
      type: this._getDocumentType()
    };
  }
  
  // Template methods for subclasses to implement
  _validateSpecific() {
    return []; // Default: no additional validation
  }
  
  _getDocumentType() {
    throw new Error('Subclasses must implement _getDocumentType');
  }
}

class TextDocument extends Document {
  constructor(title, author, content) {
    super(title, author);
    this._content = content;
  }
  
  _getDocumentType() {
    return 'text';
  }
  
  _validateSpecific() {
    const errors = [];
    if (!this._content || this._content.trim().length === 0) {
      errors.push('Content is required for text documents');
    }
    return errors;
  }
}

class ImageDocument extends Document {
  constructor(title, author, imageUrl) {
    super(title, author);
    this._imageUrl = imageUrl;
  }
  
  _getDocumentType() {
    return 'image';
  }
  
  _validateSpecific() {
    const errors = [];
    if (!this._imageUrl) {
      errors.push('Image URL is required');
    }
    return errors;
  }
}

class VideoDocument extends Document {
  constructor(title, author, videoUrl, duration) {
    super(title, author);
    this._videoUrl = videoUrl;
    this._duration = duration;
  }
  
  _getDocumentType() {
    return 'video';
  }
  
  _validateSpecific() {
    const errors = [];
    if (!this._videoUrl) {
      errors.push('Video URL is required');
    }
    if (!this._duration || this._duration <= 0) {
      errors.push('Valid duration is required');
    }
    return errors;
  }
}
```

### Service Layer Example
```javascript
// Before - Repeated error handling and logging
class UserService {
  async getUser(id) {
    try {
      console.log(`Fetching user ${id}`);
      const user = await this._repository.findById(id);
      console.log(`User ${id} fetched successfully`);
      return user;
    } catch (error) {
      console.error(`Error fetching user ${id}:`, error.message);
      throw new ServiceError(`Failed to fetch user: ${error.message}`);
    }
  }
  
  async createUser(userData) {
    try {
      console.log(`Creating user: ${userData.email}`);
      const user = await this._repository.create(userData);
      console.log(`User created successfully: ${user.id}`);
      return user;
    } catch (error) {
      console.error(`Error creating user:`, error.message);
      throw new ServiceError(`Failed to create user: ${error.message}`);
    }
  }
}

class ProductService {
  async getProduct(id) {
    try {
      console.log(`Fetching product ${id}`);
      const product = await this._repository.findById(id);
      console.log(`Product ${id} fetched successfully`);
      return product;
    } catch (error) {
      console.error(`Error fetching product ${id}:`, error.message);
      throw new ServiceError(`Failed to fetch product: ${error.message}`);
    }
  }
  
  async createProduct(productData) {
    try {
      console.log(`Creating product: ${productData.name}`);
      const product = await this._repository.create(productData);
      console.log(`Product created successfully: ${product.id}`);
      return product;
    } catch (error) {
      console.error(`Error creating product:`, error.message);
      throw new ServiceError(`Failed to create product: ${error.message}`);
    }
  }
}

// After - Common error handling moved to base class
class BaseService {
  constructor(repository) {
    this._repository = repository;
  }
  
  async executeWithLogging(operation, operationName, identifier) {
    try {
      console.log(`${operationName}: ${identifier}`);
      const result = await operation();
      console.log(`${operationName} completed successfully: ${identifier}`);
      return result;
    } catch (error) {
      console.error(`Error in ${operationName}:`, error.message);
      throw new ServiceError(`Failed to ${operationName.toLowerCase()}: ${error.message}`);
    }
  }
  
  async findById(id) {
    return this.executeWithLogging(
      () => this._repository.findById(id),
      'Fetching entity',
      id
    );
  }
  
  async create(data) {
    const identifier = data.email || data.name || 'new entity';
    return this.executeWithLogging(
      () => this._repository.create(data),
      'Creating entity',
      identifier
    );
  }
}

class UserService extends BaseService {
  constructor(userRepository) {
    super(userRepository);
  }
  
  async getUser(id) {
    return this.findById(id);
  }
  
  async createUser(userData) {
    return this.create(userData);
  }
}

class ProductService extends BaseService {
  constructor(productRepository) {
    super(productRepository);
  }
  
  async getProduct(id) {
    return this.findById(id);
  }
  
  async createProduct(productData) {
    return this.create(productData);
  }
}
```

## Mechanics

1. **Ensure methods are truly identical**
   - Compare method implementations line by line
   - Check that they use the same fields and call the same methods
   - Verify they have the same signature

2. **Check that methods access only superclass features**
   - Ensure the method only uses fields/methods available in superclass
   - If method uses subclass-specific features, consider Template Method pattern

3. **Copy the method to superclass**
   - Move one of the identical methods to the superclass
   - Ensure proper access modifiers (protected if needed by subclasses)

4. **Remove methods from subclasses**
   - Delete the method from all subclasses
   - Test that subclass functionality is preserved

5. **Run tests**
   - Verify that all subclass instances still work correctly
   - Check that polymorphism works as expected

## When to Use

- **Identical implementations**: Multiple subclasses have exactly the same method
- **Common behavior**: Method represents behavior shared by all subclasses  
- **Code duplication**: Same logic repeated across inheritance hierarchy
- **Polymorphic calls**: Want to call method on superclass reference
- **Template Method opportunity**: Method could be broken into common and variant parts

## Trade-offs

### Benefits
- **Eliminates duplication**: Method exists in only one place
- **Enables polymorphism**: Can call method on superclass references
- **Simplifies maintenance**: Changes happen in one location
- **Clarifies design**: Shows that behavior is common to all subclasses
- **Reduces testing**: Only one implementation to test

### Drawbacks
- **Reduces flexibility**: All subclasses must have the same behavior
- **Coupling**: Subclasses become more dependent on superclass
- **Inappropriate generalization**: May force behavior on subclasses that don't need it
- **Breaking changes**: Harder to modify behavior for individual subclasses

## Variations and Patterns

### Template Method Pattern
```javascript
// When methods are similar but not identical
class DataProcessor {
  process(data) {
    const validated = this.validate(data);
    const processed = this.processData(validated);
    return this.formatOutput(processed);
  }
  
  validate(data) {
    // Common validation logic
    if (!data) throw new Error('Data required');
    return this.validateSpecific(data);
  }
  
  // Template methods for subclasses
  validateSpecific(data) { return data; }
  processData(data) { throw new Error('Must implement'); }
  formatOutput(data) { return data; }
}

class CSVProcessor extends DataProcessor {
  validateSpecific(data) {
    if (typeof data !== 'string') throw new Error('CSV data must be string');
    return data;
  }
  
  processData(data) {
    return data.split('\\n').map(row => row.split(','));
  }
}
```

### Strategy Pattern Alternative
```javascript
// When behavior varies significantly, consider strategy pattern instead
class DocumentProcessor {
  constructor(strategy) {
    this._strategy = strategy;
  }
  
  process(document) {
    return this._strategy.process(document);
  }
}

class TextProcessingStrategy {
  process(document) {
    // Text-specific processing
  }
}

class ImageProcessingStrategy {
  process(document) {
    // Image-specific processing
  }
}
```

### Abstract Base Class Pattern
```javascript
// When pulled-up method should be abstract
class Shape {
  calculateArea() {
    throw new Error('Subclasses must implement calculateArea');
  }
  
  // Common method pulled up from subclasses
  getDescription() {
    return `A ${this.constructor.name} with area ${this.calculateArea()}`;
  }
}

class Rectangle extends Shape {
  constructor(width, height) {
    super();
    this._width = width;
    this._height = height;
  }
  
  calculateArea() {
    return this._width * this._height;
  }
}
```

## Common Mistakes

### Moving Non-Identical Methods
```javascript
// Bad - methods look similar but aren't identical
class Employee {
  // Don't pull this up if implementations differ
  calculatePay() {
    // This might work differently for each subclass
  }
}
```

### Breaking Encapsulation
```javascript
// Bad - method uses private subclass features
class Subclass extends Base {
  someMethod() {
    return this._privateField; // Can't access in superclass
  }
}

// Better - ensure method only uses superclass features
class Base {
  someMethod() {
    return this.getProtectedValue(); // Use protected interface
  }
}
```

### Forced Inheritance
```javascript
// Bad - forcing method on unrelated subclasses
class Vehicle {
  fly() { 
    // Not all vehicles can fly!
  }
}

class Car extends Vehicle {
  fly() {
    throw new Error('Cars cannot fly');
  }
}
```

## Related Refactorings

- [Push Down Method](push-down-method.md) - The inverse operation
- [Pull Up Field](pull-up-field.md) - Often done together
- [Extract Superclass](extract-superclass.md) - May create the target superclass
- [Form Template Method](extract-superclass.md) - For similar but not identical methods
- [Replace Inheritance with Delegation](replace-superclass-with-delegate.md) - Alternative approach