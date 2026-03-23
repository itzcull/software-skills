---
title: "Preserve Whole Object"
description: "Replace multiple parameters derived from an object with the object itself to simplify method calls"
category: "Simplifying Function Calls"
tags: ["object", "parameters", "coupling", "simplification", "whole-object"]
related: ["introduce-parameter-object", "replace-parameter-with-query", "remove-flag-argument"]
---

# Preserve Whole Object

Replace multiple parameters derived from an object with the object itself. This simplifies method calls and reduces coupling between the method and the details of the object's structure.

## Motivation

When a method needs several values from an object, instead of passing each value individually, pass the whole object. This provides several benefits:

- **Simpler method calls**: Fewer parameters to pass
- **Reduced coupling**: Method doesn't need to know object's internal structure
- **Easier maintenance**: Adding new fields doesn't require changing method signatures
- **Better expressiveness**: Shows the relationship between the data and the operation
- **Future flexibility**: Method can access other object properties as needed

## Example

### Basic Example
```javascript
// Before - Extracting multiple values from object
class Room {
  constructor(name, temperatureRange) {
    this._name = name;
    this._daysTempRange = temperatureRange;
  }
  
  get daysTempRange() { return this._daysTempRange; }
}

class HeatingPlan {
  withinRange(low, high) {
    return this._temperatureRange.low >= low && 
           this._temperatureRange.high <= high;
  }
}

// Client code
const room = new Room("Living Room", {low: 68, high: 72});
const plan = new HeatingPlan({low: 65, high: 75});

const low = room.daysTempRange.low;
const high = room.daysTempRange.high;
const comfortable = plan.withinRange(low, high);

// After - Passing the whole object
class HeatingPlan {
  withinRange(temperatureRange) {
    return this._temperatureRange.low >= temperatureRange.low && 
           this._temperatureRange.high <= temperatureRange.high;
  }
}

// Client code - simpler and more expressive
const room = new Room("Living Room", {low: 68, high: 72});
const plan = new HeatingPlan({low: 65, high: 75});

const comfortable = plan.withinRange(room.daysTempRange);
```

### Complex Example - Order Processing
```javascript
// Before - Extracting many values from customer and order
class PricingService {
  calculateTotal(baseAmount, discountRate, taxRate, shippingCost, isVIP, loyaltyPoints) {
    let total = baseAmount;
    
    // Apply discount
    if (discountRate > 0) {
      total -= total * discountRate;
    }
    
    // VIP bonus discount
    if (isVIP && total > 100) {
      total -= 10;
    }
    
    // Loyalty points discount
    if (loyaltyPoints > 1000) {
      total -= Math.min(total * 0.05, 50);
    }
    
    // Add tax
    total += total * taxRate;
    
    // Add shipping
    total += shippingCost;
    
    return total;
  }
}

class OrderService {
  processOrder(order) {
    const customer = order.customer;
    const baseAmount = order.items.reduce((sum, item) => sum + item.price, 0);
    
    const total = pricingService.calculateTotal(
      baseAmount,
      customer.discountRate,
      customer.address.state.taxRate,
      order.shippingCost,
      customer.isVIP,
      customer.loyaltyPoints
    );
    
    order.total = total;
    return order;
  }
}

// After - Passing whole objects
class PricingService {
  calculateTotal(order, customer) {
    const baseAmount = order.items.reduce((sum, item) => sum + item.price, 0);
    let total = baseAmount;
    
    // Apply discount
    if (customer.discountRate > 0) {
      total -= total * customer.discountRate;
    }
    
    // VIP bonus discount
    if (customer.isVIP && total > 100) {
      total -= 10;
    }
    
    // Loyalty points discount
    if (customer.loyaltyPoints > 1000) {
      total -= Math.min(total * 0.05, 50);
    }
    
    // Add tax
    total += total * customer.address.state.taxRate;
    
    // Add shipping
    total += order.shippingCost;
    
    return total;
  }
}

class OrderService {
  processOrder(order) {
    const total = pricingService.calculateTotal(order, order.customer);
    order.total = total;
    return order;
  }
}
```

### Report Generation Example
```javascript
// Before - Extracting individual fields for report
class ReportGenerator {
  generateUserReport(id, name, email, department, role, startDate, salary, manager) {
    return `
      User Report
      ===========
      ID: ${id}
      Name: ${name}
      Email: ${email}
      Department: ${department}
      Role: ${role}
      Start Date: ${startDate.toDateString()}
      Salary: $${salary.toLocaleString()}
      Manager: ${manager}
      Generated: ${new Date().toDateString()}
    `;
  }
  
  generateUserSummary(name, department, role, yearsOfService, performanceRating) {
    return `${name} (${department}) - ${role} - ${yearsOfService} years - Rating: ${performanceRating}/5`;
  }
}

// Client code - lots of parameter extraction
function createReports(users) {
  return users.map(user => {
    const yearsOfService = new Date().getFullYear() - user.startDate.getFullYear();
    
    const fullReport = reportGenerator.generateUserReport(
      user.id,
      user.name,
      user.email,
      user.department.name,
      user.role.title,
      user.startDate,
      user.salary,
      user.manager.name
    );
    
    const summary = reportGenerator.generateUserSummary(
      user.name,
      user.department.name,
      user.role.title,
      yearsOfService,
      user.performanceRating
    );
    
    return { fullReport, summary };
  });
}

// After - Passing whole user object
class ReportGenerator {
  generateUserReport(user) {
    return `
      User Report
      ===========
      ID: ${user.id}
      Name: ${user.name}
      Email: ${user.email}
      Department: ${user.department.name}
      Role: ${user.role.title}
      Start Date: ${user.startDate.toDateString()}
      Salary: $${user.salary.toLocaleString()}
      Manager: ${user.manager.name}
      Generated: ${new Date().toDateString()}
    `;
  }
  
  generateUserSummary(user) {
    const yearsOfService = new Date().getFullYear() - user.startDate.getFullYear();
    return `${user.name} (${user.department.name}) - ${user.role.title} - ${yearsOfService} years - Rating: ${user.performanceRating}/5`;
  }
}

// Client code - much simpler
function createReports(users) {
  return users.map(user => ({
    fullReport: reportGenerator.generateUserReport(user),
    summary: reportGenerator.generateUserSummary(user)
  }));
}
```

### API Service Example
```javascript
// Before - Extracting properties for API calls
class UserAPIService {
  updateProfile(userId, name, email, phone, address, preferences) {
    const payload = {
      name,
      email,
      phone,
      address: {
        street: address.street,
        city: address.city,
        state: address.state,
        zipCode: address.zipCode
      },
      preferences: {
        theme: preferences.theme,
        notifications: preferences.notifications,
        language: preferences.language
      }
    };
    
    return this.httpClient.put(`/users/${userId}`, payload);
  }
  
  createUser(name, email, phone, departmentId, roleId, managerId, startDate) {
    const payload = {
      name,
      email,
      phone,
      departmentId,
      roleId,
      managerId,
      startDate: startDate.toISOString()
    };
    
    return this.httpClient.post('/users', payload);
  }
}

// Client code
class UserService {
  async updateUserProfile(user, updates) {
    return userAPI.updateProfile(
      user.id,
      updates.name || user.name,
      updates.email || user.email,
      updates.phone || user.phone,
      updates.address || user.address,
      updates.preferences || user.preferences
    );
  }
  
  async createNewUser(userData) {
    return userAPI.createUser(
      userData.name,
      userData.email,
      userData.phone,
      userData.department.id,
      userData.role.id,
      userData.manager.id,
      userData.startDate
    );
  }
}

// After - Passing whole objects and extracting internally
class UserAPIService {
  updateProfile(user, updates) {
    const merged = { ...user, ...updates };
    
    const payload = {
      name: merged.name,
      email: merged.email,
      phone: merged.phone,
      address: merged.address,
      preferences: merged.preferences
    };
    
    return this.httpClient.put(`/users/${user.id}`, payload);
  }
  
  createUser(userData) {
    const payload = {
      name: userData.name,
      email: userData.email,
      phone: userData.phone,
      departmentId: userData.department.id,
      roleId: userData.role.id,
      managerId: userData.manager.id,
      startDate: userData.startDate.toISOString()
    };
    
    return this.httpClient.post('/users', payload);
  }
}

// Client code - much cleaner
class UserService {
  async updateUserProfile(user, updates) {
    return userAPI.updateProfile(user, updates);
  }
  
  async createNewUser(userData) {
    return userAPI.createUser(userData);
  }
}
```

## Mechanics

1. **Identify parameter groups from the same object**
   - Look for methods that take multiple parameters from the same source object
   - Note which object the parameters come from

2. **Create a parameter for the whole object**
   - Add the source object as a parameter
   - Keep the original parameters temporarily

3. **Update the method body**
   - Replace parameter references with object property access
   - Test that the method still works correctly

4. **Update all callers**
   - Pass the whole object instead of individual values
   - Remove the parameter extraction from calling code

5. **Remove the old parameters**
   - Delete the individual parameters from the method signature
   - Test to ensure everything still works

## When to Use

- **Multiple parameters from same object**: Method takes several values from one object
- **Frequent parameter changes**: Need to add/remove object properties often
- **Related data**: Parameters represent related concepts
- **Object-oriented design**: Want to maintain object relationships
- **API simplification**: Want cleaner method signatures

## When NOT to Use

- **Unrelated parameters**: Parameters come from different objects
- **Performance critical**: Object passing has overhead
- **Security concerns**: Don't want method to access all object data
- **Simple calculations**: Method only needs one or two values
- **Primitive obsession**: When you should be using value objects instead

## Trade-offs

### Benefits
- **Simpler method calls**: Fewer parameters to pass
- **Reduced coupling**: Less knowledge of object structure needed
- **Easier maintenance**: Adding fields doesn't break method signatures
- **More expressive**: Shows relationship between data and operation
- **Future flexibility**: Method can access additional object properties

### Drawbacks
- **Increased coupling**: Method now depends on entire object
- **Performance overhead**: Passing larger objects
- **Encapsulation concerns**: Method may access more than it needs
- **Testing complexity**: Need to create full objects for testing
- **Unclear dependencies**: Harder to see what data method actually uses

## Design Considerations

### Interface Segregation
```javascript
// Sometimes better to create specific interfaces
class PaymentProcessor {
  // Instead of passing whole order
  processPayment(order) {
    // Method might only need payment info
  }
  
  // Consider extracting payment-specific interface
  processPayment(paymentInfo) {
    // paymentInfo = { amount, method, billingAddress }
  }
}
```

### Data Transfer Objects
```javascript
// For complex scenarios, create specific DTOs
class UserRegistrationData {
  constructor(user, account, preferences) {
    this.personalInfo = {
      name: user.name,
      email: user.email,
      phone: user.phone
    };
    this.accountInfo = {
      username: account.username,
      password: account.password
    };
    this.preferences = preferences;
  }
}

class RegistrationService {
  register(registrationData) {
    // Only has access to relevant data
  }
}
```

### Partial Objects
```javascript
// When method only needs subset of properties
class NotificationService {
  sendWelcomeEmail(user) {
    // Method might only need { name, email }
    const emailData = {
      name: user.name,
      email: user.email
    };
    return this.emailService.send('welcome', emailData);
  }
}
```

## Related Refactorings

- [Introduce Parameter Object](introduce-parameter-object.md) - When parameters don't come from existing object
- [Extract Class](extract-class.md) - When object becomes too large
- [Replace Parameter with Query](replace-parameter-with-query.md) - Alternative approach
- [Hide Delegate](hide-delegate.md) - Related to object relationships
- [Encapsulate Record](encapsulate-record.md) - Creating proper objects for data