---
title: "Combine Functions into Transform"
description: "Combine functions that derive information from a single source into a transform function"
category: "Organization"
tags: ["transform", "functions", "data-transformation", "performance", "organization"]
related: ["combine-functions-into-class", "extract-function", "split-phase"]
---

# Combine Functions into Transform

Combine a group of functions that derive information from a single source into a transform function that returns an enriched version of the source data. This centralizes data transformation logic and improves performance by calculating all derived values at once.

## Motivation

Functions that derive data from the same source create several problems when kept separate:

- **Repeated calculations**: Same base calculations performed multiple times
- **Scattered logic**: Related transformations spread across different functions
- **Performance issues**: Multiple passes over the same data
- **Inconsistent access patterns**: Different ways to get derived information
- **Maintenance overhead**: Changes to source data require updating many functions
- **Missing coordination**: No single place that shows all transformations

## Example

### Basic Example
```javascript
// Before - Separate transformation functions
function getBasePrice(order) {
  return order.quantity * order.unitPrice;
}

function getDiscount(order) {
  const basePrice = order.quantity * order.unitPrice;
  if (order.quantity > 100) {
    return basePrice * 0.1; // 10% bulk discount
  }
  if (order.customer.isPremium) {
    return basePrice * 0.05; // 5% premium discount
  }
  return 0;
}

function getTax(order) {
  const basePrice = order.quantity * order.unitPrice;
  const discount = getDiscount(order);
  const taxableAmount = basePrice - discount;
  return taxableAmount * order.taxRate;
}

function getShipping(order) {
  const basePrice = order.quantity * order.unitPrice;
  if (basePrice > 50) {
    return 0; // Free shipping
  }
  return 5.99;
}

function getTotalPrice(order) {
  const basePrice = getBasePrice(order);
  const discount = getDiscount(order);
  const tax = getTax(order);
  const shipping = getShipping(order);
  
  return basePrice - discount + tax + shipping;
}

// Usage - repetitive calculations and multiple function calls
const order = {
  quantity: 10,
  unitPrice: 25.00,
  taxRate: 0.08,
  customer: { isPremium: true }
};

const basePrice = getBasePrice(order);
const discount = getDiscount(order);
const tax = getTax(order);
const shipping = getShipping(order);
const total = getTotalPrice(order);

console.log(`Base: $${basePrice}, Discount: $${discount}, Tax: $${tax}, Shipping: $${shipping}, Total: $${total}`);

// After - Single transform function
function enrichOrder(order) {
  const basePrice = order.quantity * order.unitPrice;
  
  // Calculate discount
  let discount = 0;
  if (order.quantity > 100) {
    discount = basePrice * 0.1; // 10% bulk discount
  } else if (order.customer.isPremium) {
    discount = basePrice * 0.05; // 5% premium discount
  }
  
  // Calculate tax
  const taxableAmount = basePrice - discount;
  const tax = taxableAmount * order.taxRate;
  
  // Calculate shipping
  const shipping = basePrice > 50 ? 0 : 5.99;
  
  // Calculate total
  const total = basePrice - discount + tax + shipping;
  
  // Return enriched order with all calculated values
  return {
    ...order,
    pricing: {
      basePrice,
      discount,
      tax,
      shipping,
      total,
      savings: discount,
      effectiveRate: total / basePrice
    }
  };
}

// Usage - single calculation, all values available
const order = {
  quantity: 10,
  unitPrice: 25.00,
  taxRate: 0.08,
  customer: { isPremium: true }
};

const enrichedOrder = enrichOrder(order);
const pricing = enrichedOrder.pricing;

console.log(`Base: $${pricing.basePrice}, Discount: $${pricing.discount}, Tax: $${pricing.tax}, Shipping: $${pricing.shipping}, Total: $${pricing.total}`);
console.log(`You saved $${pricing.savings} (${(pricing.savings / pricing.basePrice * 100).toFixed(1)}%)`);
```

### Advanced Example - User Analytics Transform
```javascript
// Before - Separate analytics functions
function getUserActivityScore(user) {
  const loginDays = user.loginHistory.length;
  const avgSessionLength = user.sessionLengths.reduce((a, b) => a + b, 0) / user.sessionLengths.length;
  return (loginDays * 10) + (avgSessionLength / 60 * 5);
}

function getUserEngagementLevel(user) {
  const score = getUserActivityScore(user);
  if (score > 100) return 'high';
  if (score > 50) return 'medium';
  return 'low';
}

function getUserRetentionRisk(user) {
  const daysSinceLastLogin = (Date.now() - user.lastLoginDate) / (1000 * 60 * 60 * 24);
  const activityScore = getUserActivityScore(user);
  
  if (daysSinceLastLogin > 30 || activityScore < 20) {
    return 'high';
  }
  if (daysSinceLastLogin > 7 || activityScore < 50) {
    return 'medium';
  }
  return 'low';
}

function getUserLifetimeValue(user) {
  const totalPurchases = user.purchases.reduce((sum, purchase) => sum + purchase.amount, 0);
  const avgOrderValue = totalPurchases / user.purchases.length;
  const activityScore = getUserActivityScore(user);
  
  return totalPurchases + (avgOrderValue * activityScore / 20);
}

function getUserSegment(user) {
  const ltv = getUserLifetimeValue(user);
  const engagement = getUserEngagementLevel(user);
  const risk = getUserRetentionRisk(user);
  
  if (ltv > 1000 && engagement === 'high' && risk === 'low') {
    return 'champion';
  }
  if (ltv > 500 && engagement === 'medium') {
    return 'loyal';
  }
  if (risk === 'high') {
    return 'at-risk';
  }
  return 'standard';
}

// Usage - many function calls with repeated calculations
const user = {
  id: 123,
  loginHistory: ['2023-01-01', '2023-01-03', '2023-01-05'],
  sessionLengths: [1800, 2400, 3600], // seconds
  lastLoginDate: Date.now() - (5 * 24 * 60 * 60 * 1000), // 5 days ago
  purchases: [
    { amount: 50, date: '2023-01-01' },
    { amount: 75, date: '2023-01-15' },
    { amount: 100, date: '2023-01-30' }
  ]
};

const activityScore = getUserActivityScore(user);
const engagement = getUserEngagementLevel(user);
const risk = getUserRetentionRisk(user);
const ltv = getUserLifetimeValue(user);
const segment = getUserSegment(user);

// After - Single analytics transform
function enrichUserWithAnalytics(user) {
  // Basic calculations
  const loginDays = user.loginHistory.length;
  const avgSessionLength = user.sessionLengths.reduce((a, b) => a + b, 0) / user.sessionLengths.length;
  const daysSinceLastLogin = (Date.now() - user.lastLoginDate) / (1000 * 60 * 60 * 24);
  const totalPurchases = user.purchases.reduce((sum, purchase) => sum + purchase.amount, 0);
  const avgOrderValue = user.purchases.length > 0 ? totalPurchases / user.purchases.length : 0;
  
  // Activity score calculation
  const activityScore = (loginDays * 10) + (avgSessionLength / 60 * 5);
  
  // Engagement level
  let engagementLevel = 'low';
  if (activityScore > 100) {
    engagementLevel = 'high';
  } else if (activityScore > 50) {
    engagementLevel = 'medium';
  }
  
  // Retention risk
  let retentionRisk = 'low';
  if (daysSinceLastLogin > 30 || activityScore < 20) {
    retentionRisk = 'high';
  } else if (daysSinceLastLogin > 7 || activityScore < 50) {
    retentionRisk = 'medium';
  }
  
  // Lifetime value
  const lifetimeValue = totalPurchases + (avgOrderValue * activityScore / 20);
  
  // User segment
  let segment = 'standard';
  if (lifetimeValue > 1000 && engagementLevel === 'high' && retentionRisk === 'low') {
    segment = 'champion';
  } else if (lifetimeValue > 500 && engagementLevel === 'medium') {
    segment = 'loyal';
  } else if (retentionRisk === 'high') {
    segment = 'at-risk';
  }
  
  // Additional derived metrics
  const purchaseFrequency = user.purchases.length / Math.max(1, loginDays);
  const sessionQuality = avgSessionLength > 1800 ? 'high' : avgSessionLength > 900 ? 'medium' : 'low';
  const recentActivity = daysSinceLastLogin <= 7;
  
  return {
    ...user,
    analytics: {
      // Core metrics
      activityScore,
      engagementLevel,
      retentionRisk,
      lifetimeValue,
      segment,
      
      // Detailed metrics
      loginDays,
      avgSessionLength,
      daysSinceLastLogin,
      totalPurchases,
      avgOrderValue,
      purchaseFrequency,
      sessionQuality,
      recentActivity,
      
      // Computed flags
      isHighValue: lifetimeValue > 500,
      isAtRisk: retentionRisk === 'high',
      needsAttention: retentionRisk === 'high' || engagementLevel === 'low',
      isChampion: segment === 'champion',
      
      // Recommendations
      recommendations: generateRecommendations(segment, retentionRisk, engagementLevel)
    }
  };
}

function generateRecommendations(segment, retentionRisk, engagementLevel) {
  const recommendations = [];
  
  if (retentionRisk === 'high') {
    recommendations.push('Send re-engagement email');
    recommendations.push('Offer special discount');
  }
  
  if (segment === 'champion') {
    recommendations.push('Invite to VIP program');
    recommendations.push('Request product feedback');
  }
  
  if (engagementLevel === 'low') {
    recommendations.push('Improve onboarding experience');
    recommendations.push('Send usage tips');
  }
  
  return recommendations;
}

// Usage - single transform, comprehensive data
const user = {
  id: 123,
  loginHistory: ['2023-01-01', '2023-01-03', '2023-01-05'],
  sessionLengths: [1800, 2400, 3600],
  lastLoginDate: Date.now() - (5 * 24 * 60 * 60 * 1000),
  purchases: [
    { amount: 50, date: '2023-01-01' },
    { amount: 75, date: '2023-01-15' },
    { amount: 100, date: '2023-01-30' }
  ]
};

const enrichedUser = enrichUserWithAnalytics(user);
const analytics = enrichedUser.analytics;

console.log(`User ${user.id}:`);
console.log(`- Segment: ${analytics.segment}`);
console.log(`- Activity Score: ${analytics.activityScore}`);
console.log(`- Engagement: ${analytics.engagementLevel}`);
console.log(`- Risk: ${analytics.retentionRisk}`);
console.log(`- LTV: $${analytics.lifetimeValue.toFixed(2)}`);
console.log(`- Recommendations: ${analytics.recommendations.join(', ')}`);

// Easy to use for filtering and processing
const users = [user, /* other users */];
const enrichedUsers = users.map(enrichUserWithAnalytics);

// Filter high-value at-risk users
const atRiskChampions = enrichedUsers.filter(u => 
  u.analytics.isHighValue && u.analytics.isAtRisk
);

// Group by segment
const usersBySegment = enrichedUsers.reduce((groups, user) => {
  const segment = user.analytics.segment;
  groups[segment] = groups[segment] || [];
  groups[segment].push(user);
  return groups;
}, {});
```

### Performance Comparison Example
```javascript
// Before - Multiple function calls with repeated work
function processOrdersBefore(orders) {
  return orders.map(order => ({
    id: order.id,
    basePrice: getBasePrice(order),
    discount: getDiscount(order),
    tax: getTax(order),
    shipping: getShipping(order),
    total: getTotalPrice(order)
  }));
}

// After - Single transform per order
function processOrdersAfter(orders) {
  return orders.map(enrichOrder);
}

// Performance test with 1000 orders
const orders = Array.from({ length: 1000 }, (_, i) => ({
  id: i,
  quantity: Math.floor(Math.random() * 50) + 1,
  unitPrice: Math.random() * 100 + 10,
  taxRate: 0.08,
  customer: { isPremium: Math.random() > 0.8 }
}));

console.time('Before - Multiple functions');
const resultsBefore = processOrdersBefore(orders);
console.timeEnd('Before - Multiple functions');

console.time('After - Single transform');
const resultsAfter = processOrdersAfter(orders);
console.timeEnd('After - Single transform');
```

## Mechanics

1. **Identify related transformations**
   - Find functions that derive data from the same source
   - Look for repeated calculations across functions
   - Group functions by the data they transform

2. **Analyze dependencies**
   - Map out which calculations depend on others
   - Identify base calculations that are repeated
   - Find opportunities to optimize calculation order

3. **Create transform function**
   - Create single function that accepts source data
   - Perform all calculations in optimal order
   - Return enriched data structure with all derived values

4. **Optimize calculations**
   - Calculate each value only once
   - Reuse intermediate results
   - Order calculations to minimize redundant work

5. **Design result structure**
   - Group related calculated values logically
   - Include original data alongside derived data
   - Consider flat vs nested structure based on usage

6. **Update callers**
   - Replace multiple function calls with single transform
   - Update code to access values from result structure
   - Consider caching transformed results if appropriate

7. **Test thoroughly**
   - Verify all calculations produce same results
   - Test performance improvements
   - Check that all derived values are accessible

## When to Use

- **Related calculations**: Functions that derive data from same source
- **Performance issues**: Repeated calculations causing slowness
- **Scattered logic**: Related transformations in different places
- **Batch processing**: Need to transform many items efficiently
- **Complex derivations**: Multiple interdependent calculations
- **Data enrichment**: Adding calculated fields to existing data

## Trade-offs

### Benefits
- **Performance**: Calculate each value only once
- **Centralization**: All transformations in one place
- **Consistency**: Single source of truth for calculations
- **Maintainability**: Changes to logic in one location
- **Completeness**: All derived values available together
- **Optimization**: Can optimize calculation order and reuse

### Drawbacks
- **Large functions**: Transform functions can become complex
- **Memory usage**: Returns larger objects with all calculated values
- **Unnecessary calculations**: Might calculate values that aren't needed
- **Breaking changes**: Different interface than separate functions
- **Testing complexity**: Need to test entire transformation together

## Related Refactorings

- [Combine Functions into Class](combine-functions-into-class.md) - Alternative approach when you need stateful behavior
- [Extract Function](extract-function.md) - Break down complex transform functions
- [Split Phase](split-phase.md) - Separate distinct phases of complex transformations