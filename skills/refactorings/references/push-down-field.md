---
title: "Push Down Field"
description: "Move a field from superclass to specific subclasses when only relevant to some subclasses"
category: "Dealing with Inheritance"
tags: ["push-down", "field", "inheritance", "specialization", "subclass"]
related: ["pull-up-field", "push-down-method", "extract-subclass"]
---

# Push Down Field

Move a field from a superclass to specific subclasses when the field is only relevant to some subclasses, not all of them.

## Inverse

[Pull Up Field](pull-up-field.md)

## Motivation

Sometimes a field in a superclass is only used by some subclasses. This suggests that the field doesn't belong at the superclass level and should be moved to where it's actually needed. Moving fields down:

- **Improves cohesion**: Fields are where they're actually used
- **Reduces coupling**: Subclasses that don't need the field aren't burdened with it
- **Clarifies design**: Makes it clear which subclasses have which responsibilities
- **Prevents misuse**: Eliminates the possibility of inappropriate field access
- **Simplifies superclass**: Removes unnecessary complexity from the base class

## Example

### Basic Example
```javascript
// Before - Field in superclass but only used by some subclasses
class Employee {
  constructor(name, id) {
    this._name = name;
    this._id = id;
    this._quota = 0; // Only relevant for sales employees
  }
  
  get name() { return this._name; }
  get id() { return this._id; }
  get quota() { return this._quota; }
  set quota(value) { this._quota = value; }
}

class Engineer extends Employee {
  constructor(name, id, specialization) {
    super(name, id);
    this._specialization = specialization;
    // Engineers don't need quota, but inherit it anyway
  }
  
  get specialization() { return this._specialization; }
}

class Salesman extends Employee {
  constructor(name, id, territory) {
    super(name, id);
    this._territory = territory;
    // Salesmen actually use the quota field
  }
  
  get territory() { return this._territory; }
  
  updateQuota(newQuota) {
    this.quota = newQuota;
  }
}

class Manager extends Employee {
  constructor(name, id, department) {
    super(name, id);
    this._department = department;
    // Managers don't need quota either
  }
  
  get department() { return this._department; }
}

// After - Quota field moved to Salesman class
class Employee {
  constructor(name, id) {
    this._name = name;
    this._id = id;
  }
  
  get name() { return this._name; }
  get id() { return this._id; }
}

class Engineer extends Employee {
  constructor(name, id, specialization) {
    super(name, id);
    this._specialization = specialization;
  }
  
  get specialization() { return this._specialization; }
}

class Salesman extends Employee {
  constructor(name, id, territory, quota = 0) {
    super(name, id);
    this._territory = territory;
    this._quota = quota;
  }
  
  get territory() { return this._territory; }
  get quota() { return this._quota; }
  set quota(value) { this._quota = value; }
  
  updateQuota(newQuota) {
    this.quota = newQuota;
  }
}

class Manager extends Employee {
  constructor(name, id, department) {
    super(name, id);
    this._department = department;
  }
  
  get department() { return this._department; }
}
```

### Complex Example - Document Management
```javascript
// Before - Media-specific fields in base Document class
class Document {
  constructor(title, author) {
    this._title = title;
    this._author = author;
    this._createdAt = new Date();
    
    // Fields only relevant to specific document types
    this._resolution = null;    // Only for images/videos
    this._duration = null;      // Only for videos/audio
    this._pageCount = null;     // Only for text documents
    this._wordCount = null;     // Only for text documents
    this._bitrate = null;       // Only for audio/video
  }
  
  get title() { return this._title; }
  get author() { return this._author; }
  get createdAt() { return this._createdAt; }
  
  // Getters for fields that many subclasses don't need
  get resolution() { return this._resolution; }
  get duration() { return this._duration; }
  get pageCount() { return this._pageCount; }
  get wordCount() { return this._wordCount; }
  get bitrate() { return this._bitrate; }
}

class TextDocument extends Document {
  constructor(title, author, content) {
    super(title, author);
    this._content = content;
    // Text documents use pageCount and wordCount
    this._pageCount = this._calculatePageCount(content);
    this._wordCount = this._calculateWordCount(content);
  }
  
  _calculatePageCount(content) {
    return Math.ceil(content.length / 2000); // Rough estimate
  }
  
  _calculateWordCount(content) {
    return content.split(/\\s+/).length;
  }
}

class ImageDocument extends Document {
  constructor(title, author, imageData) {
    super(title, author);
    this._imageData = imageData;
    // Image documents use resolution
    this._resolution = imageData.resolution;
  }
}

class VideoDocument extends Document {
  constructor(title, author, videoData) {
    super(title, author);
    this._videoData = videoData;
    // Video documents use resolution, duration, and bitrate
    this._resolution = videoData.resolution;
    this._duration = videoData.duration;
    this._bitrate = videoData.bitrate;
  }
}

// After - Fields moved to relevant subclasses
class Document {
  constructor(title, author) {
    this._title = title;
    this._author = author;
    this._createdAt = new Date();
  }
  
  get title() { return this._title; }
  get author() { return this._author; }
  get createdAt() { return this._createdAt; }
}

class TextDocument extends Document {
  constructor(title, author, content) {
    super(title, author);
    this._content = content;
    this._pageCount = this._calculatePageCount(content);
    this._wordCount = this._calculateWordCount(content);
  }
  
  get content() { return this._content; }
  get pageCount() { return this._pageCount; }
  get wordCount() { return this._wordCount; }
  
  _calculatePageCount(content) {
    return Math.ceil(content.length / 2000);
  }
  
  _calculateWordCount(content) {
    return content.split(/\\s+/).length;
  }
  
  updateContent(newContent) {
    this._content = newContent;
    this._pageCount = this._calculatePageCount(newContent);
    this._wordCount = this._calculateWordCount(newContent);
  }
}

class MediaDocument extends Document {
  constructor(title, author, resolution) {
    super(title, author);
    this._resolution = resolution;
  }
  
  get resolution() { return this._resolution; }
}

class ImageDocument extends MediaDocument {
  constructor(title, author, imageData) {
    super(title, author, imageData.resolution);
    this._imageData = imageData;
    this._format = imageData.format;
    this._colorDepth = imageData.colorDepth;
  }
  
  get imageData() { return this._imageData; }
  get format() { return this._format; }
  get colorDepth() { return this._colorDepth; }
}

class VideoDocument extends MediaDocument {
  constructor(title, author, videoData) {
    super(title, author, videoData.resolution);
    this._videoData = videoData;
    this._duration = videoData.duration;
    this._bitrate = videoData.bitrate;
    this._frameRate = videoData.frameRate;
  }
  
  get videoData() { return this._videoData; }
  get duration() { return this._duration; }
  get bitrate() { return this._bitrate; }
  get frameRate() { return this._frameRate; }
}
```

### E-commerce Example
```javascript
// Before - Product fields that only apply to some product types
class Product {
  constructor(name, price, sku) {
    this._name = name;
    this._price = price;
    this._sku = sku;
    
    // Fields that only apply to specific product types
    this._size = null;          // Only for clothing, shoes
    this._color = null;         // Only for clothing, accessories
    this._weight = null;        // Only for physical products
    this._dimensions = null;    // Only for physical products
    this._downloadUrl = null;   // Only for digital products
    this._licenseKey = null;    // Only for software
    this._expirationDate = null; // Only for perishables
    this._isbn = null;          // Only for books
  }
  
  // Many getters for fields that most subclasses don't use
  get size() { return this._size; }
  get color() { return this._color; }
  get weight() { return this._weight; }
  get dimensions() { return this._dimensions; }
  get downloadUrl() { return this._downloadUrl; }
  get licenseKey() { return this._licenseKey; }
  get expirationDate() { return this._expirationDate; }
  get isbn() { return this._isbn; }
}

class ClothingProduct extends Product {
  constructor(name, price, sku, size, color, material) {
    super(name, price, sku);
    this._size = size;
    this._color = color;
    this._material = material;
  }
}

class DigitalProduct extends Product {
  constructor(name, price, sku, downloadUrl, fileSize) {
    super(name, price, sku);
    this._downloadUrl = downloadUrl;
    this._fileSize = fileSize;
  }
}

class BookProduct extends Product {
  constructor(name, price, sku, isbn, author, pageCount) {
    super(name, price, sku);
    this._isbn = isbn;
    this._author = author;
    this._pageCount = pageCount;
  }
}

// After - Fields moved to relevant subclasses
class Product {
  constructor(name, price, sku) {
    this._name = name;
    this._price = price;
    this._sku = sku;
  }
  
  get name() { return this._name; }
  get price() { return this._price; }
  get sku() { return this._sku; }
}

class PhysicalProduct extends Product {
  constructor(name, price, sku, weight, dimensions) {
    super(name, price, sku);
    this._weight = weight;
    this._dimensions = dimensions;
  }
  
  get weight() { return this._weight; }
  get dimensions() { return this._dimensions; }
  
  calculateShippingCost(destination) {
    // Use weight and dimensions for shipping calculation
    return this._weight * 0.5 + (this._dimensions.volume * 0.001);
  }
}

class ClothingProduct extends PhysicalProduct {
  constructor(name, price, sku, weight, dimensions, size, color, material) {
    super(name, price, sku, weight, dimensions);
    this._size = size;
    this._color = color;
    this._material = material;
  }
  
  get size() { return this._size; }
  get color() { return this._color; }
  get material() { return this._material; }
  
  isAvailableInSize(size) {
    return this._availableSizes.includes(size);
  }
}

class DigitalProduct extends Product {
  constructor(name, price, sku, downloadUrl, fileSize) {
    super(name, price, sku);
    this._downloadUrl = downloadUrl;
    this._fileSize = fileSize;
  }
  
  get downloadUrl() { return this._downloadUrl; }
  get fileSize() { return this._fileSize; }
  
  generateDownloadLink(customerId) {
    return `${this._downloadUrl}?customer=${customerId}&token=${this._generateToken()}`;
  }
  
  _generateToken() {
    return Math.random().toString(36).substr(2, 9);
  }
}

class SoftwareProduct extends DigitalProduct {
  constructor(name, price, sku, downloadUrl, fileSize, licenseType) {
    super(name, price, sku, downloadUrl, fileSize);
    this._licenseType = licenseType;
    this._licenseKeys = [];
  }
  
  get licenseType() { return this._licenseType; }
  
  generateLicenseKey() {
    const key = this._createLicenseKey();
    this._licenseKeys.push(key);
    return key;
  }
  
  _createLicenseKey() {
    return `SW-${Date.now()}-${Math.random().toString(36).substr(2, 8).toUpperCase()}`;
  }
}

class BookProduct extends PhysicalProduct {
  constructor(name, price, sku, weight, dimensions, isbn, author, pageCount) {
    super(name, price, sku, weight, dimensions);
    this._isbn = isbn;
    this._author = author;
    this._pageCount = pageCount;
  }
  
  get isbn() { return this._isbn; }
  get author() { return this._author; }
  get pageCount() { return this._pageCount; }
  
  validateIsbn() {
    // ISBN validation logic
    return /^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)/.test(this._isbn);
  }
}
```

## Mechanics

1. **Identify fields used by only some subclasses**
   - Look for fields that remain null/undefined in some subclasses
   - Find fields that only make sense for specific subclass types
   - Check for conditional logic based on subclass type

2. **Create the field in relevant subclasses**
   - Add the field to each subclass that actually uses it
   - Include appropriate initialization in constructors
   - Add any necessary accessor methods

3. **Move field-related behavior**
   - Move methods that work with the field to the same subclasses
   - Update any validation or business logic

4. **Remove field from superclass**
   - Delete the field declaration
   - Remove any accessor methods from superclass
   - Update constructor to not initialize the field

5. **Update client code**
   - Change code that accesses the field to work with specific subclasses
   - Add type checking where necessary

6. **Test thoroughly**
   - Verify that each subclass works correctly
   - Ensure no broken references to the moved field

## When to Use

- **Unused fields**: Field is null/empty in some subclasses
- **Type-specific data**: Field only makes sense for certain subclass types
- **Conditional logic**: Code checks subclass type before using field
- **Cohesion improvement**: Field logically belongs with subclass-specific behavior
- **Interface segregation**: Want clean interfaces for each subclass type

## Trade-offs

### Benefits
- **Better cohesion**: Fields are where they're actually used
- **Cleaner interfaces**: Subclasses only expose relevant fields
- **Reduced coupling**: Unrelated subclasses don't depend on irrelevant fields
- **Prevents misuse**: Can't accidentally access inappropriate fields
- **Clearer design**: Makes subclass responsibilities explicit

### Drawbacks
- **Code duplication**: If multiple subclasses need the same field
- **Loss of polymorphism**: Can't access field through superclass reference
- **Client complexity**: Client code may need to handle different subclass types
- **Breaking changes**: Existing code accessing field through superclass breaks

## Design Patterns and Alternatives

### Intermediate Inheritance Levels
```javascript
// Create intermediate classes for shared fields
class Animal {
  constructor(name) {
    this._name = name;
  }
}

class Mammal extends Animal {
  constructor(name, furColor) {
    super(name);
    this._furColor = furColor; // Shared by mammal subclasses
  }
}

class Bird extends Animal {
  constructor(name, wingspan) {
    super(name);
    this._wingspan = wingspan; // Shared by bird subclasses
  }
}

class Dog extends Mammal {
  constructor(name, furColor, breed) {
    super(name, furColor);
    this._breed = breed;
  }
}

class Eagle extends Bird {
  constructor(name, wingspan, territory) {
    super(name, wingspan);
    this._territory = territory;
  }
}
```

### Composition Over Inheritance
```javascript
// Alternative: Use composition instead of inheritance
class Product {
  constructor(name, price, sku, attributes = {}) {
    this._name = name;
    this._price = price;
    this._sku = sku;
    this._attributes = attributes;
  }
  
  getAttribute(key) {
    return this._attributes[key];
  }
  
  hasAttribute(key) {
    return key in this._attributes;
  }
}

// Usage
const shirt = new Product('T-Shirt', 19.99, 'TSH001', {
  size: 'M',
  color: 'blue',
  material: 'cotton'
});

const ebook = new Product('JavaScript Guide', 29.99, 'EBK001', {
  downloadUrl: 'https://example.com/download',
  fileSize: '5MB',
  format: 'PDF'
});
```

### Strategy Pattern
```javascript
// Use strategy pattern for type-specific behavior
class Product {
  constructor(name, price, sku, typeStrategy) {
    this._name = name;
    this._price = price;
    this._sku = sku;
    this._typeStrategy = typeStrategy;
  }
  
  getSpecificProperties() {
    return this._typeStrategy.getProperties();
  }
  
  calculateShipping(destination) {
    return this._typeStrategy.calculateShipping(destination);
  }
}

class PhysicalProductStrategy {
  constructor(weight, dimensions) {
    this._weight = weight;
    this._dimensions = dimensions;
  }
  
  getProperties() {
    return { weight: this._weight, dimensions: this._dimensions };
  }
  
  calculateShipping(destination) {
    return this._weight * 0.5;
  }
}

class DigitalProductStrategy {
  constructor(downloadUrl, fileSize) {
    this._downloadUrl = downloadUrl;
    this._fileSize = fileSize;
  }
  
  getProperties() {
    return { downloadUrl: this._downloadUrl, fileSize: this._fileSize };
  }
  
  calculateShipping(destination) {
    return 0; // No shipping for digital products
  }
}
```

## Related Refactorings

- [Pull Up Field](pull-up-field.md) - The inverse operation
- [Push Down Method](push-down-method.md) - Often done together
- [Extract Subclass](extract-class.md) - May create new subclasses for the field
- [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md) - Alternative approach
- [Replace Inheritance with Delegation](replace-superclass-with-delegate.md) - Alternative to inheritance