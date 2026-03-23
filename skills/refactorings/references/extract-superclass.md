---
title: "Extract Superclass"
description: "Remove duplicated code by creating a common superclass to share methods and properties between classes"
category: "Dealing with Inheritance"
tags: ["extract", "superclass", "inheritance", "duplication", "polymorphism"]
related: ["pull-up-method", "pull-up-field", "extract-class", "replace-conditional-with-polymorphism"]
---

# Extract Superclass

Remove duplicated code by creating a common superclass. Allow sharing of common methods and properties between classes.

## Motivation

When you have two or more classes with similar features, you can eliminate duplication by creating a superclass that contains the common elements. This provides:
- **Code reuse**: Common behavior is written once
- **Consistency**: Shared behavior works the same way
- **Maintainability**: Changes to common behavior happen in one place
- **Polymorphism**: Can treat similar objects uniformly

## Example

### Basic Example
```javascript
// Before - Duplicated code in separate classes
class Department {
  constructor(name, staff) {
    this._name = name;
    this._staff = staff;
  }
  
  get name() { return this._name; }
  
  get totalAnnualCost() {
    return this._staff.reduce((sum, person) => sum + person.annualCost, 0);
  }
  
  get headCount() {
    return this._staff.length;
  }
}

class Employee {
  constructor(name, id, annualCost) {
    this._name = name;
    this._id = id;
    this._annualCost = annualCost;
  }
  
  get name() { return this._name; }
  
  get annualCost() { return this._annualCost; }
  
  get id() { return this._id; }
}

// After - Common elements extracted to superclass
class Party {
  constructor(name) {
    this._name = name;
  }
  
  get name() { return this._name; }
  
  // Abstract method - subclasses must implement
  get annualCost() {
    throw new Error('Subclass must implement annualCost');
  }
}

class Department extends Party {
  constructor(name, staff) {
    super(name);
    this._staff = staff;
  }
  
  get annualCost() {
    return this._staff.reduce((sum, person) => sum + person.annualCost, 0);
  }
  
  get headCount() {
    return this._staff.length;
  }
}

class Employee extends Party {
  constructor(name, id, annualCost) {
    super(name);
    this._id = id;
    this._annualCost = annualCost;
  }
  
  get annualCost() { return this._annualCost; }
  
  get id() { return this._id; }
}
```

### Complex Example with Shared Behavior
```javascript
// Before - Multiple classes with similar validation and logging
class BankAccount {
  constructor(accountNumber, balance) {
    this._accountNumber = accountNumber;
    this._balance = balance;
    this._transactions = [];
    this._createdAt = new Date();
  }
  
  deposit(amount) {
    if (amount <= 0) {
      throw new Error('Amount must be positive');
    }
    this._balance += amount;
    this._logTransaction('deposit', amount);
  }
  
  withdraw(amount) {
    if (amount <= 0) {
      throw new Error('Amount must be positive');
    }
    if (amount > this._balance) {
      throw new Error('Insufficient funds');
    }
    this._balance -= amount;
    this._logTransaction('withdrawal', amount);
  }
  
  _logTransaction(type, amount) {
    const transaction = {
      type,
      amount,
      timestamp: new Date(),
      balance: this._balance
    };
    this._transactions.push(transaction);
    console.log(`${type.toUpperCase()}: $${amount}, Balance: $${this._balance}`);
  }
  
  getStatement() {
    return {
      accountNumber: this._accountNumber,
      balance: this._balance,
      transactions: [...this._transactions]
    };
  }
}

class CreditCard {
  constructor(cardNumber, creditLimit) {
    this._cardNumber = cardNumber;
    this._creditLimit = creditLimit;
    this._balance = 0;
    this._transactions = [];
    this._createdAt = new Date();
  }
  
  charge(amount) {
    if (amount <= 0) {
      throw new Error('Amount must be positive');
    }
    if (this._balance + amount > this._creditLimit) {
      throw new Error('Credit limit exceeded');
    }
    this._balance += amount;
    this._logTransaction('charge', amount);
  }
  
  payment(amount) {
    if (amount <= 0) {
      throw new Error('Amount must be positive');
    }
    this._balance -= amount;
    this._logTransaction('payment', amount);
  }
  
  _logTransaction(type, amount) {
    const transaction = {
      type,
      amount,
      timestamp: new Date(),
      balance: this._balance
    };
    this._transactions.push(transaction);
    console.log(`${type.toUpperCase()}: $${amount}, Balance: $${this._balance}`);
  }
  
  getStatement() {
    return {
      cardNumber: this._cardNumber,
      balance: this._balance,
      creditLimit: this._creditLimit,
      transactions: [...this._transactions]
    };
  }
}

// After - Common elements in superclass
class FinancialAccount {
  constructor(accountIdentifier) {
    this._accountIdentifier = accountIdentifier;
    this._balance = 0;
    this._transactions = [];
    this._createdAt = new Date();
  }
  
  get balance() { return this._balance; }
  get accountIdentifier() { return this._accountIdentifier; }
  get transactions() { return [...this._transactions]; }
  
  _validateAmount(amount) {
    if (amount <= 0) {
      throw new Error('Amount must be positive');
    }
  }
  
  _logTransaction(type, amount) {
    const transaction = {
      type,
      amount,
      timestamp: new Date(),
      balance: this._balance
    };
    this._transactions.push(transaction);
    console.log(`${type.toUpperCase()}: $${amount}, Balance: $${this._balance}`);
  }
  
  getStatement() {
    return {
      accountIdentifier: this._accountIdentifier,
      balance: this._balance,
      transactions: [...this._transactions],
      createdAt: this._createdAt
    };
  }
  
  // Template method pattern
  processTransaction(type, amount) {
    this._validateAmount(amount);
    this._validateTransaction(type, amount);
    this._executeTransaction(type, amount);
    this._logTransaction(type, amount);
  }
  
  // Abstract methods - subclasses must implement
  _validateTransaction(type, amount) {
    throw new Error('Subclass must implement _validateTransaction');
  }
  
  _executeTransaction(type, amount) {
    throw new Error('Subclass must implement _executeTransaction');
  }
}

class BankAccount extends FinancialAccount {
  constructor(accountNumber, initialBalance) {
    super(accountNumber);
    this._balance = initialBalance;
  }
  
  deposit(amount) {
    this.processTransaction('deposit', amount);
  }
  
  withdraw(amount) {
    this.processTransaction('withdrawal', amount);
  }
  
  _validateTransaction(type, amount) {
    if (type === 'withdrawal' && amount > this._balance) {
      throw new Error('Insufficient funds');
    }
  }
  
  _executeTransaction(type, amount) {
    if (type === 'deposit') {
      this._balance += amount;
    } else if (type === 'withdrawal') {
      this._balance -= amount;
    }
  }
}

class CreditCard extends FinancialAccount {
  constructor(cardNumber, creditLimit) {
    super(cardNumber);
    this._creditLimit = creditLimit;
  }
  
  get creditLimit() { return this._creditLimit; }
  get availableCredit() { return this._creditLimit - this._balance; }
  
  charge(amount) {
    this.processTransaction('charge', amount);
  }
  
  payment(amount) {
    this.processTransaction('payment', amount);
  }
  
  _validateTransaction(type, amount) {
    if (type === 'charge' && this._balance + amount > this._creditLimit) {
      throw new Error('Credit limit exceeded');
    }
  }
  
  _executeTransaction(type, amount) {
    if (type === 'charge') {
      this._balance += amount;
    } else if (type === 'payment') {
      this._balance -= amount;
    }
  }
  
  getStatement() {
    const baseStatement = super.getStatement();
    return {
      ...baseStatement,
      creditLimit: this._creditLimit,
      availableCredit: this.availableCredit
    };
  }
}
```

## Mechanics

1. **Create an empty superclass**
   - Choose a name that represents the common concept
   - Make it abstract if the language supports it

2. **Make the original classes inherit from the superclass**
   - Use extends, inheritance, or similar mechanism
   - Update constructors to call super()

3. **Move common fields up using Pull Up Field**
   - Start with fields that are identical across classes
   - Move one field at a time
   - Test after each move

4. **Move common methods up using Pull Up Method**
   - Start with methods that are identical
   - Move methods that use the moved fields
   - Consider template methods for similar but not identical methods

5. **Look for template method opportunities**
   - Identify methods with similar structure but different details
   - Create template method in superclass
   - Extract variant parts to abstract methods

6. **Test thoroughly**
   - Ensure all functionality still works
   - Check that polymorphism works as expected

## Design Patterns

### Template Method Pattern
```javascript
class DataProcessor {
  process(data) {
    const validatedData = this.validate(data);
    const transformedData = this.transform(validatedData);
    const result = this.save(transformedData);
    this.cleanup();
    return result;
  }
  
  // Abstract methods - subclasses implement
  validate(data) { throw new Error('Must implement validate'); }
  transform(data) { throw new Error('Must implement transform'); }
  save(data) { throw new Error('Must implement save'); }
  
  // Default implementation that can be overridden
  cleanup() {
    console.log('Default cleanup');
  }
}

class CSVProcessor extends DataProcessor {
  validate(data) {
    // CSV-specific validation
    return data.split(',').filter(row => row.trim());
  }
  
  transform(data) {
    // Convert to objects
    return data.map(row => ({ value: row }));
  }
  
  save(data) {
    // Save to database
    return database.save(data);
  }
}
```

### Strategy Pattern Alternative
```javascript
// Sometimes composition is better than inheritance
class PaymentProcessor {
  constructor(strategy) {
    this._strategy = strategy;
  }
  
  process(amount) {
    return this._strategy.process(amount);
  }
}

class CreditCardStrategy {
  process(amount) {
    // Credit card processing
  }
}

class PayPalStrategy {
  process(amount) {
    // PayPal processing
  }
}
```

## When to Use

- **Duplicated code**: Multiple classes with similar methods or fields
- **Common interface**: Classes that should be treated similarly
- **Template method**: Similar algorithms with different steps
- **Polymorphism**: Need to call the same methods on different objects
- **Code maintenance**: Want to change common behavior in one place

## When NOT to Use

- **Surface similarities**: Classes that look similar but represent different concepts
- **Forced relationships**: Classes that don't have a natural "is-a" relationship
- **Complex inheritance**: When inheritance hierarchy becomes too deep
- **High coupling**: When superclass becomes too dependent on subclasses

## Trade-offs

### Benefits
- **Code reuse**: Common code written once
- **Consistency**: Shared behavior works the same way
- **Polymorphism**: Can treat related objects uniformly
- **Maintenance**: Changes to common behavior centralized
- **Understanding**: Inheritance expresses relationships

### Drawbacks
- **Coupling**: Subclasses tightly coupled to superclass
- **Complexity**: Inheritance hierarchies can be hard to understand
- **Rigidity**: Hard to change superclass without affecting subclasses
- **Fragility**: Changes to superclass can break subclasses
- **Depth**: Deep hierarchies are hard to navigate

## Guidelines

### Prefer Composition over Inheritance
```javascript
// Consider if this makes more sense as composition
class Vehicle {
  constructor(engine) {
    this._engine = engine;
  }
  
  start() {
    this._engine.start();
  }
}

class Engine {
  start() {
    console.log('Engine starting');
  }
}
```

### Keep Hierarchies Shallow
- Avoid more than 3-4 levels of inheritance
- Consider flattening deep hierarchies
- Use composition for complex relationships

### Make Intent Clear
```javascript
// Good - clear "is-a" relationship
class Animal { }
class Dog extends Animal { }

// Questionable - not a clear "is-a" relationship
class Rectangle { }
class Square extends Rectangle { } // Is a square really a rectangle in code?
```

## Related Refactorings

- [Pull Up Field](pull-up-field.md) - Move common fields to superclass
- [Pull Up Method](pull-up-method.md) - Move common methods to superclass
- [Extract Class](extract-class.md) - Alternative to inheritance
- [Replace Inheritance with Delegation](replace-superclass-with-delegate.md) - When inheritance becomes problematic
- [Collapse Hierarchy](collapse-hierarchy.md) - When inheritance becomes unnecessary