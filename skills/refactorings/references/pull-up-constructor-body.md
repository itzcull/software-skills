---
title: "Pull Up Constructor Body"
description: "Move common constructor code from subclasses to the superclass constructor"
category: "Dealing with Inheritance"
tags: ["pull-up", "constructor", "inheritance", "duplication", "initialization"]
related: ["pull-up-method", "extract-superclass", "pull-up-field"]
---

# Pull Up Constructor Body

Move common constructor code from subclasses to the superclass constructor. This eliminates duplication and ensures consistent initialization across all subclasses.

## Motivation

When subclasses have constructors that contain similar initialization logic, it's often a sign that the common code should be moved to the superclass. This provides:

- **Eliminates duplication**: Common initialization code in one place
- **Consistency**: All subclasses follow the same initialization pattern
- **Maintainability**: Changes to common logic happen in one place
- **Proper inheritance**: Leverages the inheritance hierarchy correctly

## Example

### Basic Example
```javascript
// Before - Duplicated initialization in subclasses
class Party {
  constructor() {
    // Empty constructor
  }
}

class Employee extends Party {
  constructor(name, id, monthlyCost) {
    super();
    this._name = name;
    this._id = id;
    this._monthlyCost = monthlyCost;
  }
  
  // Employee-specific methods
}

class Department extends Party {
  constructor(name, manager) {
    super();
    this._name = name;
    this._manager = manager;
  }
  
  // Department-specific methods
}

// After - Common initialization moved to superclass
class Party {
  constructor(name) {
    this._name = name;
  }
  
  get name() { return this._name; }
}

class Employee extends Party {
  constructor(name, id, monthlyCost) {
    super(name);
    this._id = id;
    this._monthlyCost = monthlyCost;
  }
  
  get id() { return this._id; }
  get monthlyCost() { return this._monthlyCost; }
}

class Department extends Party {
  constructor(name, manager) {
    super(name);
    this._manager = manager;
  }
  
  get manager() { return this._manager; }
}
```

### Complex Example - User Hierarchy
```javascript
// Before - Complex duplication across user types
class User {
  constructor() {
    this._createdAt = new Date();
    this._isActive = true;
    this._permissions = [];
  }
}

class AdminUser extends User {
  constructor(name, email, department) {
    super();
    
    // Duplicated validation logic
    if (!name || typeof name !== 'string') {
      throw new Error('Name is required and must be a string');
    }
    if (!email || !this._isValidEmail(email)) {
      throw new Error('Valid email is required');
    }
    
    this._name = name;
    this._email = email.toLowerCase();
    this._department = department;
    this._role = 'admin';
    
    // Admin-specific initialization
    this._permissions = ['read', 'write', 'admin'];
    this._lastLogin = null;
    this._loginAttempts = 0;
  }
  
  _isValidEmail(email) {
    return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
  }
}

class RegularUser extends User {
  constructor(name, email, team) {
    super();
    
    // Same validation logic duplicated
    if (!name || typeof name !== 'string') {
      throw new Error('Name is required and must be a string');
    }
    if (!email || !this._isValidEmail(email)) {
      throw new Error('Valid email is required');
    }
    
    this._name = name;
    this._email = email.toLowerCase();
    this._team = team;
    this._role = 'user';
    
    // Regular user initialization
    this._permissions = ['read'];
    this._projectsAccess = [];
  }
  
  _isValidEmail(email) {
    return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
  }
}

class GuestUser extends User {
  constructor(name, email, sessionId) {
    super();
    
    // Same validation again
    if (!name || typeof name !== 'string') {
      throw new Error('Name is required and must be a string');
    }
    if (!email || !this._isValidEmail(email)) {
      throw new Error('Valid email is required');
    }
    
    this._name = name;
    this._email = email.toLowerCase();
    this._sessionId = sessionId;
    this._role = 'guest';
    
    // Guest-specific initialization
    this._permissions = ['read'];
    this._expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000); // 24 hours
  }
  
  _isValidEmail(email) {
    return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
  }
}

// After - Common logic moved to superclass
class User {
  constructor(name, email, role) {
    // Common validation
    if (!name || typeof name !== 'string') {
      throw new Error('Name is required and must be a string');
    }
    if (!email || !this._isValidEmail(email)) {
      throw new Error('Valid email is required');
    }
    if (!role) {
      throw new Error('Role is required');
    }
    
    // Common initialization
    this._name = name;
    this._email = email.toLowerCase();
    this._role = role;
    this._createdAt = new Date();
    this._isActive = true;
    this._permissions = this._getDefaultPermissions(role);
  }
  
  get name() { return this._name; }
  get email() { return this._email; }
  get role() { return this._role; }
  get createdAt() { return this._createdAt; }
  get isActive() { return this._isActive; }
  get permissions() { return this._permissions; }
  
  _isValidEmail(email) {\n    return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);\n  }\n  \n  _getDefaultPermissions(role) {\n    const permissionMap = {\n      'admin': ['read', 'write', 'admin'],\n      'user': ['read'],\n      'guest': ['read']\n    };\n    return permissionMap[role] || ['read'];\n  }\n}\n\nclass AdminUser extends User {\n  constructor(name, email, department) {\n    super(name, email, 'admin');\n    this._department = department;\n    this._lastLogin = null;\n    this._loginAttempts = 0;\n  }\n  \n  get department() { return this._department; }\n  get lastLogin() { return this._lastLogin; }\n  get loginAttempts() { return this._loginAttempts; }\n}\n\nclass RegularUser extends User {\n  constructor(name, email, team) {\n    super(name, email, 'user');\n    this._team = team;\n    this._projectsAccess = [];\n  }\n  \n  get team() { return this._team; }\n  get projectsAccess() { return this._projectsAccess; }\n}\n\nclass GuestUser extends User {\n  constructor(name, email, sessionId) {\n    super(name, email, 'guest');\n    this._sessionId = sessionId;\n    this._expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000);\n  }\n  \n  get sessionId() { return this._sessionId; }\n  get expiresAt() { return this._expiresAt; }\n  \n  get isExpired() {\n    return new Date() > this._expiresAt;\n  }\n}\n```\n\n### Database Entity Example\n```javascript\n// Before - Repeated audit fields initialization\nclass BaseEntity {\n  constructor() {\n    // Base class with no common initialization\n  }\n}\n\nclass Product extends BaseEntity {\n  constructor(name, price, category) {\n    super();\n    \n    // Audit fields - repeated in every entity\n    this._id = generateId();\n    this._createdAt = new Date();\n    this._updatedAt = new Date();\n    this._version = 1;\n    this._isDeleted = false;\n    \n    // Product-specific fields\n    this._name = name;\n    this._price = price;\n    this._category = category;\n  }\n}\n\nclass Order extends BaseEntity {\n  constructor(customerId, items) {\n    super();\n    \n    // Same audit fields initialization\n    this._id = generateId();\n    this._createdAt = new Date();\n    this._updatedAt = new Date();\n    this._version = 1;\n    this._isDeleted = false;\n    \n    // Order-specific fields\n    this._customerId = customerId;\n    this._items = items;\n    this._status = 'pending';\n  }\n}\n\nclass Customer extends BaseEntity {\n  constructor(name, email) {\n    super();\n    \n    // Audit fields again\n    this._id = generateId();\n    this._createdAt = new Date();\n    this._updatedAt = new Date();\n    this._version = 1;\n    this._isDeleted = false;\n    \n    // Customer-specific fields\n    this._name = name;\n    this._email = email;\n  }\n}\n\n// After - Common audit initialization in base class\nclass BaseEntity {\n  constructor() {\n    this._id = generateId();\n    this._createdAt = new Date();\n    this._updatedAt = new Date();\n    this._version = 1;\n    this._isDeleted = false;\n  }\n  \n  get id() { return this._id; }\n  get createdAt() { return this._createdAt; }\n  get updatedAt() { return this._updatedAt; }\n  get version() { return this._version; }\n  get isDeleted() { return this._isDeleted; }\n  \n  markAsUpdated() {\n    this._updatedAt = new Date();\n    this._version++;\n  }\n  \n  markAsDeleted() {\n    this._isDeleted = true;\n    this.markAsUpdated();\n  }\n}\n\nclass Product extends BaseEntity {\n  constructor(name, price, category) {\n    super();\n    this._name = name;\n    this._price = price;\n    this._category = category;\n  }\n  \n  get name() { return this._name; }\n  get price() { return this._price; }\n  get category() { return this._category; }\n  \n  updatePrice(newPrice) {\n    this._price = newPrice;\n    this.markAsUpdated();\n  }\n}\n\nclass Order extends BaseEntity {\n  constructor(customerId, items) {\n    super();\n    this._customerId = customerId;\n    this._items = items;\n    this._status = 'pending';\n  }\n  \n  get customerId() { return this._customerId; }\n  get items() { return this._items; }\n  get status() { return this._status; }\n  \n  updateStatus(newStatus) {\n    this._status = newStatus;\n    this.markAsUpdated();\n  }\n}\n\nclass Customer extends BaseEntity {\n  constructor(name, email) {\n    super();\n    this._name = name;\n    this._email = email;\n  }\n  \n  get name() { return this._name; }\n  get email() { return this._email; }\n  \n  updateEmail(newEmail) {\n    this._email = newEmail;\n    this.markAsUpdated();\n  }\n}\n```\n\n## Mechanics\n\n1. **Identify common constructor code**\n   - Look for repeated initialization patterns\n   - Find shared validation logic\n   - Note common field assignments\n\n2. **Move common code to superclass constructor**\n   - Add parameters to superclass constructor as needed\n   - Move the shared initialization logic\n   - Ensure proper parameter validation\n\n3. **Update subclass constructors**\n   - Call super() with appropriate parameters\n   - Remove the duplicated code\n   - Keep only subclass-specific initialization\n\n4. **Adjust parameter passing**\n   - Ensure subclasses pass required parameters to super()\n   - Handle any parameter transformation needed\n\n5. **Test thoroughly**\n   - Verify all subclasses construct correctly\n   - Check that shared behavior is preserved\n   - Ensure subclass-specific behavior still works\n\n## When to Use\n\n- **Repeated initialization**: Same code in multiple subclass constructors\n- **Common validation**: Shared validation logic across subclasses\n- **Shared fields**: Multiple subclasses initialize the same fields\n- **Audit patterns**: Common tracking fields (created date, version, etc.)\n- **Configuration setup**: Shared setup logic\n\n## Trade-offs\n\n### Benefits\n- **DRY principle**: Eliminates code duplication\n- **Consistency**: Ensures uniform initialization\n- **Maintainability**: Changes happen in one place\n- **Proper inheritance**: Uses inheritance hierarchy correctly\n- **Validation centralization**: Common validation in one place\n\n### Drawbacks\n- **Coupling**: Subclasses become more dependent on superclass\n- **Flexibility**: May constrain subclass initialization options\n- **Complexity**: Can make inheritance hierarchy more complex\n- **Parameter explosion**: Superclass constructor may need many parameters\n\n## Implementation Patterns\n\n### Template Method Pattern\n```javascript\nclass Vehicle {\n  constructor(make, model, year) {\n    this._make = make;\n    this._model = model;\n    this._year = year;\n    this._id = generateVehicleId();\n    this._registrationDate = new Date();\n    \n    // Template method - subclasses can override\n    this._performSpecificInitialization();\n  }\n  \n  _performSpecificInitialization() {\n    // Default implementation - can be overridden\n  }\n}\n\nclass Car extends Vehicle {\n  constructor(make, model, year, doors) {\n    super(make, model, year);\n    this._doors = doors;\n  }\n  \n  _performSpecificInitialization() {\n    this._fuelType = 'gasoline';\n    this._emissions = this._calculateEmissions();\n  }\n}\n```\n\n### Builder Pattern Integration\n```javascript\nclass ConfigurableEntity {\n  constructor(builder) {\n    // Common initialization from builder\n    this._id = builder.id || generateId();\n    this._name = builder.name;\n    this._createdAt = new Date();\n    this._metadata = builder.metadata || {};\n    \n    this._validate();\n  }\n  \n  _validate() {\n    if (!this._name) {\n      throw new Error('Name is required');\n    }\n  }\n}\n\nclass Product extends ConfigurableEntity {\n  constructor(builder) {\n    super(builder);\n    this._price = builder.price;\n    this._category = builder.category;\n  }\n}\n```\n\n### Factory Method Integration\n```javascript\nclass User {\n  constructor(userData, role) {\n    this._name = userData.name;\n    this._email = userData.email;\n    this._role = role;\n    this._permissions = this._createPermissions(role);\n    this._createdAt = new Date();\n  }\n  \n  _createPermissions(role) {\n    // Factory method for creating permissions\n    throw new Error('Subclasses must implement _createPermissions');\n  }\n}\n\nclass AdminUser extends User {\n  constructor(userData) {\n    super(userData, 'admin');\n  }\n  \n  _createPermissions(role) {\n    return new AdminPermissions();\n  }\n}\n```\n\n## Related Refactorings\n\n- [Pull Up Field](pull-up-field.md) - Often done together\n- [Pull Up Method](pull-up-method.md) - Moving other shared methods\n- [Extract Superclass](extract-superclass.md) - Creating the superclass first\n- [Form Template Method](extract-superclass.md) - For more complex initialization patterns\n- [Replace Constructor with Factory Method](replace-constructor-with-factory-function.md) - Alternative approach