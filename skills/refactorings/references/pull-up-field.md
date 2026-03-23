---
title: "Pull Up Field"
description: "Move a field from subclasses to a common superclass when multiple subclasses share it"
category: "Dealing with Inheritance"
tags: ["pull-up", "field", "inheritance", "duplication", "superclass"]
related: ["push-down-field", "extract-superclass", "pull-up-method"]
---

# Pull Up Field

Move a field from subclasses to a common superclass when multiple subclasses share the same field.

## Inverse

[Push Down Field](push-down-field.md)

## Motivation

When you find the same field in multiple subclasses, it's a sign that the field belongs in the superclass. Moving shared fields up the hierarchy:

- **Eliminates duplication**: Field declared once instead of multiple times
- **Simplifies maintenance**: Changes to field happen in one place
- **Enables shared behavior**: Methods in superclass can work with the field
- **Clarifies design**: Shows that the field is a common concept
- **Reduces coupling**: Subclasses don't need to know about shared concerns

## Example

### Basic Example
```java
// Before - Duplicated field in subclasses
class Employee {
  // Base employee functionality
}

class Salesman extends Employee {
  private String name;
  private int id;
  // Salesman-specific methods
}

class Engineer extends Employee {
  private String name;
  private int id;
  // Engineer-specific methods
}

// After - Field moved to superclass
class Employee {
  protected String name;
  protected int id;
  
  public String getName() { return name; }
  public int getId() { return id; }
}

class Salesman extends Employee {
  // Salesman-specific methods only
}

class Engineer extends Employee {
  // Engineer-specific methods only
}
```

### JavaScript Example - User Types
```javascript
// Before - Repeated fields across user types
class User {
  constructor() {
    this._createdAt = new Date();
  }
}

class AdminUser extends User {
  constructor(name, email, permissions) {
    super();
    this._name = name;
    this._email = email;
    this._lastLogin = null;
    this._permissions = permissions;
  }
  
  get name() { return this._name; }
  get email() { return this._email; }
  get lastLogin() { return this._lastLogin; }
}

class RegularUser extends User {
  constructor(name, email, department) {
    super();
    this._name = name;           // Duplicated
    this._email = email;         // Duplicated
    this._lastLogin = null;      // Duplicated
    this._department = department;
  }
  
  get name() { return this._name; }
  get email() { return this._email; }
  get lastLogin() { return this._lastLogin; }
}

class GuestUser extends User {
  constructor(name, email, sessionId) {
    super();
    this._name = name;           // Duplicated
    this._email = email;         // Duplicated
    this._lastLogin = null;      // Duplicated
    this._sessionId = sessionId;
  }
  
  get name() { return this._name; }
  get email() { return this._email; }
  get lastLogin() { return this._lastLogin; }
}

// After - Common fields moved to superclass
class User {
  constructor(name, email) {
    this._name = name;
    this._email = email;
    this._createdAt = new Date();
    this._lastLogin = null;
  }
  
  get name() { return this._name; }
  get email() { return this._email; }
  get createdAt() { return this._createdAt; }
  get lastLogin() { return this._lastLogin; }
  
  recordLogin() {
    this._lastLogin = new Date();
  }
}

class AdminUser extends User {
  constructor(name, email, permissions) {
    super(name, email);
    this._permissions = permissions;
  }
  
  get permissions() { return this._permissions; }
  
  hasPermission(permission) {
    return this._permissions.includes(permission);
  }
}

class RegularUser extends User {
  constructor(name, email, department) {
    super(name, email);
    this._department = department;
  }
  
  get department() { return this._department; }
}

class GuestUser extends User {
  constructor(name, email, sessionId) {
    super(name, email);
    this._sessionId = sessionId;
  }
  
  get sessionId() { return this._sessionId; }
}
```

### Complex Example - Document Types
```javascript
// Before - Repeated metadata across document types
class Document {
  constructor() {
    this._createdAt = new Date();
  }
}

class TextDocument extends Document {
  constructor(title, author, content) {
    super();
    this._title = title;         // Repeated
    this._author = author;       // Repeated
    this._version = 1;           // Repeated
    this._isPublished = false;   // Repeated
    this._tags = [];             // Repeated
    this._content = content;
  }
  
  get title() { return this._title; }
  get author() { return this._author; }
  get version() { return this._version; }
  get isPublished() { return this._isPublished; }
  
  publish() {
    this._isPublished = true;
    this._version++;
  }
}

class ImageDocument extends Document {
  constructor(title, author, imageUrl, format) {
    super();
    this._title = title;         // Repeated
    this._author = author;       // Repeated
    this._version = 1;           // Repeated
    this._isPublished = false;   // Repeated
    this._tags = [];             // Repeated
    this._imageUrl = imageUrl;
    this._format = format;
  }
  
  get title() { return this._title; }
  get author() { return this._author; }
  get version() { return this._version; }
  get isPublished() { return this._isPublished; }
  
  publish() {
    this._isPublished = true;
    this._version++;
  }
}

class VideoDocument extends Document {
  constructor(title, author, videoUrl, duration) {
    super();
    this._title = title;         // Repeated
    this._author = author;       // Repeated
    this._version = 1;           // Repeated
    this._isPublished = false;   // Repeated
    this._tags = [];             // Repeated
    this._videoUrl = videoUrl;
    this._duration = duration;
  }
  
  get title() { return this._title; }
  get author() { return this._author; }
  get version() { return this._version; }
  get isPublished() { return this._isPublished; }
  
  publish() {
    this._isPublished = true;
    this._version++;
  }
}

// After - Common fields moved to superclass
class Document {
  constructor(title, author) {
    this._title = title;
    this._author = author;
    this._createdAt = new Date();
    this._version = 1;
    this._isPublished = false;
    this._tags = [];
    this._updatedAt = new Date();
  }
  
  get title() { return this._title; }
  get author() { return this._author; }
  get createdAt() { return this._createdAt; }
  get version() { return this._version; }
  get isPublished() { return this._isPublished; }
  get tags() { return [...this._tags]; }
  get updatedAt() { return this._updatedAt; }
  
  addTag(tag) {
    if (!this._tags.includes(tag)) {
      this._tags.push(tag);
      this._markAsUpdated();
    }
  }
  
  removeTag(tag) {
    const index = this._tags.indexOf(tag);\n    if (index > -1) {\n      this._tags.splice(index, 1);\n      this._markAsUpdated();\n    }\n  }\n  \n  publish() {\n    this._isPublished = true;\n    this._version++;\n    this._markAsUpdated();\n  }\n  \n  _markAsUpdated() {\n    this._updatedAt = new Date();\n  }\n}\n\nclass TextDocument extends Document {\n  constructor(title, author, content) {\n    super(title, author);\n    this._content = content;\n  }\n  \n  get content() { return this._content; }\n  \n  updateContent(newContent) {\n    this._content = newContent;\n    this._markAsUpdated();\n  }\n  \n  getWordCount() {\n    return this._content.split(/\\s+/).length;\n  }\n}\n\nclass ImageDocument extends Document {\n  constructor(title, author, imageUrl, format) {\n    super(title, author);\n    this._imageUrl = imageUrl;\n    this._format = format;\n  }\n  \n  get imageUrl() { return this._imageUrl; }\n  get format() { return this._format; }\n  \n  updateImage(newUrl, newFormat) {\n    this._imageUrl = newUrl;\n    this._format = newFormat;\n    this._markAsUpdated();\n  }\n}\n\nclass VideoDocument extends Document {\n  constructor(title, author, videoUrl, duration) {\n    super(title, author);\n    this._videoUrl = videoUrl;\n    this._duration = duration;\n  }\n  \n  get videoUrl() { return this._videoUrl; }\n  get duration() { return this._duration; }\n  \n  updateVideo(newUrl, newDuration) {\n    this._videoUrl = newUrl;\n    this._duration = newDuration;\n    this._markAsUpdated();\n  }\n}\n```\n\n### Entity Framework Example\n```javascript\n// Before - Audit fields repeated in every entity\nclass Product {\n  constructor(name, price) {\n    this._id = generateId();\n    this._name = name;\n    this._price = price;\n    this._createdAt = new Date();\n    this._updatedAt = new Date();\n    this._createdBy = getCurrentUser();\n    this._isActive = true;\n  }\n}\n\nclass Order {\n  constructor(customerId, items) {\n    this._id = generateId();\n    this._customerId = customerId;\n    this._items = items;\n    this._createdAt = new Date();\n    this._updatedAt = new Date();\n    this._createdBy = getCurrentUser();\n    this._isActive = true;\n  }\n}\n\nclass Customer {\n  constructor(name, email) {\n    this._id = generateId();\n    this._name = name;\n    this._email = email;\n    this._createdAt = new Date();\n    this._updatedAt = new Date();\n    this._createdBy = getCurrentUser();\n    this._isActive = true;\n  }\n}\n\n// After - Audit fields in base entity class\nclass BaseEntity {\n  constructor() {\n    this._id = generateId();\n    this._createdAt = new Date();\n    this._updatedAt = new Date();\n    this._createdBy = getCurrentUser();\n    this._isActive = true;\n  }\n  \n  get id() { return this._id; }\n  get createdAt() { return this._createdAt; }\n  get updatedAt() { return this._updatedAt; }\n  get createdBy() { return this._createdBy; }\n  get isActive() { return this._isActive; }\n  \n  markAsUpdated(updatedBy = getCurrentUser()) {\n    this._updatedAt = new Date();\n    this._updatedBy = updatedBy;\n  }\n  \n  deactivate() {\n    this._isActive = false;\n    this.markAsUpdated();\n  }\n  \n  activate() {\n    this._isActive = true;\n    this.markAsUpdated();\n  }\n}\n\nclass Product extends BaseEntity {\n  constructor(name, price) {\n    super();\n    this._name = name;\n    this._price = price;\n  }\n  \n  get name() { return this._name; }\n  get price() { return this._price; }\n  \n  updatePrice(newPrice) {\n    this._price = newPrice;\n    this.markAsUpdated();\n  }\n}\n\nclass Order extends BaseEntity {\n  constructor(customerId, items) {\n    super();\n    this._customerId = customerId;\n    this._items = items;\n    this._status = 'pending';\n  }\n  \n  get customerId() { return this._customerId; }\n  get items() { return this._items; }\n  get status() { return this._status; }\n  \n  updateStatus(newStatus) {\n    this._status = newStatus;\n    this.markAsUpdated();\n  }\n}\n\nclass Customer extends BaseEntity {\n  constructor(name, email) {\n    super();\n    this._name = name;\n    this._email = email;\n  }\n  \n  get name() { return this._name; }\n  get email() { return this._email; }\n  \n  updateEmail(newEmail) {\n    this._email = newEmail;\n    this.markAsUpdated();\n  }\n}\n```\n\n## Mechanics\n\n1. **Identify duplicate fields**\n   - Look for fields with the same name and type across subclasses\n   - Check that they serve the same purpose\n\n2. **Ensure field usage is compatible**\n   - Verify all subclasses use the field in similar ways\n   - Check for any subclass-specific constraints\n\n3. **Move field to superclass**\n   - Add the field to the superclass\n   - Make it protected if subclasses need direct access\n   - Add appropriate accessors (getters/setters)\n\n4. **Update subclass constructors**\n   - Modify constructors to set the field in superclass\n   - Often involves updating constructor chaining\n\n5. **Remove field from subclasses**\n   - Delete the field declarations\n   - Remove any duplicate accessor methods\n\n6. **Test thoroughly**\n   - Ensure all subclasses still work correctly\n   - Verify that field behavior is preserved\n\n## When to Use\n\n- **Duplicate fields**: Same field appears in multiple subclasses\n- **Common behavior**: Field represents a shared concept\n- **Inheritance hierarchy**: Clear is-a relationship exists\n- **Consistent usage**: Field used similarly across subclasses\n- **Shared operations**: Superclass methods could work with the field\n\n## Trade-offs\n\n### Benefits\n- **Eliminates duplication**: Field declared once\n- **Enables shared behavior**: Superclass methods can use the field\n- **Simplifies maintenance**: Changes happen in one place\n- **Clarifies design**: Shows field is a common concept\n- **Consistent access**: Same interface across subclasses\n\n### Drawbacks\n- **Increased coupling**: Subclasses depend more on superclass\n- **Reduced flexibility**: All subclasses must have the field\n- **Inappropriate generalization**: May force field on unrelated subclasses\n- **Access complexity**: May need to manage field visibility\n\n## Design Considerations\n\n### Field Access Patterns\n```javascript\n// Use protected for subclass access\nclass Vehicle {\n  constructor() {\n    this._engineType = null; // Protected field\n  }\n  \n  // Public interface\n  get engineType() { return this._engineType; }\n}\n\n// Use private for internal superclass logic\nclass AuditableEntity {\n  constructor() {\n    this._auditLog = []; // Private to superclass\n  }\n  \n  _logChange(field, oldValue, newValue) {\n    this._auditLog.push({ field, oldValue, newValue, timestamp: new Date() });\n  }\n}\n```\n\n### Conditional Fields\n```javascript\n// Sometimes not all subclasses need the field\nclass Document {\n  constructor(title, requiresApproval = false) {\n    this._title = title;\n    this._requiresApproval = requiresApproval;\n    this._approvedBy = null; // May not be used by all subclasses\n  }\n}\n\nclass PublicDocument extends Document {\n  constructor(title) {\n    super(title, false); // Doesn't require approval\n  }\n}\n\nclass InternalDocument extends Document {\n  constructor(title) {\n    super(title, true); // Requires approval\n  }\n}\n```\n\n### Abstract Fields\n```javascript\n// Use abstract pattern for fields that must be provided\nclass Shape {\n  constructor() {\n    this._color = null;\n    this._position = { x: 0, y: 0 };\n    \n    // Ensure subclasses provide required properties\n    if (this.constructor === Shape) {\n      throw new Error('Shape is abstract');\n    }\n  }\n  \n  get color() { return this._color; }\n  get position() { return this._position; }\n}\n```\n\n## Common Patterns\n\n### Audit Trail Pattern\n```javascript\nclass AuditableEntity {\n  constructor() {\n    this._createdAt = new Date();\n    this._createdBy = getCurrentUser();\n    this._updatedAt = new Date();\n    this._updatedBy = getCurrentUser();\n    this._version = 1;\n  }\n}\n```\n\n### State Management Pattern\n```javascript\nclass StatefulEntity {\n  constructor() {\n    this._state = 'active';\n    this._stateHistory = [];\n  }\n  \n  changeState(newState) {\n    this._stateHistory.push({\n      from: this._state,\n      to: newState,\n      timestamp: new Date()\n    });\n    this._state = newState;\n  }\n}\n```\n\n### Identification Pattern\n```javascript\nclass IdentifiableEntity {\n  constructor() {\n    this._id = generateId();\n    this._uuid = generateUUID();\n  }\n}\n```\n\n## Related Refactorings\n\n- [Push Down Field](push-down-field.md) - The inverse operation\n- [Pull Up Method](pull-up-method.md) - Often done together\n- [Extract Superclass](extract-superclass.md) - May create the target superclass\n- [Pull Up Constructor Body](pull-up-constructor-body.md) - For constructor-related fields\n- [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md) - May lead to this refactoring