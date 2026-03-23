---
title: "Rename Variable"
description: "Change a variable name to better express its purpose and make code self-documenting"
category: "Rename"
tags: ["rename", "variable", "naming", "clarity", "readability", "self-documenting"]
related: ["rename-function", "extract-variable", "introduce-explaining-variable"]
---

# Rename Variable

Change a variable name to better express its purpose. Good variable names make code self-documenting and significantly improve readability.

## Motivation

Poor variable names create several problems:

- **Unclear intent**: Purpose of the variable is not obvious
- **Mental overhead**: Readers must remember what cryptic names mean
- **Maintenance difficulties**: Hard to understand and modify code
- **Increased bugs**: Misunderstanding variable purpose leads to errors
- **Poor communication**: Code doesn't effectively communicate with other developers

## Example

### Basic Example
```javascript
// Before - Cryptic variable names
function processOrder(o) {
  const t = o.items.reduce((s, i) => s + i.price * i.qty, 0);
  const d = t > 100 ? t * 0.1 : 0;
  const tx = (t - d) * 0.08;
  const sh = t > 50 ? 0 : 10;
  const f = t - d + tx + sh;
  
  if (f > 0) {
    const p = {
      amt: f,
      method: o.payment,
      id: generateId()
    };
    return processPayment(p);
  }
  
  return null;
}

// After - Clear variable names
function processOrder(order) {
  const subtotal = order.items.reduce((sum, item) => {
    return sum + item.price * item.quantity;
  }, 0);
  
  const discount = subtotal > 100 ? subtotal * 0.1 : 0;
  const tax = (subtotal - discount) * 0.08;
  const shipping = subtotal > 50 ? 0 : 10;
  const totalAmount = subtotal - discount + tax + shipping;
  
  if (totalAmount > 0) {
    const paymentRequest = {
      amount: totalAmount,
      method: order.paymentMethod,
      transactionId: generateTransactionId()
    };
    return processPayment(paymentRequest);
  }
  
  return null;
}
```

### Complex Example - Data Processing
```javascript
// Before - Poor variable naming throughout
function analyzeUserData(data) {
  const res = {};
  const u = data.users;
  let c = 0;
  let s = 0;
  const g = {};
  const a = {};
  
  for (const x of u) {
    c++;
    s += x.age;
    
    const k = x.location;
    if (!g[k]) g[k] = 0;
    g[k]++;
    
    const y = Math.floor(x.age / 10) * 10;
    const z = `${y}-${y + 9}`;
    if (!a[z]) a[z] = 0;
    a[z]++;
  }
  
  const avg = s / c;
  const t = Object.keys(g).reduce((m, k) => g[k] > g[m] ? k : m);
  const ma = Object.keys(a).reduce((m, k) => a[k] > a[m] ? k : m);
  
  res.count = c;
  res.averageAge = avg;
  res.topLocation = t;
  res.popularAgeGroup = ma;
  res.locationDistribution = g;
  res.ageDistribution = a;
  
  return res;
}

// After - Meaningful variable names
function analyzeUserData(userData) {
  const analysisResult = {};
  const users = userData.users;
  
  let userCount = 0;
  let totalAge = 0;
  const locationCounts = {};
  const ageGroupCounts = {};
  
  for (const user of users) {
    userCount++;
    totalAge += user.age;
    
    // Count users by location
    const userLocation = user.location;
    if (!locationCounts[userLocation]) {
      locationCounts[userLocation] = 0;
    }
    locationCounts[userLocation]++;
    
    // Count users by age group (decades)
    const ageGroupStart = Math.floor(user.age / 10) * 10;
    const ageGroupLabel = `${ageGroupStart}-${ageGroupStart + 9}`;
    if (!ageGroupCounts[ageGroupLabel]) {
      ageGroupCounts[ageGroupLabel] = 0;
    }
    ageGroupCounts[ageGroupLabel]++;
  }
  
  const averageAge = totalAge / userCount;
  
  const mostPopularLocation = Object.keys(locationCounts).reduce((mostPopular, location) => {
    return locationCounts[location] > locationCounts[mostPopular] ? location : mostPopular;
  });
  
  const largestAgeGroup = Object.keys(ageGroupCounts).reduce((largest, ageGroup) => {
    return ageGroupCounts[ageGroup] > ageGroupCounts[largest] ? ageGroup : largest;
  });
  
  analysisResult.userCount = userCount;
  analysisResult.averageAge = averageAge;
  analysisResult.mostPopularLocation = mostPopularLocation;
  analysisResult.largestAgeGroup = largestAgeGroup;
  analysisResult.locationDistribution = locationCounts;
  analysisResult.ageGroupDistribution = ageGroupCounts;
  
  return analysisResult;
}
```

### Loop Variable Example
```javascript
// Before - Generic loop variables
function processMatrix(matrix) {
  const result = [];
  
  for (let i = 0; i < matrix.length; i++) {
    const row = [];
    for (let j = 0; j < matrix[i].length; j++) {
      let sum = 0;
      for (let k = -1; k <= 1; k++) {
        for (let l = -1; l <= 1; l++) {
          const x = i + k;
          const y = j + l;
          if (x >= 0 && x < matrix.length && y >= 0 && y < matrix[x].length) {
            sum += matrix[x][y];
          }
        }
      }
      row.push(sum / 9);
    }
    result.push(row);
  }
  
  return result;
}

// After - Descriptive loop variables
function applyAverageFilter(imageMatrix) {
  const filteredMatrix = [];
  
  for (let currentRow = 0; currentRow < imageMatrix.length; currentRow++) {
    const processedRow = [];
    
    for (let currentCol = 0; currentCol < imageMatrix[currentRow].length; currentCol++) {
      let neighborSum = 0;
      
      // Examine 3x3 neighborhood around current pixel
      for (let rowOffset = -1; rowOffset <= 1; rowOffset++) {
        for (let colOffset = -1; colOffset <= 1; colOffset++) {
          const neighborRow = currentRow + rowOffset;
          const neighborCol = currentCol + colOffset;
          
          // Check if neighbor is within matrix bounds
          if (neighborRow >= 0 && neighborRow < imageMatrix.length && 
              neighborCol >= 0 && neighborCol < imageMatrix[neighborRow].length) {
            neighborSum += imageMatrix[neighborRow][neighborCol];
          }
        }
      }
      
      const averageValue = neighborSum / 9;
      processedRow.push(averageValue);
    }
    
    filteredMatrix.push(processedRow);
  }
  
  return filteredMatrix;
}
```

### Configuration and Setup Example
```javascript
// Before - Abbreviated configuration variables
function setupDatabase(cfg) {
  const h = cfg.host || 'localhost';
  const p = cfg.port || 5432;
  const db = cfg.database;
  const u = cfg.username;
  const pw = cfg.password;
  const ssl = cfg.ssl || false;
  const tm = cfg.timeout || 30000;
  const mx = cfg.maxConnections || 10;
  
  const cs = `postgresql://${u}:${pw}@${h}:${p}/${db}`;
  
  const opts = {
    connectionString: cs,
    ssl: ssl,
    connectionTimeoutMillis: tm,
    max: mx,
  };
  
  const pool = new Pool(opts);
  
  pool.on('error', (err, client) => {
    console.error('Database pool error:', err);
  });
  
  return pool;
}

// After - Self-documenting configuration variables
function setupDatabaseConnection(configuration) {
  const hostname = configuration.host || 'localhost';
  const portNumber = configuration.port || 5432;
  const databaseName = configuration.database;
  const username = configuration.username;
  const password = configuration.password;
  const useSSL = configuration.ssl || false;
  const connectionTimeoutMs = configuration.timeout || 30000;
  const maxConnections = configuration.maxConnections || 10;
  
  const connectionString = `postgresql://${username}:${password}@${hostname}:${portNumber}/${databaseName}`;
  
  const poolOptions = {
    connectionString: connectionString,
    ssl: useSSL,
    connectionTimeoutMillis: connectionTimeoutMs,
    max: maxConnections,
  };
  
  const connectionPool = new Pool(poolOptions);
  
  connectionPool.on('error', (error, client) => {
    console.error('Database connection pool error:', error);
  });
  
  return connectionPool;
}
```

### Event Handler Example
```javascript
// Before - Generic event handler variables
function handleFormSubmit(e) {
  e.preventDefault();
  
  const f = e.target;
  const d = new FormData(f);
  const v = {};
  
  for (const [k, val] of d.entries()) {
    v[k] = val;
  }
  
  const req = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(v)
  };
  
  fetch('/api/submit', req)
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showMessage('Form submitted successfully');
        f.reset();
      } else {
        showError(data.error);
      }
    })
    .catch(err => {
      showError('Network error occurred');
    });
}

// After - Clear event handler variables
function handleFormSubmission(submitEvent) {
  submitEvent.preventDefault();
  
  const submittedForm = submitEvent.target;
  const formData = new FormData(submittedForm);
  const formValues = {};
  
  // Extract form values into object
  for (const [fieldName, fieldValue] of formData.entries()) {
    formValues[fieldName] = fieldValue;
  }
  
  const submitRequest = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(formValues)
  };
  
  fetch('/api/submit', submitRequest)
    .then(response => response.json())
    .then(responseData => {
      if (responseData.success) {
        showSuccessMessage('Form submitted successfully');
        submittedForm.reset();
      } else {
        showErrorMessage(responseData.error);
      }
    })
    .catch(networkError => {
      showErrorMessage('Network error occurred');
      console.error('Form submission failed:', networkError);
    });
}
```

### Algorithm Implementation Example
```javascript
// Before - Mathematical variable names
function quickSort(arr, l = 0, r = arr.length - 1) {
  if (l < r) {
    const p = partition(arr, l, r);
    quickSort(arr, l, p - 1);
    quickSort(arr, p + 1, r);
  }
  return arr;
}

function partition(arr, l, r) {
  const pv = arr[r];
  let i = l - 1;
  
  for (let j = l; j < r; j++) {
    if (arr[j] <= pv) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }
  
  [arr[i + 1], arr[r]] = [arr[r], arr[i + 1]];
  return i + 1;
}

// After - Descriptive algorithm variable names
function quickSort(array, leftIndex = 0, rightIndex = array.length - 1) {
  if (leftIndex < rightIndex) {
    const pivotIndex = partitionArray(array, leftIndex, rightIndex);
    quickSort(array, leftIndex, pivotIndex - 1);
    quickSort(array, pivotIndex + 1, rightIndex);
  }
  return array;
}

function partitionArray(array, leftBoundary, rightBoundary) {
  const pivotValue = array[rightBoundary];
  let partitionIndex = leftBoundary - 1;
  
  for (let currentIndex = leftBoundary; currentIndex < rightBoundary; currentIndex++) {
    if (array[currentIndex] <= pivotValue) {
      partitionIndex++;
      // Swap elements
      [array[partitionIndex], array[currentIndex]] = [array[currentIndex], array[partitionIndex]];
    }
  }
  
  // Place pivot in correct position
  [array[partitionIndex + 1], array[rightBoundary]] = [array[rightBoundary], array[partitionIndex + 1]];
  return partitionIndex + 1;
}
```

## Mechanics

1. **Identify problematic variable names**
   - Look for single letters (except standard loop counters)
   - Find abbreviations that aren't clear
   - Check for misleading or ambiguous names
   - Identify variables with unclear scope

2. **Choose better names**
   - Use full words that describe the variable's purpose
   - Include units or types when relevant
   - Make the scope and lifetime clear
   - Follow consistent naming conventions

3. **Use IDE features**
   - Use "rename" refactoring tools when available
   - Let the IDE find and update all references
   - Verify the changes are correct

4. **Manual replacement**
   - If IDE tools aren't available, use search and replace carefully
   - Check each occurrence to ensure it's the right variable
   - Be careful with scope - same name might be used in different contexts

5. **Test thoroughly**
   - Run all tests to ensure functionality is preserved
   - Check that the renamed variables don't conflict with existing names
   - Verify that the code is more readable

## Variable Naming Guidelines

### Use Intention-Revealing Names
```javascript
// Bad
let d; // days? distance? data?

// Good
let daysSinceCreation;
let distanceInKilometers;
let customerData;
```

### Avoid Mental Mapping
```javascript
// Bad - reader must remember what 'u' means
const u = users.filter(u => u.active);

// Good - clear and searchable
const activeUsers = users.filter(user => user.isActive);
```

### Use Searchable Names
```javascript
// Bad - hard to search for
const e = employees.find(e => e.id === 7);

// Good - searchable
const targetEmployee = employees.find(employee => employee.id === MANAGER_ID);
```

### Avoid Encodings
```javascript
// Bad - Hungarian notation is outdated
let strName;
let intAge;
let boolIsActive;

// Good - types are clear from context
let customerName;
let customerAge;
let isActive;
```

### Use Consistent Vocabulary
```javascript
// Bad - mixing terms
function getUserInfo(userId) {
  const customer = findClient(userId);
  return customer;
}

// Good - consistent terminology
function getUserInfo(userId) {
  const user = findUser(userId);
  return user;
}
```

### Length Should Correspond to Scope
```javascript
// OK for small scope
for (let i = 0; i < items.length; i++) {
  process(items[i]);
}

// Better for larger scope
function processOrderItems(orderItems) {
  for (let itemIndex = 0; itemIndex < orderItems.length; itemIndex++) {
    const currentItem = orderItems[itemIndex];
    // ... more complex processing
  }
}
```

## When to Use

- **Unclear purpose**: Variable name doesn't indicate what it contains
- **Abbreviations**: Cryptic shortened names
- **Generic names**: Variables named 'data', 'info', 'obj'
- **Single letters**: Beyond standard loop counters (i, j, k)
- **Misleading names**: Name suggests wrong type or purpose
- **Context changes**: Variable purpose has evolved
- **Code reviews**: Reviewers struggle to understand variables

## Trade-offs

### Benefits
- **Improved readability**: Code becomes self-documenting
- **Reduced cognitive load**: No need to remember what variables mean
- **Easier debugging**: Clear variable names help track values
- **Better maintainability**: Future developers understand the code
- **Fewer bugs**: Clear intent reduces misunderstandings

### Considerations
- **Longer names**: May increase line length
- **Verbosity**: Can make code more verbose
- **Refactoring effort**: Need to update all references
- **Consistency**: Must maintain naming conventions

## Common Patterns

### Boolean Variables
```javascript
// Good boolean naming
let isValid = true;
let hasPermission = false;
let canEdit = user.role === 'admin';
let shouldNotify = user.preferences.notifications;
```

### Collections
```javascript
// Good collection naming
const users = []; // plural for arrays
const userById = new Map(); // descriptive for maps
const activeUserSet = new Set(); // include type when helpful
```

### Constants
```javascript
// Good constant naming
const MAX_RETRY_ATTEMPTS = 3;
const DEFAULT_TIMEOUT_MS = 5000;
const API_BASE_URL = 'https://api.example.com';
```

### Temporary Variables
```javascript
// Even temporary variables should be clear

// Bad
const temp = user.firstName + ' ' + user.lastName;

// Good
const fullName = user.firstName + ' ' + user.lastName;
```

## Related Refactorings

- [Rename Field](rename-field.md) - Similar concept for object properties
- [Extract Variable](extract-variable.md) - Create well-named variables from expressions
- [Inline Variable](inline-variable.md) - Remove unnecessary variables
- [Change Function Declaration](change-function-declaration.md) - Rename parameters
- [Introduce Parameter Object](introduce-parameter-object.md) - Group related variables