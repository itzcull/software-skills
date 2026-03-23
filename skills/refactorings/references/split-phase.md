---
title: "Split Phase"
description: "Divide a function doing two different things into two separate phases with single responsibilities"
category: "Organization"
tags: ["phase", "separation", "single-responsibility", "clarity", "organization"]
related: ["extract-function", "separate-query-from-modifier", "combine-functions-into-transform"]
---

# Split Phase

Divide a function that's doing two different things into two separate phases where each phase has a single responsibility. This improves clarity and makes each phase easier to understand and test.

## Motivation

Functions that do multiple things at once create several problems:

- **Mixed levels of abstraction**: High-level and low-level operations intermixed
- **Hard to understand**: Multiple concerns in one function
- **Difficult to test**: Can't test phases independently
- **Poor reusability**: Can't reuse individual phases
- **Maintenance burden**: Changes to one concern affect others
- **Violation of SRP**: Single Responsibility Principle violation

## Example

### Basic Example
```javascript
// Before - Mixed calculation and formatting phases
function generateInvoiceReport(orders) {
  let totalRevenue = 0;
  let totalTax = 0;
  let totalShipping = 0;
  let itemCount = 0;
  
  // Calculation phase mixed with formatting
  let report = 'INVOICE REPORT\n';
  report += '=============\n\n';
  
  for (const order of orders) {
    totalRevenue += order.subtotal;
    totalTax += order.tax;
    totalShipping += order.shipping;
    itemCount += order.items.length;
    
    // Formatting mixed in calculation loop
    report += `Order ${order.id}: $${order.total.toFixed(2)}\n`;
    report += `  Items: ${order.items.length}\n`;
    report += `  Customer: ${order.customerName}\n\n`;
  }
  
  const grandTotal = totalRevenue + totalTax + totalShipping;
  const averageOrderValue = totalRevenue / orders.length;
  
  // More formatting mixed with calculations
  report += 'SUMMARY\n';
  report += '-------\n';
  report += `Total Orders: ${orders.length}\n`;
  report += `Total Items: ${itemCount}\n`;
  report += `Revenue: $${totalRevenue.toFixed(2)}\n`;
  report += `Tax: $${totalTax.toFixed(2)}\n`;
  report += `Shipping: $${totalShipping.toFixed(2)}\n`;
  report += `Grand Total: $${grandTotal.toFixed(2)}\n`;
  report += `Average Order Value: $${averageOrderValue.toFixed(2)}\n`;
  
  return report;
}

// After - Separate calculation and formatting phases
function generateInvoiceReport(orders) {
  const invoiceData = calculateInvoiceData(orders);
  return formatInvoiceReport(invoiceData);
}

function calculateInvoiceData(orders) {
  let totalRevenue = 0;
  let totalTax = 0;
  let totalShipping = 0;
  let itemCount = 0;
  
  const orderSummaries = [];
  
  for (const order of orders) {
    totalRevenue += order.subtotal;
    totalTax += order.tax;
    totalShipping += order.shipping;
    itemCount += order.items.length;
    
    orderSummaries.push({
      id: order.id,
      total: order.total,
      itemCount: order.items.length,
      customerName: order.customerName
    });
  }
  
  return {
    orders: orderSummaries,
    totals: {
      revenue: totalRevenue,
      tax: totalTax,
      shipping: totalShipping,
      grand: totalRevenue + totalTax + totalShipping,
      items: itemCount
    },
    metrics: {
      orderCount: orders.length,
      averageOrderValue: totalRevenue / orders.length
    }
  };
}

function formatInvoiceReport(invoiceData) {
  let report = 'INVOICE REPORT\n';
  report += '=============\n\n';
  
  // Format individual orders
  for (const order of invoiceData.orders) {
    report += `Order ${order.id}: $${order.total.toFixed(2)}\n`;
    report += `  Items: ${order.itemCount}\n`;
    report += `  Customer: ${order.customerName}\n\n`;
  }
  
  // Format summary
  report += 'SUMMARY\n';
  report += '-------\n';
  report += `Total Orders: ${invoiceData.metrics.orderCount}\n`;
  report += `Total Items: ${invoiceData.totals.items}\n`;
  report += `Revenue: $${invoiceData.totals.revenue.toFixed(2)}\n`;
  report += `Tax: $${invoiceData.totals.tax.toFixed(2)}\n`;
  report += `Shipping: $${invoiceData.totals.shipping.toFixed(2)}\n`;
  report += `Grand Total: $${invoiceData.totals.grand.toFixed(2)}\n`;
  report += `Average Order Value: $${invoiceData.metrics.averageOrderValue.toFixed(2)}\n`;
  
  return report;
}
```

### Complex Example - Data Processing Pipeline
```javascript
// Before - Mixed parsing, validation, transformation, and storage
function processCustomerData(csvData) {
  const results = [];
  const errors = [];
  
  // Parse CSV mixed with validation and transformation
  const lines = csvData.split('\n');
  
  for (let i = 1; i < lines.length; i++) { // Skip header
    const line = lines[i].trim();
    if (!line) continue;
    
    try {
      // Parsing phase
      const fields = line.split(',');
      if (fields.length !== 5) {
        throw new Error('Invalid number of fields');
      }
      
      const rawCustomer = {
        name: fields[0],
        email: fields[1],
        phone: fields[2],
        city: fields[3],
        country: fields[4]
      };
      
      // Validation mixed with parsing
      if (!rawCustomer.name || rawCustomer.name.length < 2) {
        throw new Error('Invalid name');
      }
      
      if (!rawCustomer.email.includes('@')) {
        throw new Error('Invalid email');
      }
      
      if (!rawCustomer.phone.match(/^\+?[\d\s\-\(\)]+$/)) {
        throw new Error('Invalid phone number');
      }
      
      // Transformation mixed with validation
      const transformedCustomer = {
        id: generateCustomerId(),
        name: rawCustomer.name.trim().replace(/\s+/g, ' '),
        email: rawCustomer.email.toLowerCase().trim(),
        phone: rawCustomer.phone.replace(/[\s\-\(\)]/g, ''),
        address: {
          city: rawCustomer.city.trim(),
          country: rawCustomer.country.trim().toUpperCase()
        },
        createdAt: new Date(),
        isActive: true
      };
      
      // More validation after transformation
      if (transformedCustomer.phone.length < 10) {
        throw new Error('Phone number too short');
      }
      
      // Enrichment mixed with everything else
      if (transformedCustomer.address.country === 'US') {
        transformedCustomer.timezone = getTimezoneForCity(transformedCustomer.address.city);
        transformedCustomer.taxRate = getTaxRateForCity(transformedCustomer.address.city);
      }
      
      // Storage preparation mixed with processing
      const customerForStorage = {
        ...transformedCustomer,
        searchTags: [
          transformedCustomer.name.toLowerCase(),
          transformedCustomer.email,
          transformedCustomer.address.city.toLowerCase(),
          transformedCustomer.address.country.toLowerCase()
        ].join(' ')
      };
      
      results.push(customerForStorage);
      
    } catch (error) {
      errors.push({
        line: i + 1,
        data: line,
        error: error.message
      });
    }
  }
  
  // Storage mixed with processing
  const saved = [];
  for (const customer of results) {
    try {
      const savedCustomer = saveCustomer(customer);
      saved.push(savedCustomer);
      updateSearchIndex(customer.searchTags, customer.id);
    } catch (error) {
      errors.push({
        customerId: customer.id,
        error: `Storage failed: ${error.message}`
      });
    }
  }
  
  return {
    processed: saved.length,
    errors: errors.length,
    details: {
      saved,
      errors
    }
  };
}

// After - Clear separation of phases
function processCustomerData(csvData) {
  const parsedData = parseCustomerCSV(csvData);
  const validatedData = validateCustomers(parsedData.customers, parsedData.errors);
  const transformedData = transformCustomers(validatedData.valid, validatedData.errors);
  const enrichedData = enrichCustomers(transformedData.customers, transformedData.errors);
  const storageResults = storeCustomers(enrichedData.customers, enrichedData.errors);
  
  return {
    processed: storageResults.saved.length,
    errors: storageResults.errors.length,
    details: {
      saved: storageResults.saved,
      errors: storageResults.errors
    }
  };
}

// Phase 1: Parse CSV data
function parseCustomerCSV(csvData) {
  const customers = [];
  const errors = [];
  const lines = csvData.split('\n');
  
  for (let i = 1; i < lines.length; i++) { // Skip header
    const line = lines[i].trim();
    if (!line) continue;
    
    try {
      const fields = line.split(',');
      if (fields.length !== 5) {
        throw new Error('Invalid number of fields');
      }
      
      customers.push({
        lineNumber: i + 1,
        name: fields[0],
        email: fields[1],
        phone: fields[2],
        city: fields[3],
        country: fields[4]
      });
      
    } catch (error) {
      errors.push({
        line: i + 1,
        data: line,
        error: error.message,
        phase: 'parsing'
      });
    }
  }
  
  return { customers, errors };
}

// Phase 2: Validate parsed data
function validateCustomers(customers, existingErrors) {
  const valid = [];
  const errors = [...existingErrors];
  
  for (const customer of customers) {
    try {
      // Name validation
      if (!customer.name || customer.name.length < 2) {
        throw new Error('Invalid name');
      }
      
      // Email validation
      if (!customer.email.includes('@')) {
        throw new Error('Invalid email');
      }
      
      // Phone validation
      if (!customer.phone.match(/^\+?[\d\s\-\(\)]+$/)) {
        throw new Error('Invalid phone number');
      }
      
      valid.push(customer);
      
    } catch (error) {
      errors.push({
        line: customer.lineNumber,
        data: customer,
        error: error.message,
        phase: 'validation'
      });
    }
  }
  
  return { valid, errors };
}

// Phase 3: Transform data
function transformCustomers(customers, existingErrors) {
  const transformed = [];
  const errors = [...existingErrors];
  
  for (const customer of customers) {
    try {
      const transformedCustomer = {
        id: generateCustomerId(),
        name: customer.name.trim().replace(/\s+/g, ' '),
        email: customer.email.toLowerCase().trim(),
        phone: customer.phone.replace(/[\s\-\(\)]/g, ''),
        address: {
          city: customer.city.trim(),
          country: customer.country.trim().toUpperCase()
        },
        createdAt: new Date(),
        isActive: true
      };
      
      // Post-transformation validation
      if (transformedCustomer.phone.length < 10) {
        throw new Error('Phone number too short');
      }
      
      transformed.push(transformedCustomer);
      
    } catch (error) {
      errors.push({
        line: customer.lineNumber,
        data: customer,
        error: error.message,
        phase: 'transformation'
      });
    }
  }
  
  return { customers: transformed, errors };
}

// Phase 4: Enrich data
function enrichCustomers(customers, existingErrors) {
  const enriched = [];
  const errors = [...existingErrors];
  
  for (const customer of customers) {
    try {
      const enrichedCustomer = { ...customer };
      
      // Add location-specific data
      if (customer.address.country === 'US') {
        enrichedCustomer.timezone = getTimezoneForCity(customer.address.city);
        enrichedCustomer.taxRate = getTaxRateForCity(customer.address.city);
      }
      
      // Add search tags
      enrichedCustomer.searchTags = [
        customer.name.toLowerCase(),
        customer.email,
        customer.address.city.toLowerCase(),
        customer.address.country.toLowerCase()
      ].join(' ');
      
      enriched.push(enrichedCustomer);
      
    } catch (error) {
      errors.push({
        customerId: customer.id,
        error: `Enrichment failed: ${error.message}`,
        phase: 'enrichment'
      });
    }
  }
  
  return { customers: enriched, errors };
}

// Phase 5: Store data
function storeCustomers(customers, existingErrors) {
  const saved = [];
  const errors = [...existingErrors];
  
  for (const customer of customers) {
    try {
      const savedCustomer = saveCustomer(customer);
      updateSearchIndex(customer.searchTags, customer.id);
      saved.push(savedCustomer);
      
    } catch (error) {
      errors.push({
        customerId: customer.id,
        error: `Storage failed: ${error.message}`,
        phase: 'storage'
      });
    }
  }
  
  return { saved, errors };
}
```

### Web Request Processing Example
```javascript
// Before - Mixed request parsing, business logic, and response formatting
function handleCreateOrder(request, response) {
  try {
    // Request parsing mixed with validation
    const body = JSON.parse(request.body);
    
    if (!body.customerId) {
      return response.status(400).json({ error: 'Customer ID required' });
    }
    
    if (!body.items || body.items.length === 0) {
      return response.status(400).json({ error: 'Order items required' });
    }
    
    // Business logic mixed with parsing
    const customer = getCustomer(body.customerId);
    if (!customer) {
      return response.status(404).json({ error: 'Customer not found' });
    }
    
    let subtotal = 0;
    const orderItems = [];
    
    // More validation mixed with calculation
    for (const item of body.items) {
      if (!item.productId || !item.quantity) {
        return response.status(400).json({ error: 'Invalid item format' });
      }
      
      const product = getProduct(item.productId);
      if (!product) {
        return response.status(404).json({ error: `Product ${item.productId} not found` });
      }
      
      if (product.stock < item.quantity) {
        return response.status(400).json({ 
          error: `Insufficient stock for product ${item.productId}` 
        });
      }
      
      const lineTotal = product.price * item.quantity;
      subtotal += lineTotal;
      
      orderItems.push({
        productId: item.productId,
        productName: product.name,
        quantity: item.quantity,
        price: product.price,
        lineTotal
      });
    }
    
    // More business logic
    const tax = subtotal * 0.08;
    const shipping = calculateShipping(customer.address, orderItems);
    const total = subtotal + tax + shipping;
    
    if (customer.creditLimit < total) {
      return response.status(400).json({ error: 'Order exceeds credit limit' });
    }
    
    // Order creation mixed with inventory updates
    const order = {
      id: generateOrderId(),
      customerId: body.customerId,
      items: orderItems,
      subtotal,
      tax,
      shipping,
      total,
      status: 'pending',
      createdAt: new Date()
    };
    
    const savedOrder = saveOrder(order);
    
    // Update inventory mixed with order creation
    for (const item of orderItems) {
      updateProductStock(item.productId, -item.quantity);
    }
    
    // Response formatting mixed with business logic
    const responseData = {
      orderId: savedOrder.id,
      status: savedOrder.status,
      total: savedOrder.total,
      estimatedDelivery: calculateDeliveryDate(customer.address),
      items: savedOrder.items.map(item => ({
        productName: item.productName,
        quantity: item.quantity,
        price: item.price
      }))
    };
    
    response.status(201).json({
      success: true,
      order: responseData
    });
    
  } catch (error) {
    response.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
}

// After - Clear phase separation
function handleCreateOrder(request, response) {
  try {
    const orderRequest = parseOrderRequest(request);
    const orderData = processOrder(orderRequest);
    const responseData = formatOrderResponse(orderData);
    
    response.status(201).json(responseData);
    
  } catch (error) {
    handleOrderError(error, response);
  }
}

// Phase 1: Parse and validate request
function parseOrderRequest(request) {
  const body = JSON.parse(request.body);
  
  // Input validation
  if (!body.customerId) {
    throw new ValidationError('Customer ID required');
  }
  
  if (!body.items || body.items.length === 0) {
    throw new ValidationError('Order items required');
  }
  
  // Validate item format
  for (const item of body.items) {
    if (!item.productId || !item.quantity) {
      throw new ValidationError('Invalid item format');
    }
  }
  
  return {
    customerId: body.customerId,
    items: body.items,
    shippingAddress: body.shippingAddress
  };
}

// Phase 2: Business logic processing
function processOrder(orderRequest) {
  // Get customer
  const customer = getCustomer(orderRequest.customerId);
  if (!customer) {
    throw new NotFoundError('Customer not found');
  }
  
  // Process items
  const orderItems = [];
  let subtotal = 0;
  
  for (const item of orderRequest.items) {
    const product = getProduct(item.productId);
    if (!product) {
      throw new NotFoundError(`Product ${item.productId} not found`);
    }
    
    if (product.stock < item.quantity) {
      throw new ValidationError(`Insufficient stock for product ${item.productId}`);
    }
    
    const lineTotal = product.price * item.quantity;
    subtotal += lineTotal;
    
    orderItems.push({
      productId: item.productId,
      productName: product.name,
      quantity: item.quantity,
      price: product.price,
      lineTotal
    });
  }
  
  // Calculate totals
  const tax = subtotal * 0.08;
  const shipping = calculateShipping(customer.address, orderItems);
  const total = subtotal + tax + shipping;
  
  // Credit check
  if (customer.creditLimit < total) {
    throw new ValidationError('Order exceeds credit limit');
  }
  
  // Create and save order
  const order = {
    id: generateOrderId(),
    customerId: orderRequest.customerId,
    items: orderItems,
    subtotal,
    tax,
    shipping,
    total,
    status: 'pending',
    createdAt: new Date()
  };
  
  const savedOrder = saveOrder(order);
  
  // Update inventory
  for (const item of orderItems) {
    updateProductStock(item.productId, -item.quantity);
  }
  
  return {
    order: savedOrder,
    customer
  };
}

// Phase 3: Format response
function formatOrderResponse(orderData) {
  return {
    success: true,
    order: {
      orderId: orderData.order.id,
      status: orderData.order.status,
      total: orderData.order.total,
      estimatedDelivery: calculateDeliveryDate(orderData.customer.address),
      items: orderData.order.items.map(item => ({
        productName: item.productName,
        quantity: item.quantity,
        price: item.price
      }))
    }
  };
}

// Error handling phase
function handleOrderError(error, response) {
  if (error instanceof ValidationError) {
    response.status(400).json({
      success: false,
      error: error.message
    });
  } else if (error instanceof NotFoundError) {
    response.status(404).json({
      success: false,
      error: error.message
    });
  } else {
    response.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
}
```

## Mechanics

1. **Identify distinct phases**
   - Look for different levels of abstraction
   - Find operations that could be grouped logically
   - Check for data transformation boundaries

2. **Determine phase boundaries**
   - Find natural breaking points in the logic
   - Look for intermediate data structures
   - Identify where one concern ends and another begins

3. **Extract intermediate data structure**
   - Create a data structure to pass between phases
   - Include all necessary information for subsequent phases
   - Make the structure focused and cohesive

4. **Split into separate functions**
   - Create a function for each phase
   - Each function should have a single responsibility
   - Pass data between phases through the intermediate structure

5. **Update the main function**
   - Call phases in sequence
   - Pass results from one phase to the next
   - Keep the main function focused on orchestration

6. **Test each phase independently**
   - Test phases with different inputs
   - Verify that the overall behavior is preserved
   - Check error handling in each phase

## When to Use

- **Mixed abstraction levels**: Function operates at different levels of detail
- **Sequential phases**: Function does things in distinct steps
- **Different error handling**: Different phases need different error strategies
- **Reusability**: Phases could be useful independently
- **Testing complexity**: Function is hard to test as a whole
- **Multiple concerns**: Function violates Single Responsibility Principle

## Trade-offs

### Benefits
- **Clearer responsibilities**: Each phase has a single purpose
- **Easier testing**: Can test phases independently
- **Better reusability**: Phases can be reused in different contexts
- **Improved maintainability**: Changes are localized to relevant phases
- **Better error handling**: Each phase can handle errors appropriately
- **Enhanced readability**: Code structure matches logical flow

### Drawbacks
- **More functions**: Increases number of functions to maintain
- **Potential over-engineering**: May be overkill for simple functions
- **Performance overhead**: Function calls and data structure creation
- **Coupling through data**: Phases are coupled through intermediate data structure

## Common Phase Patterns

### Input → Process → Output
```javascript
function processRequest(request) {
  const data = parseRequest(request);      // Input phase
  const result = processData(data);        // Process phase
  return formatResponse(result);           // Output phase
}
```

### Validate → Transform → Store
```javascript
function saveUser(userData) {
  const validData = validateUserData(userData);  // Validate phase
  const user = transformToUser(validData);       // Transform phase
  return storeUser(user);                        // Store phase
}
```

### Parse → Calculate → Format
```javascript
function generateReport(rawData) {
  const data = parseReportData(rawData);     // Parse phase
  const metrics = calculateMetrics(data);    // Calculate phase
  return formatReport(metrics);              // Format phase
}
```

### Collect → Analyze → Present
```javascript
function analyzePerformance(config) {
  const metrics = collectMetrics(config);    // Collect phase
  const analysis = analyzeMetrics(metrics);  // Analyze phase
  return presentAnalysis(analysis);          // Present phase
}
```

## Related Refactorings

- [Extract Function](extract-function.md) - Extract each phase into its own function
- [Introduce Parameter Object](introduce-parameter-object.md) - Create data structure for phase communication
- [Replace Temp with Query](replace-derived-variable-with-query.md) - Eliminate temporary variables between phases
- [Move Statements](slide-statements.md) - Group related statements before splitting phases
- [Extract Class](extract-class.md) - Create classes for complex phases
- [Substitute Algorithm](substitute-algorithm.md) - Replace entire phases with better algorithms