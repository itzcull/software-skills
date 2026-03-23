---
title: "Split Loop"
description: "Take a loop doing multiple things and duplicate it into separate loops with single purposes"
category: "Organization"
tags: ["split", "loop", "single-responsibility", "optimization", "readability"]
related: ["extract-function", "replace-loop-with-pipeline", "slide-statements"]
---

# Split Loop

Take a loop that's doing two different things and duplicate it into separate loops that each do one thing. This improves readability and makes it easier to optimize each operation independently.

## Motivation

Loops that do multiple things create several problems:

- **Mixed concerns**: Single loop handles unrelated operations
- **Hard to understand**: Cognitive overhead of tracking multiple purposes
- **Difficult to optimize**: Can't optimize different operations independently
- **Poor reusability**: Can't reuse parts of the loop logic
- **Maintenance burden**: Changes to one concern affect others
- **Testing complexity**: Hard to test individual operations

## Example

### Basic Example
```javascript
// Before - Loop doing multiple things
function analyzeUsers(users) {
  let totalAge = 0;
  let activeCount = 0;
  const usersByCity = {};
  let oldestUser = null;
  let youngestUser = null;
  
  for (const user of users) {
    // Age calculations
    totalAge += user.age;
    if (!oldestUser || user.age > oldestUser.age) {
      oldestUser = user;
    }
    if (!youngestUser || user.age < youngestUser.age) {
      youngestUser = user;
    }
    
    // Active user counting
    if (user.isActive) {
      activeCount++;
    }
    
    // City grouping
    if (!usersByCity[user.city]) {
      usersByCity[user.city] = [];
    }
    usersByCity[user.city].push(user);
  }
  
  return {
    averageAge: totalAge / users.length,
    activeCount,
    usersByCity,
    oldestUser,
    youngestUser
  };
}

// After - Separate loops for different concerns
function analyzeUsers(users) {
  // Age-related calculations
  let totalAge = 0;
  let oldestUser = null;
  let youngestUser = null;
  
  for (const user of users) {
    totalAge += user.age;
    if (!oldestUser || user.age > oldestUser.age) {
      oldestUser = user;
    }
    if (!youngestUser || user.age < youngestUser.age) {
      youngestUser = user;
    }
  }
  
  // Active user counting
  let activeCount = 0;
  for (const user of users) {
    if (user.isActive) {
      activeCount++;
    }
  }
  
  // City grouping
  const usersByCity = {};
  for (const user of users) {
    if (!usersByCity[user.city]) {
      usersByCity[user.city] = [];
    }
    usersByCity[user.city].push(user);
  }
  
  return {
    averageAge: totalAge / users.length,
    activeCount,
    usersByCity,
    oldestUser,
    youngestUser
  };
}

// Even better - Using functional approaches for some loops
function analyzeUsers(users) {
  // Age-related calculations (still using loop for efficiency)
  let totalAge = 0;
  let oldestUser = null;
  let youngestUser = null;
  
  for (const user of users) {
    totalAge += user.age;
    if (!oldestUser || user.age > oldestUser.age) {
      oldestUser = user;
    }
    if (!youngestUser || user.age < youngestUser.age) {
      youngestUser = user;
    }
  }
  
  // Active user counting (functional approach)
  const activeCount = users.filter(user => user.isActive).length;
  
  // City grouping (functional approach)
  const usersByCity = users.reduce((cities, user) => {
    (cities[user.city] = cities[user.city] || []).push(user);
    return cities;
  }, {});
  
  return {
    averageAge: totalAge / users.length,
    activeCount,
    usersByCity,
    oldestUser,
    youngestUser
  };
}
```

### Complex Example - Order Processing
```javascript
// Before - Complex loop doing many things
function processOrderBatch(orders) {
  let totalRevenue = 0;
  let totalTax = 0;
  let totalShipping = 0;
  const ordersByStatus = {};
  const customerOrderCounts = {};
  const productSales = {};
  const errorOrders = [];
  const highValueOrders = [];
  const internationalOrders = [];
  let earliestOrder = null;
  let latestOrder = null;
  
  for (const order of orders) {
    try {
      // Revenue calculations
      totalRevenue += order.subtotal;
      totalTax += order.tax;
      totalShipping += order.shipping;
      
      // High value order detection
      if (order.total > 1000) {
        highValueOrders.push({
          orderId: order.id,
          customerId: order.customerId,
          total: order.total
        });
      }
      
      // Status grouping
      if (!ordersByStatus[order.status]) {
        ordersByStatus[order.status] = 0;
      }
      ordersByStatus[order.status]++;
      
      // Customer order counting
      if (!customerOrderCounts[order.customerId]) {
        customerOrderCounts[order.customerId] = 0;
      }
      customerOrderCounts[order.customerId]++;
      
      // Product sales tracking
      for (const item of order.items) {
        if (!productSales[item.productId]) {
          productSales[item.productId] = {
            quantity: 0,
            revenue: 0,
            orderCount: 0
          };
        }
        productSales[item.productId].quantity += item.quantity;
        productSales[item.productId].revenue += item.price * item.quantity;
        productSales[item.productId].orderCount++;
      }
      
      // International order detection
      if (order.shippingAddress.country !== 'US') {
        internationalOrders.push({
          orderId: order.id,
          country: order.shippingAddress.country,
          total: order.total
        });
      }
      
      // Date range tracking
      const orderDate = new Date(order.createdAt);
      if (!earliestOrder || orderDate < new Date(earliestOrder.createdAt)) {
        earliestOrder = order;
      }
      if (!latestOrder || orderDate > new Date(latestOrder.createdAt)) {
        latestOrder = order;
      }
      
    } catch (error) {
      errorOrders.push({
        orderId: order.id,
        error: error.message
      });
    }
  }
  
  return {
    totals: { revenue: totalRevenue, tax: totalTax, shipping: totalShipping },
    ordersByStatus,
    customerOrderCounts,
    productSales,
    highValueOrders,
    internationalOrders,
    dateRange: { earliest: earliestOrder, latest: latestOrder },
    errorOrders
  };
}

// After - Split into focused loops
function processOrderBatch(orders) {
  // Revenue and totals calculation
  let totalRevenue = 0;
  let totalTax = 0;
  let totalShipping = 0;
  
  for (const order of orders) {
    totalRevenue += order.subtotal;
    totalTax += order.tax;
    totalShipping += order.shipping;
  }
  
  // Order status grouping
  const ordersByStatus = {};
  for (const order of orders) {
    ordersByStatus[order.status] = (ordersByStatus[order.status] || 0) + 1;
  }
  
  // Customer order counting
  const customerOrderCounts = {};
  for (const order of orders) {
    customerOrderCounts[order.customerId] = (customerOrderCounts[order.customerId] || 0) + 1;
  }
  
  // Product sales analysis
  const productSales = {};
  for (const order of orders) {
    for (const item of order.items) {
      if (!productSales[item.productId]) {
        productSales[item.productId] = {
          quantity: 0,
          revenue: 0,
          orderCount: 0
        };
      }
      productSales[item.productId].quantity += item.quantity;
      productSales[item.productId].revenue += item.price * item.quantity;
      productSales[item.productId].orderCount++;
    }
  }
  
  // Special order detection
  const highValueOrders = [];
  const internationalOrders = [];
  for (const order of orders) {
    if (order.total > 1000) {
      highValueOrders.push({
        orderId: order.id,
        customerId: order.customerId,
        total: order.total
      });
    }
    
    if (order.shippingAddress.country !== 'US') {
      internationalOrders.push({
        orderId: order.id,
        country: order.shippingAddress.country,
        total: order.total
      });
    }
  }
  
  // Date range calculation
  let earliestOrder = null;
  let latestOrder = null;
  for (const order of orders) {
    const orderDate = new Date(order.createdAt);
    if (!earliestOrder || orderDate < new Date(earliestOrder.createdAt)) {
      earliestOrder = order;
    }
    if (!latestOrder || orderDate > new Date(latestOrder.createdAt)) {
      latestOrder = order;
    }
  }
  
  // Error detection and handling
  const errorOrders = [];
  for (const order of orders) {
    try {
      validateOrder(order);
    } catch (error) {
      errorOrders.push({
        orderId: order.id,
        error: error.message
      });
    }
  }
  
  return {
    totals: { revenue: totalRevenue, tax: totalTax, shipping: totalShipping },
    ordersByStatus,
    customerOrderCounts,
    productSales,
    highValueOrders,
    internationalOrders,
    dateRange: { earliest: earliestOrder, latest: latestOrder },
    errorOrders
  };
}

// Alternative - Using functional approaches where appropriate
function processOrderBatch(orders) {
  // Revenue and totals (reduce for multiple accumulations)
  const totals = orders.reduce((acc, order) => ({
    revenue: acc.revenue + order.subtotal,
    tax: acc.tax + order.tax,
    shipping: acc.shipping + order.shipping
  }), { revenue: 0, tax: 0, shipping: 0 });
  
  // Order status grouping (functional)
  const ordersByStatus = orders.reduce((acc, order) => {
    acc[order.status] = (acc[order.status] || 0) + 1;
    return acc;
  }, {});
  
  // Customer order counting (functional)
  const customerOrderCounts = orders.reduce((acc, order) => {
    acc[order.customerId] = (acc[order.customerId] || 0) + 1;
    return acc;
  }, {});
  
  // Product sales analysis (functional)
  const productSales = orders
    .flatMap(order => order.items.map(item => ({ ...item, orderId: order.id })))
    .reduce((acc, item) => {
      if (!acc[item.productId]) {
        acc[item.productId] = { quantity: 0, revenue: 0, orderCount: 0 };
      }
      acc[item.productId].quantity += item.quantity;
      acc[item.productId].revenue += item.price * item.quantity;
      acc[item.productId].orderCount++;
      return acc;
    }, {});
  
  // Special orders (filter and map)
  const highValueOrders = orders
    .filter(order => order.total > 1000)
    .map(order => ({
      orderId: order.id,
      customerId: order.customerId,
      total: order.total
    }));
  
  const internationalOrders = orders
    .filter(order => order.shippingAddress.country !== 'US')
    .map(order => ({
      orderId: order.id,
      country: order.shippingAddress.country,
      total: order.total
    }));
  
  // Date range (reduce for min/max)
  const dateRange = orders.reduce((acc, order) => {
    const orderDate = new Date(order.createdAt);
    return {
      earliest: !acc.earliest || orderDate < new Date(acc.earliest.createdAt) ? order : acc.earliest,
      latest: !acc.latest || orderDate > new Date(acc.latest.createdAt) ? order : acc.latest
    };
  }, { earliest: null, latest: null });
  
  // Error detection
  const errorOrders = orders.reduce((acc, order) => {
    try {
      validateOrder(order);
    } catch (error) {
      acc.push({ orderId: order.id, error: error.message });
    }
    return acc;
  }, []);
  
  return {
    totals,
    ordersByStatus,
    customerOrderCounts,
    productSales,
    highValueOrders,
    internationalOrders,
    dateRange,
    errorOrders
  };
}
```

### File Processing Example
```javascript
// Before - Single loop doing file validation, transformation, and statistics
function processFileData(fileContent) {
  const lines = fileContent.split('\n');
  const errors = [];
  const processedData = [];
  let totalRecords = 0;
  let validRecords = 0;
  let invalidRecords = 0;
  const fieldStatistics = {};
  const duplicateEmails = new Set();
  const emailsSeen = new Set();
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    
    if (line === '') continue;
    
    totalRecords++;
    
    try {
      // Parse and validate
      const record = JSON.parse(line);
      
      // Required field validation
      if (!record.email || !record.name) {
        throw new Error('Missing required fields');
      }
      
      // Email format validation
      if (!record.email.includes('@')) {
        throw new Error('Invalid email format');
      }
      
      // Duplicate detection
      if (emailsSeen.has(record.email)) {
        duplicateEmails.add(record.email);
      } else {
        emailsSeen.add(record.email);
      }
      
      // Data transformation
      const processedRecord = {
        id: record.id || generateId(),
        name: record.name.trim().toLowerCase(),
        email: record.email.toLowerCase(),
        age: parseInt(record.age) || 0,
        city: record.city ? record.city.trim() : 'Unknown',
        processedAt: new Date()
      };
      
      processedData.push(processedRecord);
      validRecords++;
      
      // Field statistics
      Object.keys(processedRecord).forEach(key => {
        if (!fieldStatistics[key]) {
          fieldStatistics[key] = { count: 0, nullCount: 0 };
        }
        fieldStatistics[key].count++;
        if (!processedRecord[key] || processedRecord[key] === 'Unknown') {
          fieldStatistics[key].nullCount++;
        }
      });
      
    } catch (error) {
      invalidRecords++;
      errors.push({
        line: i + 1,
        content: line,
        error: error.message
      });
    }
  }
  
  return {
    processedData,
    statistics: {
      totalRecords,
      validRecords,
      invalidRecords,
      duplicateEmails: Array.from(duplicateEmails),
      fieldStatistics
    },
    errors
  };
}

// After - Split into focused processing steps
function processFileData(fileContent) {
  const lines = fileContent.split('\n').filter(line => line.trim() !== '');
  
  // Step 1: Parse and validate records
  const parseResults = parseAndValidateRecords(lines);
  
  // Step 2: Transform valid records
  const processedData = transformRecords(parseResults.validRecords);
  
  // Step 3: Generate statistics
  const statistics = generateStatistics(lines.length, parseResults);
  
  // Step 4: Calculate field statistics
  const fieldStatistics = calculateFieldStatistics(processedData);
  
  return {
    processedData,
    statistics: {
      ...statistics,
      fieldStatistics
    },
    errors: parseResults.errors
  };
}

function parseAndValidateRecords(lines) {
  const validRecords = [];
  const errors = [];
  const emailsSeen = new Set();
  const duplicateEmails = new Set();
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    try {
      const record = JSON.parse(line);
      
      // Validation
      if (!record.email || !record.name) {
        throw new Error('Missing required fields');
      }
      
      if (!record.email.includes('@')) {
        throw new Error('Invalid email format');
      }
      
      // Duplicate detection
      if (emailsSeen.has(record.email)) {
        duplicateEmails.add(record.email);
      } else {
        emailsSeen.add(record.email);
      }
      
      validRecords.push(record);
      
    } catch (error) {
      errors.push({
        line: i + 1,
        content: line,
        error: error.message
      });
    }
  }
  
  return { validRecords, errors, duplicateEmails };
}

function transformRecords(validRecords) {
  return validRecords.map(record => ({
    id: record.id || generateId(),
    name: record.name.trim().toLowerCase(),
    email: record.email.toLowerCase(),
    age: parseInt(record.age) || 0,
    city: record.city ? record.city.trim() : 'Unknown',
    processedAt: new Date()
  }));
}

function generateStatistics(totalLines, parseResults) {
  return {
    totalRecords: totalLines,
    validRecords: parseResults.validRecords.length,
    invalidRecords: parseResults.errors.length,
    duplicateEmails: Array.from(parseResults.duplicateEmails)
  };
}

function calculateFieldStatistics(processedData) {
  const fieldStatistics = {};
  
  for (const record of processedData) {
    Object.keys(record).forEach(key => {
      if (!fieldStatistics[key]) {
        fieldStatistics[key] = { count: 0, nullCount: 0 };
      }
      fieldStatistics[key].count++;
      if (!record[key] || record[key] === 'Unknown') {
        fieldStatistics[key].nullCount++;
      }
    });
  }
  
  return fieldStatistics;
}
```

## Mechanics

1. **Identify different concerns in the loop**
   - Look for unrelated operations in the same loop
   - Find different types of data being accumulated
   - Check for independent calculations

2. **Check for dependencies**
   - Ensure operations can be safely separated
   - Verify that one operation doesn't depend on results from another
   - Consider if order of operations matters

3. **Duplicate the loop**
   - Copy the entire loop structure
   - Keep only relevant operations in each copy
   - Remove unrelated variables and operations

4. **Clean up each loop**
   - Remove unused variables from each loop
   - Simplify operations that are now focused
   - Consider converting to functional approaches where appropriate

5. **Consider performance implications**
   - Evaluate if multiple passes are acceptable
   - Consider combining loops if performance is critical
   - Look for opportunities to optimize individual loops

6. **Test thoroughly**
   - Verify that results are identical
   - Test with edge cases
   - Check performance if it's critical

## When to Use

- **Mixed concerns**: Loop handles unrelated operations
- **Complex loops**: Single loop is hard to understand
- **Different optimization needs**: Operations have different performance characteristics
- **Reusability**: Want to reuse parts of the loop logic
- **Testing**: Want to test operations independently
- **Maintainability**: Changes to one concern shouldn't affect others

## When NOT to Use

- **Performance critical**: Multiple passes are too expensive
- **Tightly coupled operations**: Operations depend on each other
- **Simple loops**: Loop is already focused and clear
- **Memory constraints**: Can't afford multiple iterations over large datasets
- **Small datasets**: Performance difference is negligible

## Trade-offs

### Benefits
- **Clarity**: Each loop has a single, clear purpose
- **Maintainability**: Changes are isolated to relevant loops
- **Reusability**: Individual loops can be extracted and reused
- **Optimization**: Each loop can be optimized independently
- **Testing**: Each operation can be tested separately
- **Debugging**: Easier to debug focused operations

### Drawbacks
- **Performance**: Multiple passes over the same data
- **Memory**: May require storing intermediate results
- **Code duplication**: Similar loop structures
- **Complexity**: More loops to maintain

## Performance Considerations

### When to Keep Combined Loop
```javascript
// For very large datasets or performance-critical code
function processLargeDataset(data) {
  let sum = 0;
  let count = 0;
  const categories = {};
  
  // Single pass for performance
  for (const item of data) {
    sum += item.value;
    count++;
    categories[item.category] = (categories[item.category] || 0) + 1;
  }
  
  return { average: sum / count, categories };
}
```

### Optimizing Split Loops
```javascript
// Use functional methods for readability when performance allows
function processModerateDataset(data) {
  // Calculate average
  const average = data.reduce((sum, item) => sum + item.value, 0) / data.length;
  
  // Group by category
  const categories = data.reduce((acc, item) => {
    acc[item.category] = (acc[item.category] || 0) + 1;
    return acc;
  }, {});
  
  return { average, categories };
}
```

## Related Refactorings

- [Extract Function](extract-function.md) - Extract each loop into its own function
- [Replace Loop with Pipeline](replace-loop-with-pipeline.md) - Convert loops to functional operations
- [Consolidate Conditional Expression](consolidate-conditional-expression.md) - Simplify conditions in split loops
- [Extract Variable](extract-variable.md) - Extract complex expressions from loops
- [Slide Statements](slide-statements.md) - Group related statements before splitting
- [Substitute Algorithm](substitute-algorithm.md) - Replace loops with more efficient algorithms