---
title: "Replace Query with Parameter"
description: "Replace a method's query call or global variable access with a parameter for explicit dependencies"
category: "Simplifying Function Calls"
tags: ["query", "parameter", "dependencies", "testing", "coupling"]
related: ["replace-parameter-with-query", "introduce-parameter-object", "parameterize-function"]
---

# Replace Query with Parameter

Replace a method's call to a query method or access to a global variable with a parameter. This makes the method more explicit about its dependencies and easier to test.

## Inverse

[Replace Parameter with Query](replace-parameter-with-query.md)

## Motivation

Methods that query for data internally create several problems:

- **Hidden dependencies**: It's not clear what data the method needs
- **Testing difficulties**: Hard to test with different data scenarios
- **Coupling**: Method is tightly coupled to specific data sources
- **Inflexibility**: Can't easily use the method with different data
- **Side effects**: Method behavior depends on external state
- **Concurrency issues**: External state can change during method execution

## Example

### Basic Example
```javascript
// Before - Method queries for current user internally
class NotificationService {
  constructor(userService) {
    this._userService = userService;
  }
  
  sendOrderConfirmation(order) {
    // Hidden dependency on current user
    const currentUser = this._userService.getCurrentUser();
    
    const message = `Hello ${currentUser.name}, your order #${order.id} has been confirmed.`;
    
    if (currentUser.emailNotifications) {
      this._sendEmail(currentUser.email, 'Order Confirmation', message);
    }
    
    if (currentUser.smsNotifications) {
      this._sendSMS(currentUser.phone, message);
    }
  }
  
  sendShippingUpdate(order, trackingNumber) {
    // Same hidden dependency
    const currentUser = this._userService.getCurrentUser();
    
    const message = `Your order #${order.id} has shipped. Tracking: ${trackingNumber}`;
    
    if (currentUser.emailNotifications) {
      this._sendEmail(currentUser.email, 'Shipping Update', message);
    }
  }
}

// Testing is difficult - need to mock user service
const mockUserService = {
  getCurrentUser: () => ({ 
    name: 'Test User', 
    email: 'test@example.com',
    emailNotifications: true 
  })
};

// After - Method accepts user as parameter
class NotificationService {
  sendOrderConfirmation(order, user) {
    // Explicit dependency on user parameter
    const message = `Hello ${user.name}, your order #${order.id} has been confirmed.`;
    
    if (user.emailNotifications) {
      this._sendEmail(user.email, 'Order Confirmation', message);
    }
    
    if (user.smsNotifications) {
      this._sendSMS(user.phone, message);
    }
  }
  
  sendShippingUpdate(order, user, trackingNumber) {
    // Explicit dependency
    const message = `Your order #${order.id} has shipped. Tracking: ${trackingNumber}`;
    
    if (user.emailNotifications) {
      this._sendEmail(user.email, 'Shipping Update', message);
    }
  }
}

// Testing is much easier - just pass test data
const testUser = {
  name: 'Test User',
  email: 'test@example.com',
  emailNotifications: true,
  smsNotifications: false
};

const service = new NotificationService();
service.sendOrderConfirmation(order, testUser); // Easy to test!
```

### Complex Example - Report Generation
```javascript
// Before - Multiple hidden dependencies
class ReportGenerator {
  constructor(database, configService, userService) {
    this._database = database;
    this._configService = configService;
    this._userService = userService;
  }
  
  generateSalesReport(startDate, endDate) {
    // Hidden dependency on current user for permissions
    const currentUser = this._userService.getCurrentUser();
    if (!this._hasReportPermission(currentUser, 'sales')) {
      throw new Error('Insufficient permissions');
    }
    
    // Hidden dependency on configuration
    const reportConfig = this._configService.getReportConfig();
    const includeInternalSales = reportConfig.includeInternal;
    const currency = reportConfig.defaultCurrency;
    
    // Hidden dependency on current user's department for filtering
    const userDepartment = currentUser.department;
    let salesData;
    
    if (currentUser.role === 'admin') {
      salesData = this._database.getAllSales(startDate, endDate);
    } else {
      salesData = this._database.getSalesByDepartment(startDate, endDate, userDepartment);
    }
    
    if (!includeInternalSales) {
      salesData = salesData.filter(sale => !sale.isInternal);
    }
    
    return this._formatReport(salesData, currency);
  }
  
  generateInventoryReport() {
    // More hidden dependencies
    const currentUser = this._userService.getCurrentUser();
    const reportConfig = this._configService.getReportConfig();
    
    if (!this._hasReportPermission(currentUser, 'inventory')) {
      throw new Error('Insufficient permissions');
    }
    
    const includeBackorders = reportConfig.includeBackorders;
    const warehouseFilter = currentUser.accessibleWarehouses;
    
    let inventoryData = this._database.getInventoryData();
    
    // Filter by accessible warehouses
    inventoryData = inventoryData.filter(item => 
      warehouseFilter.includes(item.warehouseId)
    );
    
    if (!includeBackorders) {
      inventoryData = inventoryData.filter(item => item.quantity > 0);
    }
    
    return this._formatInventoryReport(inventoryData);
  }
}

// Testing is complex - need to set up multiple mocks
const mockDatabase = { /* complex mock */ };
const mockConfigService = { /* complex mock */ };
const mockUserService = { /* complex mock */ };

// After - Explicit parameters
class ReportGenerator {
  constructor(database) {
    this._database = database;
  }
  
  generateSalesReport(startDate, endDate, user, reportConfig) {
    // Explicit dependencies as parameters
    if (!this._hasReportPermission(user, 'sales')) {
      throw new Error('Insufficient permissions');
    }
    
    const includeInternalSales = reportConfig.includeInternal;
    const currency = reportConfig.defaultCurrency;
    
    let salesData;
    
    if (user.role === 'admin') {
      salesData = this._database.getAllSales(startDate, endDate);
    } else {
      salesData = this._database.getSalesByDepartment(startDate, endDate, user.department);
    }
    
    if (!includeInternalSales) {
      salesData = salesData.filter(sale => !sale.isInternal);
    }
    
    return this._formatReport(salesData, currency);
  }
  
  generateInventoryReport(user, reportConfig) {
    // Explicit dependencies
    if (!this._hasReportPermission(user, 'inventory')) {
      throw new Error('Insufficient permissions');
    }
    
    const includeBackorders = reportConfig.includeBackorders;
    const warehouseFilter = user.accessibleWarehouses;
    
    let inventoryData = this._database.getInventoryData();
    
    // Filter by accessible warehouses
    inventoryData = inventoryData.filter(item => 
      warehouseFilter.includes(item.warehouseId)
    );
    
    if (!includeBackorders) {
      inventoryData = inventoryData.filter(item => item.quantity > 0);
    }
    
    return this._formatInventoryReport(inventoryData);
  }
  
  _hasReportPermission(user, reportType) {
    return user.permissions.includes(`report_${reportType}`);
  }
  
  _formatReport(salesData, currency) {
    // Report formatting logic
    return { data: salesData, currency };
  }
  
  _formatInventoryReport(inventoryData) {
    // Inventory report formatting logic
    return { data: inventoryData };
  }
}

// Testing is much simpler - just pass test data
const testUser = {
  role: 'manager',
  department: 'sales',
  permissions: ['report_sales', 'report_inventory'],
  accessibleWarehouses: ['warehouse1', 'warehouse2']
};

const testConfig = {
  includeInternal: false,
  defaultCurrency: 'USD',
  includeBackorders: true
};

const generator = new ReportGenerator(database);
const report = generator.generateSalesReport(
  new Date('2023-01-01'),
  new Date('2023-01-31'),
  testUser,
  testConfig
); // Easy to test with different scenarios!
```

### Configuration Example
```javascript
// Before - Methods query configuration internally
class EmailService {
  constructor(configService, templateService) {
    this._configService = configService;
    this._templateService = templateService;
  }
  
  sendWelcomeEmail(user) {
    // Hidden dependency on email configuration
    const emailConfig = this._configService.getEmailConfig();
    
    const template = this._templateService.getTemplate('welcome');
    const fromAddress = emailConfig.fromAddress;
    const replyToAddress = emailConfig.replyToAddress;
    const smtpSettings = emailConfig.smtp;
    
    const message = {
      to: user.email,
      from: fromAddress,
      replyTo: replyToAddress,
      subject: template.subject,
      body: template.render({ userName: user.name }),
      settings: smtpSettings
    };
    
    return this._sendEmail(message);
  }
  
  sendPasswordReset(user, resetToken) {
    // Same hidden dependency
    const emailConfig = this._configService.getEmailConfig();
    
    const template = this._templateService.getTemplate('password_reset');
    const fromAddress = emailConfig.fromAddress;
    const replyToAddress = emailConfig.replyToAddress;
    const smtpSettings = emailConfig.smtp;
    
    const resetUrl = `${emailConfig.baseUrl}/reset?token=${resetToken}`;
    
    const message = {
      to: user.email,
      from: fromAddress,
      replyTo: replyToAddress,
      subject: template.subject,
      body: template.render({ userName: user.name, resetUrl }),
      settings: smtpSettings
    };
    
    return this._sendEmail(message);
  }
}

// After - Configuration passed as parameters
class EmailService {
  constructor(templateService) {
    this._templateService = templateService;
  }
  
  sendWelcomeEmail(user, emailConfig) {
    // Explicit dependency on email configuration
    const template = this._templateService.getTemplate('welcome');
    
    const message = {
      to: user.email,
      from: emailConfig.fromAddress,
      replyTo: emailConfig.replyToAddress,
      subject: template.subject,
      body: template.render({ userName: user.name }),
      settings: emailConfig.smtp
    };
    
    return this._sendEmail(message);
  }
  
  sendPasswordReset(user, resetToken, emailConfig) {
    // Explicit dependency
    const template = this._templateService.getTemplate('password_reset');
    const resetUrl = `${emailConfig.baseUrl}/reset?token=${resetToken}`;
    
    const message = {
      to: user.email,
      from: emailConfig.fromAddress,
      replyTo: emailConfig.replyToAddress,
      subject: template.subject,
      body: template.render({ userName: user.name, resetUrl }),
      settings: emailConfig.smtp
    };
    
    return this._sendEmail(message);
  }
  
  _sendEmail(message) {
    // Email sending logic
    console.log(`Sending email to ${message.to}`);
    return { messageId: 'test-id' };
  }
}

// Testing with different configurations is easy
const testEmailConfig = {
  fromAddress: 'test@example.com',
  replyToAddress: 'noreply@example.com',
  baseUrl: 'https://test.example.com',
  smtp: { host: 'test-smtp.example.com', port: 587 }
};

const prodEmailConfig = {
  fromAddress: 'noreply@company.com',
  replyToAddress: 'support@company.com',
  baseUrl: 'https://app.company.com',
  smtp: { host: 'smtp.company.com', port: 587 }
};

const emailService = new EmailService(templateService);

// Can easily test with different configurations
emailService.sendWelcomeEmail(user, testEmailConfig);
emailService.sendPasswordReset(user, token, prodEmailConfig);
```

### Date/Time Example
```javascript
// Before - Methods use current time internally
class OrderService {
  createOrder(customerId, items) {
    // Hidden dependency on current time
    const now = new Date();
    
    const order = {
      id: generateOrderId(),
      customerId,
      items,
      createdAt: now,
      status: 'pending',
      estimatedDelivery: this._calculateDeliveryDate(now)
    };
    
    return this._saveOrder(order);
  }
  
  processOrder(orderId) {
    const order = this._getOrder(orderId);
    
    // Hidden dependency on current time
    const now = new Date();
    
    // Check if order is too old
    const hoursSinceCreated = (now - order.createdAt) / (1000 * 60 * 60);
    if (hoursSinceCreated > 24) {
      throw new Error('Order is too old to process');
    }
    
    order.processedAt = now;
    order.status = 'processing';
    
    return this._saveOrder(order);
  }
  
  _calculateDeliveryDate(orderDate) {
    // Add 3 business days
    const deliveryDate = new Date(orderDate);
    let daysAdded = 0;
    
    while (daysAdded < 3) {
      deliveryDate.setDate(deliveryDate.getDate() + 1);
      // Skip weekends
      if (deliveryDate.getDay() !== 0 && deliveryDate.getDay() !== 6) {
        daysAdded++;
      }
    }
    
    return deliveryDate;
  }
}

// Testing with specific dates is difficult
// Need to mock Date.now() or use time libraries

// After - Time passed as parameter
class OrderService {
  createOrder(customerId, items, currentTime = new Date()) {
    // Explicit dependency on time
    const order = {
      id: generateOrderId(),
      customerId,
      items,
      createdAt: currentTime,
      status: 'pending',
      estimatedDelivery: this._calculateDeliveryDate(currentTime)
    };
    
    return this._saveOrder(order);
  }
  
  processOrder(orderId, currentTime = new Date()) {
    const order = this._getOrder(orderId);
    
    // Explicit dependency on time
    const hoursSinceCreated = (currentTime - order.createdAt) / (1000 * 60 * 60);
    if (hoursSinceCreated > 24) {
      throw new Error('Order is too old to process');
    }
    
    order.processedAt = currentTime;
    order.status = 'processing';
    
    return this._saveOrder(order);
  }
  
  _calculateDeliveryDate(orderDate) {
    // Add 3 business days
    const deliveryDate = new Date(orderDate);
    let daysAdded = 0;
    
    while (daysAdded < 3) {
      deliveryDate.setDate(deliveryDate.getDate() + 1);
      // Skip weekends
      if (deliveryDate.getDay() !== 0 && deliveryDate.getDay() !== 6) {
        daysAdded++;
      }
    }
    
    return deliveryDate;
  }
}

// Testing with specific dates is easy
const orderService = new OrderService();

// Test with specific date
const testDate = new Date('2023-01-15T10:00:00Z');
const order = orderService.createOrder('customer123', items, testDate);

// Test order processing after 25 hours (should fail)
const laterDate = new Date('2023-01-16T11:00:00Z');
try {
  orderService.processOrder(order.id, laterDate);
} catch (error) {
  console.log(error.message); // "Order is too old to process"
}
```

## Mechanics

1. **Identify hidden dependencies**
   - Look for methods that query external state
   - Find calls to getCurrentUser(), getConfig(), new Date()
   - Check for access to global variables

2. **Add parameter for the dependency**
   - Add a parameter for the queried value
   - Choose a descriptive parameter name
   - Consider providing a default value for convenience

3. **Remove the query**
   - Delete the internal query or global access
   - Use the parameter value instead
   - Remove any related imports or dependencies

4. **Update all callers**
   - Find all places that call the method
   - Pass the required value as a parameter
   - Consider extracting the query to a higher level

5. **Consider convenience methods**
   - Provide overloaded versions for common cases
   - Create facade methods that do the querying
   - Use default parameters where appropriate

6. **Test thoroughly**
   - Test with different parameter values
   - Verify that behavior is preserved
   - Test edge cases and error conditions

## When to Use

- **Testing difficulties**: Hard to test method with different scenarios
- **Hidden dependencies**: Method dependencies are not obvious
- **Coupling issues**: Method is tightly coupled to specific data sources
- **Reusability**: Want to use method in different contexts
- **Concurrency**: External state can change during method execution
- **Pure functions**: Want to make method more functional

## When NOT to Use

- **Simple queries**: Query is trivial and unlikely to change
- **Performance**: Query result is expensive to compute
- **Convenience**: Method is primarily for convenience
- **Stable dependencies**: Dependency is stable and well-encapsulated
- **Large parameters**: Parameter would be very large or complex

## Trade-offs

### Benefits
- **Explicit dependencies**: Clear what data the method needs
- **Easier testing**: Can test with any data values
- **Flexibility**: Method can work with different data sources
- **Pure functions**: Method becomes more predictable
- **Parallelism**: Easier to use in concurrent environments
- **Reusability**: Method can be used in different contexts

### Drawbacks
- **Longer parameter lists**: More parameters to pass
- **Caller complexity**: Callers must provide the data
- **Performance**: May compute values more often
- **Convenience**: Less convenient for common cases
- **Breaking changes**: Changes method signature

## Design Patterns

### Default Parameters
```javascript
// Provide convenience while allowing flexibility
function processOrder(order, currentTime = new Date()) {
  // Use currentTime parameter
}
```

### Method Overloading Pattern
```javascript
class Service {
  // Convenience method
  process(data) {
    return this.processWithUser(data, getCurrentUser());
  }
  
  // Explicit method
  processWithUser(data, user) {
    // Explicit user parameter
  }
}
```

### Context Objects
```javascript
// Group related parameters
class ExecutionContext {
  constructor(user, config, currentTime) {
    this.user = user;
    this.config = config;
    this.currentTime = currentTime;
  }
}

function processOrder(order, context) {
  // Use context.user, context.config, context.currentTime
}
```

### Dependency Injection
```javascript
// Inject dependencies rather than querying
class OrderService {
  constructor(userProvider, configProvider, timeProvider) {
    this._userProvider = userProvider;
    this._configProvider = configProvider;
    this._timeProvider = timeProvider;
  }
  
  processOrder(order) {
    const user = this._userProvider.getCurrentUser();
    const config = this._configProvider.getConfig();
    const currentTime = this._timeProvider.now();
    
    // Process with explicit dependencies
  }
}
```

## Related Refactorings

- [Replace Parameter with Query](replace-parameter-with-query.md) - The inverse operation
- [Add Parameter](change-function-declaration.md) - Add the new parameter
- [Extract Variable](extract-variable.md) - Extract parameter computation
- [Introduce Parameter Object](introduce-parameter-object.md) - Group related parameters
- [Move Method](move-method.md) - Move method closer to data source