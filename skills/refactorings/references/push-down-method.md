---
title: "Push Down Method"
description: "Move a method from superclass to specific subclasses when only relevant to certain subclasses"
category: "Dealing with Inheritance"
tags: ["push-down", "method", "inheritance", "specialization", "subclass"]
related: ["pull-up-method", "push-down-field", "extract-subclass"]
---

# Push Down Method

Move a method from a superclass to specific subclasses when the method is only relevant to those particular subclasses.

## Inverse

[Pull Up Method](pull-up-method.md)

## Motivation

Sometimes a method in a superclass is only used by some subclasses. This indicates that the method doesn't represent behavior common to all subclasses and should be moved to where it's actually needed. Moving methods down:

- **Improves cohesion**: Methods are where they're actually used
- **Clarifies design**: Makes subclass responsibilities explicit
- **Reduces coupling**: Subclasses that don't need the method aren't burdened with it
- **Prevents misuse**: Eliminates inappropriate method calls
- **Simplifies superclass**: Removes unnecessary complexity from the base class

## Example

### Basic Example
```javascript
// Before - Method in superclass but only used by some subclasses
class Employee {
  constructor(name, id) {
    this._name = name;
    this._id = id;
  }
  
  get name() { return this._name; }
  get id() { return this._id; }
  
  // Only relevant for sales employees
  getQuota() {
    return this._quota || 0;
  }
  
  setQuota(quota) {
    this._quota = quota;
  }
}

class Engineer extends Employee {
  constructor(name, id, specialization) {
    super(name, id);
    this._specialization = specialization;
  }
  
  get specialization() { return this._specialization; }
  // Engineers inherit quota methods but don't use them
}

class Salesman extends Employee {
  constructor(name, id, territory) {
    super(name, id);
    this._territory = territory;
  }
  
  get territory() { return this._territory; }
  
  // Salesmen actually use the quota methods
  updateQuotaProgress(sales) {
    const quota = this.getQuota();
    const progress = (sales / quota) * 100;
    console.log(`Quota progress: ${progress}%`);
  }
}

class Manager extends Employee {
  constructor(name, id, department) {
    super(name, id);
    this._department = department;
  }
  
  get department() { return this._department; }
  // Managers inherit quota methods but don't use them
}

// After - Quota methods moved to Salesman class
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
  constructor(name, id, territory) {
    super(name, id);
    this._territory = territory;
    this._quota = 0;
  }
  
  get territory() { return this._territory; }
  
  getQuota() {
    return this._quota;
  }
  
  setQuota(quota) {
    this._quota = quota;
  }
  
  updateQuotaProgress(sales) {
    const progress = (sales / this._quota) * 100;
    console.log(`Quota progress: ${progress}%`);
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

### Complex Example - Document Processing
```javascript
// Before - Media-specific methods in base Document class
class Document {
  constructor(title, author) {
    this._title = title;
    this._author = author;
    this._createdAt = new Date();
  }
  
  get title() { return this._title; }
  get author() { return this._author; }
  get createdAt() { return this._createdAt; }
  
  // Methods that only apply to specific document types
  getWordCount() {
    // Only makes sense for text documents
    if (this._content) {
      return this._content.split(/\\s+/).length;
    }
    return 0;
  }
  
  getResolution() {
    // Only makes sense for images/videos
    return this._resolution || 'Unknown';
  }
  
  getDuration() {
    // Only makes sense for audio/video
    return this._duration || 0;
  }
  
  generateThumbnail() {
    // Only makes sense for images/videos
    if (this._thumbnailData) {
      return this._thumbnailData;
    }
    return null;
  }
  
  extractText() {
    // Could apply to multiple types but implementation varies
    if (this._content) {
      return this._content;
    }
    return '';
  }
}

class TextDocument extends Document {
  constructor(title, author, content) {
    super(title, author);
    this._content = content;
  }
  
  get content() { return this._content; }
  
  // Uses getWordCount() from superclass
  analyze() {
    return {
      wordCount: this.getWordCount(),
      text: this.extractText()
    };
  }
}

class ImageDocument extends Document {
  constructor(title, author, imageData) {
    super(title, author);
    this._imageData = imageData;
    this._resolution = imageData.resolution;
    this._thumbnailData = imageData.thumbnail;
  }
  
  // Uses getResolution() and generateThumbnail() from superclass
  getImageInfo() {
    return {
      resolution: this.getResolution(),
      thumbnail: this.generateThumbnail()
    };
  }
}

class VideoDocument extends Document {
  constructor(title, author, videoData) {
    super(title, author);
    this._videoData = videoData;
    this._resolution = videoData.resolution;
    this._duration = videoData.duration;
    this._thumbnailData = videoData.thumbnail;
  }
  
  // Uses multiple superclass methods
  getVideoInfo() {
    return {
      resolution: this.getResolution(),
      duration: this.getDuration(),
      thumbnail: this.generateThumbnail()
    };
  }
}

// After - Methods moved to relevant subclasses
class Document {
  constructor(title, author) {
    this._title = title;
    this._author = author;
    this._createdAt = new Date();
  }
  
  get title() { return this._title; }
  get author() { return this._author; }
  get createdAt() { return this._createdAt; }
  
  // Only common behavior remains
  getMetadata() {
    return {
      title: this._title,
      author: this._author,
      createdAt: this._createdAt,
      type: this.getDocumentType()
    };
  }
  
  // Template method for subclasses to implement
  getDocumentType() {
    throw new Error('Subclasses must implement getDocumentType');
  }
}

class TextDocument extends Document {
  constructor(title, author, content) {
    super(title, author);
    this._content = content;
  }
  
  get content() { return this._content; }
  
  getDocumentType() {
    return 'text';
  }
  
  // Text-specific methods moved here
  getWordCount() {
    return this._content.split(/\\s+/).length;
  }
  
  getCharacterCount() {
    return this._content.length;
  }
  
  extractText() {
    return this._content;
  }
  
  searchText(term) {
    const regex = new RegExp(term, 'gi');
    return this._content.match(regex) || [];
  }
  
  analyze() {
    return {
      wordCount: this.getWordCount(),
      characterCount: this.getCharacterCount(),
      text: this.extractText()
    };
  }
}

class MediaDocument extends Document {
  constructor(title, author, resolution) {
    super(title, author);
    this._resolution = resolution;
  }
  
  getResolution() {
    return this._resolution;
  }
  
  generateThumbnail() {
    // Base implementation for media documents
    throw new Error('Subclasses must implement generateThumbnail');
  }
}

class ImageDocument extends MediaDocument {
  constructor(title, author, imageData) {
    super(title, author, imageData.resolution);
    this._imageData = imageData;
    this._format = imageData.format;
  }
  
  getDocumentType() {
    return 'image';
  }
  
  get format() { return this._format; }
  
  generateThumbnail() {
    // Image-specific thumbnail generation
    return this._imageData.generateThumbnail(150, 150);
  }
  
  getImageInfo() {
    return {
      resolution: this.getResolution(),
      format: this._format,
      thumbnail: this.generateThumbnail()
    };
  }
  
  resize(width, height) {
    return this._imageData.resize(width, height);
  }
}

class VideoDocument extends MediaDocument {
  constructor(title, author, videoData) {
    super(title, author, videoData.resolution);
    this._videoData = videoData;
    this._duration = videoData.duration;
    this._frameRate = videoData.frameRate;
  }
  
  getDocumentType() {
    return 'video';
  }
  
  get duration() { return this._duration; }
  get frameRate() { return this._frameRate; }
  
  getDuration() {
    return this._duration;
  }
  
  generateThumbnail() {
    // Video-specific thumbnail generation (frame at 10% of duration)
    const timeOffset = this._duration * 0.1;
    return this._videoData.extractFrame(timeOffset);
  }
  
  getVideoInfo() {
    return {
      resolution: this.getResolution(),
      duration: this.getDuration(),
      frameRate: this._frameRate,
      thumbnail: this.generateThumbnail()
    };
  }
  
  extractFrameAt(timeOffset) {
    return this._videoData.extractFrame(timeOffset);
  }
}
```

### API Controller Example
```javascript
// Before - Admin-specific methods in base controller
class UserController {
  constructor(userService) {
    this._userService = userService;
  }
  
  async getUser(req, res) {
    const user = await this._userService.findById(req.params.id);
    res.json(user);
  }
  
  async createUser(req, res) {
    const user = await this._userService.create(req.body);
    res.status(201).json(user);
  }
  
  // Admin-only methods in base class
  async getAllUsersWithDetails(req, res) {
    const users = await this._userService.findAllWithDetails();
    res.json(users);
  }
  
  async getUserAuditLog(req, res) {
    const log = await this._userService.getAuditLog(req.params.id);
    res.json(log);
  }
  
  async suspendUser(req, res) {
    await this._userService.suspend(req.params.id, req.body.reason);
    res.status(204).send();
  }
  
  async deleteUser(req, res) {
    await this._userService.delete(req.params.id);
    res.status(204).send();
  }
}

class PublicUserController extends UserController {
  // Public users inherit admin methods but can't use them
  constructor(userService) {
    super(userService);
  }
  
  // Overrides to prevent access
  async getAllUsersWithDetails(req, res) {
    res.status(403).json({ error: 'Forbidden' });
  }
  
  async getUserAuditLog(req, res) {
    res.status(403).json({ error: 'Forbidden' });
  }
  
  async suspendUser(req, res) {
    res.status(403).json({ error: 'Forbidden' });
  }
  
  async deleteUser(req, res) {
    res.status(403).json({ error: 'Forbidden' });
  }
}

class AdminUserController extends UserController {
  // Admin controller actually uses the admin methods
  constructor(userService) {
    super(userService);
  }
}

// After - Admin methods moved to AdminUserController
class UserController {
  constructor(userService) {
    this._userService = userService;
  }
  
  async getUser(req, res) {
    const user = await this._userService.findById(req.params.id);
    res.json(user);
  }
  
  async createUser(req, res) {
    const user = await this._userService.create(req.body);
    res.status(201).json(user);
  }
  
  async updateUser(req, res) {
    const user = await this._userService.update(req.params.id, req.body);
    res.json(user);
  }
}

class PublicUserController extends UserController {
  constructor(userService) {
    super(userService);
  }
  
  // Public-specific methods
  async register(req, res) {
    const user = await this._userService.register(req.body);
    res.status(201).json(user);
  }
  
  async login(req, res) {
    const token = await this._userService.authenticate(req.body);
    res.json({ token });
  }
}

class AdminUserController extends UserController {
  constructor(userService, auditService) {
    super(userService);
    this._auditService = auditService;
  }
  
  // Admin-specific methods moved here
  async getAllUsersWithDetails(req, res) {
    const users = await this._userService.findAllWithDetails();
    res.json(users);
  }
  
  async getUserAuditLog(req, res) {
    const log = await this._auditService.getUserLog(req.params.id);
    res.json(log);
  }
  
  async suspendUser(req, res) {
    await this._userService.suspend(req.params.id, req.body.reason);
    await this._auditService.logAction('suspend', req.params.id, req.user.id);
    res.status(204).send();
  }
  
  async deleteUser(req, res) {
    await this._userService.delete(req.params.id);
    await this._auditService.logAction('delete', req.params.id, req.user.id);
    res.status(204).send();
  }
  
  async getSystemStats(req, res) {
    const stats = await this._userService.getSystemStatistics();
    res.json(stats);
  }
}
```

## Mechanics

1. **Identify methods only used by some subclasses**
   - Look for methods that throw "not supported" exceptions in some subclasses
   - Find methods with conditional logic based on subclass type
   - Check for methods that only make sense for certain subclass types

2. **Copy the method to relevant subclasses**
   - Add the method to each subclass that actually uses it
   - Ensure the method has access to necessary data

3. **Adapt the method for each subclass**
   - Customize the implementation if needed
   - Use subclass-specific fields and methods

4. **Remove the method from superclass**
   - Delete the method from the base class
   - Remove any abstract method declarations

5. **Update client code**
   - Change code to work with specific subclass types
   - Add type checking where necessary
   - Update method calls to use appropriate subclass

6. **Test thoroughly**
   - Verify each subclass works correctly
   - Ensure client code handles the new structure

## When to Use

- **Unused methods**: Method is not used by all subclasses
- **Type-specific behavior**: Method only makes sense for certain subclass types
- **Conditional implementations**: Method throws exceptions or returns defaults in some subclasses
- **Interface segregation**: Want clean interfaces for each subclass type
- **Cohesion improvement**: Method logically belongs with subclass-specific behavior

## Trade-offs

### Benefits
- **Better cohesion**: Methods are where they're actually used
- **Cleaner interfaces**: Subclasses only expose relevant methods
- **Prevents misuse**: Can't accidentally call inappropriate methods
- **Clearer design**: Makes subclass responsibilities explicit
- **Interface segregation**: Each subclass has appropriate interface

### Drawbacks
- **Code duplication**: If multiple subclasses need similar methods
- **Loss of polymorphism**: Can't call method through superclass reference
- **Client complexity**: Client code may need to handle different subclass types
- **Breaking changes**: Existing code calling method through superclass breaks

## Design Patterns and Alternatives

### Template Method Pattern
```javascript
// When methods have common structure but different implementations
class DataProcessor {
  process(data) {
    const validated = this.validate(data);
    const processed = this.processSpecific(validated);
    return this.formatOutput(processed);
  }
  
  validate(data) {
    // Common validation
    if (!data) throw new Error('Data required');
    return data;
  }
  
  formatOutput(data) {
    // Common formatting
    return { result: data, timestamp: new Date() };
  }
  
  // Push this down to subclasses
  processSpecific(data) {
    throw new Error('Subclasses must implement processSpecific');
  }
}

class CSVProcessor extends DataProcessor {
  processSpecific(data) {
    return data.split('\\n').map(row => row.split(','));
  }
}

class JSONProcessor extends DataProcessor {
  processSpecific(data) {
    return JSON.parse(data);
  }
}
```

### Strategy Pattern Alternative
```javascript
// Use strategy pattern instead of inheritance
class Document {
  constructor(title, author, processingStrategy) {
    this._title = title;
    this._author = author;
    this._strategy = processingStrategy;
  }
  
  process() {
    return this._strategy.process(this);
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

### Composition Over Inheritance
```javascript
// Use composition instead of inheritance
class Document {
  constructor(title, author, processor) {
    this._title = title;
    this._author = author;
    this._processor = processor;
  }
  
  process() {
    return this._processor.process(this);
  }
}

class TextProcessor {
  process(document) {
    // Text-specific processing
  }
}

class ImageProcessor {
  process(document) {
    // Image-specific processing
  }
}
```

## Related Refactorings

- [Pull Up Method](pull-up-method.md) - The inverse operation
- [Push Down Field](push-down-field.md) - Often done together
- [Extract Subclass](extract-class.md) - May create new subclasses for the method
- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Alternative approach
- [Replace Inheritance with Delegation](replace-superclass-with-delegate.md) - Alternative to inheritance