---
title: "Replace Constructor with Factory Function"
description: "Replace constructor calls with factory function calls for more flexible object creation"
category: "Simplifying Function Calls"
tags: ["constructor", "factory", "object-creation", "flexibility"]
related: ["extract-function", "introduce-parameter-object", "replace-function-with-command"]
---

# Replace Constructor with Factory Function

Replace constructor calls with factory function calls. Factory functions provide more flexibility in object creation and can handle complex initialization logic better than constructors.

## Motivation

Constructors can be limiting in several ways:

- **Fixed return type**: Constructors must return instances of their class
- **Complex initialization**: Constructors can become bloated with setup logic
- **Conditional creation**: Hard to return different types based on parameters
- **Error handling**: Limited ability to handle creation failures gracefully
- **Caching/pooling**: Difficult to implement object reuse patterns
- **Testing**: Hard to mock or substitute object creation

## Example

### Basic Example
```javascript
// Before - Constructor with complex logic
class Employee {
  constructor(name, type, salary, benefits) {
    this._name = name;
    this._type = type;
    this._salary = salary;
    this._benefits = benefits || [];
    
    // Complex initialization logic in constructor
    if (type === 'manager') {
      this._salary = salary * 1.2; // Manager bonus
      this._benefits.push('company_car', 'expense_account');
      this._reportingLevel = 'senior';
    } else if (type === 'senior') {
      this._benefits.push('stock_options');
      this._reportingLevel = 'mid';
    } else if (type === 'intern') {
      this._salary = Math.min(salary, 30000); // Cap intern salary
      this._reportingLevel = 'entry';
    } else {
      this._reportingLevel = 'entry';
    }
    
    this._id = this._generateId();
    this._startDate = new Date();
  }
  
  _generateId() {
    return Math.random().toString(36).substr(2, 9);
  }
}

// Usage is verbose and error-prone
const manager = new Employee('Alice', 'manager', 80000, ['health_insurance']);
const developer = new Employee('Bob', 'senior', 75000);
const intern = new Employee('Charlie', 'intern', 40000); // Will be capped

// After - Factory functions with clear intent
class Employee {
  constructor(name, type, salary, benefits, reportingLevel, id) {
    this._name = name;
    this._type = type;
    this._salary = salary;
    this._benefits = benefits;
    this._reportingLevel = reportingLevel;
    this._id = id;
    this._startDate = new Date();
  }
  
  get name() { return this._name; }
  get type() { return this._type; }
  get salary() { return this._salary; }
  get benefits() { return [...this._benefits]; }
  get reportingLevel() { return this._reportingLevel; }
  get id() { return this._id; }
  get startDate() { return this._startDate; }
}

// Factory functions with clear names and purposes
function createManager(name, baseSalary, additionalBenefits = []) {
  const managerSalary = baseSalary * 1.2;
  const managerBenefits = [
    'health_insurance',
    'company_car',
    'expense_account',
    ...additionalBenefits
  ];
  const employeeId = generateEmployeeId('MGR');
  
  return new Employee(name, 'manager', managerSalary, managerBenefits, 'senior', employeeId);
}

function createSeniorDeveloper(name, salary, additionalBenefits = []) {
  const seniorBenefits = [
    'health_insurance',
    'stock_options',
    ...additionalBenefits
  ];
  const employeeId = generateEmployeeId('SEN');
  
  return new Employee(name, 'senior', salary, seniorBenefits, 'mid', employeeId);
}

function createIntern(name, proposedSalary, additionalBenefits = []) {
  const internSalary = Math.min(proposedSalary, 30000); // Enforce salary cap
  const internBenefits = [
    'health_insurance',
    ...additionalBenefits
  ];
  const employeeId = generateEmployeeId('INT');
  
  return new Employee(name, 'intern', internSalary, internBenefits, 'entry', employeeId);
}

function createRegularEmployee(name, salary, additionalBenefits = []) {
  const regularBenefits = [
    'health_insurance',
    ...additionalBenefits
  ];
  const employeeId = generateEmployeeId('EMP');
  
  return new Employee(name, 'regular', salary, regularBenefits, 'entry', employeeId);
}

function generateEmployeeId(prefix) {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
}

// Usage is now clear and intentional
const manager = createManager('Alice', 80000, ['dental_insurance']);
const developer = createSeniorDeveloper('Bob', 75000);
const intern = createIntern('Charlie', 40000); // Automatically capped
const regular = createRegularEmployee('Diana', 55000);
```

### Complex Example - Database Connection Factory
```javascript
// Before - Constructor tries to handle all connection types
class DatabaseConnection {
  constructor(type, config) {
    this._type = type;
    this._config = config;
    this._connection = null;
    this._isConnected = false;
    
    // Complex conditional logic in constructor
    if (type === 'mysql') {
      this._validateMySQLConfig(config);
      this._connection = this._createMySQLConnection(config);
    } else if (type === 'postgresql') {
      this._validatePostgreSQLConfig(config);
      this._connection = this._createPostgreSQLConnection(config);
    } else if (type === 'mongodb') {
      this._validateMongoDBConfig(config);
      this._connection = this._createMongoDBConnection(config);
    } else if (type === 'redis') {
      this._validateRedisConfig(config);
      this._connection = this._createRedisConnection(config);
    } else {
      throw new Error(`Unsupported database type: ${type}`);
    }
    
    // Attempt connection
    try {
      this._connect();
    } catch (error) {
      throw new Error(`Failed to connect to ${type}: ${error.message}`);
    }
  }
  
  _validateMySQLConfig(config) {
    if (!config.host || !config.user || !config.password || !config.database) {
      throw new Error('MySQL requires host, user, password, and database');
    }
  }
  
  _createMySQLConnection(config) {
    return {
      type: 'mysql',
      connectionString: `mysql://${config.user}:${config.password}@${config.host}:${config.port || 3306}/${config.database}`
    };
  }
  
  // Similar methods for other database types...
}

// Usage is confusing and error-prone
try {
  const mysql = new DatabaseConnection('mysql', {
    host: 'localhost',
    user: 'root',
    password: 'secret',
    database: 'myapp'
  });
} catch (error) {
  console.error('Connection failed:', error.message);
}

// After - Specialized factory functions
class DatabaseConnection {
  constructor(type, connectionString, config) {
    this._type = type;
    this._connectionString = connectionString;
    this._config = config;
    this._connection = null;
    this._isConnected = false;
  }
  
  get type() { return this._type; }
  get connectionString() { return this._connectionString; }
  get isConnected() { return this._isConnected; }
  
  async connect() {
    // Generic connection logic
    this._isConnected = true;
    return this;
  }
  
  async disconnect() {
    this._isConnected = false;
  }
  
  async query(sql, params) {
    if (!this._isConnected) {
      throw new Error('Not connected to database');
    }
    // Database-specific query logic would go here
    return { sql, params };
  }
}

// Factory functions for each database type
async function createMySQLConnection(config) {
  const { host, port = 3306, user, password, database, ...options } = config;
  
  if (!host || !user || !password || !database) {
    throw new Error('MySQL requires host, user, password, and database');
  }
  
  const connectionString = `mysql://${user}:${password}@${host}:${port}/${database}`;
  const connection = new DatabaseConnection('mysql', connectionString, {
    host, port, user, database, ...options
  });
  
  await connection.connect();
  return connection;
}

async function createPostgreSQLConnection(config) {
  const { host, port = 5432, user, password, database, ssl = false, ...options } = config;
  
  if (!host || !user || !password || !database) {
    throw new Error('PostgreSQL requires host, user, password, and database');
  }
  
  const sslParam = ssl ? '?ssl=true' : '';
  const connectionString = `postgresql://${user}:${password}@${host}:${port}/${database}${sslParam}`;
  const connection = new DatabaseConnection('postgresql', connectionString, {
    host, port, user, database, ssl, ...options
  });
  
  await connection.connect();
  return connection;
}

async function createMongoDBConnection(config) {
  const { host, port = 27017, database, username, password, ...options } = config;
  
  if (!host || !database) {
    throw new Error('MongoDB requires host and database');
  }
  
  let connectionString = `mongodb://`;
  if (username && password) {
    connectionString += `${username}:${password}@`;
  }
  connectionString += `${host}:${port}/${database}`;
  
  const connection = new DatabaseConnection('mongodb', connectionString, {
    host, port, database, username, ...options
  });
  
  await connection.connect();
  return connection;
}

async function createRedisConnection(config) {
  const { host, port = 6379, password, database = 0, ...options } = config;
  
  if (!host) {
    throw new Error('Redis requires host');
  }
  
  let connectionString = `redis://`;
  if (password) {
    connectionString += `:${password}@`;
  }
  connectionString += `${host}:${port}/${database}`;
  
  const connection = new DatabaseConnection('redis', connectionString, {
    host, port, database, ...options
  });
  
  await connection.connect();
  return connection;
}

// Connection factory with caching
class ConnectionFactory {
  constructor() {
    this._connections = new Map();
  }
  
  async getConnection(type, config) {
    const key = this._generateKey(type, config);
    
    if (this._connections.has(key)) {
      const connection = this._connections.get(key);
      if (connection.isConnected) {
        return connection;
      }
    }
    
    let connection;
    switch (type) {
      case 'mysql':
        connection = await createMySQLConnection(config);
        break;
      case 'postgresql':
        connection = await createPostgreSQLConnection(config);
        break;
      case 'mongodb':
        connection = await createMongoDBConnection(config);
        break;
      case 'redis':
        connection = await createRedisConnection(config);
        break;
      default:
        throw new Error(`Unsupported database type: ${type}`);
    }
    
    this._connections.set(key, connection);
    return connection;
  }
  
  _generateKey(type, config) {
    return `${type}:${config.host}:${config.port || 'default'}:${config.database || 'default'}`;
  }
}

// Usage is now clear and type-safe
async function setupDatabases() {
  try {
    const factory = new ConnectionFactory();
    
    const mysql = await factory.getConnection('mysql', {
      host: 'localhost',
      user: 'root',
      password: 'secret',
      database: 'myapp'
    });
    
    const postgres = await factory.getConnection('postgresql', {
      host: 'localhost',
      user: 'postgres',
      password: 'secret',
      database: 'myapp',
      ssl: true
    });
    
    const mongo = await factory.getConnection('mongodb', {
      host: 'localhost',
      database: 'myapp',
      username: 'user',
      password: 'secret'
    });
    
    return { mysql, postgres, mongo };
    
  } catch (error) {
    console.error('Database setup failed:', error.message);
    throw error;
  }
}
```

### Configuration Object Factory
```javascript
// Before - Constructor with many optional parameters
class ServerConfig {
  constructor(port, host, ssl, cors, auth, logging, middleware, routes) {
    this.port = port || 3000;
    this.host = host || 'localhost';
    this.ssl = ssl || false;
    this.cors = cors || { enabled: false };
    this.auth = auth || { enabled: false };
    this.logging = logging || { level: 'info' };
    this.middleware = middleware || [];
    this.routes = routes || [];
    
    // Validation and normalization in constructor
    if (this.port < 1 || this.port > 65535) {
      throw new Error('Port must be between 1 and 65535');
    }
    
    if (this.ssl && (!this.ssl.cert || !this.ssl.key)) {
      throw new Error('SSL requires cert and key files');
    }
    
    if (this.cors.enabled && !this.cors.origin) {
      this.cors.origin = '*';
    }
  }
}

// Usage is confusing with many parameters
const config = new ServerConfig(
  8080,
  '0.0.0.0',
  { cert: 'cert.pem', key: 'key.pem' },
  { enabled: true, origin: 'https://example.com' },
  { enabled: true, secret: 'secret' },
  { level: 'debug', file: 'app.log' },
  ['cors', 'auth'],
  ['/api', '/health']
);

// After - Factory functions for different scenarios
class ServerConfig {
  constructor(options) {
    this.port = options.port;
    this.host = options.host;
    this.ssl = options.ssl;
    this.cors = options.cors;
    this.auth = options.auth;
    this.logging = options.logging;
    this.middleware = options.middleware;
    this.routes = options.routes;
  }
}

// Factory function for development
function createDevelopmentConfig(overrides = {}) {
  const defaultOptions = {
    port: 3000,
    host: 'localhost',
    ssl: false,
    cors: {
      enabled: true,
      origin: 'http://localhost:3000',
      credentials: true
    },
    auth: {
      enabled: false
    },
    logging: {
      level: 'debug',
      console: true,
      file: null
    },
    middleware: ['cors', 'helmet', 'compression'],
    routes: ['/api', '/health', '/dev']
  };
  
  return new ServerConfig({ ...defaultOptions, ...overrides });
}

// Factory function for production
function createProductionConfig(options) {
  const { port, host, sslCert, sslKey, corsOrigin, authSecret, ...overrides } = options;
  
  if (!port || !host) {
    throw new Error('Production config requires port and host');
  }
  
  if (!sslCert || !sslKey) {
    throw new Error('Production config requires SSL certificate and key');
  }
  
  if (!authSecret) {
    throw new Error('Production config requires auth secret');
  }
  
  const productionOptions = {
    port,
    host,
    ssl: {
      enabled: true,
      cert: sslCert,
      key: sslKey
    },
    cors: {
      enabled: true,
      origin: corsOrigin,
      credentials: true
    },
    auth: {
      enabled: true,
      secret: authSecret,
      tokenExpiry: '24h'
    },
    logging: {
      level: 'warn',
      console: false,
      file: '/var/log/app.log'
    },
    middleware: ['cors', 'helmet', 'compression', 'rateLimit'],
    routes: ['/api', '/health']
  };
  
  return new ServerConfig({ ...productionOptions, ...overrides });
}

// Factory function for testing
function createTestConfig(overrides = {}) {
  const testOptions = {
    port: 0, // Random available port
    host: 'localhost',
    ssl: false,
    cors: {
      enabled: true,
      origin: '*'
    },
    auth: {
      enabled: false
    },
    logging: {
      level: 'error',
      console: false,
      file: null
    },
    middleware: [],
    routes: ['/api', '/health', '/test']
  };
  
  return new ServerConfig({ ...testOptions, ...overrides });
}

// Builder pattern factory
class ServerConfigBuilder {
  constructor() {
    this._options = {
      port: 3000,
      host: 'localhost',
      ssl: false,
      cors: { enabled: false },
      auth: { enabled: false },
      logging: { level: 'info' },
      middleware: [],
      routes: []
    };
  }
  
  port(port) {
    if (port < 1 || port > 65535) {
      throw new Error('Port must be between 1 and 65535');
    }
    this._options.port = port;
    return this;
  }
  
  host(host) {
    this._options.host = host;
    return this;
  }
  
  enableSSL(cert, key) {
    this._options.ssl = { enabled: true, cert, key };
    return this;
  }
  
  enableCORS(origin = '*') {
    this._options.cors = { enabled: true, origin };
    return this;
  }
  
  enableAuth(secret, tokenExpiry = '1h') {
    this._options.auth = { enabled: true, secret, tokenExpiry };
    return this;
  }
  
  setLogging(level, options = {}) {
    this._options.logging = { level, ...options };
    return this;
  }
  
  addMiddleware(...middleware) {
    this._options.middleware.push(...middleware);
    return this;
  }
  
  addRoutes(...routes) {
    this._options.routes.push(...routes);
    return this;
  }
  
  build() {
    return new ServerConfig(this._options);
  }
}

// Usage is now clear and flexible
const devConfig = createDevelopmentConfig({ port: 8080 });

const prodConfig = createProductionConfig({
  port: 443,
  host: '0.0.0.0',
  sslCert: '/etc/ssl/cert.pem',
  sslKey: '/etc/ssl/key.pem',
  corsOrigin: 'https://myapp.com',
  authSecret: process.env.AUTH_SECRET
});

const testConfig = createTestConfig();

const customConfig = new ServerConfigBuilder()
  .port(8080)
  .host('0.0.0.0')
  .enableCORS('https://example.com')
  .enableAuth('secret123')
  .setLogging('debug', { console: true })
  .addMiddleware('cors', 'helmet')
  .addRoutes('/api', '/health')
  .build();
```

## Mechanics

1. **Identify complex constructors**
   - Look for constructors with conditional logic
   - Find constructors with many parameters
   - Check for constructors that validate or transform input

2. **Create factory functions**
   - Extract constructor logic into separate functions
   - Give functions descriptive names that express intent
   - Handle validation and transformation in factories

3. **Simplify constructors**
   - Move complex logic out of constructors
   - Keep constructors simple and focused on initialization
   - Accept pre-validated and pre-processed parameters

4. **Update client code**
   - Replace constructor calls with factory function calls
   - Use factory functions that match the use case
   - Remove complex parameter passing

5. **Consider caching/pooling**
   - Add object reuse if beneficial
   - Implement caching for expensive object creation
   - Use singleton pattern where appropriate

6. **Test thoroughly**
   - Ensure all object creation scenarios work
   - Verify that validation and error handling work correctly
   - Check that factory functions return correct object types

## When to Use

- **Complex initialization**: Constructor has complex setup logic
- **Conditional creation**: Different objects based on parameters
- **Validation**: Extensive parameter validation needed
- **Caching/pooling**: Object reuse or expensive creation
- **Multiple creation patterns**: Different ways to create the same type
- **Error handling**: Need graceful handling of creation failures
- **Testing**: Need to mock or substitute object creation

## Trade-offs

### Benefits
- **Flexibility**: Can return different types or cached instances
- **Clarity**: Factory names express creation intent
- **Validation**: Better error handling and input validation
- **Caching**: Can implement object pooling or caching
- **Testing**: Easier to mock and test object creation
- **Maintainability**: Complex creation logic is separated

### Drawbacks
- **More functions**: Additional factory functions to maintain
- **Indirection**: Object creation is less direct
- **Discovery**: Harder to find all ways to create objects
- **Consistency**: Need to maintain consistent factory interfaces

## Design Patterns

### Factory Method Pattern
```javascript
class ShapeFactory {
  static createShape(type, ...args) {
    switch (type) {
      case 'circle':
        return new Circle(...args);
      case 'rectangle':
        return new Rectangle(...args);
      default:
        throw new Error(`Unknown shape: ${type}`);
    }
  }
}
```

### Abstract Factory Pattern
```javascript
class DatabaseFactory {
  static createFactory(type) {
    switch (type) {
      case 'mysql':
        return new MySQLFactory();
      case 'postgresql':
        return new PostgreSQLFactory();
      default:
        throw new Error(`Unknown database: ${type}`);
    }
  }
}
```

### Builder Pattern
```javascript
class QueryBuilder {
  constructor() {
    this._query = {};
  }
  
  select(fields) {
    this._query.select = fields;
    return this;
  }
  
  from(table) {
    this._query.from = table;
    return this;
  }
  
  where(condition) {
    this._query.where = condition;
    return this;
  }
  
  build() {
    return new Query(this._query);
  }
}
```

## Related Refactorings

- [Extract Method](extract-function.md) - Extract factory logic from constructors
- [Introduce Parameter Object](introduce-parameter-object.md) - Simplify factory parameters
- [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md) - Create specific types
- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Handle type-based creation
- [Remove Setting Method](remove-setting-method.md) - Make objects immutable after creation