---
title: ACID Transactions
description: Understanding the four fundamental properties of database transactions - Atomicity, Consistency, Isolation, and Durability
source: https://blog.algomaster.io/p/what-are-acid-transactions-in-databases
tags: [acid, transactions, databases, atomicity, consistency, isolation, durability, data-integrity]
category: key-concepts
---

# ACID Transactions

## Definition

> A transaction is a sequence of one or more operations that the database treats as one single action that either fully succeeds or fully fails.

ACID is an acronym that describes four fundamental properties that guarantee reliable database transactions: **Atomicity**, **Consistency**, **Isolation**, and **Durability**. These properties ensure that database transactions are processed reliably and maintain data integrity even in the face of errors, power failures, or other unexpected issues.

## The Four ACID Properties

### 1. Atomicity

**Definition**: A transaction executes as a single and indivisible unit of work - either all operations within the transaction complete successfully, or none of them do.

#### Key Characteristics:
- **All-or-Nothing**: Either every operation in the transaction succeeds, or the entire transaction is rolled back
- **Indivisible**: The transaction cannot be partially completed
- **Failure Recovery**: If any operation fails, all previous operations in the transaction are undone

#### Implementation Techniques:

**Transaction Logs (Write-Ahead Logs)**
- Record all changes before they're applied to the database
- Enable rollback of incomplete transactions
- Maintain a complete history of operations

**Commit/Rollback Protocols**
- **Commit**: Permanently apply all transaction changes
- **Rollback**: Undo all transaction changes and restore previous state
- **Two-Phase Commit**: Coordinate commits across multiple databases

#### Practical Example:

```sql
-- Bank Transfer Transaction
BEGIN TRANSACTION;

-- Step 1: Debit source account
UPDATE accounts 
SET balance = balance - 1000 
WHERE account_id = 'ACC001';

-- Step 2: Credit destination account  
UPDATE accounts 
SET balance = balance + 1000 
WHERE account_id = 'ACC002';

-- Step 3: Log the transfer
INSERT INTO transfer_log (from_account, to_account, amount, timestamp)
VALUES ('ACC001', 'ACC002', 1000, NOW());

COMMIT; -- All operations succeed together
-- OR
ROLLBACK; -- If any operation fails, undo all changes
```

**Without Atomicity**: The system could debit one account but fail to credit the other, resulting in lost money.

**With Atomicity**: Either both accounts are updated correctly, or neither is changed.

### 2. Consistency

**Definition**: A transaction brings the database from one valid state to another valid state, maintaining all defined rules, constraints, and relationships.

#### Key Characteristics:
- **Data Integrity**: All database constraints are satisfied before and after the transaction
- **Business Rules**: Application-specific rules are enforced
- **Referential Integrity**: Foreign key relationships remain valid
- **Domain Constraints**: Data types and value ranges are respected

#### Types of Consistency:

**Database Constraints**
- Primary key uniqueness
- Foreign key relationships
- Check constraints
- Not null constraints

**Business Logic Constraints**
- Account balances cannot be negative
- Order quantities must be positive
- User ages must be realistic ranges

#### Implementation Strategies:

**Constraint Checking**
```sql
-- Example: Prevent negative inventory
ALTER TABLE products 
ADD CONSTRAINT check_positive_stock 
CHECK (stock_quantity >= 0);

-- This transaction would fail if it violates the constraint
BEGIN TRANSACTION;
UPDATE products 
SET stock_quantity = stock_quantity - 100 
WHERE product_id = 'PROD001';
-- Fails if stock_quantity would become negative
COMMIT;
```

**Triggers and Stored Procedures**
```sql
-- Trigger to maintain consistency
CREATE TRIGGER update_order_total
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE orders 
    SET total_amount = (
        SELECT SUM(quantity * price) 
        FROM order_items 
        WHERE order_id = NEW.order_id
    )
    WHERE order_id = NEW.order_id;
END;
```

#### Practical Example:

**E-commerce Order Processing**
```sql
BEGIN TRANSACTION;

-- Check product availability
SELECT stock_quantity FROM products WHERE product_id = 'PROD001';

-- Create order (must have valid customer_id)
INSERT INTO orders (customer_id, total_amount) 
VALUES (12345, 299.99);

-- Add order items (must reference valid order and product)
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES (LAST_INSERT_ID(), 'PROD001', 2, 149.99);

-- Update inventory (cannot go below zero)
UPDATE products 
SET stock_quantity = stock_quantity - 2
WHERE product_id = 'PROD001' AND stock_quantity >= 2;

COMMIT;
```

### 3. Isolation

**Definition**: Concurrent transactions are isolated from each other, preventing interference and ensuring that intermediate states of one transaction are not visible to other transactions.

#### Isolation Levels

Database systems provide different isolation levels that balance consistency with performance:

#### 1. Read Uncommitted (Lowest Isolation)
- **Allows**: Dirty reads, non-repeatable reads, phantom reads
- **Behavior**: Transactions can see uncommitted changes from other transactions
- **Use Case**: Analytics where approximate data is acceptable

```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
-- Can read data that other transactions haven't committed yet
```

#### 2. Read Committed
- **Prevents**: Dirty reads
- **Allows**: Non-repeatable reads, phantom reads
- **Behavior**: Only committed data is visible to other transactions
- **Use Case**: Most common isolation level

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Only sees committed data, but data can change between reads
```

#### 3. Repeatable Read
- **Prevents**: Dirty reads, non-repeatable reads
- **Allows**: Phantom reads
- **Behavior**: Same data is returned for repeated reads within a transaction
- **Use Case**: Financial reporting where consistency within transaction is critical

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Same SELECT returns same results throughout transaction
```

#### 4. Serializable (Highest Isolation)
- **Prevents**: All concurrency phenomena
- **Behavior**: Transactions execute as if they were run sequentially
- **Use Case**: Critical systems requiring complete isolation

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Complete isolation, but lowest concurrency
```

#### Concurrency Problems

**Dirty Read**
```sql
-- Transaction A
UPDATE accounts SET balance = 5000 WHERE id = 1;
-- Not committed yet

-- Transaction B (with Read Uncommitted)
SELECT balance FROM accounts WHERE id = 1; -- Sees 5000

-- Transaction A
ROLLBACK; -- Balance is actually still original value
```

**Non-Repeatable Read**
```sql
-- Transaction A
SELECT balance FROM accounts WHERE id = 1; -- Returns 1000

-- Transaction B
UPDATE accounts SET balance = 2000 WHERE id = 1;
COMMIT;

-- Transaction A
SELECT balance FROM accounts WHERE id = 1; -- Returns 2000 (different!)
```

**Phantom Read**
```sql
-- Transaction A
SELECT COUNT(*) FROM orders WHERE status = 'pending'; -- Returns 5

-- Transaction B
INSERT INTO orders (status) VALUES ('pending');
COMMIT;

-- Transaction A  
SELECT COUNT(*) FROM orders WHERE status = 'pending'; -- Returns 6 (phantom!)
```

#### Implementation Mechanisms

**Locking**
- **Shared Locks**: Multiple transactions can read the same data
- **Exclusive Locks**: Only one transaction can modify data
- **Lock Granularity**: Row-level, page-level, or table-level

**Multi-Version Concurrency Control (MVCC)**
- Each transaction sees a consistent snapshot of data
- Multiple versions of data are maintained
- Readers don't block writers and vice versa

**Snapshot Isolation**
- Each transaction operates on a snapshot of the database
- Changes are only visible after commit
- Reduces locking overhead

### 4. Durability

**Definition**: Once a transaction is committed, its changes are permanently stored and will survive system failures, power outages, or crashes.

#### Key Characteristics:
- **Persistence**: Committed changes survive system failures
- **Crash Recovery**: Database can recover to a consistent state after failure
- **Data Protection**: Multiple layers of protection against data loss

#### Implementation Techniques:

**Write-Ahead Logging (WAL)**
```sql
-- Before any data page is written to disk:
-- 1. Write log entry describing the change
-- 2. Ensure log entry is written to stable storage
-- 3. Then write the data page

-- Recovery process:
-- 1. Read transaction log from last checkpoint
-- 2. Redo committed transactions
-- 3. Undo uncommitted transactions
```

**Checkpointing**
- Periodically flush all committed changes to disk
- Create recovery points to limit replay time
- Balance between recovery time and system performance

**Replication**
```sql
-- Master-Slave Replication
-- Primary database writes to transaction log
-- Secondary databases replicate changes
-- Automatic failover if primary fails

-- Example PostgreSQL replication
-- Configure streaming replication for durability
```

**Backup Strategies**
- **Full Backups**: Complete database copy
- **Incremental Backups**: Only changes since last backup
- **Point-in-Time Recovery**: Restore to specific moment
- **Cross-Region Backups**: Geographic distribution for disaster recovery

#### Storage Considerations:

**Durable Storage Media**
- Traditional HDDs with battery-backed caches
- SSDs with power-loss protection
- Storage arrays with RAID configurations
- Cloud storage with replication guarantees

**fsync and Data Flushing**
```c
// Example: Ensuring data reaches disk
int fd = open("transaction.log", O_WRONLY | O_APPEND);
write(fd, transaction_data, size);
fsync(fd); // Force data to disk before returning
close(fd);
```

## ACID in Practice

### Database Examples

#### PostgreSQL
```sql
-- ACID Properties in PostgreSQL
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Atomicity: All or nothing
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 123;
INSERT INTO sales (product_id, quantity) VALUES (123, 1);

-- Consistency: Constraints enforced
-- Isolation: Serializable level prevents concurrency issues  
-- Durability: WAL ensures persistence

COMMIT; -- All ACID properties guaranteed
```

#### MySQL InnoDB
```sql
-- InnoDB storage engine provides full ACID compliance
SET autocommit = 0; -- Explicit transaction control

START TRANSACTION;
-- ACID-compliant operations
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

#### NoSQL Considerations

**MongoDB**
```javascript
// MongoDB supports ACID transactions (4.0+)
const session = client.startSession();

try {
  await session.withTransaction(async () => {
    await accounts.updateOne(
      { _id: "account1" },
      { $inc: { balance: -100 } },
      { session }
    );
    
    await accounts.updateOne(
      { _id: "account2" },
      { $inc: { balance: 100 } },
      { session }
    );
  });
} finally {
  await session.endSession();
}
```

### Performance Trade-offs

#### ACID vs. Performance
- **Stronger ACID guarantees** = **Lower performance**
- **Weaker ACID guarantees** = **Higher performance**

#### Optimization Strategies

**Batch Processing**
```sql
-- Group multiple operations into single transaction
BEGIN;
INSERT INTO orders VALUES (...), (...), (...); -- Batch insert
COMMIT;
```

**Read Replicas**
```sql
-- Separate read and write workloads
-- Write to master (full ACID)
-- Read from replicas (eventual consistency acceptable)
```

**Connection Pooling**
```python
# Reduce transaction overhead
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30
)
```

## Common Anti-Patterns

### 1. Long-Running Transactions
```sql
-- BAD: Transaction holds locks too long
BEGIN;
SELECT * FROM large_table; -- Processes millions of rows
-- Complex business logic here...
UPDATE accounts SET balance = balance + 1;
COMMIT; -- Locks held for too long
```

### 2. Nested Transactions Without Savepoints
```sql
-- BAD: No way to partially rollback
BEGIN;
INSERT INTO orders ...;
-- Some operation that might fail
INSERT INTO invalid_data ...; -- Fails
ROLLBACK; -- Loses all work

-- BETTER: Use savepoints
BEGIN;
INSERT INTO orders ...;
SAVEPOINT sp1;
INSERT INTO risky_operation ...;
-- If this fails, rollback to savepoint
ROLLBACK TO sp1;
COMMIT; -- Keep successful operations
```

### 3. Ignoring Isolation Levels
```sql
-- BAD: Using wrong isolation level
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
-- Financial calculations with dirty reads!

-- GOOD: Choose appropriate level
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Critical financial operations
```

## Best Practices

### 1. Transaction Design
- Keep transactions short and focused
- Minimize the data locked during transactions
- Batch related operations together
- Use appropriate isolation levels

### 2. Error Handling
```python
def transfer_money(from_account, to_account, amount):
    try:
        with database.transaction():
            # Perform transfer operations
            debit_account(from_account, amount)
            credit_account(to_account, amount)
            log_transfer(from_account, to_account, amount)
            
    except InsufficientFundsError:
        # Handle business logic errors
        raise
    except DatabaseError:
        # Transaction automatically rolled back
        log_error("Transfer failed due to database error")
        raise
```

### 3. Monitoring and Alerting
- Monitor transaction success/failure rates
- Track long-running transactions
- Alert on constraint violations
- Monitor lock contention

### 4. Testing ACID Properties
```python
# Test atomicity
def test_atomicity():
    initial_balance = get_total_balance()
    
    try:
        # Force a failure in the middle of transaction
        transfer_money_with_forced_failure()
    except:
        pass
    
    final_balance = get_total_balance()
    assert initial_balance == final_balance  # No partial updates

# Test isolation
def test_isolation():
    # Run concurrent transactions
    # Verify no interference between them
    pass
```

## ACID Alternatives

### BASE (Eventually Consistent)
- **Basically Available**: System remains available
- **Soft State**: Data may change over time
- **Eventual Consistency**: System will become consistent eventually

### SAGA Pattern
- Manages distributed transactions across microservices
- Uses compensating actions instead of rollbacks
- Better for long-running workflows

ACID transactions provide the foundation for reliable data management in traditional databases. While they may introduce performance overhead, they are essential for applications requiring strong consistency and data integrity guarantees. Modern systems often balance ACID properties with performance requirements by choosing appropriate isolation levels and transaction scopes.