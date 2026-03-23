---
title: "Rename Field"
description: "Change a field name to better express its purpose and meaning"
category: "Rename"
tags: ["rename", "field", "naming", "clarity", "purpose"]
related: ["rename-variable", "rename-function", "encapsulate-variable"]
---

# Rename Field

Change a field name to better express its purpose and meaning. A good field name clearly communicates what the field represents and how it should be used.

## Motivation

Field names should clearly express their purpose. Poor field names can:

- **Mislead developers**: Unclear names cause misunderstandings
- **Hide intent**: Purpose of the field is not obvious
- **Create confusion**: Similar names for different purposes
- **Reduce maintainability**: Code becomes harder to understand and modify
- **Increase bugs**: Misunderstandings lead to incorrect usage

## Example

### Basic Example
```javascript
// Before - Unclear field names
class Person {
  constructor(n, a, e) {
    this.n = n;     // What is 'n'?
    this.a = a;     // What is 'a'?
    this.e = e;     // What is 'e'?
    this.d = null;  // What is 'd'?
  }
  
  getAge() {
    const today = new Date();
    return today.getFullYear() - this.d.getFullYear();
  }
  
  isAdult() {
    return this.a >= 18;
  }
  
  sendEmail(message) {
    emailService.send(this.e, message);
  }
}

// After - Clear field names
class Person {
  constructor(name, age, email) {
    this._name = name;
    this._age = age;
    this._email = email;
    this._birthDate = null;
  }
  
  get name() { return this._name; }
  get age() { return this._age; }
  get email() { return this._email; }
  get birthDate() { return this._birthDate; }
  
  getAge() {
    const today = new Date();
    return today.getFullYear() - this._birthDate.getFullYear();
  }
  
  isAdult() {
    return this._age >= 18;
  }
  
  sendEmail(message) {
    emailService.send(this._email, message);
  }
}
```

### Complex Example - E-commerce Order
```javascript
// Before - Confusing and misleading field names
class Order {
  constructor(id, uid, items) {
    this.id = id;
    this.uid = uid;           // User ID or Unique ID?
    this.items = items;
    this.amt = 0;             // Amount? Amplitude?
    this.disc = 0;            // Discount? Disc?
    this.tx = 0;              // Tax? Transaction?
    this.sh = 0;              // Shipping? Show?
    this.tot = 0;             // Total?
    this.dt = new Date();     // Date? DateTime?
    this.stat = 'pending';    // Status? Statistics?
    this.addr = null;         // Address?
    this.pay = null;          // Payment? Pay?
    this.proc = false;        // Processed? Procedure?
    this.ship = false;        // Shipped? Ship?
    this.del = false;         // Delivered? Delete?
    this.ret = false;         // Returned? Retry?
  }
  
  calc() {
    this.amt = this.items.reduce((sum, item) => sum + item.price * item.qty, 0);
    this.disc = this.amt > 100 ? this.amt * 0.1 : 0;
    this.tx = (this.amt - this.disc) * 0.08;
    this.sh = this.amt > 50 ? 0 : 10;
    this.tot = this.amt - this.disc + this.tx + this.sh;
  }
  
  process() {
    if (this.proc) return false;
    
    if (!this.addr || !this.pay) {
      throw new Error('Missing address or payment');
    }
    
    this.proc = true;
    this.stat = 'processing';
    return true;
  }
  
  markShipped() {
    if (!this.proc) throw new Error('Order not processed');
    this.ship = true;
    this.stat = 'shipped';
  }
  
  markDelivered() {
    if (!this.ship) throw new Error('Order not shipped');
    this.del = true;
    this.stat = 'delivered';
  }
}

// After - Clear, meaningful field names
class Order {
  constructor(orderId, customerId, items) {
    this._orderId = orderId;
    this._customerId = customerId;
    this._items = items;
    this._subtotalAmount = 0;
    this._discountAmount = 0;
    this._taxAmount = 0;
    this._shippingAmount = 0;
    this._totalAmount = 0;
    this._orderDate = new Date();
    this._orderStatus = 'pending';
    this._shippingAddress = null;
    this._paymentMethod = null;
    this._isProcessed = false;
    this._isShipped = false;
    this._isDelivered = false;
    this._isReturned = false;
  }
  
  get orderId() { return this._orderId; }
  get customerId() { return this._customerId; }
  get items() { return [...this._items]; }
  get subtotalAmount() { return this._subtotalAmount; }
  get discountAmount() { return this._discountAmount; }
  get taxAmount() { return this._taxAmount; }
  get shippingAmount() { return this._shippingAmount; }
  get totalAmount() { return this._totalAmount; }
  get orderDate() { return new Date(this._orderDate); }
  get orderStatus() { return this._orderStatus; }
  get shippingAddress() { return this._shippingAddress; }
  get paymentMethod() { return this._paymentMethod; }
  get isProcessed() { return this._isProcessed; }
  get isShipped() { return this._isShipped; }
  get isDelivered() { return this._isDelivered; }
  get isReturned() { return this._isReturned; }
  
  calculateTotals() {
    this._subtotalAmount = this._items.reduce((sum, item) => {
      return sum + item.price * item.quantity;
    }, 0);
    
    this._discountAmount = this._subtotalAmount > 100 
      ? this._subtotalAmount * 0.1 
      : 0;
    
    this._taxAmount = (this._subtotalAmount - this._discountAmount) * 0.08;
    
    this._shippingAmount = this._subtotalAmount > 50 ? 0 : 10;
    
    this._totalAmount = this._subtotalAmount 
      - this._discountAmount 
      + this._taxAmount 
      + this._shippingAmount;
  }
  
  processOrder() {
    if (this._isProcessed) {
      return false;
    }
    
    if (!this._shippingAddress || !this._paymentMethod) {
      throw new Error('Missing shipping address or payment method');
    }
    
    this._isProcessed = true;
    this._orderStatus = 'processing';
    return true;
  }
  
  markAsShipped() {
    if (!this._isProcessed) {
      throw new Error('Order must be processed before shipping');
    }
    
    this._isShipped = true;
    this._orderStatus = 'shipped';
  }
  
  markAsDelivered() {
    if (!this._isShipped) {
      throw new Error('Order must be shipped before delivery');
    }
    
    this._isDelivered = true;
    this._orderStatus = 'delivered';
  }
}
```

### Data Model Example
```javascript
// Before - Database-style abbreviated names
class User {
  constructor(data) {
    this.usr_id = data.usr_id;
    this.usr_nm = data.usr_nm;
    this.usr_email = data.usr_email;
    this.usr_pwd = data.usr_pwd;
    this.usr_fname = data.usr_fname;
    this.usr_lname = data.usr_lname;
    this.usr_dob = data.usr_dob;
    this.usr_addr_st = data.usr_addr_st;
    this.usr_addr_city = data.usr_addr_city;
    this.usr_addr_zip = data.usr_addr_zip;
    this.usr_ph = data.usr_ph;
    this.usr_created = data.usr_created;
    this.usr_updated = data.usr_updated;
    this.usr_active = data.usr_active;
    this.usr_verified = data.usr_verified;
    this.usr_last_login = data.usr_last_login;
    this.usr_login_cnt = data.usr_login_cnt;
  }
  
  getFullName() {
    return `${this.usr_fname} ${this.usr_lname}`;
  }
  
  getAddress() {
    return `${this.usr_addr_st}, ${this.usr_addr_city} ${this.usr_addr_zip}`;
  }
  
  isActive() {
    return this.usr_active && this.usr_verified;
  }
  
  updateLoginInfo() {
    this.usr_last_login = new Date();
    this.usr_login_cnt++;
  }
}

// After - Clear, descriptive field names
class User {
  constructor(data) {
    this._userId = data.userId;
    this._username = data.username;
    this._email = data.email;
    this._passwordHash = data.passwordHash;
    this._firstName = data.firstName;
    this._lastName = data.lastName;
    this._dateOfBirth = data.dateOfBirth;
    this._streetAddress = data.streetAddress;
    this._city = data.city;
    this._postalCode = data.postalCode;
    this._phoneNumber = data.phoneNumber;
    this._createdAt = data.createdAt;
    this._updatedAt = data.updatedAt;
    this._isActive = data.isActive;
    this._isEmailVerified = data.isEmailVerified;
    this._lastLoginAt = data.lastLoginAt;
    this._loginCount = data.loginCount;
  }
  
  get userId() { return this._userId; }
  get username() { return this._username; }
  get email() { return this._email; }
  get firstName() { return this._firstName; }
  get lastName() { return this._lastName; }
  get dateOfBirth() { return this._dateOfBirth; }
  get streetAddress() { return this._streetAddress; }
  get city() { return this._city; }
  get postalCode() { return this._postalCode; }
  get phoneNumber() { return this._phoneNumber; }
  get createdAt() { return this._createdAt; }
  get updatedAt() { return this._updatedAt; }
  get isActive() { return this._isActive; }
  get isEmailVerified() { return this._isEmailVerified; }
  get lastLoginAt() { return this._lastLoginAt; }
  get loginCount() { return this._loginCount; }
  
  getFullName() {
    return `${this._firstName} ${this._lastName}`;
  }
  
  getFormattedAddress() {
    return `${this._streetAddress}, ${this._city} ${this._postalCode}`;
  }
  
  isAccountActive() {
    return this._isActive && this._isEmailVerified;
  }
  
  recordLogin() {
    this._lastLoginAt = new Date();
    this._loginCount++;
    this._updatedAt = new Date();
  }
}
```

### Configuration Object Example
```javascript
// Before - Cryptic configuration field names
class DatabaseConfig {
  constructor(opts) {
    this.h = opts.h || 'localhost';      // host
    this.p = opts.p || 5432;             // port
    this.db = opts.db;                   // database
    this.u = opts.u;                     // user
    this.pw = opts.pw;                   // password
    this.ssl = opts.ssl || false;        // ssl (this one is ok)
    this.tm = opts.tm || 30000;          // timeout
    this.mx = opts.mx || 10;             // max connections
    this.mn = opts.mn || 1;              // min connections
    this.idle = opts.idle || 300000;     // idle timeout
    this.acq = opts.acq || 60000;        // acquire timeout
    this.ret = opts.ret || 3;            // retry count
    this.log = opts.log || false;        // logging
    this.dbg = opts.dbg || false;        // debug
  }
  
  getConnectionString() {
    const auth = this.u && this.pw ? `${this.u}:${this.pw}@` : '';
    const protocol = this.ssl ? 'postgres' : 'postgresql';
    return `${protocol}://${auth}${this.h}:${this.p}/${this.db}`;
  }
  
  getPoolConfig() {
    return {
      max: this.mx,
      min: this.mn,
      idleTimeoutMillis: this.idle,
      acquireTimeoutMillis: this.acq,
      createTimeoutMillis: this.tm,
      reapIntervalMillis: 1000,
      createRetryIntervalMillis: 100,
      propagateCreateError: false
    };
  }
}

// After - Self-documenting field names
class DatabaseConfig {
  constructor(options) {
    this._host = options.host || 'localhost';
    this._port = options.port || 5432;
    this._databaseName = options.databaseName;
    this._username = options.username;
    this._password = options.password;
    this._useSsl = options.useSsl || false;
    this._connectionTimeoutMs = options.connectionTimeoutMs || 30000;
    this._maxConnections = options.maxConnections || 10;
    this._minConnections = options.minConnections || 1;
    this._idleTimeoutMs = options.idleTimeoutMs || 300000;
    this._acquireTimeoutMs = options.acquireTimeoutMs || 60000;
    this._maxRetryAttempts = options.maxRetryAttempts || 3;
    this._enableLogging = options.enableLogging || false;
    this._enableDebugMode = options.enableDebugMode || false;
  }
  
  get host() { return this._host; }
  get port() { return this._port; }
  get databaseName() { return this._databaseName; }
  get username() { return this._username; }
  get password() { return this._password; }
  get useSsl() { return this._useSsl; }
  get connectionTimeoutMs() { return this._connectionTimeoutMs; }
  get maxConnections() { return this._maxConnections; }
  get minConnections() { return this._minConnections; }
  get idleTimeoutMs() { return this._idleTimeoutMs; }
  get acquireTimeoutMs() { return this._acquireTimeoutMs; }
  get maxRetryAttempts() { return this._maxRetryAttempts; }
  get enableLogging() { return this._enableLogging; }
  get enableDebugMode() { return this._enableDebugMode; }
  
  getConnectionString() {
    const auth = this._username && this._password 
      ? `${this._username}:${this._password}@` 
      : '';
    const protocol = this._useSsl ? 'postgres' : 'postgresql';
    return `${protocol}://${auth}${this._host}:${this._port}/${this._databaseName}`;
  }
  
  getPoolConfiguration() {
    return {
      max: this._maxConnections,
      min: this._minConnections,
      idleTimeoutMillis: this._idleTimeoutMs,
      acquireTimeoutMillis: this._acquireTimeoutMs,
      createTimeoutMillis: this._connectionTimeoutMs,
      reapIntervalMillis: 1000,
      createRetryIntervalMillis: 100,
      propagateCreateError: false
    };
  }
  
  validate() {
    if (!this._host) {
      throw new Error('Database host is required');
    }
    if (!this._databaseName) {
      throw new Error('Database name is required');
    }
    if (!this._username) {
      throw new Error('Database username is required');
    }
    if (!this._password) {
      throw new Error('Database password is required');
    }
  }
}
```

## Mechanics

1. **Identify poorly named fields**
   - Look for abbreviations that aren't clear
   - Find single-letter or very short names
   - Check for misleading or ambiguous names
   - Identify names that don't express purpose

2. **Choose better names**
   - Use full words instead of abbreviations
   - Make the purpose clear from the name
   - Follow consistent naming conventions
   - Consider the domain context

3. **Update field declarations**
   - Rename the field in the class
   - Update any related accessor methods
   - Ensure consistency across the class

4. **Update all references**
   - Find all places where the field is accessed
   - Update constructor parameters if needed
   - Modify method implementations
   - Update tests and documentation

5. **Use IDE refactoring tools**
   - Use automated rename refactoring when available
   - Verify all references are updated
   - Check for string literals that might reference the field

6. **Test thoroughly**
   - Run all tests to ensure nothing is broken
   - Check that functionality is preserved
   - Verify that the intent is now clearer

## Naming Guidelines

### Use Descriptive Names
```javascript
// Bad
class User {
  constructor(n, a, e) {
    this.n = n;
    this.a = a;
    this.e = e;
  }
}

// Good
class User {
  constructor(name, age, email) {
    this._name = name;
    this._age = age;
    this._email = email;
  }
}
```

### Avoid Misleading Names
```javascript
// Bad - misleading
class Rectangle {
  constructor(width, height) {
    this.data = [width, height]; // 'data' doesn't tell us what it contains
  }
}

// Good - clear
class Rectangle {
  constructor(width, height) {
    this._dimensions = [width, height];
  }
}
```

### Use Consistent Conventions
```javascript
// Bad - inconsistent
class Order {
  constructor() {
    this.userId = null;     // camelCase
    this.order_date = null; // snake_case
    this.TotalAmt = 0;      // PascalCase
    this.isactive = false;  // lowercase
  }
}

// Good - consistent camelCase
class Order {
  constructor() {
    this._userId = null;
    this._orderDate = null;
    this._totalAmount = 0;
    this._isActive = false;
  }
}
```

### Use Domain Language
```javascript
// Generic - not domain-specific
class Item {
  constructor() {
    this._value = 0;
    this._status = 'new';
    this._owner = null;
  }
}

// Domain-specific - e-commerce
class Product {
  constructor() {
    this._price = 0;
    this._stockStatus = 'available';
    this._vendor = null;
  }
}
```

### Boolean Field Naming
```javascript
// Good boolean naming patterns
class User {
  constructor() {
    this._isActive = false;      // is + adjective
    this._hasPermission = false; // has + noun
    this._canEdit = false;       // can + verb
    this._shouldNotify = false;  // should + verb
  }
}
```

## When to Use

- **Unclear purpose**: Field name doesn't express what it represents
- **Abbreviations**: Cryptic shortened names that aren't obvious
- **Misleading names**: Name suggests wrong purpose or type
- **Inconsistent naming**: Field names don't follow project conventions
- **Domain evolution**: Business language has changed
- **Code reviews**: Reviewers struggle to understand field purpose

## Trade-offs

### Benefits
- **Better readability**: Code is easier to understand
- **Reduced confusion**: Clear names prevent misunderstandings
- **Improved maintainability**: Easier to modify and extend
- **Self-documenting**: Good names reduce need for comments
- **Fewer bugs**: Clear intent reduces usage errors

### Risks
- **Breaking changes**: External code may depend on field names
- **Merge conflicts**: Large renaming can cause version control issues
- **Inconsistency**: Partial renaming can make things worse
- **Effort required**: Need to update all references

## Tools and Techniques

### IDE Support
```javascript
// Most IDEs support rename refactoring
// 1. Right-click on field name
// 2. Select "Rename" or "Refactor > Rename"
// 3. IDE updates all references automatically
```

### Search and Replace
```bash
# Use grep to find all references
grep -r "oldFieldName" src/

# Use sed for simple replacements (be careful!)
sed -i 's/oldFieldName/newFieldName/g' src/**/*.js
```

### Gradual Approach
```javascript
// For public APIs, use gradual deprecation
class User {
  constructor(name) {
    this._fullName = name; // New field
  }
  
  get fullName() {
    return this._fullName;
  }
  
  // Deprecated - for backward compatibility
  get name() {
    console.warn('name is deprecated, use fullName instead');
    return this._fullName;
  }
}
```

## Related Refactorings

- [Rename Variable](rename-variable.md) - Similar concept for local variables
- [Change Function Declaration](change-function-declaration.md) - Rename methods
- [Encapsulate Field](encapsulate-record.md) - Hide field access behind methods
- [Extract Variable](extract-variable.md) - Create well-named variables
- [Introduce Parameter Object](introduce-parameter-object.md) - Group related fields