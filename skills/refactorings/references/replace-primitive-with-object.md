---
title: "Replace Primitive with Object"
description: "Replace a primitive value with a small class that provides encapsulation, validation, and behavior"
category: "Organizing Data"
tags: ["primitive", "object", "encapsulation", "validation", "domain-object"]
related: ["encapsulate-record", "extract-class", "introduce-parameter-object"]
---

# Replace Primitive with Object

Replace a primitive value (string, number, boolean) with a small class that provides better encapsulation, validation, and behavior related to that data.

## Motivation

Using primitive types for domain concepts creates several problems:

- **Lost domain meaning**: A string could represent anything
- **No validation**: Primitive values can't validate themselves
- **Scattered behavior**: Related logic is spread across the codebase
- **Type confusion**: Easy to mix up similar primitive values
- **No encapsulation**: No way to control how the value is accessed or modified
- **Poor expressiveness**: Code doesn't clearly communicate domain concepts

## Example

### Basic Example
```javascript
// Before - Using primitive strings for phone numbers
class Customer {
  constructor(name, phoneNumber) {
    this._name = name;
    this._phoneNumber = phoneNumber; // Just a string
  }
  
  get phoneNumber() {
    return this._phoneNumber;
  }
  
  set phoneNumber(value) {
    // Validation scattered wherever phone numbers are set
    if (!value.match(/^\+?[1-9]\d{1,14}$/)) {
      throw new Error('Invalid phone number format');
    }
    this._phoneNumber = value;
  }
  
  getFormattedPhoneNumber() {
    // Formatting logic in the customer class
    if (this._phoneNumber.startsWith('+1')) {
      const number = this._phoneNumber.slice(2);
      return `(${number.slice(0, 3)}) ${number.slice(3, 6)}-${number.slice(6)}`;
    }
    return this._phoneNumber;
  }
  
  canReceiveSMS() {
    // Business logic mixed with customer logic
    return this._phoneNumber.startsWith('+1') || this._phoneNumber.startsWith('+44');
  }
}

// Validation and formatting logic repeated elsewhere
function validatePhoneNumber(phoneNumber) {
  return phoneNumber.match(/^\+?[1-9]\d{1,14}$/);
}

function formatPhoneNumber(phoneNumber) {
  if (phoneNumber.startsWith('+1')) {
    const number = phoneNumber.slice(2);
    return `(${number.slice(0, 3)}) ${number.slice(3, 6)}-${number.slice(6)}`;
  }
  return phoneNumber;
}

// After - Phone number as a proper object
class PhoneNumber {
  constructor(value) {
    this._value = this._validate(value);
  }
  
  static isValid(value) {
    return /^\+?[1-9]\d{1,14}$/.test(value);
  }
  
  _validate(value) {
    if (!PhoneNumber.isValid(value)) {
      throw new Error('Invalid phone number format');
    }
    return value;
  }
  
  get value() {
    return this._value;
  }
  
  get countryCode() {
    if (this._value.startsWith('+')) {
      const match = this._value.match(/^\+(\d{1,3})/);
      return match ? match[1] : null;
    }
    return null;
  }
  
  get nationalNumber() {
    if (this._value.startsWith('+')) {
      const countryCode = this.countryCode;
      return this._value.slice(countryCode.length + 1);
    }
    return this._value;
  }
  
  isUSNumber() {
    return this._value.startsWith('+1');
  }
  
  isUKNumber() {
    return this._value.startsWith('+44');
  }
  
  canReceiveSMS() {
    return this.isUSNumber() || this.isUKNumber();
  }
  
  formatForDisplay() {
    if (this.isUSNumber()) {
      const number = this.nationalNumber;
      if (number.length === 10) {
        return `(${number.slice(0, 3)}) ${number.slice(3, 6)}-${number.slice(6)}`;
      }
    }
    return this._value;
  }
  
  formatForInternational() {
    return this._value.startsWith('+') ? this._value : `+${this._value}`;
  }
  
  equals(other) {
    return other instanceof PhoneNumber && this._value === other._value;
  }
  
  toString() {
    return this._value;
  }
}

class Customer {
  constructor(name, phoneNumber) {
    this._name = name;
    this._phoneNumber = new PhoneNumber(phoneNumber);
  }
  
  get phoneNumber() {
    return this._phoneNumber;
  }
  
  set phoneNumber(value) {
    this._phoneNumber = new PhoneNumber(value);
  }
  
  getFormattedPhoneNumber() {
    return this._phoneNumber.formatForDisplay();
  }
  
  canReceiveSMS() {
    return this._phoneNumber.canReceiveSMS();
  }
}

// Usage is now clearer and safer
const customer = new Customer('John Doe', '+14155552345');
console.log(customer.phoneNumber.formatForDisplay()); // (415) 555-2345
console.log(customer.phoneNumber.countryCode); // 1
console.log(customer.canReceiveSMS()); // true
```

### Complex Example - Money and Currency
```javascript
// Before - Using numbers for money (problematic!)
class Order {
  constructor(items) {
    this._items = items;
    this._subtotal = 0;
    this._tax = 0;
    this._shipping = 0;
    this._currency = 'USD'; // String for currency
  }
  
  addItem(name, price, quantity = 1) {
    // Price is just a number - no currency information
    this._items.push({ name, price, quantity });
    this._subtotal += price * quantity;
  }
  
  calculateTax(rate) {
    // Floating point arithmetic issues
    this._tax = this._subtotal * rate;
  }
  
  calculateShipping(cost) {
    this._shipping = cost;
  }
  
  getTotal() {
    // More floating point issues
    return this._subtotal + this._tax + this._shipping;
  }
  
  // Currency conversion is complex and error-prone
  convertToCurrency(targetCurrency, exchangeRate) {
    if (this._currency === targetCurrency) {
      return {
        subtotal: this._subtotal,
        tax: this._tax,
        shipping: this._shipping,
        total: this.getTotal(),
        currency: this._currency
      };
    }
    
    return {
      subtotal: this._subtotal * exchangeRate,
      tax: this._tax * exchangeRate,
      shipping: this._shipping * exchangeRate,
      total: this.getTotal() * exchangeRate,
      currency: targetCurrency
    };
  }
  
  formatPrice(amount) {
    // Formatting logic scattered everywhere
    if (this._currency === 'USD') {
      return `$${amount.toFixed(2)}`;
    } else if (this._currency === 'EUR') {
      return `€${amount.toFixed(2)}`;
    } else if (this._currency === 'GBP') {
      return `£${amount.toFixed(2)}`;
    }
    return `${amount.toFixed(2)} ${this._currency}`;
  }
}

// After - Money as a proper value object
class Money {
  constructor(amount, currency = 'USD') {
    this._amount = this._validateAmount(amount);
    this._currency = this._validateCurrency(currency);
  }
  
  static zero(currency = 'USD') {
    return new Money(0, currency);
  }
  
  static fromCents(cents, currency = 'USD') {
    return new Money(cents / 100, currency);
  }
  
  _validateAmount(amount) {
    if (typeof amount !== 'number' || !isFinite(amount)) {
      throw new Error('Amount must be a finite number');
    }
    // Store as cents to avoid floating point issues
    return Math.round(amount * 100);
  }
  
  _validateCurrency(currency) {
    const validCurrencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD'];
    if (!validCurrencies.includes(currency)) {
      throw new Error(`Unsupported currency: ${currency}`);
    }
    return currency;
  }
  
  get amount() {
    return this._amount / 100;
  }
  
  get currency() {
    return this._currency;
  }
  
  get cents() {
    return this._amount;
  }
  
  add(other) {
    this._ensureSameCurrency(other);
    return new Money((this._amount + other._amount) / 100, this._currency);
  }
  
  subtract(other) {
    this._ensureSameCurrency(other);
    return new Money((this._amount - other._amount) / 100, this._currency);
  }
  
  multiply(factor) {
    if (typeof factor !== 'number') {
      throw new Error('Factor must be a number');
    }
    return new Money((this._amount * factor) / 100, this._currency);
  }
  
  divide(divisor) {
    if (typeof divisor !== 'number' || divisor === 0) {
      throw new Error('Divisor must be a non-zero number');
    }
    return new Money((this._amount / divisor) / 100, this._currency);
  }
  
  convertTo(targetCurrency, exchangeRate) {
    if (this._currency === targetCurrency) {
      return this;
    }
    
    if (typeof exchangeRate !== 'number' || exchangeRate <= 0) {
      throw new Error('Exchange rate must be a positive number');
    }
    
    return new Money(this.amount * exchangeRate, targetCurrency);
  }
  
  equals(other) {
    return other instanceof Money && 
           this._amount === other._amount && 
           this._currency === other._currency;
  }
  
  isGreaterThan(other) {
    this._ensureSameCurrency(other);
    return this._amount > other._amount;
  }
  
  isLessThan(other) {
    this._ensureSameCurrency(other);
    return this._amount < other._amount;
  }
  
  isZero() {
    return this._amount === 0;
  }
  
  format() {
    const symbols = {
      'USD': '$',
      'EUR': '€',
      'GBP': '£',
      'JPY': '¥',
      'CAD': 'C$'
    };
    
    const symbol = symbols[this._currency] || this._currency;
    const formatted = this.amount.toFixed(2);
    
    if (this._currency === 'JPY') {
      // Japanese Yen doesn't use decimal places
      return `${symbol}${Math.round(this.amount)}`;
    }
    
    return `${symbol}${formatted}`;
  }
  
  _ensureSameCurrency(other) {
    if (!(other instanceof Money)) {
      throw new Error('Operand must be a Money instance');
    }
    if (this._currency !== other._currency) {
      throw new Error(`Currency mismatch: ${this._currency} vs ${other._currency}`);
    }
  }
  
  toString() {
    return this.format();
  }
}

class Order {
  constructor() {
    this._items = [];
    this._currency = 'USD';
  }
  
  addItem(name, price, quantity = 1) {
    // Price is now a Money object with validation and behavior
    if (!(price instanceof Money)) {
      throw new Error('Price must be a Money instance');
    }
    
    this._items.push({ 
      name, 
      price, 
      quantity,
      lineTotal: price.multiply(quantity)
    });
  }
  
  getSubtotal() {
    return this._items.reduce((sum, item) => {
      return sum.add(item.lineTotal);
    }, Money.zero(this._currency));
  }
  
  calculateTax(rate) {
    return this.getSubtotal().multiply(rate);
  }
  
  calculateShipping(cost) {
    if (!(cost instanceof Money)) {
      throw new Error('Shipping cost must be a Money instance');
    }
    return cost;
  }
  
  getTotal(taxRate = 0, shippingCost = Money.zero(this._currency)) {
    const subtotal = this.getSubtotal();
    const tax = this.calculateTax(taxRate);
    const shipping = this.calculateShipping(shippingCost);
    
    return subtotal.add(tax).add(shipping);
  }
  
  convertToCurrency(targetCurrency, exchangeRate) {
    const convertedItems = this._items.map(item => ({
      ...item,
      price: item.price.convertTo(targetCurrency, exchangeRate),
      lineTotal: item.lineTotal.convertTo(targetCurrency, exchangeRate)
    }));
    
    const convertedOrder = new Order();
    convertedOrder._items = convertedItems;
    convertedOrder._currency = targetCurrency;
    
    return convertedOrder;
  }
  
  getOrderSummary() {
    const subtotal = this.getSubtotal();
    const tax = this.calculateTax(0.08); // 8% tax
    const shipping = Money.fromCents(500, this._currency); // $5.00 shipping
    const total = this.getTotal(0.08, shipping);
    
    return {
      subtotal: subtotal.format(),
      tax: tax.format(),
      shipping: shipping.format(),
      total: total.format()
    };
  }
}

// Usage is much safer and more expressive
const order = new Order();
order.addItem('Widget', new Money(29.99), 2);
order.addItem('Gadget', new Money(15.50), 1);

const summary = order.getOrderSummary();
console.log(summary); // { subtotal: '$75.48', tax: '$6.04', shipping: '$5.00', total: '$86.52' }

// Currency conversion is safe and explicit
const eurOrder = order.convertToCurrency('EUR', 0.85);
console.log(eurOrder.getSubtotal().format()); // €64.16
```

### Email Address Example
```javascript
// Before - Email as string with scattered validation
class User {
  constructor(name, email) {
    this._name = name;
    this._email = email; // Just a string
  }
  
  setEmail(email) {
    // Validation repeated everywhere
    if (!email.includes('@') || !email.includes('.')) {
      throw new Error('Invalid email');
    }
    this._email = email.toLowerCase();
  }
  
  getEmailDomain() {
    return this._email.split('@')[1];
  }
  
  getEmailLocalPart() {
    return this._email.split('@')[0];
  }
  
  isCompanyEmail() {
    const companyDomains = ['company.com', 'subsidiary.com'];
    return companyDomains.includes(this.getEmailDomain());
  }
}

// After - Email as a value object
class EmailAddress {
  constructor(email) {
    this._value = this._validate(email);
  }
  
  static isValid(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
  
  _validate(email) {
    if (!email || typeof email !== 'string') {
      throw new Error('Email must be a non-empty string');
    }
    
    const normalized = email.toLowerCase().trim();
    
    if (!EmailAddress.isValid(normalized)) {
      throw new Error('Invalid email format');
    }
    
    return normalized;
  }
  
  get value() {
    return this._value;
  }
  
  get localPart() {
    return this._value.split('@')[0];
  }
  
  get domain() {
    return this._value.split('@')[1];
  }
  
  get topLevelDomain() {
    const parts = this.domain.split('.');
    return parts[parts.length - 1];
  }
  
  isFromDomain(domain) {
    return this.domain === domain.toLowerCase();
  }
  
  isFromDomains(domains) {
    return domains.some(domain => this.isFromDomain(domain));
  }
  
  isGmail() {
    return this.isFromDomain('gmail.com');
  }
  
  isOutlook() {
    return this.isFromDomains(['outlook.com', 'hotmail.com', 'live.com']);
  }
  
  isCorporate() {
    const personalProviders = [
      'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
      'live.com', 'aol.com', 'icloud.com'
    ];
    return !this.isFromDomains(personalProviders);
  }
  
  obfuscate() {
    const [local, domain] = this._value.split('@');
    const obfuscatedLocal = local.length > 2 
      ? local[0] + '*'.repeat(local.length - 2) + local[local.length - 1]
      : local[0] + '*';
    return `${obfuscatedLocal}@${domain}`;
  }
  
  equals(other) {
    return other instanceof EmailAddress && this._value === other._value;
  }
  
  toString() {
    return this._value;
  }
}

class User {
  constructor(name, email) {
    this._name = name;
    this._email = new EmailAddress(email);
  }
  
  get email() {
    return this._email;
  }
  
  setEmail(email) {
    this._email = new EmailAddress(email);
  }
  
  isCompanyEmail() {
    return this._email.isFromDomains(['company.com', 'subsidiary.com']);
  }
  
  getObfuscatedEmail() {
    return this._email.obfuscate();
  }
}

// Usage is safer and more expressive
const user = new User('John Doe', 'john.doe@company.com');
console.log(user.email.domain); // company.com
console.log(user.email.isCorporate()); // true
console.log(user.getObfuscatedEmail()); // j*****e@company.com
```

## Mechanics

1. **Identify primitive obsession**
   - Look for primitive values that represent domain concepts
   - Find repeated validation or formatting logic
   - Check for primitive values with business rules

2. **Create the value object class**
   - Create a new class for the domain concept
   - Add validation in the constructor
   - Make the class immutable if possible

3. **Add behavior to the class**
   - Move related methods from other classes
   - Add domain-specific operations
   - Include formatting and comparison methods

4. **Replace primitive usage**
   - Update fields to use the new class
   - Modify constructors and setters
   - Update method parameters and return types

5. **Move related logic**
   - Move validation logic to the value object
   - Move formatting and parsing logic
   - Move domain-specific operations

6. **Test thoroughly**
   - Test all validation scenarios
   - Verify behavior is preserved
   - Check that all usages are updated

## When to Use

- **Domain concepts**: Primitive represents a meaningful domain concept
- **Validation needed**: Value requires validation rules
- **Behavior exists**: Logic related to the value is scattered
- **Type safety**: Need to prevent mixing up similar primitive values
- **Formatting required**: Value needs specific display formatting
- **Business rules**: Value has associated business logic

## Trade-offs

### Benefits
- **Better encapsulation**: Validation and behavior are contained
- **Type safety**: Harder to mix up different kinds of values
- **Expressiveness**: Code clearly shows domain concepts
- **Centralized logic**: Related behavior is in one place
- **Immutability**: Value objects can be made immutable
- **Reusability**: Value objects can be used across different contexts

### Drawbacks
- **Increased complexity**: More classes to maintain
- **Performance overhead**: Object creation vs primitive values
- **Learning curve**: Team needs to understand value objects
- **Serialization**: May complicate data persistence and transfer

## Value Object Patterns

### Immutable Value Objects
```javascript
class Temperature {
  constructor(value, unit = 'celsius') {
    this._value = value;
    this._unit = unit;
    Object.freeze(this); // Make immutable
  }
  
  toCelsius() {
    if (this._unit === 'fahrenheit') {
      return new Temperature((this._value - 32) * 5/9, 'celsius');
    }
    return this;
  }
  
  toFahrenheit() {
    if (this._unit === 'celsius') {
      return new Temperature(this._value * 9/5 + 32, 'fahrenheit');
    }
    return this;
  }
}
```

### Factory Methods
```javascript
class Duration {
  constructor(milliseconds) {
    this._milliseconds = milliseconds;
  }
  
  static fromSeconds(seconds) {
    return new Duration(seconds * 1000);
  }
  
  static fromMinutes(minutes) {
    return new Duration(minutes * 60 * 1000);
  }
  
  static fromHours(hours) {
    return new Duration(hours * 60 * 60 * 1000);
  }
}
```

### Comparison Methods
```javascript
class Version {
  constructor(major, minor, patch) {
    this._major = major;
    this._minor = minor;
    this._patch = patch;
  }
  
  isGreaterThan(other) {
    if (this._major !== other._major) {
      return this._major > other._major;
    }
    if (this._minor !== other._minor) {
      return this._minor > other._minor;
    }
    return this._patch > other._patch;
  }
  
  equals(other) {
    return this._major === other._major &&
           this._minor === other._minor &&
           this._patch === other._patch;
  }
}
```

## Related Refactorings

- [Extract Class](extract-class.md) - Create the value object class
- [Move Method](move-method.md) - Move behavior to the value object
- [Introduce Parameter Object](introduce-parameter-object.md) - Group related primitives
- [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md) - Alternative for enums
- [Change Reference to Value](change-reference-to-value.md) - Make objects value-based