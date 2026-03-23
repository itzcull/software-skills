---
title: "Split Variable"
description: "Replace a variable with multiple responsibilities with separate variables, each with a single purpose"
category: "Organization"
tags: ["split", "variable", "single-responsibility", "clarity", "confusion"]
related: ["extract-variable", "rename-variable", "introduce-explaining-variable"]
---

# Split Variable

Replace a variable that has more than one responsibility with separate variables, each responsible for only one thing. This clarifies what each variable represents and eliminates confusion.

## Motivation

Variables that serve multiple purposes create several problems:

- **Confusing semantics**: Hard to understand what the variable represents at any point
- **Maintenance difficulties**: Changes to one use can affect others
- **Debugging complexity**: Harder to track what value should be at any time
- **Poor readability**: Single variable name doesn't capture multiple meanings
- **Hidden dependencies**: Changes to one usage can break another
- **Type confusion**: Variable may hold different types of values

## Example

### Basic Example
```javascript
// Before - Variable used for multiple purposes
function calculateOrderTotal(order) {
  let temp = order.items.length;  // First use: item count
  
  if (temp === 0) {
    throw new Error('Order must have at least one item');
  }
  
  temp = 0;  // Now used for: subtotal accumulation
  for (const item of order.items) {
    temp += item.price * item.quantity;
  }
  
  const subtotal = temp;
  
  temp = subtotal * 0.08;  // Now used for: tax calculation
  const tax = temp;
  
  temp = subtotal + tax;  // Now used for: total calculation
  
  if (order.shipping) {
    temp += order.shipping;  // Adding shipping to total
  }
  
  return temp;
}

// After - Separate variables for each purpose
function calculateOrderTotal(order) {
  const itemCount = order.items.length;  // Clear purpose: item count
  
  if (itemCount === 0) {
    throw new Error('Order must have at least one item');
  }
  
  let subtotal = 0;  // Clear purpose: subtotal accumulation
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  
  const tax = subtotal * 0.08;  // Clear purpose: tax amount
  
  let total = subtotal + tax;  // Clear purpose: running total
  
  if (order.shipping) {
    total += order.shipping;
  }
  
  return total;
}
```

### Complex Example - Data Processing
```javascript
// Before - Variable reused for different types of data
function processUserData(userData) {
  let result = userData.name;  // First use: storing name
  
  // Validate name
  if (!result || result.length < 2) {
    throw new Error('Invalid name');
  }
  
  result = result.trim().toLowerCase();  // Still name, but transformed
  const processedName = result;
  
  result = userData.email;  // Now used for: email
  
  // Validate email
  if (!result || !result.includes('@')) {
    throw new Error('Invalid email');
  }
  
  result = result.toLowerCase().trim();  // Email transformation
  const processedEmail = result;
  
  result = userData.age;  // Now used for: age
  
  // Validate and process age
  if (typeof result !== 'number' || result < 0 || result > 120) {
    throw new Error('Invalid age');
  }
  
  if (result < 18) {
    result = 'minor';  // Now storing age category as string!
  } else if (result < 65) {
    result = 'adult';
  } else {
    result = 'senior';
  }
  
  const ageCategory = result;
  
  result = {  // Now used for: final user object
    id: generateUserId(),
    name: processedName,
    email: processedEmail,
    ageCategory: ageCategory,
    createdAt: new Date()
  };
  
  // Add additional fields based on age category
  if (ageCategory === 'minor') {
    result.requiresParentalConsent = true;
  } else if (ageCategory === 'senior') {
    result.eligibleForDiscount = true;
  }
  
  return result;
}

// After - Separate variables for each type of data
function processUserData(userData) {
  // Name processing with clear variable names
  let rawName = userData.name;
  if (!rawName || rawName.length < 2) {
    throw new Error('Invalid name');
  }
  const processedName = rawName.trim().toLowerCase();
  
  // Email processing with clear variable names
  let rawEmail = userData.email;
  if (!rawEmail || !rawEmail.includes('@')) {
    throw new Error('Invalid email');
  }
  const processedEmail = rawEmail.toLowerCase().trim();
  
  // Age processing with clear variable names
  const age = userData.age;
  if (typeof age !== 'number' || age < 0 || age > 120) {
    throw new Error('Invalid age');
  }
  
  let ageCategory;
  if (age < 18) {
    ageCategory = 'minor';
  } else if (age < 65) {
    ageCategory = 'adult';
  } else {
    ageCategory = 'senior';
  }
  
  // User object construction with clear purpose
  const user = {
    id: generateUserId(),
    name: processedName,
    email: processedEmail,
    ageCategory: ageCategory,
    createdAt: new Date()
  };
  
  // Add category-specific fields
  if (ageCategory === 'minor') {
    user.requiresParentalConsent = true;
  } else if (ageCategory === 'senior') {
    user.eligibleForDiscount = true;
  }
  
  return user;
}
```

### Loop Variable Example
```javascript
// Before - Loop variable reused for different calculations
function analyzeOrderData(orders) {
  let i = 0;  // Used as loop counter
  let total = 0;
  
  // First loop: calculate total revenue
  for (i = 0; i < orders.length; i++) {
    total += orders[i].amount;
  }
  
  const totalRevenue = total;
  
  // Reuse 'i' for counting high-value orders
  i = 0;  // Reset for counting
  for (const order of orders) {
    if (order.amount > 1000) {
      i++;  // Now 'i' is a counter, not an index
    }
  }
  
  const highValueOrderCount = i;
  
  // Reuse 'i' for calculating average order age
  i = 0;  // Reset for accumulation
  for (const order of orders) {
    const orderAge = Date.now() - new Date(order.createdAt).getTime();
    i += orderAge;  // Now 'i' accumulates age in milliseconds
  }
  
  const averageOrderAge = i / orders.length;
  
  return {
    totalRevenue,
    highValueOrderCount,
    averageOrderAge: averageOrderAge / (1000 * 60 * 60 * 24) // Convert to days
  };
}

// After - Separate variables for each purpose
function analyzeOrderData(orders) {
  // Calculate total revenue
  let totalRevenue = 0;
  for (let orderIndex = 0; orderIndex < orders.length; orderIndex++) {
    totalRevenue += orders[orderIndex].amount;
  }
  
  // Count high-value orders
  let highValueOrderCount = 0;
  for (const order of orders) {
    if (order.amount > 1000) {
      highValueOrderCount++;
    }
  }
  
  // Calculate average order age
  let totalOrderAge = 0;
  for (const order of orders) {
    const orderAge = Date.now() - new Date(order.createdAt).getTime();
    totalOrderAge += orderAge;
  }
  const averageOrderAge = totalOrderAge / orders.length;
  
  return {
    totalRevenue,
    highValueOrderCount,
    averageOrderAge: averageOrderAge / (1000 * 60 * 60 * 24) // Convert to days
  };
}
```

### Parameter Processing Example
```javascript
// Before - Parameter variable modified for different purposes
function formatUserProfile(user, options) {
  // 'options' initially contains formatting preferences
  options = options || {};  // Default value
  
  // Modify 'options' to add computed values
  options.displayName = user.firstName + ' ' + user.lastName;
  
  if (user.isVIP) {
    options.displayName = '⭐ ' + options.displayName;
  }
  
  // 'options' now also contains processed date information
  options.memberSince = new Date(user.createdAt).getFullYear();
  options.isNewMember = (Date.now() - new Date(user.createdAt).getTime()) < (30 * 24 * 60 * 60 * 1000);
  
  // More processing - 'options' becomes a mixed bag
  options.profileImage = user.avatar || '/default-avatar.png';
  options.contactInfo = {
    email: options.showEmail ? user.email : 'Hidden',
    phone: options.showPhone ? user.phone : 'Hidden'
  };
  
  // 'options' has completely changed purpose
  return {
    html: `
      <div class="user-profile">
        <img src="${options.profileImage}" alt="Profile">
        <h2>${options.displayName}</h2>
        <p>Member since: ${options.memberSince}</p>
        ${options.isNewMember ? '<span class="new-badge">New Member</span>' : ''}
        <div class="contact">
          <p>Email: ${options.contactInfo.email}</p>
          <p>Phone: ${options.contactInfo.phone}</p>
        </div>
      </div>
    `,
    metadata: options
  };
}

// After - Separate variables for different purposes
function formatUserProfile(user, formatOptions) {
  // Keep original options unchanged
  const options = formatOptions || {};
  
  // Create display data with clear purpose
  const displayData = {
    displayName: user.firstName + ' ' + user.lastName,
    profileImage: user.avatar || '/default-avatar.png',
    memberSince: new Date(user.createdAt).getFullYear(),
    isNewMember: (Date.now() - new Date(user.createdAt).getTime()) < (30 * 24 * 60 * 60 * 1000)
  };
  
  // Add VIP indicator if applicable
  if (user.isVIP) {
    displayData.displayName = '⭐ ' + displayData.displayName;
  }
  
  // Create contact info based on privacy settings
  const contactInfo = {
    email: options.showEmail ? user.email : 'Hidden',
    phone: options.showPhone ? user.phone : 'Hidden'
  };
  
  // Generate HTML using the structured data
  const html = `
    <div class="user-profile">
      <img src="${displayData.profileImage}" alt="Profile">
      <h2>${displayData.displayName}</h2>
      <p>Member since: ${displayData.memberSince}</p>
      ${displayData.isNewMember ? '<span class="new-badge">New Member</span>' : ''}
      <div class="contact">
        <p>Email: ${contactInfo.email}</p>
        <p>Phone: ${contactInfo.phone}</p>
      </div>
    </div>
  `;
  
  return {
    html,
    metadata: {
      ...displayData,
      contactInfo,
      originalOptions: options
    }
  };
}
```

### State Machine Example
```javascript
// Before - State variable overloaded
function processPayment(paymentData) {
  let state = 'validating';  // Initial state
  
  // Validation phase
  if (!paymentData.amount || paymentData.amount <= 0) {
    state = 'invalid_amount';  // Error state
    throw new Error(`Payment failed: ${state}`);
  }
  
  if (!paymentData.cardNumber || paymentData.cardNumber.length !== 16) {
    state = 'invalid_card';  // Different error state
    throw new Error(`Payment failed: ${state}`);
  }
  
  state = 'processing';  // Processing state
  
  try {
    const authResult = authorizePayment(paymentData);
    
    if (authResult.approved) {
      state = 'authorized';  // Success state
    } else {
      state = 'declined';  // Decline state
      throw new Error(`Payment ${state}: ${authResult.reason}`);
    }
    
    // Now 'state' is reused to store charge result
    state = chargeCard(paymentData, authResult.token);
    
    if (state.success) {
      // 'state' now holds transaction data, not state!
      return {
        success: true,
        transactionId: state.transactionId,
        amount: state.amount,
        status: 'completed'  // Hard-coded because 'state' no longer means state
      };
    } else {
      throw new Error(`Charge failed: ${state.error}`);
    }
    
  } catch (error) {
    state = 'error';  // Back to being a state
    throw new Error(`Payment processing failed: ${error.message}`);
  }
}

// After - Separate variables for state and data
function processPayment(paymentData) {
  let paymentState = 'validating';
  
  // Validation phase
  if (!paymentData.amount || paymentData.amount <= 0) {
    paymentState = 'invalid_amount';
    throw new Error(`Payment failed: ${paymentState}`);
  }
  
  if (!paymentData.cardNumber || paymentData.cardNumber.length !== 16) {
    paymentState = 'invalid_card';
    throw new Error(`Payment failed: ${paymentState}`);
  }
  
  paymentState = 'processing';
  
  try {
    const authResult = authorizePayment(paymentData);
    
    if (authResult.approved) {
      paymentState = 'authorized';
    } else {
      paymentState = 'declined';
      throw new Error(`Payment ${paymentState}: ${authResult.reason}`);
    }
    
    // Separate variable for charge result
    const chargeResult = chargeCard(paymentData, authResult.token);
    
    if (chargeResult.success) {
      paymentState = 'completed';
      
      return {
        success: true,
        transactionId: chargeResult.transactionId,
        amount: chargeResult.amount,
        status: paymentState
      };
    } else {
      paymentState = 'charge_failed';
      throw new Error(`Charge failed: ${chargeResult.error}`);
    }
    
  } catch (error) {
    paymentState = 'error';
    throw new Error(`Payment processing failed: ${error.message}`);
  }
}
```

## Mechanics

1. **Identify variable reuse**
   - Look for variables that are assigned multiple times
   - Find variables that hold different types of data
   - Check for variables whose meaning changes

2. **Analyze each usage**
   - Determine what each assignment represents
   - Check if usages are truly independent
   - Identify the scope of each usage

3. **Create new variables**
   - Give each usage its own variable with a descriptive name
   - Choose names that clearly indicate purpose
   - Consider using `const` for values that don't change

4. **Update all references**
   - Replace references to use the appropriate new variable
   - Ensure each reference uses the correct variable
   - Remove the old variable if no longer needed

5. **Handle scope and initialization**
   - Declare variables in the appropriate scope
   - Initialize variables at the right time
   - Consider moving declarations closer to usage

6. **Test thoroughly**
   - Verify behavior is unchanged
   - Test all code paths
   - Check that variable names make sense in context

## When to Use

- **Multiple assignments**: Variable is assigned different types of values
- **Changing semantics**: Variable meaning changes throughout the function
- **Loop counters**: Loop variables reused for different purposes
- **Temporary calculations**: Same variable used for different calculations
- **State confusion**: Variable represents different states or data
- **Type changes**: Variable holds different types at different times

## Trade-offs

### Benefits
- **Clearer intent**: Each variable has a single, clear purpose
- **Easier debugging**: Can track specific values independently
- **Better maintainability**: Changes don't affect unrelated uses
- **Improved readability**: Variable names match their purpose
- **Reduced bugs**: Less chance of using wrong value
- **Better tooling**: IDEs can provide better analysis

### Drawbacks
- **More variables**: Increases number of variables to track
- **Potential verbosity**: May require longer, more descriptive names
- **Memory usage**: Multiple variables instead of reusing one
- **Initial effort**: Requires analysis to identify separate purposes

## Common Patterns

### Accumulator Pattern
```javascript
// Before
let result = 0;
for (const item of items) {
  result += item.value;
}
// result is now sum

result = result / items.length;
// result is now average

// After
let sum = 0;
for (const item of items) {
  sum += item.value;
}
const average = sum / items.length;
```

### Guard Clauses
```javascript
// Before
let value = input;
if (!value) {
  value = 'default';
}
if (value.length > 100) {
  value = value.substring(0, 100);
}

// After
const defaultedValue = input || 'default';
const truncatedValue = defaultedValue.length > 100 
  ? defaultedValue.substring(0, 100) 
  : defaultedValue;
```

### Multi-step Transformation
```javascript
// Before
let data = rawInput;
data = parseData(data);
data = validateData(data);
data = transformData(data);

// After
const parsedData = parseData(rawInput);
const validatedData = validateData(parsedData);
const transformedData = transformData(validatedData);
```

### Conditional Processing
```javascript
// Before
let result = baseValue;
if (condition1) {
  result = processType1(result);
} else if (condition2) {
  result = processType2(result);
}

// After
let result;
if (condition1) {
  result = processType1(baseValue);
} else if (condition2) {
  result = processType2(baseValue);
} else {
  result = baseValue;
}
```

## Related Refactorings

- [Extract Variable](extract-variable.md) - Extract complex expressions into well-named variables
- [Inline Variable](inline-variable.md) - Remove unnecessary variables
- [Rename Variable](rename-variable.md) - Give variables better names
- [Extract Function](extract-function.md) - Extract code sections that use different variables
- [Introduce Parameter Object](introduce-parameter-object.md) - Group related variables
- [Replace Temp with Query](replace-derived-variable-with-query.md) - Replace calculated variables with method calls