---
title: "Move Function"
description: "Move a function from one class to another when it references features of another class more"
category: "Moving Features"
tags: ["move", "function", "organization", "cohesion", "coupling"]
related: ["move-field", "move-statements-into-function", "extract-class"]
---

# Move Function

Move a function from one class to another when it references features of another class more than those of its current class.

## Also Known As

- Move Method

## Motivation

Functions should live where they have the most context and where they work with the most relevant data. Signs a function should move:

- It references another object more than its current host
- It would eliminate or reduce dependencies between classes  
- It logically belongs with related functions in another class
- It's only called by methods in another class
- Moving it would improve cohesion

Good design keeps related elements together and minimizes coupling between classes.

## Example

### Basic Example
```javascript
// Before - Function uses more features of another class
class Account {
  constructor(type, daysOverdrawn) {
    this._type = type;
    this._daysOverdrawn = daysOverdrawn;
  }
  
  get type() { return this._type; }
  get daysOverdrawn() { return this._daysOverdrawn; }
  
  get overdraftCharge() {
    if (this._type.isPremium) {
      const baseCharge = 10;
      if (this._daysOverdrawn <= 7) {
        return baseCharge;
      } else {
        return baseCharge + (this._daysOverdrawn - 7) * 0.85;
      }
    } else {
      return this._daysOverdrawn * 1.75;
    }
  }
  
  get bankCharge() {
    let result = 4.5;
    if (this._daysOverdrawn > 0) {
      result += this.overdraftCharge;
    }
    return result;
  }
}

class AccountType {
  constructor(name, isPremium) {
    this._name = name;
    this._isPremium = isPremium;
  }
  
  get name() { return this._name; }
  get isPremium() { return this._isPremium; }
}

// After - Function moved to class it references more
class Account {
  constructor(type, daysOverdrawn) {
    this._type = type;
    this._daysOverdrawn = daysOverdrawn;
  }
  
  get type() { return this._type; }
  get daysOverdrawn() { return this._daysOverdrawn; }
  
  get overdraftCharge() {
    return this._type.overdraftCharge(this._daysOverdrawn);
  }
  
  get bankCharge() {
    let result = 4.5;
    if (this._daysOverdrawn > 0) {
      result += this.overdraftCharge;
    }
    return result;
  }
}

class AccountType {
  constructor(name, isPremium) {
    this._name = name;
    this._isPremium = isPremium;
  }
  
  get name() { return this._name; }
  get isPremium() { return this._isPremium; }
  
  overdraftCharge(daysOverdrawn) {
    if (this._isPremium) {
      const baseCharge = 10;
      if (daysOverdrawn <= 7) {
        return baseCharge;
      } else {
        return baseCharge + (daysOverdrawn - 7) * 0.85;
      }
    } else {
      return daysOverdrawn * 1.75;
    }
  }
}
```

### Complex Example - Moving Related Functions
```javascript
// Before - Functions in wrong class
class TrackingService {
  constructor() {
    this._shipments = [];
  }
  
  trackShipment(shipment) {
    this._shipments.push(shipment);
    this.sendTrackingEmail(shipment);
    this.updateTrackingDatabase(shipment);
  }
  
  sendTrackingEmail(shipment) {
    const customer = shipment.customer;
    const trackingInfo = this.generateTrackingInfo(shipment);
    
    emailService.send({
      to: customer.email,
      subject: `Tracking info for order ${shipment.orderId}`,
      body: trackingInfo
    });
  }
  
  generateTrackingInfo(shipment) {
    return `
      Order: ${shipment.orderId}
      Status: ${shipment.status}
      Tracking Number: ${shipment.trackingNumber}
      Estimated Delivery: ${shipment.estimatedDelivery}
      Current Location: ${shipment.currentLocation}
    `;
  }
  
  updateTrackingDatabase(shipment) {
    database.updateTracking(shipment.trackingNumber, {
      status: shipment.status,
      location: shipment.currentLocation,
      lastUpdate: new Date()
    });
  }
  
  getShipmentLocation(trackingNumber) {
    const shipment = this._shipments.find(s => s.trackingNumber === trackingNumber);
    return shipment ? shipment.currentLocation : 'Unknown';
  }
}

class Shipment {
  constructor(orderId, customer, trackingNumber) {
    this._orderId = orderId;
    this._customer = customer;
    this._trackingNumber = trackingNumber;
    this._status = 'pending';
    this._currentLocation = 'warehouse';
    this._estimatedDelivery = null;
  }
  
  // Just data accessors
  get orderId() { return this._orderId; }
  get customer() { return this._customer; }
  get trackingNumber() { return this._trackingNumber; }
  get status() { return this._status; }
  get currentLocation() { return this._currentLocation; }
  get estimatedDelivery() { return this._estimatedDelivery; }
}

// After - Functions moved to where they belong
class TrackingService {
  constructor() {
    this._shipments = [];
  }
  
  trackShipment(shipment) {
    this._shipments.push(shipment);
    shipment.notifyCustomer();
    shipment.updateTrackingDatabase();
  }
  
  findShipment(trackingNumber) {
    return this._shipments.find(s => s.trackingNumber === trackingNumber);
  }
}

class Shipment {
  constructor(orderId, customer, trackingNumber) {
    this._orderId = orderId;
    this._customer = customer;
    this._trackingNumber = trackingNumber;
    this._status = 'pending';
    this._currentLocation = 'warehouse';
    this._estimatedDelivery = null;
  }
  
  get orderId() { return this._orderId; }
  get customer() { return this._customer; }
  get trackingNumber() { return this._trackingNumber; }
  get status() { return this._status; }
  get currentLocation() { return this._currentLocation; }
  get estimatedDelivery() { return this._estimatedDelivery; }
  
  updateStatus(newStatus, location) {
    this._status = newStatus;
    this._currentLocation = location;
    this.updateTrackingDatabase();
  }
  
  notifyCustomer() {
    emailService.send({
      to: this._customer.email,
      subject: `Tracking info for order ${this._orderId}`,
      body: this.generateTrackingInfo()
    });
  }
  
  generateTrackingInfo() {
    return `
      Order: ${this._orderId}
      Status: ${this._status}
      Tracking Number: ${this._trackingNumber}
      Estimated Delivery: ${this._estimatedDelivery || 'TBD'}
      Current Location: ${this._currentLocation}
    `;
  }
  
  updateTrackingDatabase() {
    database.updateTracking(this._trackingNumber, {
      status: this._status,
      location: this._currentLocation,
      lastUpdate: new Date()
    });
  }
}
```

### Moving Static Utility Functions
```javascript
// Before - Utility functions in the wrong place
class OrderController {
  processOrder(orderData) {
    const validatedData = this.validateOrderData(orderData);
    const pricedOrder = this.calculatePricing(validatedData);
    const order = new Order(pricedOrder);
    return order;
  }
  
  validateOrderData(data) {
    if (!data.items || data.items.length === 0) {
      throw new Error('Order must have items');
    }
    
    data.items.forEach(item => {
      if (!item.productId || !item.quantity) {
        throw new Error('Invalid item data');
      }
      if (item.quantity <= 0) {
        throw new Error('Quantity must be positive');
      }
    });
    
    if (!data.customerId) {
      throw new Error('Customer ID required');
    }
    
    return data;
  }
  
  calculatePricing(orderData) {
    const subtotal = orderData.items.reduce((sum, item) => {
      const product = productService.getProduct(item.productId);
      return sum + (product.price * item.quantity);
    }, 0);
    
    const tax = subtotal * 0.08;
    const shipping = this.calculateShipping(orderData.items);
    
    return {
      ...orderData,
      subtotal,
      tax,
      shipping,
      total: subtotal + tax + shipping
    };
  }
  
  calculateShipping(items) {
    const weight = items.reduce((sum, item) => {
      const product = productService.getProduct(item.productId);
      return sum + (product.weight * item.quantity);
    }, 0);
    
    return weight * 0.5 + 5; // $0.50 per pound plus $5 base
  }
}

// After - Functions moved to appropriate classes
class OrderController {
  processOrder(orderData) {
    const order = Order.createFromData(orderData);
    return order;
  }
}

class Order {
  constructor(data) {
    this._customerId = data.customerId;
    this._items = data.items;
    this._subtotal = data.subtotal;
    this._tax = data.tax;
    this._shipping = data.shipping;
    this._total = data.total;
  }
  
  static createFromData(orderData) {
    const validatedData = Order.validateOrderData(orderData);
    const pricedData = Order.calculatePricing(validatedData);
    return new Order(pricedData);
  }
  
  static validateOrderData(data) {
    if (!data.items || data.items.length === 0) {
      throw new Error('Order must have items');
    }
    
    data.items.forEach(item => {
      OrderItem.validate(item);
    });
    
    if (!data.customerId) {
      throw new Error('Customer ID required');
    }
    
    return data;
  }
  
  static calculatePricing(orderData) {
    const items = orderData.items.map(item => new OrderItem(item));
    const subtotal = items.reduce((sum, item) => sum + item.totalPrice, 0);
    const tax = subtotal * 0.08;
    const shipping = Order.calculateShipping(items);
    
    return {
      ...orderData,
      subtotal,
      tax,
      shipping,
      total: subtotal + tax + shipping
    };
  }
  
  static calculateShipping(items) {
    const totalWeight = items.reduce((sum, item) => sum + item.totalWeight, 0);
    return totalWeight * 0.5 + 5; // $0.50 per pound plus $5 base
  }
}

class OrderItem {
  constructor(data) {
    this._productId = data.productId;
    this._quantity = data.quantity;
    this._product = productService.getProduct(data.productId);
  }
  
  static validate(data) {
    if (!data.productId || !data.quantity) {
      throw new Error('Invalid item data');
    }
    if (data.quantity <= 0) {
      throw new Error('Quantity must be positive');
    }
  }
  
  get totalPrice() {
    return this._product.price * this._quantity;
  }
  
  get totalWeight() {
    return this._product.weight * this._quantity;
  }
}
```

## Mechanics

1. **Examine the function's dependencies**
   - What data does it use from its current class?
   - What data does it use from other classes?
   - Which class does it reference more?

2. **Copy the function to the target class**
   - Give it an appropriate name in the new context
   - Adjust parameters as needed

3. **Adjust the function in its new home**
   - Replace references to the source object with parameters
   - Use features of the new host class directly

4. **Replace the original function body**
   - Delegate to the new function
   - Or inline the call if simple enough

5. **Update all callers**
   - Change to call the function in its new location
   - Remove the delegating function when done

6. **Test thoroughly**
   - Ensure all calling code still works
   - Verify the function works correctly in its new context

## When to Use

- **Feature envy**: Function uses another class's features extensively
- **Inappropriate intimacy**: Function knows too much about another class
- **Message chains**: Function navigates through multiple objects
- **Data class improvement**: Adding behavior to data-heavy classes
- **Reducing coupling**: Move function to reduce dependencies

## Trade-offs

### Benefits
- **Better cohesion**: Related functions stay together
- **Reduced coupling**: Less dependency between classes
- **Clearer responsibilities**: Each class has appropriate behavior
- **Easier testing**: Functions have better access to needed data

### Drawbacks
- **Breaking changes**: May affect many callers
- **Complex dependencies**: Some functions are hard to move
- **Performance**: May add indirection or parameter passing
- **Design disruption**: Can require rethinking class relationships

## Patterns and Variations

### Moving to a Parameter
```javascript
// When function mainly works with a parameter
class Renderer {
  renderPerson(person) {
    return `<div>
      <h1>${person.name}</h1>
      <p>Age: ${person.age}</p>
      <p>Email: ${person.email}</p>
    </div>`;
  }
}

// Move to Person class
class Person {
  renderHTML() {
    return `<div>
      <h1>${this.name}</h1>
      <p>Age: ${this.age}</p>
      <p>Email: ${this.email}</p>
    </div>`;
  }
}
```

### Moving to a New Class
```javascript
// When function doesn't fit anywhere, create new class
class Order {
  // Complex tax calculation doesn't really belong here
  calculateTax() {
    // Complex tax logic
  }
}

// Create TaxCalculator
class TaxCalculator {
  calculateForOrder(order) {
    // Complex tax logic
  }
}
```

### Moving Static Methods
```javascript
// Static methods are easier to move
class DateUtils {
  static formatDate(date) {
    return date.toISOString().split('T')[0];
  }
}

// Can move to Date prototype or new module
Date.prototype.formatSimple = function() {
  return this.toISOString().split('T')[0];
};
```

## Common Scenarios

### Moving Validation Logic
```javascript
// Before - Validation in controller
class UserController {
  validateUser(userData) {
    // Validation logic
  }
}

// After - Validation in model
class User {
  static validate(userData) {
    // Validation logic
  }
}
```

### Moving Business Rules
```javascript
// Before - Business rule in service
class OrderService {
  canBeCancelled(order) {
    return order.status === 'pending' && 
           order.createdAt > Date.now() - 3600000;
  }
}

// After - Business rule in domain object
class Order {
  canBeCancelled() {
    return this.status === 'pending' && 
           this.createdAt > Date.now() - 3600000;
  }
}
```

### Moving Calculations
```javascript
// Before - Calculation in wrong place
class ShoppingCart {
  calculateItemDiscount(item, customer) {
    if (customer.isVIP) {
      return item.price * 0.2;
    }
    return 0;
  }
}

// After - Calculation where it belongs
class Customer {
  calculateDiscountForItem(item) {
    if (this.isVIP) {
      return item.price * 0.2;
    }
    return 0;
  }
}
```

## Related Refactorings

- [Move Field](move-field.md) - Often done together
- [Extract Function](extract-function.md) - Prepare complex functions for moving
- [Inline Function](inline-function.md) - Alternative to moving simple functions
- [Extract Class](extract-class.md) - When many functions should move together
- [Hide Delegate](hide-delegate.md) - Alternative to moving