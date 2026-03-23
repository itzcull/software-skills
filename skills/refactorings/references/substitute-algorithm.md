---
title: "Substitute Algorithm"
description: "Replace a method's algorithm with a clearer, more efficient, or more maintainable one"
category: "Organization"
tags: ["substitute", "algorithm", "performance", "clarity", "efficiency"]
related: ["extract-function", "inline-function", "replace-loop-with-pipeline"]
---

# Substitute Algorithm

Replace the body of a method with a clearer, more efficient, or more maintainable algorithm while keeping the interface the same. This improves performance, readability, or correctness.

## Motivation

Algorithms may need replacement for several reasons:

- **Performance issues**: Current algorithm is too slow or uses too much memory
- **Clarity problems**: Algorithm is hard to understand or maintain
- **Correctness issues**: Algorithm has bugs or edge case problems
- **Better approach discovered**: New algorithm is simpler or more elegant
- **Technology changes**: New language features or libraries available
- **Requirements evolution**: Algorithm no longer fits the problem well

## Example

### Basic Example - Finding Maximum
```javascript
// Before - Complex manual approach
function findMaxValue(numbers) {
  if (!numbers || numbers.length === 0) {
    throw new Error('Array cannot be empty');
  }
  
  let max = numbers[0];
  let i = 1;
  
  while (i < numbers.length) {
    if (numbers[i] > max) {
      max = numbers[i];
    }
    i++;
  }
  
  return max;
}

// After - Using built-in method
function findMaxValue(numbers) {
  if (!numbers || numbers.length === 0) {
    throw new Error('Array cannot be empty');
  }
  
  return Math.max(...numbers);
}
```

### Performance Optimization Example
```javascript
// Before - O(n²) algorithm for finding duplicates
function findDuplicates(array) {
  const duplicates = [];
  
  for (let i = 0; i < array.length; i++) {
    for (let j = i + 1; j < array.length; j++) {
      if (array[i] === array[j]) {
        if (!duplicates.includes(array[i])) {
          duplicates.push(array[i]);
        }
      }
    }
  }
  
  return duplicates;
}

// After - O(n) algorithm using Set
function findDuplicates(array) {
  const seen = new Set();
  const duplicates = new Set();
  
  for (const item of array) {
    if (seen.has(item)) {
      duplicates.add(item);
    } else {
      seen.add(item);
    }
  }
  
  return Array.from(duplicates);
}
```

### Complex Example - User Authentication
```javascript
// Before - Complex manual token validation
function validateUserToken(token) {
  if (!token) {
    return { valid: false, error: 'Token required' };
  }
  
  // Manual base64 decoding
  let decoded;
  try {
    const base64 = token.replace(/-/g, '+').replace(/_/g, '/');
    const padding = base64.length % 4;
    const padded = base64 + '='.repeat(padding ? 4 - padding : 0);
    decoded = atob(padded);
  } catch (error) {
    return { valid: false, error: 'Invalid token format' };
  }
  
  // Manual JSON parsing
  let payload;
  try {
    payload = JSON.parse(decoded);
  } catch (error) {
    return { valid: false, error: 'Invalid token payload' };
  }
  
  // Manual signature verification (simplified)
  const parts = token.split('.');
  if (parts.length !== 3) {
    return { valid: false, error: 'Invalid token structure' };
  }
  
  const header = parts[0];
  const payloadPart = parts[1];
  const signature = parts[2];
  
  // Simplified signature check (not cryptographically secure)
  const expectedSignature = btoa(header + '.' + payloadPart + 'secret');
  if (signature !== expectedSignature) {
    return { valid: false, error: 'Invalid signature' };
  }
  
  // Manual expiration check
  const now = Math.floor(Date.now() / 1000);
  if (payload.exp && payload.exp < now) {
    return { valid: false, error: 'Token expired' };
  }
  
  // Manual issuer check
  if (payload.iss !== 'our-app') {
    return { valid: false, error: 'Invalid issuer' };
  }
  
  return {
    valid: true,
    user: {
      id: payload.sub,
      email: payload.email,
      roles: payload.roles || []
    }
  };
}

// After - Using JWT library (much more secure and maintainable)
const jwt = require('jsonwebtoken');

function validateUserToken(token) {
  if (!token) {
    return { valid: false, error: 'Token required' };
  }
  
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET, {
      issuer: 'our-app',
      algorithms: ['HS256']
    });
    
    return {
      valid: true,
      user: {
        id: payload.sub,
        email: payload.email,
        roles: payload.roles || []
      }
    };
  } catch (error) {
    let errorMessage = 'Invalid token';
    
    if (error.name === 'TokenExpiredError') {
      errorMessage = 'Token expired';
    } else if (error.name === 'JsonWebTokenError') {
      errorMessage = 'Invalid token format';
    } else if (error.name === 'NotBeforeError') {
      errorMessage = 'Token not active yet';
    }
    
    return { valid: false, error: errorMessage };
  }
}
```

### Sorting Algorithm Example
```javascript
// Before - Manual bubble sort implementation
function sortUsers(users) {
  const sorted = [...users]; // Don't mutate original array
  
  for (let i = 0; i < sorted.length - 1; i++) {
    for (let j = 0; j < sorted.length - i - 1; j++) {
      // Compare by last name, then first name
      const user1 = sorted[j];
      const user2 = sorted[j + 1];
      
      const lastName1 = user1.lastName.toLowerCase();
      const lastName2 = user2.lastName.toLowerCase();
      
      let shouldSwap = false;
      
      if (lastName1 > lastName2) {
        shouldSwap = true;
      } else if (lastName1 === lastName2) {
        const firstName1 = user1.firstName.toLowerCase();
        const firstName2 = user2.firstName.toLowerCase();
        if (firstName1 > firstName2) {
          shouldSwap = true;
        }
      }
      
      if (shouldSwap) {
        const temp = sorted[j];
        sorted[j] = sorted[j + 1];
        sorted[j + 1] = temp;
      }
    }
  }
  
  return sorted;
}

// After - Using native sort with proper comparator
function sortUsers(users) {
  return [...users].sort((a, b) => {
    const lastNameComparison = a.lastName.localeCompare(b.lastName);
    if (lastNameComparison !== 0) {
      return lastNameComparison;
    }
    return a.firstName.localeCompare(b.firstName);
  });
}
```

### String Processing Example
```javascript
// Before - Manual string parsing
function parseEmailAddress(email) {
  if (!email || typeof email !== 'string') {
    return null;
  }
  
  // Manual validation
  let atCount = 0;
  let atIndex = -1;
  
  for (let i = 0; i < email.length; i++) {
    if (email[i] === '@') {
      atCount++;
      if (atCount === 1) {
        atIndex = i;
      }
    }
  }
  
  if (atCount !== 1 || atIndex === 0 || atIndex === email.length - 1) {
    return null;
  }
  
  const localPart = email.substring(0, atIndex);
  const domain = email.substring(atIndex + 1);
  
  // Manual domain validation
  if (!domain.includes('.')) {
    return null;
  }
  
  let dotIndex = -1;
  for (let i = domain.length - 1; i >= 0; i--) {
    if (domain[i] === '.') {
      dotIndex = i;
      break;
    }
  }
  
  if (dotIndex === 0 || dotIndex === domain.length - 1) {
    return null;
  }
  
  const domainName = domain.substring(0, dotIndex);
  const tld = domain.substring(dotIndex + 1);
  
  // Check for valid characters (simplified)
  const validChars = /^[a-zA-Z0-9.-]+$/;
  if (!validChars.test(localPart) || !validChars.test(domain)) {
    return null;
  }
  
  return {
    localPart,
    domain,
    domainName,
    tld,
    full: email
  };
}

// After - Using regular expressions
function parseEmailAddress(email) {
  if (!email || typeof email !== 'string') {
    return null;
  }
  
  const emailRegex = /^([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})$/;
  const match = email.match(emailRegex);
  
  if (!match) {
    return null;
  }
  
  const [full, localPart, domainPart, tld] = match;
  const domain = domainPart + '.' + tld;
  
  return {
    localPart,
    domain,
    domainName: domainPart,
    tld,
    full
  };
}
```

### Data Processing Example
```javascript
// Before - Manual data aggregation
function calculateMonthlyStats(transactions) {
  const monthlyData = {};
  
  // Group by month manually
  for (const transaction of transactions) {
    const date = new Date(transaction.date);
    const monthKey = date.getFullYear() + '-' + (date.getMonth() + 1);
    
    if (!monthlyData[monthKey]) {
      monthlyData[monthKey] = {
        transactions: [],
        totalAmount: 0,
        count: 0,
        categories: {}
      };
    }
    
    monthlyData[monthKey].transactions.push(transaction);
    monthlyData[monthKey].totalAmount += transaction.amount;
    monthlyData[monthKey].count++;
    
    if (!monthlyData[monthKey].categories[transaction.category]) {
      monthlyData[monthKey].categories[transaction.category] = {
        amount: 0,
        count: 0
      };
    }
    
    monthlyData[monthKey].categories[transaction.category].amount += transaction.amount;
    monthlyData[monthKey].categories[transaction.category].count++;
  }
  
  // Calculate averages manually
  const result = [];
  for (const monthKey in monthlyData) {
    const data = monthlyData[monthKey];
    result.push({
      month: monthKey,
      totalAmount: data.totalAmount,
      transactionCount: data.count,
      averageAmount: data.totalAmount / data.count,
      categories: Object.entries(data.categories).map(([category, stats]) => ({
        category,
        amount: stats.amount,
        count: stats.count,
        percentage: (stats.amount / data.totalAmount) * 100
      }))
    });
  }
  
  return result;
}

// After - Using functional programming approach
function calculateMonthlyStats(transactions) {
  const groupedByMonth = transactions.reduce((acc, transaction) => {
    const date = new Date(transaction.date);
    const monthKey = `${date.getFullYear()}-${date.getMonth() + 1}`;
    
    if (!acc[monthKey]) {
      acc[monthKey] = [];
    }
    acc[monthKey].push(transaction);
    
    return acc;
  }, {});
  
  return Object.entries(groupedByMonth).map(([month, monthTransactions]) => {
    const totalAmount = monthTransactions.reduce((sum, t) => sum + t.amount, 0);
    
    const categories = monthTransactions
      .reduce((acc, transaction) => {
        const category = transaction.category;
        if (!acc[category]) {
          acc[category] = { amount: 0, count: 0 };
        }
        acc[category].amount += transaction.amount;
        acc[category].count++;
        return acc;
      }, {});
    
    return {
      month,
      totalAmount,
      transactionCount: monthTransactions.length,
      averageAmount: totalAmount / monthTransactions.length,
      categories: Object.entries(categories).map(([category, stats]) => ({
        category,
        amount: stats.amount,
        count: stats.count,
        percentage: (stats.amount / totalAmount) * 100
      }))
    };
  });
}
```

### Search Algorithm Example
```javascript
// Before - Linear search implementation
function findUserById(users, targetId) {
  for (let i = 0; i < users.length; i++) {
    if (users[i].id === targetId) {
      return users[i];
    }
  }
  return null;
}

function findUsersByRole(users, targetRole) {
  const results = [];
  for (let i = 0; i < users.length; i++) {
    if (users[i].role === targetRole) {
      results.push(users[i]);
    }
  }
  return results;
}

function findUsersByDepartment(users, department) {
  const results = [];
  for (let i = 0; i < users.length; i++) {
    if (users[i].department === department) {
      results.push(users[i]);
    }
  }
  return results;
}

// After - Using native array methods
function findUserById(users, targetId) {
  return users.find(user => user.id === targetId) || null;
}

function findUsersByRole(users, targetRole) {
  return users.filter(user => user.role === targetRole);
}

function findUsersByDepartment(users, department) {
  return users.filter(user => user.department === department);
}

// Even better - For large datasets, use Map for O(1) lookups
class UserRepository {
  constructor(users) {
    this.users = users;
    this.userById = new Map(users.map(user => [user.id, user]));
    this.usersByRole = this.groupBy('role');
    this.usersByDepartment = this.groupBy('department');
  }
  
  groupBy(field) {
    return this.users.reduce((acc, user) => {
      const key = user[field];
      if (!acc.has(key)) {
        acc.set(key, []);
      }
      acc.get(key).push(user);
      return acc;
    }, new Map());
  }
  
  findUserById(targetId) {
    return this.userById.get(targetId) || null;
  }
  
  findUsersByRole(targetRole) {
    return this.usersByRole.get(targetRole) || [];
  }
  
  findUsersByDepartment(department) {
    return this.usersByDepartment.get(department) || [];
  }
}
```

## Mechanics

1. **Understand the current algorithm**
   - Document what the algorithm does
   - Identify inputs, outputs, and side effects
   - Note any assumptions or constraints
   - Understand performance characteristics

2. **Research alternative approaches**
   - Look for standard algorithms for the problem
   - Consider built-in language features or libraries
   - Evaluate different algorithmic approaches
   - Consider performance and maintainability trade-offs

3. **Choose the replacement algorithm**
   - Select based on requirements (performance, clarity, maintainability)
   - Ensure the new algorithm handles all edge cases
   - Verify it meets the same interface contract
   - Consider the impact on the rest of the codebase

4. **Implement the new algorithm**
   - Replace the algorithm body while keeping the interface
   - Handle any new dependencies or imports
   - Ensure error handling is equivalent or better
   - Maintain the same level of input validation

5. **Test thoroughly**
   - Run existing tests to ensure compatibility
   - Test edge cases and boundary conditions
   - Performance test if that was a motivation
   - Consider adding new tests for the new implementation

6. **Consider gradual migration**
   - For critical systems, consider feature flags
   - Monitor performance and correctness
   - Have rollback plans if issues arise

## When to Use

- **Performance problems**: Current algorithm is too slow or memory-intensive
- **Complexity issues**: Algorithm is hard to understand or maintain
- **Bug fixes**: Current algorithm has correctness issues
- **Library availability**: Better solutions become available
- **Requirements change**: Algorithm no longer fits the problem
- **Code modernization**: Updating to use newer language features

## When NOT to Use

- **Working well**: Current algorithm meets all requirements
- **Risk too high**: Changes could introduce critical bugs
- **No clear benefit**: New algorithm isn't significantly better
- **External dependencies**: Team doesn't want new dependencies
- **Time constraints**: Not enough time to properly test changes

## Trade-offs

### Benefits
- **Improved performance**: Faster execution or lower memory usage
- **Better maintainability**: Clearer, more understandable code
- **Correctness**: Fix bugs or handle edge cases better
- **Modern practices**: Use current best practices and idioms
- **Library benefits**: Leverage well-tested, optimized libraries
- **Reduced complexity**: Simpler algorithms are easier to debug

### Drawbacks
- **Risk of introducing bugs**: Any change can introduce new issues
- **Learning curve**: Team may need to understand new approach
- **Dependencies**: May introduce new external dependencies
- **Testing overhead**: Need to thoroughly test the replacement
- **Compatibility**: May need to ensure backward compatibility

## Common Algorithm Substitutions

### Linear to Binary Search
```javascript
// Before: O(n)
function findInSorted(array, target) {
  for (let i = 0; i < array.length; i++) {
    if (array[i] === target) return i;
  }
  return -1;
}

// After: O(log n)
function findInSorted(array, target) {
  let left = 0;
  let right = array.length - 1;
  
  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (array[mid] === target) return mid;
    if (array[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  
  return -1;
}
```

### Manual Loops to Functional
```javascript
// Before: Imperative
function processUsers(users) {
  const result = [];
  for (const user of users) {
    if (user.isActive) {
      result.push(user.name.toUpperCase());
    }
  }
  return result;
}

// After: Functional
function processUsers(users) {
  return users
    .filter(user => user.isActive)
    .map(user => user.name.toUpperCase());
}
```

### Regular Loops to Built-in Methods
```javascript
// Before: Manual implementation
function sumArray(numbers) {
  let sum = 0;
  for (const num of numbers) {
    sum += num;
  }
  return sum;
}

// After: Built-in method
function sumArray(numbers) {
  return numbers.reduce((sum, num) => sum + num, 0);
}
```

## Related Refactorings

- [Extract Function](extract-function.md) - Extract the algorithm into its own function before substitution
- [Replace Loop with Pipeline](replace-loop-with-pipeline.md) - Replace manual loops with functional operations
- [Introduce Parameter Object](introduce-parameter-object.md) - Simplify complex algorithm parameters
- [Extract Variable](extract-variable.md) - Make complex algorithms more readable
- [Split Phase](split-phase.md) - Separate algorithm phases before substitution
- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Replace algorithmic conditionals with polymorphism