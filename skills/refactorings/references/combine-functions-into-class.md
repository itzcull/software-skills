---
title: "Combine Functions into Class"
description: "Transform a set of functions that operate on the same data into a class with methods and fields"
category: "Organization"
tags: ["class", "organization", "encapsulation", "functions", "data", "methods"]
related: ["combine-functions-into-transform", "extract-class", "move-function"]
---

# Combine Functions into Class

Transform a set of functions that operate on the same data into a class where the functions become methods and the data becomes fields. This improves organization and encapsulation.

## Motivation

Related functions that operate on shared data create several problems when kept separate:

- **Scattered functionality**: Related operations are spread across different functions
- **Parameter repetition**: Same data passed to multiple functions repeatedly
- **Poor organization**: Hard to find all operations that work with specific data
- **Lack of encapsulation**: Data and behavior are separated
- **Difficult maintenance**: Changes to data structure require updating many functions
- **Missing abstraction**: No clear conceptual entity that groups related operations

## Example

### Basic Example
```javascript
// Before - Separate functions operating on same data
function calculateCircleArea(radius) {
  return Math.PI * radius * radius;
}

function calculateCircleCircumference(radius) {
  return 2 * Math.PI * radius;
}

function calculateCircleDiameter(radius) {
  return radius * 2;
}

function isValidCircle(radius) {
  return radius > 0;
}

function formatCircleInfo(radius) {
  if (!isValidCircle(radius)) {
    return 'Invalid circle';
  }
  
  return `Circle - Radius: ${radius}, Area: ${calculateCircleArea(radius).toFixed(2)}, Circumference: ${calculateCircleCircumference(radius).toFixed(2)}`;
}

function scaleCircle(radius, factor) {
  return radius * factor;
}

// Usage - repetitive parameter passing
const radius = 5;
const area = calculateCircleArea(radius);
const circumference = calculateCircleCircumference(radius);
const diameter = calculateCircleDiameter(radius);
const info = formatCircleInfo(radius);
const scaledRadius = scaleCircle(radius, 2);

// After - Organized into a class
class Circle {
  constructor(radius) {
    if (radius <= 0) {
      throw new Error('Radius must be positive');
    }
    this._radius = radius;
  }
  
  get radius() {
    return this._radius;
  }
  
  get area() {
    return Math.PI * this._radius * this._radius;
  }
  
  get circumference() {
    return 2 * Math.PI * this._radius;
  }
  
  get diameter() {
    return this._radius * 2;
  }
  
  isValid() {
    return this._radius > 0;
  }
  
  toString() {
    return `Circle - Radius: ${this._radius}, Area: ${this.area.toFixed(2)}, Circumference: ${this.circumference.toFixed(2)}`;
  }
  
  scale(factor) {
    if (factor <= 0) {
      throw new Error('Scale factor must be positive');
    }
    return new Circle(this._radius * factor);
  }
  
  // Additional methods that make sense in the context
  contains(point) {
    const distance = Math.sqrt(point.x * point.x + point.y * point.y);
    return distance <= this._radius;
  }
  
  equals(other) {
    return other instanceof Circle && Math.abs(this._radius - other._radius) < 0.001;
  }
}

// Usage - cleaner and more organized
const circle = new Circle(5);
const area = circle.area;
const circumference = circle.circumference;
const diameter = circle.diameter;
const info = circle.toString();
const scaledCircle = circle.scale(2);
```

### Advanced Example - Financial Calculations
```javascript
// Before - Scattered financial functions
function calculateMonthlyPayment(principal, annualRate, termYears) {
  const monthlyRate = annualRate / 12;
  const numPayments = termYears * 12;
  
  if (monthlyRate === 0) {
    return principal / numPayments;
  }
  
  return principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / 
         (Math.pow(1 + monthlyRate, numPayments) - 1);
}

function calculateTotalPayment(principal, annualRate, termYears) {
  const monthlyPayment = calculateMonthlyPayment(principal, annualRate, termYears);
  return monthlyPayment * termYears * 12;
}

function calculateTotalInterest(principal, annualRate, termYears) {
  const totalPayment = calculateTotalPayment(principal, annualRate, termYears);
  return totalPayment - principal;
}

function calculateRemainingBalance(principal, annualRate, termYears, paymentsMade) {
  const monthlyRate = annualRate / 12;
  const numPayments = termYears * 12;
  const monthlyPayment = calculateMonthlyPayment(principal, annualRate, termYears);
  
  if (paymentsMade >= numPayments) {
    return 0;
  }
  
  return principal * Math.pow(1 + monthlyRate, paymentsMade) - 
         monthlyPayment * ((Math.pow(1 + monthlyRate, paymentsMade) - 1) / monthlyRate);
}

function generateAmortizationSchedule(principal, annualRate, termYears) {
  const monthlyPayment = calculateMonthlyPayment(principal, annualRate, termYears);
  const monthlyRate = annualRate / 12;
  const numPayments = termYears * 12;
  const schedule = [];
  
  let balance = principal;
  
  for (let payment = 1; payment <= numPayments; payment++) {
    const interestPayment = balance * monthlyRate;
    const principalPayment = monthlyPayment - interestPayment;
    balance -= principalPayment;
    
    schedule.push({
      payment,
      principalPayment: Math.round(principalPayment * 100) / 100,
      interestPayment: Math.round(interestPayment * 100) / 100,
      totalPayment: Math.round(monthlyPayment * 100) / 100,
      balance: Math.round(Math.max(0, balance) * 100) / 100
    });
  }
  
  return schedule;
}

// Usage - repetitive parameter passing
const principal = 200000;
const rate = 0.045;
const term = 30;

const monthlyPayment = calculateMonthlyPayment(principal, rate, term);
const totalPayment = calculateTotalPayment(principal, rate, term);
const totalInterest = calculateTotalInterest(principal, rate, term);
const remainingAfter60 = calculateRemainingBalance(principal, rate, term, 60);
const schedule = generateAmortizationSchedule(principal, rate, term);

// After - Organized into a class
class Loan {
  constructor(principal, annualRate, termYears) {
    this._validateInputs(principal, annualRate, termYears);
    
    this._principal = principal;
    this._annualRate = annualRate;
    this._termYears = termYears;
    
    // Derived properties
    this._monthlyRate = annualRate / 12;
    this._numPayments = termYears * 12;
    this._monthlyPayment = this._calculateMonthlyPayment();
  }
  
  // Getters for loan properties
  get principal() { return this._principal; }
  get annualRate() { return this._annualRate; }
  get termYears() { return this._termYears; }
  get monthlyRate() { return this._monthlyRate; }
  get numPayments() { return this._numPayments; }
  get monthlyPayment() { return this._monthlyPayment; }
  
  // Calculated properties
  get totalPayment() {
    return this._monthlyPayment * this._numPayments;
  }
  
  get totalInterest() {
    return this.totalPayment - this._principal;
  }
  
  get interestRate() {
    return this._annualRate * 100; // Return as percentage
  }
  
  // Methods
  getRemainingBalance(paymentsMade) {
    if (paymentsMade < 0) {
      throw new Error('Payments made cannot be negative');
    }
    
    if (paymentsMade >= this._numPayments) {
      return 0;
    }
    
    return this._principal * Math.pow(1 + this._monthlyRate, paymentsMade) - 
           this._monthlyPayment * ((Math.pow(1 + this._monthlyRate, paymentsMade) - 1) / this._monthlyRate);
  }
  
  getAmortizationSchedule() {
    const schedule = [];
    let balance = this._principal;
    
    for (let payment = 1; payment <= this._numPayments; payment++) {
      const interestPayment = balance * this._monthlyRate;
      const principalPayment = this._monthlyPayment - interestPayment;
      balance -= principalPayment;
      
      schedule.push({
        payment,
        principalPayment: Math.round(principalPayment * 100) / 100,
        interestPayment: Math.round(interestPayment * 100) / 100,
        totalPayment: Math.round(this._monthlyPayment * 100) / 100,
        balance: Math.round(Math.max(0, balance) * 100) / 100
      });
    }
    
    return schedule;
  }
  
  getPaymentBreakdown(paymentNumber) {
    if (paymentNumber < 1 || paymentNumber > this._numPayments) {
      throw new Error('Invalid payment number');
    }
    
    const balance = this.getRemainingBalance(paymentNumber - 1);
    const interestPayment = balance * this._monthlyRate;
    const principalPayment = this._monthlyPayment - interestPayment;
    
    return {
      payment: paymentNumber,
      principalPayment: Math.round(principalPayment * 100) / 100,
      interestPayment: Math.round(interestPayment * 100) / 100,
      totalPayment: Math.round(this._monthlyPayment * 100) / 100,
      remainingBalance: Math.round((balance - principalPayment) * 100) / 100
    };
  }
  
  // Comparison and analysis methods
  compareToLoan(otherLoan) {
    return {
      monthlyPaymentDiff: this._monthlyPayment - otherLoan.monthlyPayment,
      totalInterestDiff: this.totalInterest - otherLoan.totalInterest,
      totalPaymentDiff: this.totalPayment - otherLoan.totalPayment
    };
  }
  
  toString() {
    return `Loan: $${this._principal.toLocaleString()} at ${(this._annualRate * 100).toFixed(2)}% for ${this._termYears} years
Monthly Payment: $${this._monthlyPayment.toFixed(2)}
Total Interest: $${this.totalInterest.toFixed(2)}`;
  }
  
  // Private helper methods
  _calculateMonthlyPayment() {
    if (this._monthlyRate === 0) {
      return this._principal / this._numPayments;
    }
    
    return this._principal * (this._monthlyRate * Math.pow(1 + this._monthlyRate, this._numPayments)) / 
           (Math.pow(1 + this._monthlyRate, this._numPayments) - 1);
  }
  
  _validateInputs(principal, annualRate, termYears) {
    if (principal <= 0) {
      throw new Error('Principal must be positive');
    }
    if (annualRate < 0) {
      throw new Error('Annual rate cannot be negative');
    }
    if (termYears <= 0) {
      throw new Error('Term must be positive');
    }
  }
  
  // Factory methods
  static createMortgage(homePrice, downPayment, annualRate, termYears) {
    const principal = homePrice - downPayment;
    return new Loan(principal, annualRate, termYears);
  }
  
  static createFromMonthlyPayment(targetPayment, annualRate, termYears) {
    // Calculate principal that would result in target monthly payment
    const monthlyRate = annualRate / 12;
    const numPayments = termYears * 12;
    
    if (monthlyRate === 0) {
      return new Loan(targetPayment * numPayments, annualRate, termYears);
    }
    
    const principal = targetPayment * (Math.pow(1 + monthlyRate, numPayments) - 1) / 
                     (monthlyRate * Math.pow(1 + monthlyRate, numPayments));
    
    return new Loan(principal, annualRate, termYears);
  }
}

// Usage - much cleaner and more powerful
const loan = new Loan(200000, 0.045, 30);

// Simple property access
console.log(`Monthly payment: $${loan.monthlyPayment.toFixed(2)}`);
console.log(`Total interest: $${loan.totalInterest.toFixed(2)}`);

// Method calls with clear intent
const remainingAfter60 = loan.getRemainingBalance(60);
const fifthPaymentBreakdown = loan.getPaymentBreakdown(5);
const schedule = loan.getAmortizationSchedule();

// Factory methods for specific scenarios
const mortgage = Loan.createMortgage(350000, 70000, 0.035, 30);
const budgetLoan = Loan.createFromMonthlyPayment(1500, 0.04, 25);

// Comparison between loans
const comparison = loan.compareToLoan(mortgage);
```

## Mechanics

1. **Identify related functions**
   - Find functions that operate on the same data
   - Look for repeated parameter patterns
   - Group functions by the data they manipulate

2. **Analyze data and behavior**
   - Determine what data should become instance variables
   - Identify which functions should become methods
   - Check for validation and constraint logic

3. **Create the class**
   - Design constructor to initialize the data
   - Add validation in constructor
   - Make data private and provide getters if needed

4. **Convert functions to methods**
   - Move function logic into class methods
   - Remove redundant parameters (use instance variables instead)
   - Update method implementations to use `this`

5. **Add encapsulation**
   - Make fields private
   - Add getters and setters as appropriate
   - Include validation and constraint checking

6. **Enhance with class features**
   - Add computed properties
   - Create factory methods for common scenarios
   - Add comparison and utility methods

7. **Update callers**
   - Replace function calls with object creation and method calls
   - Update tests to work with new class structure

## When to Use

- **Related function groups**: Functions that always work with the same data
- **Parameter repetition**: Same parameters passed to multiple functions
- **Missing abstraction**: Related operations lack a unifying concept
- **Data validation**: Need to ensure data consistency across operations
- **Complex state**: Data has complex relationships and constraints
- **Utility improvements**: Want to add derived properties and convenience methods

## Trade-offs

### Benefits
- **Better organization**: Related functionality grouped together
- **Reduced parameter passing**: Data stored in object, not passed repeatedly
- **Encapsulation**: Data and behavior kept together with proper access control
- **Extensibility**: Easy to add new methods and computed properties
- **Validation**: Can ensure data consistency through constructor and methods
- **Reusability**: Objects can be passed around and used in different contexts

### Drawbacks
- **Object creation overhead**: Need to create objects instead of direct function calls
- **Increased complexity**: More complex than simple functions for simple operations
- **Stateful behavior**: Objects maintain state, which can complicate reasoning
- **Breaking changes**: Existing code needs significant updates
- **Over-engineering**: May be overkill for simple, unrelated functions

## Related Refactorings

- [Extract Class](extract-class.md) - Break down classes that are too large
- [Move Function](move-function.md) - Move functions to classes where they belong
- [Combine Functions into Transform](combine-functions-into-transform.md) - Alternative approach for read-only transformations