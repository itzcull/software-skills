---
title: "Replace Loop with Pipeline"
description: "Replace traditional loops with functional pipeline operations like map, filter, and reduce"
category: "Organization"
tags: ["loop", "pipeline", "functional", "declarative", "map", "filter", "reduce"]
related: ["split-loop", "extract-function", "substitute-algorithm"]
---

# Replace Loop with Pipeline

Replace traditional loops with a pipeline of operations using functional programming methods like map, filter, and reduce. This makes the code more declarative and easier to understand.

## Motivation

Traditional loops can be hard to understand and maintain:

- **Imperative style**: Focus on "how" rather than "what"
- **Cognitive overhead**: Need to track loop state and mutations
- **Error-prone**: Easy to make off-by-one errors or forget edge cases
- **Hard to test**: Difficult to test individual transformation steps
- **Poor composability**: Hard to combine or reuse loop logic
- **Readability issues**: Intent is obscured by loop mechanics

## Example

### Basic Example
```javascript
// Before - Traditional loop
function processUsers(users) {
  const result = [];
  
  for (let i = 0; i < users.length; i++) {
    const user = users[i];
    
    // Skip inactive users
    if (!user.isActive) {
      continue;
    }
    
    // Skip users without email
    if (!user.email) {
      continue;
    }
    
    // Transform user data
    const processedUser = {
      id: user.id,
      name: user.name.trim().toUpperCase(),
      email: user.email.toLowerCase(),
      domain: user.email.split('@')[1],
      registrationYear: new Date(user.createdAt).getFullYear()
    };
    
    result.push(processedUser);
  }
  
  return result;
}

// After - Functional pipeline
function processUsers(users) {
  return users
    .filter(user => user.isActive)
    .filter(user => user.email)
    .map(user => ({
      id: user.id,
      name: user.name.trim().toUpperCase(),
      email: user.email.toLowerCase(),
      domain: user.email.split('@')[1],
      registrationYear: new Date(user.createdAt).getFullYear()
    }));
}
```

### Complex Example - Data Analysis
```javascript
// Before - Complex nested loops with multiple accumulations
function analyzeOrderData(orders) {
  let totalRevenue = 0;
  let ordersByStatus = {};
  let topProducts = {};
  let monthlyRevenue = {};
  let customerStats = {};
  
  for (let i = 0; i < orders.length; i++) {
    const order = orders[i];
    
    // Skip cancelled orders
    if (order.status === 'cancelled') {
      continue;
    }
    
    // Calculate total revenue
    totalRevenue += order.total;
    
    // Count orders by status
    if (!ordersByStatus[order.status]) {
      ordersByStatus[order.status] = 0;
    }
    ordersByStatus[order.status]++;
    
    // Track monthly revenue
    const month = new Date(order.createdAt).toISOString().slice(0, 7);
    if (!monthlyRevenue[month]) {
      monthlyRevenue[month] = 0;
    }
    monthlyRevenue[month] += order.total;
    
    // Track customer statistics
    if (!customerStats[order.customerId]) {
      customerStats[order.customerId] = {
        orderCount: 0,
        totalSpent: 0,
        avgOrderValue: 0
      };
    }
    customerStats[order.customerId].orderCount++;
    customerStats[order.customerId].totalSpent += order.total;
    customerStats[order.customerId].avgOrderValue = 
      customerStats[order.customerId].totalSpent / customerStats[order.customerId].orderCount;
    
    // Process order items for product analysis
    for (let j = 0; j < order.items.length; j++) {
      const item = order.items[j];
      
      if (!topProducts[item.productId]) {
        topProducts[item.productId] = {
          name: item.name,
          quantitySold: 0,
          revenue: 0
        };
      }
      
      topProducts[item.productId].quantitySold += item.quantity;
      topProducts[item.productId].revenue += item.price * item.quantity;
    }
  }
  
  // Convert topProducts to sorted array
  const topProductsArray = [];
  for (const productId in topProducts) {
    topProductsArray.push({
      productId,
      ...topProducts[productId]
    });
  }
  
  // Sort by revenue
  topProductsArray.sort((a, b) => b.revenue - a.revenue);
  
  return {
    totalRevenue,
    ordersByStatus,
    monthlyRevenue,
    customerStats,
    topProducts: topProductsArray.slice(0, 10)
  };
}

// After - Functional pipeline approach
function analyzeOrderData(orders) {
  const activeOrders = orders.filter(order => order.status !== 'cancelled');
  
  const totalRevenue = activeOrders
    .reduce((sum, order) => sum + order.total, 0);
  
  const ordersByStatus = activeOrders
    .reduce((counts, order) => {
      counts[order.status] = (counts[order.status] || 0) + 1;
      return counts;
    }, {});
  
  const monthlyRevenue = activeOrders
    .reduce((monthly, order) => {
      const month = new Date(order.createdAt).toISOString().slice(0, 7);
      monthly[month] = (monthly[month] || 0) + order.total;
      return monthly;
    }, {});
  
  const customerStats = activeOrders
    .reduce((stats, order) => {
      if (!stats[order.customerId]) {
        stats[order.customerId] = { orderCount: 0, totalSpent: 0 };
      }
      
      stats[order.customerId].orderCount++;
      stats[order.customerId].totalSpent += order.total;
      stats[order.customerId].avgOrderValue = 
        stats[order.customerId].totalSpent / stats[order.customerId].orderCount;
      
      return stats;
    }, {});
  
  const topProducts = activeOrders
    .flatMap(order => order.items)
    .reduce((products, item) => {
      if (!products[item.productId]) {
        products[item.productId] = {
          name: item.name,
          quantitySold: 0,
          revenue: 0
        };
      }
      
      products[item.productId].quantitySold += item.quantity;
      products[item.productId].revenue += item.price * item.quantity;
      
      return products;
    }, {})
    |> Object.entries
    |> (entries => entries.map(([productId, data]) => ({ productId, ...data })))
    |> (products => products.sort((a, b) => b.revenue - a.revenue))
    |> (sorted => sorted.slice(0, 10));
  
  return {
    totalRevenue,
    ordersByStatus,
    monthlyRevenue,
    customerStats,
    topProducts
  };
}

// Alternative without pipeline operator (current JavaScript)
function analyzeOrderData(orders) {
  const activeOrders = orders.filter(order => order.status !== 'cancelled');
  
  const totalRevenue = activeOrders
    .reduce((sum, order) => sum + order.total, 0);
  
  const ordersByStatus = activeOrders
    .reduce((counts, order) => {
      counts[order.status] = (counts[order.status] || 0) + 1;
      return counts;
    }, {});
  
  const monthlyRevenue = activeOrders
    .reduce((monthly, order) => {
      const month = new Date(order.createdAt).toISOString().slice(0, 7);
      monthly[month] = (monthly[month] || 0) + order.total;
      return monthly;
    }, {});
  
  const customerStats = activeOrders
    .reduce((stats, order) => {
      if (!stats[order.customerId]) {
        stats[order.customerId] = { orderCount: 0, totalSpent: 0 };
      }
      
      stats[order.customerId].orderCount++;
      stats[order.customerId].totalSpent += order.total;
      stats[order.customerId].avgOrderValue = 
        stats[order.customerId].totalSpent / stats[order.customerId].orderCount;
      
      return stats;
    }, {});
  
  const topProducts = Object.entries(
    activeOrders
      .flatMap(order => order.items)
      .reduce((products, item) => {
        if (!products[item.productId]) {
          products[item.productId] = {
            name: item.name,
            quantitySold: 0,
            revenue: 0
          };
        }
        
        products[item.productId].quantitySold += item.quantity;
        products[item.productId].revenue += item.price * item.quantity;
        
        return products;
      }, {})
  )
    .map(([productId, data]) => ({ productId, ...data }))
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 10);
  
  return {
    totalRevenue,
    ordersByStatus,
    monthlyRevenue,
    customerStats,
    topProducts
  };
}
```

### File Processing Example
```javascript
// Before - Loop-based file processing
function processLogFiles(logFiles) {
  const errorCounts = {};
  const warningsByHour = {};
  const userActions = [];
  const systemEvents = [];
  
  for (let i = 0; i < logFiles.length; i++) {
    const file = logFiles[i];
    const lines = file.content.split('\n');
    
    for (let j = 0; j < lines.length; j++) {
      const line = lines[j].trim();
      
      if (line === '') {
        continue;
      }
      
      try {
        const logEntry = JSON.parse(line);
        
        // Count errors by type
        if (logEntry.level === 'error') {
          if (!errorCounts[logEntry.error_type]) {
            errorCounts[logEntry.error_type] = 0;
          }
          errorCounts[logEntry.error_type]++;
        }
        
        // Count warnings by hour
        if (logEntry.level === 'warning') {
          const hour = new Date(logEntry.timestamp).getHours();
          if (!warningsByHour[hour]) {
            warningsByHour[hour] = 0;
          }
          warningsByHour[hour]++;
        }
        
        // Collect user actions
        if (logEntry.category === 'user_action') {
          userActions.push({
            userId: logEntry.user_id,
            action: logEntry.action,
            timestamp: logEntry.timestamp,
            metadata: logEntry.metadata
          });
        }
        
        // Collect system events
        if (logEntry.category === 'system') {
          systemEvents.push({
            event: logEntry.event,
            timestamp: logEntry.timestamp,
            severity: logEntry.level
          });
        }
        
      } catch (parseError) {
        // Skip invalid JSON lines
        continue;
      }
    }
  }
  
  // Sort user actions by timestamp
  userActions.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  
  // Sort system events by timestamp
  systemEvents.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  
  return {
    errorCounts,
    warningsByHour,
    userActions,
    systemEvents
  };
}

// After - Pipeline-based processing
function processLogFiles(logFiles) {
  const parseLogEntry = (line) => {
    try {
      return JSON.parse(line.trim());
    } catch {
      return null;
    }
  };
  
  const isValidEntry = (entry) => entry !== null;
  
  const logEntries = logFiles
    .flatMap(file => file.content.split('\n'))
    .filter(line => line.trim() !== '')
    .map(parseLogEntry)
    .filter(isValidEntry);
  
  const errorCounts = logEntries
    .filter(entry => entry.level === 'error')
    .reduce((counts, entry) => {
      counts[entry.error_type] = (counts[entry.error_type] || 0) + 1;
      return counts;
    }, {});
  
  const warningsByHour = logEntries
    .filter(entry => entry.level === 'warning')
    .reduce((counts, entry) => {
      const hour = new Date(entry.timestamp).getHours();
      counts[hour] = (counts[hour] || 0) + 1;
      return counts;
    }, {});
  
  const userActions = logEntries
    .filter(entry => entry.category === 'user_action')
    .map(entry => ({
      userId: entry.user_id,
      action: entry.action,
      timestamp: entry.timestamp,
      metadata: entry.metadata
    }))
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  
  const systemEvents = logEntries
    .filter(entry => entry.category === 'system')
    .map(entry => ({
      event: entry.event,
      timestamp: entry.timestamp,
      severity: entry.level
    }))
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  
  return {
    errorCounts,
    warningsByHour,
    userActions,
    systemEvents
  };
}
```

### Performance-Critical Example with Optimizations
```javascript
// Before - Performance-focused loop
function processLargeDataset(data) {
  const results = [];
  const cache = new Map();
  
  for (let i = 0; i < data.length; i++) {
    const item = data[i];
    
    // Skip items that don't meet criteria
    if (item.value < 10 || item.status !== 'active') {
      continue;
    }
    
    // Expensive computation with caching
    let computed;
    if (cache.has(item.category)) {
      computed = cache.get(item.category);
    } else {
      computed = expensiveComputation(item.category);
      cache.set(item.category, computed);
    }
    
    // Transform and collect
    results.push({
      id: item.id,
      processedValue: item.value * computed.multiplier + computed.offset,
      category: item.category,
      rank: computed.rank
    });
  }
  
  return results;
}

// After - Pipeline with performance optimizations
function processLargeDataset(data) {
  const cache = new Map();
  
  const getComputedValue = (category) => {
    if (!cache.has(category)) {
      cache.set(category, expensiveComputation(category));
    }
    return cache.get(category);
  };
  
  return data
    .filter(item => item.value >= 10 && item.status === 'active')
    .map(item => {
      const computed = getComputedValue(item.category);
      return {
        id: item.id,
        processedValue: item.value * computed.multiplier + computed.offset,
        category: item.category,
        rank: computed.rank
      };
    });
}

// Alternative: Custom pipeline builder for performance
class Pipeline {
  constructor(data) {
    this.data = data;
    this.operations = [];
  }
  
  filter(predicate) {
    this.operations.push({ type: 'filter', fn: predicate });
    return this;
  }
  
  map(transform) {
    this.operations.push({ type: 'map', fn: transform });
    return this;
  }
  
  execute() {
    let result = this.data;
    
    for (const operation of this.operations) {
      if (operation.type === 'filter') {
        result = result.filter(operation.fn);
      } else if (operation.type === 'map') {
        result = result.map(operation.fn);
      }
    }
    
    return result;
  }
}

// Usage with custom pipeline
function processLargeDatasetOptimized(data) {
  const cache = new Map();
  
  const getComputedValue = (category) => {
    if (!cache.has(category)) {
      cache.set(category, expensiveComputation(category));
    }
    return cache.get(category);
  };
  
  return new Pipeline(data)
    .filter(item => item.value >= 10 && item.status === 'active')
    .map(item => {
      const computed = getComputedValue(item.category);
      return {
        id: item.id,
        processedValue: item.value * computed.multiplier + computed.offset,
        category: item.category,
        rank: computed.rank
      };
    })
    .execute();
}
```

## Mechanics

1. **Identify loop patterns**
   - Look for loops that filter, transform, or accumulate data
   - Find loops with multiple concerns mixed together
   - Check for nested loops that can be flattened

2. **Break down loop logic**
   - Separate filtering from transformation
   - Identify mapping operations
   - Find accumulation/reduction patterns

3. **Choose appropriate array methods**
   - Use `filter()` for conditional inclusion
   - Use `map()` for one-to-one transformations
   - Use `reduce()` for accumulation
   - Use `flatMap()` for flattening nested arrays
   - Use `find()` for locating specific items

4. **Chain operations**
   - Start with the source array
   - Chain methods in logical order
   - Keep each operation focused on a single concern

5. **Handle edge cases**
   - Ensure null/undefined safety
   - Handle empty arrays appropriately
   - Consider performance implications

6. **Test thoroughly**
   - Verify same results as original loop
   - Test edge cases and error conditions
   - Check performance if critical

## When to Use

- **Data transformation**: Converting data from one format to another
- **Filtering and mapping**: Common patterns of selection and transformation
- **Readable intent**: Want to emphasize what rather than how
- **Functional style**: Team prefers functional programming approaches
- **Composable logic**: Need to combine or reuse transformation steps
- **Immutable data**: Working with immutable data structures

## When NOT to Use

- **Performance critical**: Loops are significantly faster for large datasets
- **Complex state**: Loop maintains complex state that's hard to express functionally
- **Early termination**: Need to break out of loop based on conditions
- **Memory constraints**: Pipeline creates intermediate arrays
- **Side effects**: Loop performs significant side effects

## Trade-offs

### Benefits
- **Declarative**: Expresses intent clearly
- **Composable**: Easy to combine and reuse operations
- **Immutable**: Doesn't modify original data
- **Readable**: Clear separation of concerns
- **Testable**: Each operation can be tested separately
- **Less error-prone**: No index management or mutation bugs

### Drawbacks
- **Performance**: Can be slower for large datasets
- **Memory usage**: Creates intermediate arrays
- **Learning curve**: Team needs to understand functional methods
- **Debugging**: Harder to debug complex chains
- **Limited flexibility**: Some patterns are hard to express functionally

## Common Patterns

### Filter-Map Pattern
```javascript
// Before
const results = [];
for (const item of items) {
  if (item.isValid) {
    results.push(transform(item));
  }
}

// After
const results = items
  .filter(item => item.isValid)
  .map(transform);
```

### Reduce for Grouping
```javascript
// Before
const groups = {};
for (const item of items) {
  if (!groups[item.category]) {
    groups[item.category] = [];
  }
  groups[item.category].push(item);
}

// After
const groups = items.reduce((acc, item) => {
  (acc[item.category] = acc[item.category] || []).push(item);
  return acc;
}, {});
```

### Find Pattern
```javascript
// Before
let found = null;
for (const item of items) {
  if (item.id === targetId) {
    found = item;
    break;
  }
}

// After
const found = items.find(item => item.id === targetId);
```

### FlatMap for Nested Data
```javascript
// Before
const allItems = [];
for (const container of containers) {
  for (const item of container.items) {
    allItems.push(item);
  }
}

// After
const allItems = containers.flatMap(container => container.items);
```

## Performance Considerations

### When Performance Matters
```javascript
// For very large datasets, consider traditional loops
function processLargeArray(largeArray) {
  const results = new Array(largeArray.length);
  let resultIndex = 0;
  
  for (let i = 0; i < largeArray.length; i++) {
    const item = largeArray[i];
    if (item.isValid) {
      results[resultIndex++] = transform(item);
    }
  }
  
  // Trim array to actual size
  results.length = resultIndex;
  return results;
}
```

### Lazy Evaluation Alternative
```javascript
// Use generators for lazy evaluation
function* filterMap(iterable, predicate, transform) {
  for (const item of iterable) {
    if (predicate(item)) {
      yield transform(item);
    }
  }
}

// Usage
const results = [...filterMap(items, item => item.isValid, transform)];
```

## Related Refactorings

- [Extract Function](extract-function.md) - Extract pipeline operations into functions
- [Extract Variable](extract-variable.md) - Break down complex pipeline chains
- [Introduce Parameter Object](introduce-parameter-object.md) - Simplify pipeline parameters
- [Replace Temp with Query](replace-derived-variable-with-query.md) - Use functional approach for calculations
- [Split Loop](split-loop.md) - Separate different concerns before converting to pipeline