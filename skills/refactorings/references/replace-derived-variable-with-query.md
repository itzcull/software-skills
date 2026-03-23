---
title: "Replace Derived Variable with Query"
description: "Replace a variable holding a calculated value with a method that calculates on demand"
category: "Organizing Data"
tags: ["derived", "variable", "query", "synchronization", "calculation"]
related: ["extract-function", "replace-temp-with-query", "split-variable"]
---

# Replace Derived Variable with Query

Replace a variable that holds a calculated value with a method that calculates the value on demand. This eliminates the need to keep derived data synchronized with its source data.

## Motivation

Derived variables that store calculated values create several problems:

- **Synchronization issues**: Derived data can become stale when source data changes
- **Complex updates**: Need to remember to update derived values everywhere
- **Memory overhead**: Storing calculated values that could be computed
- **Consistency bugs**: Derived values may not match their source data
- **Temporal coupling**: Order of updates becomes critical

## Example

### Basic Example
```javascript
// Before - Derived variable that can get out of sync
class ShoppingCart {
  constructor() {
    this._items = [];
    this._totalPrice = 0; // Derived variable
    this._itemCount = 0;  // Derived variable
  }
  
  addItem(item) {
    this._items.push(item);
    // Must remember to update derived variables
    this._totalPrice += item.price;
    this._itemCount++;
  }
  
  removeItem(item) {
    const index = this._items.indexOf(item);
    if (index > -1) {
      this._items.splice(index, 1);
      // Must remember to update derived variables
      this._totalPrice -= item.price;
      this._itemCount--;
    }
  }
  
  updateItemQuantity(item, newQuantity) {
    const oldQuantity = item.quantity;
    const priceDifference = item.price * (newQuantity - oldQuantity);
    
    item.quantity = newQuantity;
    // Easy to forget this update!
    this._totalPrice += priceDifference;
  }
  
  applyDiscount(percentage) {
    // This breaks our total calculation!
    this._items.forEach(item => {
      item.price *= (1 - percentage / 100);
    });
    // Forgot to update _totalPrice - now it's wrong!
  }
  
  get totalPrice() {
    return this._totalPrice;
  }
  
  get itemCount() {
    return this._itemCount;
  }
}

// After - Calculate values on demand
class ShoppingCart {
  constructor() {
    this._items = [];
  }
  
  addItem(item) {
    this._items.push(item);
    // No need to update derived values
  }
  
  removeItem(item) {
    const index = this._items.indexOf(item);
    if (index > -1) {
      this._items.splice(index, 1);
      // No synchronization needed
    }
  }
  
  updateItemQuantity(item, newQuantity) {
    item.quantity = newQuantity;
    // Derived values automatically reflect changes
  }
  
  applyDiscount(percentage) {
    this._items.forEach(item => {
      item.price *= (1 - percentage / 100);
    });
    // Total price automatically updates
  }
  
  // Calculate total price on demand
  get totalPrice() {
    return this._items.reduce((total, item) => {
      return total + (item.price * item.quantity);
    }, 0);
  }
  
  // Calculate item count on demand
  get itemCount() {
    return this._items.reduce((count, item) => {
      return count + item.quantity;
    }, 0);
  }
  
  // Additional calculated properties
  get averageItemPrice() {
    if (this.itemCount === 0) return 0;
    return this.totalPrice / this.itemCount;
  }
  
  get uniqueItemCount() {
    return this._items.length;
  }
}
```

### Complex Example - Employee Analytics
```javascript
// Before - Multiple derived variables that are hard to keep in sync
class EmployeeAnalytics {
  constructor() {
    this._employees = [];
    
    // Derived variables that need constant updates
    this._totalSalary = 0;
    this._averageSalary = 0;
    this._departmentCounts = {};
    this._seniorityDistribution = {};
    this._salaryByDepartment = {};
    this._totalEmployees = 0;
    this._activeEmployees = 0;
  }
  
  addEmployee(employee) {
    this._employees.push(employee);
    
    // Update all derived variables - error-prone!
    this._totalSalary += employee.salary;
    this._totalEmployees++;
    
    if (employee.isActive) {
      this._activeEmployees++;
    }
    
    // Update department counts
    if (!this._departmentCounts[employee.department]) {
      this._departmentCounts[employee.department] = 0;
    }
    this._departmentCounts[employee.department]++;
    
    // Update seniority distribution
    const seniorityLevel = this._getSeniorityLevel(employee.yearsOfService);
    if (!this._seniorityDistribution[seniorityLevel]) {
      this._seniorityDistribution[seniorityLevel] = 0;
    }
    this._seniorityDistribution[seniorityLevel]++;
    
    // Update salary by department
    if (!this._salaryByDepartment[employee.department]) {
      this._salaryByDepartment[employee.department] = 0;
    }
    this._salaryByDepartment[employee.department] += employee.salary;
    
    // Recalculate average
    this._averageSalary = this._totalSalary / this._totalEmployees;
  }
  
  removeEmployee(employee) {
    const index = this._employees.indexOf(employee);
    if (index === -1) return;
    
    this._employees.splice(index, 1);
    
    // Update all derived variables - lots of room for errors!
    this._totalSalary -= employee.salary;
    this._totalEmployees--;
    
    if (employee.isActive) {
      this._activeEmployees--;
    }
    
    this._departmentCounts[employee.department]--;
    if (this._departmentCounts[employee.department] === 0) {
      delete this._departmentCounts[employee.department];
    }
    
    const seniorityLevel = this._getSeniorityLevel(employee.yearsOfService);
    this._seniorityDistribution[seniorityLevel]--;
    if (this._seniorityDistribution[seniorityLevel] === 0) {
      delete this._seniorityDistribution[seniorityLevel];
    }
    
    this._salaryByDepartment[employee.department] -= employee.salary;
    if (this._salaryByDepartment[employee.department] === 0) {
      delete this._salaryByDepartment[employee.department];
    }
    
    // Recalculate average
    this._averageSalary = this._totalEmployees > 0 ? this._totalSalary / this._totalEmployees : 0;
  }
  
  updateEmployeeSalary(employee, newSalary) {
    const oldSalary = employee.salary;
    employee.salary = newSalary;
    
    // Update derived values - easy to miss!
    this._totalSalary += (newSalary - oldSalary);
    this._salaryByDepartment[employee.department] += (newSalary - oldSalary);
    this._averageSalary = this._totalSalary / this._totalEmployees;
  }
  
  promoteEmployee(employee, newDepartment) {
    const oldDepartment = employee.department;
    employee.department = newDepartment;
    
    // Complex updates across multiple derived variables
    this._departmentCounts[oldDepartment]--;
    if (this._departmentCounts[oldDepartment] === 0) {
      delete this._departmentCounts[oldDepartment];
    }
    
    if (!this._departmentCounts[newDepartment]) {
      this._departmentCounts[newDepartment] = 0;
    }
    this._departmentCounts[newDepartment]++;
    
    this._salaryByDepartment[oldDepartment] -= employee.salary;
    if (this._salaryByDepartment[oldDepartment] === 0) {
      delete this._salaryByDepartment[oldDepartment];
    }
    
    if (!this._salaryByDepartment[newDepartment]) {
      this._salaryByDepartment[newDepartment] = 0;
    }
    this._salaryByDepartment[newDepartment] += employee.salary;
  }
  
  // Getters that return pre-calculated values
  get totalSalary() { return this._totalSalary; }
  get averageSalary() { return this._averageSalary; }
  get totalEmployees() { return this._totalEmployees; }
  get activeEmployees() { return this._activeEmployees; }
  get departmentCounts() { return { ...this._departmentCounts }; }
  get seniorityDistribution() { return { ...this._seniorityDistribution }; }
  get salaryByDepartment() { return { ...this._salaryByDepartment }; }
  
  _getSeniorityLevel(years) {
    if (years < 2) return 'junior';
    if (years < 5) return 'mid';
    if (years < 10) return 'senior';
    return 'principal';
  }
}

// After - Calculate everything on demand
class EmployeeAnalytics {
  constructor() {
    this._employees = [];
  }
  
  addEmployee(employee) {
    this._employees.push(employee);
    // No derived variables to update!
  }
  
  removeEmployee(employee) {
    const index = this._employees.indexOf(employee);
    if (index > -1) {
      this._employees.splice(index, 1);
      // Everything automatically stays in sync
    }
  }
  
  updateEmployeeSalary(employee, newSalary) {
    employee.salary = newSalary;
    // All calculations automatically reflect the change
  }
  
  promoteEmployee(employee, newDepartment) {
    employee.department = newDepartment;
    // No manual updates needed
  }
  
  setEmployeeActive(employee, isActive) {
    employee.isActive = isActive;
    // Active count automatically updates
  }
  
  // Calculate values on demand - always accurate
  get totalSalary() {
    return this._employees.reduce((total, emp) => total + emp.salary, 0);
  }
  
  get averageSalary() {
    if (this._employees.length === 0) return 0;
    return this.totalSalary / this._employees.length;
  }
  
  get totalEmployees() {
    return this._employees.length;
  }
  
  get activeEmployees() {
    return this._employees.filter(emp => emp.isActive).length;
  }
  
  get departmentCounts() {
    return this._employees.reduce((counts, emp) => {
      counts[emp.department] = (counts[emp.department] || 0) + 1;
      return counts;
    }, {});
  }
  
  get seniorityDistribution() {
    return this._employees.reduce((dist, emp) => {
      const level = this._getSeniorityLevel(emp.yearsOfService);
      dist[level] = (dist[level] || 0) + 1;
      return dist;
    }, {});
  }
  
  get salaryByDepartment() {
    return this._employees.reduce((salaries, emp) => {
      salaries[emp.department] = (salaries[emp.department] || 0) + emp.salary;
      return salaries;
    }, {});
  }
  
  // Additional calculated properties - easy to add!
  get averageSalaryByDepartment() {
    const salaryByDept = this.salaryByDepartment;
    const countsByDept = this.departmentCounts;
    
    const result = {};
    for (const dept in salaryByDept) {
      result[dept] = salaryByDept[dept] / countsByDept[dept];
    }
    return result;
  }
  
  get seniorityByDepartment() {
    return this._employees.reduce((result, emp) => {
      if (!result[emp.department]) {
        result[emp.department] = [];
      }
      result[emp.department].push({
        name: emp.name,
        seniority: this._getSeniorityLevel(emp.yearsOfService),
        years: emp.yearsOfService
      });
      return result;
    }, {});
  }
  
  get highestPaidByDepartment() {
    return this._employees.reduce((result, emp) => {
      if (!result[emp.department] || emp.salary > result[emp.department].salary) {
        result[emp.department] = emp;
      }
      return result;
    }, {});
  }
  
  _getSeniorityLevel(years) {
    if (years < 2) return 'junior';
    if (years < 5) return 'mid';
    if (years < 10) return 'senior';
    return 'principal';
  }
}
```

### Performance-Conscious Example with Caching
```javascript
// When calculations are expensive, use caching with invalidation
class ProductCatalog {
  constructor() {
    this._products = [];
    this._cache = new Map();
    this._cacheVersion = 0;
  }
  
  addProduct(product) {
    this._products.push(product);
    this._invalidateCache();
  }
  
  removeProduct(productId) {
    this._products = this._products.filter(p => p.id !== productId);
    this._invalidateCache();
  }
  
  updateProduct(productId, updates) {
    const product = this._products.find(p => p.id === productId);
    if (product) {
      Object.assign(product, updates);
      this._invalidateCache();
    }
  }
  
  // Expensive calculation with caching
  get categoryStatistics() {
    return this._getCachedValue('categoryStats', () => {
      const stats = {};
      
      for (const product of this._products) {
        if (!stats[product.category]) {
          stats[product.category] = {
            count: 0,
            totalValue: 0,
            averagePrice: 0,
            priceRange: { min: Infinity, max: -Infinity }
          };
        }
        
        const categoryStats = stats[product.category];
        categoryStats.count++;
        categoryStats.totalValue += product.price;
        categoryStats.priceRange.min = Math.min(categoryStats.priceRange.min, product.price);
        categoryStats.priceRange.max = Math.max(categoryStats.priceRange.max, product.price);
      }
      
      // Calculate averages
      for (const category in stats) {
        stats[category].averagePrice = stats[category].totalValue / stats[category].count;
      }
      
      return stats;
    });
  }
  
  get priceDistribution() {
    return this._getCachedValue('priceDistribution', () => {
      const buckets = {
        'under_10': 0,
        '10_to_50': 0,
        '50_to_100': 0,
        '100_to_500': 0,
        'over_500': 0
      };
      
      for (const product of this._products) {
        if (product.price < 10) buckets['under_10']++;
        else if (product.price < 50) buckets['10_to_50']++;
        else if (product.price < 100) buckets['50_to_100']++;
        else if (product.price < 500) buckets['100_to_500']++;
        else buckets['over_500']++;
      }
      
      return buckets;
    });
  }
  
  get totalInventoryValue() {
    return this._getCachedValue('totalValue', () => {
      return this._products.reduce((total, product) => {
        return total + (product.price * product.stockQuantity);
      }, 0);
    });
  }
  
  _getCachedValue(key, calculator) {
    const cacheKey = `${key}_${this._cacheVersion}`;
    
    if (this._cache.has(cacheKey)) {
      return this._cache.get(cacheKey);
    }
    
    const value = calculator();
    this._cache.set(cacheKey, value);
    
    // Clean old cache entries
    this._cleanOldCacheEntries(key);
    
    return value;
  }
  
  _invalidateCache() {
    this._cacheVersion++;
  }
  
  _cleanOldCacheEntries(key) {
    const currentCacheKey = `${key}_${this._cacheVersion}`;
    const keysToDelete = [];
    
    for (const cacheKey of this._cache.keys()) {
      if (cacheKey.startsWith(`${key}_`) && cacheKey !== currentCacheKey) {
        keysToDelete.push(cacheKey);
      }
    }
    
    keysToDelete.forEach(key => this._cache.delete(key));
  }
}
```

## Mechanics

1. **Identify derived variables**
   - Look for variables that store calculated values
   - Find variables that need updating when source data changes
   - Check for synchronization bugs between derived and source data

2. **Create query methods**
   - Replace each derived variable with a method or getter
   - Calculate the value from source data on each call
   - Ensure the calculation is correct and complete

3. **Remove derived variables**
   - Delete the derived variable fields
   - Remove all code that updates these variables
   - Simplify methods that no longer need to maintain derived state

4. **Update client code**
   - Change direct variable access to method calls
   - Remove any code that manually updates derived variables
   - Verify that all calculations are correct

5. **Consider performance**
   - Add caching if calculations are expensive
   - Use memoization for frequently accessed values
   - Profile to ensure performance is acceptable

6. **Test thoroughly**
   - Verify that calculated values are always correct
   - Test that changes to source data are reflected immediately
   - Check that performance is acceptable

## When to Use

- **Synchronization problems**: Derived variables get out of sync with source data
- **Complex update logic**: Many places need to update derived variables
- **Frequent bugs**: Derived values don't match their calculations
- **Simple calculations**: Calculations are fast enough to do on demand
- **Infrequent access**: Derived values aren't accessed very often
- **Source data changes**: Source data is modified in many places

## When NOT to Use

- **Expensive calculations**: Computing the value is very costly
- **Frequent access**: Value is accessed many times per second
- **Complex dependencies**: Calculation depends on many external factors
- **Real-time requirements**: Need immediate access to calculated values
- **Memory is cheap**: Storage cost is lower than calculation cost

## Trade-offs

### Benefits
- **Always accurate**: Values are always up-to-date with source data
- **Simpler code**: No need to maintain synchronization logic
- **Fewer bugs**: Eliminates synchronization errors
- **Easier maintenance**: Changes to calculations are localized
- **Memory savings**: Don't store calculated values

### Drawbacks
- **Performance cost**: Recalculate values on each access
- **CPU usage**: More computation per access
- **Complexity**: Some calculations may be complex to implement
- **Dependencies**: May need to redesign data access patterns

## Performance Optimization Strategies

### Lazy Evaluation with Caching
```javascript
class DataAnalyzer {
  constructor() {
    this._data = [];
    this._cache = {};
    this._version = 0;
  }
  
  updateData(newData) {
    this._data = newData;
    this._version++;
    this._cache = {}; // Invalidate cache
  }
  
  get expensiveCalculation() {
    const cacheKey = `expensiveCalc_${this._version}`;
    if (!this._cache[cacheKey]) {
      this._cache[cacheKey] = this._performExpensiveCalculation();
    }
    return this._cache[cacheKey];
  }
}
```

### Incremental Updates
```javascript
class RunningStatistics {
  constructor() {
    this._values = [];
    this._sum = 0;
    this._sumOfSquares = 0;
  }
  
  addValue(value) {
    this._values.push(value);
    this._sum += value;
    this._sumOfSquares += value * value;
  }
  
  get mean() {
    return this._sum / this._values.length;
  }
  
  get variance() {
    const n = this._values.length;
    return (this._sumOfSquares - (this._sum * this._sum) / n) / (n - 1);
  }
}
```

## Related Refactorings

- [Extract Variable](extract-variable.md) - Create intermediate calculations
- [Inline Variable](inline-variable.md) - Remove unnecessary stored calculations
- [Replace Temp with Query](replace-derived-variable-with-query.md) - Similar concept for temporary variables
- [Introduce Parameter Object](introduce-parameter-object.md) - Group related data for calculations
- [Move Method](move-method.md) - Move calculations to appropriate classes