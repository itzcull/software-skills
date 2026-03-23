---
title: "Remove Flag Argument"
description: "Replace a flag parameter that determines behavior with separate functions for each behavior"
category: "Simplifying Function Calls"
tags: ["flag", "argument", "boolean", "separate-functions", "explicit"]
related: ["parameterize-function", "replace-conditional-with-polymorphism", "decompose-conditional"]
---

# Remove Flag Argument

Replace a parameter that is used as a flag to determine different behaviors with separate functions for each behavior. This makes the code more explicit and easier to understand.

## Motivation

Flag arguments (boolean parameters that control function behavior) create several problems:

- **Unclear intent**: Function calls don't clearly express what they do
- **Complex function logic**: Single function handles multiple behaviors
- **Hard to extend**: Adding new behaviors requires changing existing function
- **Poor readability**: Boolean parameters don't explain their purpose at call site
- **Maintenance overhead**: Need to understand all possible flag combinations
- **Violation of single responsibility**: One function does multiple things

## Example

### Basic Example
```javascript
// Before - Flag argument controls behavior
class DeliveryService {
  calculateShipping(weight, distance, isPriorityShipping) {
    let baseCost = weight * 0.1 + distance * 0.05;
    
    if (isPriorityShipping) {
      // Priority shipping logic
      baseCost *= 2.5;
      baseCost += 15; // Priority handling fee
      
      if (distance > 500) {
        baseCost += 25; // Long distance priority fee
      }
    } else {
      // Standard shipping logic
      if (distance > 500) {
        baseCost += 10; // Long distance standard fee
      }
      
      if (weight > 50) {
        baseCost += 5; // Heavy package fee
      }
    }
    
    return Math.round(baseCost * 100) / 100;
  }
  
  scheduleDelivery(address, packageInfo, isPriorityShipping) {
    if (isPriorityShipping) {
      console.log('Scheduling priority delivery');
      return { deliveryDate: new Date(Date.now() + 24 * 60 * 60 * 1000) }; // Next day
    } else {
      console.log('Scheduling standard delivery');
      return { deliveryDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000) }; // 5 days
    }
  }
}

// Usage - unclear what the boolean means
const delivery = new DeliveryService();
const cost1 = delivery.calculateShipping(10, 300, true);  // What does true mean?
const cost2 = delivery.calculateShipping(15, 600, false); // What does false mean?

const schedule1 = delivery.scheduleDelivery(address, package, true);
const schedule2 = delivery.scheduleDelivery(address, package, false);

// After - Separate functions with clear intent
class DeliveryService {
  calculateStandardShipping(weight, distance) {
    let baseCost = weight * 0.1 + distance * 0.05;
    
    if (distance > 500) {
      baseCost += 10; // Long distance standard fee
    }
    
    if (weight > 50) {
      baseCost += 5; // Heavy package fee
    }
    
    return Math.round(baseCost * 100) / 100;
  }
  
  calculatePriorityShipping(weight, distance) {
    let baseCost = weight * 0.1 + distance * 0.05;
    
    // Priority shipping multiplier and handling fee
    baseCost *= 2.5;
    baseCost += 15;
    
    if (distance > 500) {
      baseCost += 25; // Long distance priority fee
    }
    
    return Math.round(baseCost * 100) / 100;
  }
  
  scheduleStandardDelivery(address, packageInfo) {
    console.log('Scheduling standard delivery');
    return { 
      deliveryDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
      type: 'standard'
    };
  }
  
  schedulePriorityDelivery(address, packageInfo) {
    console.log('Scheduling priority delivery');
    return { 
      deliveryDate: new Date(Date.now() + 24 * 60 * 60 * 1000),
      type: 'priority'
    };
  }
}

// Usage - clear and explicit
const delivery = new DeliveryService();
const standardCost = delivery.calculateStandardShipping(10, 300);
const priorityCost = delivery.calculatePriorityShipping(15, 600);

const standardSchedule = delivery.scheduleStandardDelivery(address, package);
const prioritySchedule = delivery.schedulePriorityDelivery(address, package);
```

### Advanced Example - Multiple Flags
```javascript
// Before - Multiple flag arguments create complexity
class ReportGenerator {
  generateReport(data, includeCharts, includeDetails, exportToPdf, sendEmail, compressFile) {
    let report = { title: 'Sales Report', data: data };
    
    if (includeCharts) {
      report.charts = this.generateCharts(data);
    }
    
    if (includeDetails) {
      report.details = this.generateDetailedAnalysis(data);
    }
    
    let output;
    if (exportToPdf) {
      output = this.convertToPdf(report);
    } else {
      output = this.convertToHtml(report);
    }
    
    if (compressFile) {
      output = this.compressFile(output);
    }
    
    if (sendEmail) {
      this.emailReport(output);
    }
    
    return output;
  }
}

// Usage - confusing combinations of flags
const generator = new ReportGenerator();
const report1 = generator.generateReport(data, true, false, true, false, true);
const report2 = generator.generateReport(data, false, true, false, true, false);

// After - Configuration object and builder pattern
class ReportConfig {
  constructor() {
    this._includeCharts = false;
    this._includeDetails = false;
    this._format = 'html';
    this._compressed = false;
    this._emailDelivery = false;
  }
  
  withCharts() {
    this._includeCharts = true;
    return this;
  }
  
  withDetails() {
    this._includeDetails = true;
    return this;
  }
  
  asPdf() {
    this._format = 'pdf';
    return this;
  }
  
  asHtml() {
    this._format = 'html';
    return this;
  }
  
  compressed() {
    this._compressed = true;
    return this;
  }
  
  withEmailDelivery() {
    this._emailDelivery = true;
    return this;
  }
  
  // Getters
  get includeCharts() { return this._includeCharts; }
  get includeDetails() { return this._includeDetails; }
  get format() { return this._format; }
  get compressed() { return this._compressed; }
  get emailDelivery() { return this._emailDelivery; }
}

class ReportGenerator {
  generateReport(data, config) {
    let report = { title: 'Sales Report', data: data };
    
    if (config.includeCharts) {
      report.charts = this.generateCharts(data);
    }
    
    if (config.includeDetails) {
      report.details = this.generateDetailedAnalysis(data);
    }
    
    let output;
    if (config.format === 'pdf') {
      output = this.convertToPdf(report);
    } else {
      output = this.convertToHtml(report);
    }
    
    if (config.compressed) {
      output = this.compressFile(output);
    }
    
    if (config.emailDelivery) {
      this.emailReport(output);
    }
    
    return output;
  }
  
  // Convenience methods for common configurations
  generateBasicReport(data) {
    return this.generateReport(data, new ReportConfig());
  }
  
  generateDetailedReport(data) {
    const config = new ReportConfig()
      .withCharts()
      .withDetails();
    return this.generateReport(data, config);
  }
  
  generatePdfReport(data) {
    const config = new ReportConfig()
      .withCharts()
      .withDetails()
      .asPdf()
      .compressed();
    return this.generateReport(data, config);
  }
  
  generateEmailReport(data) {
    const config = new ReportConfig()
      .withCharts()
      .asPdf()
      .withEmailDelivery();
    return this.generateReport(data, config);
  }
}

// Usage - clear and flexible
const generator = new ReportGenerator();

// Using convenience methods
const basicReport = generator.generateBasicReport(data);
const detailedReport = generator.generateDetailedReport(data);
const pdfReport = generator.generatePdfReport(data);

// Using configuration builder
const customReport = generator.generateReport(data, 
  new ReportConfig()
    .withCharts()
    .asPdf()
    .compressed()
    .withEmailDelivery()
);

// Quick HTML report with details
const htmlDetailReport = generator.generateReport(data,
  new ReportConfig().withDetails().asHtml()
);
```

### Alternative Approach - Polymorphism
```javascript
// Alternative approach using polymorphism for delivery example
class DeliveryService {
  calculateShipping(shippingType, weight, distance) {
    return shippingType.calculateCost(weight, distance);
  }
  
  scheduleDelivery(shippingType, address, packageInfo) {
    return shippingType.schedule(address, packageInfo);
  }
}

class StandardShipping {
  calculateCost(weight, distance) {
    let baseCost = weight * 0.1 + distance * 0.05;
    
    if (distance > 500) {
      baseCost += 10;
    }
    
    if (weight > 50) {
      baseCost += 5;
    }
    
    return Math.round(baseCost * 100) / 100;
  }
  
  schedule(address, packageInfo) {
    console.log('Scheduling standard delivery');
    return { 
      deliveryDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
      type: 'standard'
    };
  }
}

class PriorityShipping {
  calculateCost(weight, distance) {
    let baseCost = weight * 0.1 + distance * 0.05;
    baseCost *= 2.5;
    baseCost += 15;
    
    if (distance > 500) {
      baseCost += 25;
    }
    
    return Math.round(baseCost * 100) / 100;
  }
  
  schedule(address, packageInfo) {
    console.log('Scheduling priority delivery');
    return { 
      deliveryDate: new Date(Date.now() + 24 * 60 * 60 * 1000),
      type: 'priority'
    };
  }
}

// Usage with polymorphism
const delivery = new DeliveryService();
const standardShipping = new StandardShipping();
const priorityShipping = new PriorityShipping();

const standardCost = delivery.calculateShipping(standardShipping, 10, 300);
const priorityCost = delivery.calculateShipping(priorityShipping, 15, 600);
```

## Mechanics

1. **Identify flag arguments**
   - Find boolean parameters that control function behavior
   - Look for parameters with names like `isX`, `enableX`, `withX`
   - Check for functions with multiple boolean parameters

2. **Analyze flag usage**
   - Understand what different flag combinations do
   - Identify distinct behaviors triggered by flags
   - Check if flags are mutually exclusive or combinable

3. **Create separate functions**
   - Create one function for each distinct behavior
   - Choose descriptive names that explain the behavior
   - Move flag-specific logic to appropriate functions

4. **Handle complex flag combinations**
   - Use configuration objects for multiple flags
   - Consider builder pattern for complex configurations
   - Create convenience methods for common combinations

5. **Update callers**
   - Replace flag-based calls with explicit function calls
   - Use configuration objects where appropriate
   - Update tests to use new methods

6. **Test thoroughly**
   - Verify all behaviors work correctly
   - Test that no functionality is lost
   - Check that intent is clearer in new code

## When to Use

- **Boolean parameters**: Functions with boolean flags that control behavior
- **Unclear intent**: Function calls don't clearly express what they do
- **Complex combinations**: Multiple flags with various combinations
- **Repeated patterns**: Same flag patterns used across multiple functions
- **API design**: Want to provide clear, intention-revealing interfaces
- **Single responsibility**: Functions doing too many different things

## Trade-offs

### Benefits
- **Clear intent**: Function names express exactly what they do
- **Better maintainability**: Each function has single responsibility
- **Easier to extend**: Can add new behaviors without changing existing functions
- **Improved readability**: No need to understand what flags mean
- **Type safety**: Can use different parameter types for different behaviors
- **Self-documenting**: Function names serve as documentation

### Drawbacks
- **More functions**: Increases number of methods in interface
- **Code duplication**: May duplicate some common logic
- **Breaking changes**: Existing code needs to be updated
- **Interface size**: Can make classes larger
- **Discovery**: May be harder to find all related functions

## Related Refactorings

- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Use polymorphism instead of flags
- [Introduce Parameter Object](introduce-parameter-object.md) - Group related flags into configuration object
- [Extract Function](extract-function.md) - Extract flag-specific behavior into separate functions