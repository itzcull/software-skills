---
title: "Introduce Special Case"
description: "Replace common conditional logic for special values with special case objects"
category: "Simplifying Conditional Logic"
tags: ["special-case", "null-object", "conditional", "exception-handling"]
related: ["replace-conditional-with-polymorphism", "consolidate-conditional-expression", "introduce-assertion"]
---

# Introduce Special Case

Replace common conditional logic that tests for special values with special case objects that handle the exceptional behavior. This eliminates repetitive null checks and special value handling throughout the codebase.

## Motivation

Code that deals with special values often becomes cluttered with repetitive conditional logic:

- **Repetitive null checks**: Same null/undefined checks scattered throughout code
- **Scattered special handling**: Special case logic duplicated in multiple places
- **Default value repetition**: Same default values used in many locations
- **Complex conditionals**: Multiple conditions testing for various special states
- **Error-prone patterns**: Easy to forget special case handling in new code
- **Maintenance overhead**: Changes to special case behavior require updates in many places

## Example

### Basic Example - Null Object Pattern
```javascript
// Before - Repetitive null checks
class Customer {
  constructor(name, email, plan) {
    this._name = name;
    this._email = email;
    this._plan = plan; // Can be null for unknown customers
  }
  
  get name() { return this._name; }
  get email() { return this._email; }
  get plan() { return this._plan; }
}

class BillingService {
  calculateMonthlyCharge(customer) {
    // Repetitive null checking
    if (customer.plan === null) {
      return 0;
    }
    return customer.plan.monthlyFee;
  }
  
  getDiscountRate(customer) {
    // More null checking
    if (customer.plan === null) {
      return 0;
    }
    return customer.plan.discountRate;
  }
  
  canAccessPremiumFeatures(customer) {
    // Yet more null checking
    if (customer.plan === null) {
      return false;
    }
    return customer.plan.isPremium;
  }
}

// After - Special case object handles null behavior
class Customer {
  constructor(name, email, plan) {
    this._name = name;
    this._email = email;
    this._plan = plan || new NullPlan(); // Use special case instead of null
  }
  
  get name() { return this._name; }
  get email() { return this._email; }
  get plan() { return this._plan; }
}

class Plan {
  constructor(name, monthlyFee, discountRate, isPremium) {
    this._name = name;
    this._monthlyFee = monthlyFee;
    this._discountRate = discountRate;
    this._isPremium = isPremium;
  }
  
  get name() { return this._name; }
  get monthlyFee() { return this._monthlyFee; }
  get discountRate() { return this._discountRate; }
  get isPremium() { return this._isPremium; }
}

// Special case object that provides null behavior
class NullPlan extends Plan {
  constructor() {
    super('No Plan', 0, 0, false);
  }
  
  get name() { return 'No Plan'; }
  get monthlyFee() { return 0; }
  get discountRate() { return 0; }
  get isPremium() { return false; }
  
  // Can override any behavior specific to null case
  toString() {
    return 'Customer has no active plan';
  }
}

class BillingService {
  calculateMonthlyCharge(customer) {
    // No null checking needed - special case handles it
    return customer.plan.monthlyFee;
  }
  
  getDiscountRate(customer) {
    // Clean, simple code
    return customer.plan.discountRate;
  }
  
  canAccessPremiumFeatures(customer) {
    // No conditional logic needed
    return customer.plan.isPremium;
  }
}
```

### Advanced Example - Multiple Special Cases
```javascript
// Before - Complex special value handling
class FileProcessor {
  processFile(filePath) {
    if (filePath === null || filePath === '') {
      console.log('No file to process');
      return { status: 'skipped', message: 'No file provided' };
    }
    
    if (filePath === 'STDIN') {
      console.log('Reading from standard input');
      return this.readFromStdin();
    }
    
    if (filePath.startsWith('http://') || filePath.startsWith('https://')) {
      console.log(`Downloading from URL: ${filePath}`);
      return this.downloadAndProcess(filePath);
    }
    
    // Regular file processing
    console.log(`Processing file: ${filePath}`);
    return this.processRegularFile(filePath);
  }
}

// After - Special case objects handle different scenarios
class FileProcessor {
  processFile(fileSource) {
    // Factory creates appropriate special case object
    const source = FileSource.create(fileSource);
    return source.process(this);
  }
  
  processRegularFile(filePath) {
    console.log(`Processing file: ${filePath}`);
    // Regular file processing logic
    return { status: 'processed', file: filePath };
  }
  
  readFromStdin() {
    // STDIN processing logic
    return { status: 'processed', source: 'stdin' };
  }
  
  downloadAndProcess(url) {
    // URL processing logic
    return { status: 'processed', url: url };
  }
}

// Base class for file sources
class FileSource {
  static create(input) {
    if (!input || input === '') {
      return new NullFileSource();
    }
    if (input === 'STDIN') {
      return new StdinFileSource();
    }
    if (input.startsWith('http://') || input.startsWith('https://')) {
      return new UrlFileSource(input);
    }
    return new RegularFileSource(input);
  }
  
  process(processor) {
    throw new Error('Subclasses must implement process method');
  }
}

class NullFileSource extends FileSource {
  process(processor) {
    console.log('No file to process');
    return { status: 'skipped', message: 'No file provided' };
  }
}

class StdinFileSource extends FileSource {
  process(processor) {
    console.log('Reading from standard input');
    return processor.readFromStdin();
  }
}

class UrlFileSource extends FileSource {
  constructor(url) {
    super();
    this._url = url;
  }
  
  process(processor) {
    console.log(`Downloading from URL: ${this._url}`);
    return processor.downloadAndProcess(this._url);
  }
}

class RegularFileSource extends FileSource {
  constructor(filePath) {
    super();
    this._filePath = filePath;
  }
  
  process(processor) {
    console.log(`Processing file: ${this._filePath}`);
    return processor.processRegularFile(this._filePath);
  }
}
```

## Mechanics

1. **Identify special case patterns**
   - Find repetitive null/undefined checks
   - Look for common default value usage
   - Identify scattered special value handling

2. **Create special case class**
   - Create class that provides special case behavior
   - Implement same interface as regular objects
   - Return appropriate default values for special case

3. **Replace special values**
   - Replace null/undefined with special case instances
   - Update creation code to use special case objects
   - Remove conditional checks that test for special values

4. **Move behavior to special case**
   - Move special case logic into special case methods
   - Consolidate scattered special case handling
   - Make special case behavior explicit and reusable

5. **Test thoroughly**
   - Verify all special case scenarios work correctly
   - Test that no null reference errors occur
   - Check that behavior is consistent across usage

## When to Use

- **Repetitive null checks**: Same null checks appear in multiple places
- **Default value patterns**: Common default values used throughout code
- **Special value handling**: Code handles specific special values repeatedly
- **Null object pattern**: Need to eliminate null reference errors
- **API boundaries**: External APIs that might return special values
- **Optional features**: Features that may or may not be available

## Trade-offs

### Benefits
- **Eliminates repetition**: Centralized special case handling
- **Cleaner code**: No scattered conditional logic
- **Null safety**: Prevents null reference errors
- **Consistent behavior**: Special cases behave consistently
- **Easier maintenance**: Changes to special case logic in one place
- **Polymorphism**: Special cases work seamlessly with regular objects

### Drawbacks
- **More classes**: Additional classes to maintain
- **Indirection**: May hide the fact that special case is being handled
- **Memory overhead**: Special case objects use more memory than null
- **Complexity**: Can make simple null checks seem overly complex
- **Debugging**: May be harder to identify when special case is in use

## Related Refactorings

- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Use polymorphism for special case behavior
- [Extract Class](extract-class.md) - Extract special case handling into separate class
- [Introduce Parameter Object](introduce-parameter-object.md) - Group special case parameters together