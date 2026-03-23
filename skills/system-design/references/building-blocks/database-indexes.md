---
title: "Database Indexes: A Detailed Guide to Performance Optimization"
description: "Comprehensive guide to database indexes covering types, implementation, performance optimization, and best practices"
category: "Building Blocks"
tags: ["database", "indexes", "performance", "optimization", "b-tree", "sql"]
difficulty: "intermediate"
last_updated: "2025-07-27"
---

# Database Indexes: A Detailed Guide to Performance Optimization

Database indexes are one of the most powerful tools for optimizing query performance. Understanding how indexes work, when to use them, and how to implement them effectively is crucial for building performant database systems.

## What are Database Indexes?

A database index is a data structure that provides fast access paths to table data. Think of it as a "super-efficient lookup table" that allows the database to find specific rows without scanning the entire table.

### Index Analogy
```
Phone Book (Table)          Index (Last Name)
┌──────────────────────┐   ┌─────────────────┐
│ Adams, John - 123... │   │ Adams    → Page 1│
│ Brown, Sarah - 456...│   │ Brown    → Page 1│
│ Davis, Mike - 789... │   │ Davis    → Page 1│
│ Smith, Jane - 012... │   │ Smith    → Page 2│
│ Wilson, Bob - 345... │   │ Wilson   → Page 2│
└──────────────────────┘   └─────────────────┘
```

Instead of reading every page to find "Smith", you can use the index to jump directly to Page 2.

## How Indexes Work Internally

### Without Index (Full Table Scan)
```sql
-- Query without index
SELECT * FROM employees WHERE last_name = 'Smith';

-- Database operation:
┌─────────────────────────────────────┐
│ 1. Start at first row               │
│ 2. Check: last_name = 'Smith'? No   │
│ 3. Move to next row                 │
│ 4. Check: last_name = 'Smith'? No   │
│ 5. Repeat until end of table       │
│ Result: O(n) time complexity       │
└─────────────────────────────────────┘
```

### With Index (Index Lookup)
```sql
-- Query with index
CREATE INDEX idx_last_name ON employees (last_name);
SELECT * FROM employees WHERE last_name = 'Smith';

-- Database operation:
┌─────────────────────────────────────┐
│ 1. Look up 'Smith' in index        │
│ 2. Get pointer to row location     │
│ 3. Jump directly to row            │
│ Result: O(log n) time complexity   │
└─────────────────────────────────────┘
```

## Index Data Structures

### B-Tree Index (Most Common)

B-Tree (Balanced Tree) is the most widely used index structure, providing efficient operations for range queries and exact matches.

```
B-Tree Structure:
                    [50, 75]
                   /    |    \
              [25, 40]  [60]  [80, 90]
             /   |   \   |   /   |    \
         [10]  [30]  [45][65][78] [85] [95]
           |     |     |   |   |    |    |
        Data   Data  Data Data Data Data Data
```

**Implementation Example:**
```python
class BTreeNode:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.values = []  # Row pointers
        self.children = []
        self.is_leaf = is_leaf
    
    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        
        if i < len(self.keys) and key == self.keys[i]:
            return self.values[i]  # Return row pointer
        
        if self.is_leaf:
            return None
        
        return self.children[i].search(key)
```

**B-Tree Characteristics:**
- **Balanced**: All leaf nodes at same level
- **Sorted**: Keys maintained in sorted order
- **Logarithmic Performance**: O(log n) for search, insert, delete
- **Range Queries**: Efficient for range scans

### Hash Index

Hash indexes use hash functions for exact-match lookups with O(1) average performance.

```python
class HashIndex:
    def __init__(self, size=1000):
        self.size = size
        self.buckets = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def insert(self, key, row_pointer):
        bucket_index = self._hash(key)
        self.buckets[bucket_index].append((key, row_pointer))
    
    def search(self, key):
        bucket_index = self._hash(key)
        for stored_key, row_pointer in self.buckets[bucket_index]:
            if stored_key == key:
                return row_pointer
        return None
```

**Hash Index Characteristics:**
- **Exact Matches Only**: Cannot handle range queries
- **O(1) Performance**: Constant time for exact lookups
- **Memory Efficient**: Compact storage
- **No Ordering**: Cannot support ORDER BY clauses

### Bitmap Index

Bitmap indexes are efficient for low-cardinality data (few distinct values).

```python
class BitmapIndex:
    def __init__(self):
        self.bitmaps = {}  # value -> bitmap
        self.row_count = 0
    
    def add_value(self, value, row_id):
        if value not in self.bitmaps:
            self.bitmaps[value] = [False] * (row_id + 1)
        
        # Extend bitmap if necessary
        while len(self.bitmaps[value]) <= row_id:
            self.bitmaps[value].append(False)
        
        self.bitmaps[value][row_id] = True
        self.row_count = max(self.row_count, row_id + 1)
    
    def find_rows(self, value):
        if value not in self.bitmaps:
            return []
        
        return [i for i, bit in enumerate(self.bitmaps[value]) if bit]
    
    def and_operation(self, value1, value2):
        bitmap1 = self.bitmaps.get(value1, [])
        bitmap2 = self.bitmaps.get(value2, [])
        
        result = []
        for i in range(min(len(bitmap1), len(bitmap2))):
            if bitmap1[i] and bitmap2[i]:
                result.append(i)
        return result
```

**Bitmap Index Use Case:**
```sql
-- Efficient for low-cardinality columns
CREATE BITMAP INDEX idx_gender ON employees (gender);
CREATE BITMAP INDEX idx_department ON employees (department);

-- Efficient bitmap operations
SELECT * FROM employees 
WHERE gender = 'Female' AND department = 'Engineering';
```

## Types of Indexes

### 1. Primary Index (Clustered)

The primary index determines the physical storage order of data in the table.

```sql
-- Table creation with primary key
CREATE TABLE employees (
    id INT PRIMARY KEY,        -- Automatically creates clustered index
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);

-- Data is physically stored in ID order
┌─────────────────────────────────────┐
│ Physical Storage (ordered by ID)    │
├─────────────────────────────────────┤
│ ID=1: John, Smith, john@example.com │
│ ID=2: Jane, Doe, jane@example.com   │
│ ID=3: Bob, Wilson, bob@example.com  │
└─────────────────────────────────────┘
```

**Characteristics:**
- **Physical Ordering**: Data rows stored in index key order
- **One Per Table**: Only one clustered index per table
- **Fast Range Queries**: Sequential reads are very efficient
- **Slower Inserts**: May require row movement

### 2. Secondary Index (Non-Clustered)

Secondary indexes provide alternative access paths without changing physical storage.

```sql
-- Creating secondary indexes
CREATE INDEX idx_last_name ON employees (last_name);
CREATE INDEX idx_email ON employees (email);

-- Index structure points to primary key
┌─────────────────────────────────────┐
│ Secondary Index (last_name)         │
├─────────────────────────────────────┤
│ Doe     → Primary Key: 2           │
│ Smith   → Primary Key: 1           │
│ Wilson  → Primary Key: 3           │
└─────────────────────────────────────┘
```

### 3. Composite Index

Indexes on multiple columns, useful for multi-column queries.

```sql
-- Composite index creation
CREATE INDEX idx_name_dept ON employees (last_name, department, hire_date);

-- Index structure (left-to-right order matters)
┌─────────────────────────────────────┐
│ Composite Index Structure           │
├─────────────────────────────────────┤
│ (Adams, Engineering, 2023-01-15)   │
│ (Adams, Marketing, 2023-02-10)     │
│ (Brown, Engineering, 2023-01-20)   │
│ (Smith, Engineering, 2023-03-01)   │
└─────────────────────────────────────┘
```

**Column Order Importance:**
```sql
-- These queries can use the composite index efficiently:
SELECT * FROM employees WHERE last_name = 'Smith';                                    -- ✓
SELECT * FROM employees WHERE last_name = 'Smith' AND department = 'Engineering';     -- ✓
SELECT * FROM employees WHERE last_name = 'Smith' AND department = 'Engineering' 
                              AND hire_date > '2023-01-01';                           -- ✓

-- These queries CANNOT use the index efficiently:
SELECT * FROM employees WHERE department = 'Engineering';                             -- ✗
SELECT * FROM employees WHERE hire_date > '2023-01-01';                              -- ✗
```

### 4. Unique Index

Ensures uniqueness while providing fast lookups.

```sql
-- Unique index creation
CREATE UNIQUE INDEX idx_email_unique ON employees (email);

-- Automatically prevents duplicates
INSERT INTO employees (id, email) VALUES (1, 'john@example.com');     -- ✓
INSERT INTO employees (id, email) VALUES (2, 'john@example.com');     -- ✗ Error
```

### 5. Partial/Filtered Index

Indexes only a subset of rows based on a condition.

```sql
-- PostgreSQL partial index
CREATE INDEX idx_active_employees ON employees (last_name) 
WHERE status = 'ACTIVE';

-- SQL Server filtered index
CREATE INDEX idx_recent_orders ON orders (customer_id) 
WHERE order_date >= '2023-01-01';
```

**Benefits:**
- **Smaller Index Size**: Only indexes relevant rows
- **Faster Maintenance**: Updates only affect relevant rows
- **Better Performance**: More focused index usage

### 6. Covering Index

Includes all columns needed for a query, avoiding table lookups.

```sql
-- Covering index includes all queried columns
CREATE INDEX idx_employee_summary ON employees (department) 
INCLUDE (first_name, last_name, salary);

-- This query can be satisfied entirely from the index
SELECT first_name, last_name, salary 
FROM employees 
WHERE department = 'Engineering';
```

### 7. Function-Based Index

Creates indexes on computed expressions.

```sql
-- PostgreSQL function-based index
CREATE INDEX idx_upper_last_name ON employees (UPPER(last_name));

-- Oracle function-based index
CREATE INDEX idx_full_name ON employees (first_name || ' ' || last_name);

-- Enables efficient queries on expressions
SELECT * FROM employees WHERE UPPER(last_name) = 'SMITH';
```

## Index Performance Analysis

### Query Execution Plans

**Without Index:**
```sql
EXPLAIN ANALYZE SELECT * FROM employees WHERE last_name = 'Smith';

-- Execution Plan:
Seq Scan on employees  (cost=0.00..25000.00 rows=1000 width=50)
  Filter: (last_name = 'Smith'::text)
  Rows Removed by Filter: 99000
Planning Time: 0.123 ms
Execution Time: 45.678 ms
```

**With Index:**
```sql
CREATE INDEX idx_last_name ON employees (last_name);
EXPLAIN ANALYZE SELECT * FROM employees WHERE last_name = 'Smith';

-- Execution Plan:
Index Scan using idx_last_name on employees  (cost=0.42..8.44 rows=1000 width=50)
  Index Cond: (last_name = 'Smith'::text)
Planning Time: 0.234 ms
Execution Time: 2.345 ms
```

### Performance Metrics

```python
# Performance comparison framework
class IndexPerformanceTest:
    def __init__(self, table_size):
        self.table_size = table_size
    
    def table_scan_time(self, selectivity):
        # O(n) - must scan entire table
        return self.table_size * 0.001  # 1ms per 1000 rows
    
    def index_scan_time(self, selectivity):
        # O(log n) for index lookup + O(selectivity * n) for data access
        index_lookup = math.log2(self.table_size) * 0.01
        data_access = selectivity * self.table_size * 0.001
        return index_lookup + data_access
    
    def analyze_query(self, selectivity):
        table_scan = self.table_scan_time(selectivity)
        index_scan = self.index_scan_time(selectivity)
        
        return {
            'table_scan_ms': table_scan,
            'index_scan_ms': index_scan,
            'improvement': table_scan / index_scan if index_scan > 0 else float('inf')
        }

# Example analysis
test = IndexPerformanceTest(1000000)  # 1M rows
print(test.analyze_query(0.001))      # 0.1% selectivity
# {'table_scan_ms': 1000.0, 'index_scan_ms': 1.2, 'improvement': 833.33}
```

## Index Design Best Practices

### 1. Column Selection Strategy

```sql
-- ✓ Good candidates for indexing
CREATE INDEX idx_status ON orders (status);              -- High selectivity
CREATE INDEX idx_customer_id ON orders (customer_id);    -- Foreign key
CREATE INDEX idx_order_date ON orders (order_date);      -- Range queries

-- ✗ Poor candidates for indexing
CREATE INDEX idx_gender ON employees (gender);           -- Low selectivity (2 values)
CREATE INDEX idx_description ON products (description);  -- Large text columns
```

### 2. Composite Index Design

```sql
-- ✓ Proper column ordering (most selective first)
CREATE INDEX idx_order_lookup ON orders (status, customer_id, order_date);

-- Query patterns this index supports:
-- WHERE status = 'PENDING'
-- WHERE status = 'PENDING' AND customer_id = 123
-- WHERE status = 'PENDING' AND customer_id = 123 AND order_date > '2023-01-01'

-- ✗ Poor column ordering
CREATE INDEX idx_order_bad ON orders (order_date, customer_id, status);
-- Cannot efficiently support: WHERE status = 'PENDING'
```

### 3. Index Maintenance Considerations

```python
class IndexMaintenanceMonitor:
    def __init__(self):
        self.index_stats = {}
    
    def analyze_index_usage(self, index_name):
        # PostgreSQL index usage stats
        query = """
        SELECT 
            schemaname,
            tablename,
            indexname,
            idx_scan,
            idx_tup_read,
            idx_tup_fetch
        FROM pg_stat_user_indexes 
        WHERE indexname = %s
        """
        
        return self.execute_query(query, [index_name])
    
    def find_unused_indexes(self):
        # Find indexes with zero scans
        query = """
        SELECT indexname 
        FROM pg_stat_user_indexes 
        WHERE idx_scan = 0 
        AND schemaname = 'public'
        """
        
        return self.execute_query(query)
    
    def analyze_index_size(self):
        # Monitor index storage overhead
        query = """
        SELECT 
            indexname,
            pg_size_pretty(pg_total_relation_size(indexname::regclass)) as size
        FROM pg_stat_user_indexes
        ORDER BY pg_total_relation_size(indexname::regclass) DESC
        """
        
        return self.execute_query(query)
```

### 4. Write Performance Impact

```sql
-- Indexes slow down INSERT/UPDATE/DELETE operations
-- Example: Table with 5 indexes

INSERT INTO employees (id, first_name, last_name, email, department)
VALUES (1001, 'John', 'Doe', 'john.doe@example.com', 'Engineering');

-- Database must update:
-- 1. Primary index (id)
-- 2. idx_last_name
-- 3. idx_email (unique)
-- 4. idx_department
-- 5. idx_full_name (composite)
```

**Index Overhead Management:**
```python
def calculate_write_overhead(num_indexes, rows_affected):
    """
    Estimate write operation overhead from indexes
    """
    base_write_time = rows_affected * 0.1  # Base write time
    index_overhead = num_indexes * rows_affected * 0.05  # Index maintenance
    
    return {
        'base_time_ms': base_write_time,
        'index_overhead_ms': index_overhead,
        'total_time_ms': base_write_time + index_overhead,
        'overhead_percentage': (index_overhead / base_write_time) * 100
    }

# Example: 1000 row insert with 5 indexes
overhead = calculate_write_overhead(5, 1000)
print(overhead)
# {'base_time_ms': 100.0, 'index_overhead_ms': 250.0, 'total_time_ms': 350.0, 'overhead_percentage': 250.0}
```

## Advanced Index Techniques

### 1. Index-Only Scans

```sql
-- Create covering index
CREATE INDEX idx_order_summary ON orders (customer_id) 
INCLUDE (order_date, total_amount, status);

-- Query satisfied entirely from index
SELECT order_date, total_amount, status
FROM orders
WHERE customer_id = 123;

-- Execution plan shows "Index Only Scan"
```

### 2. Index Intersection

```sql
-- Two separate indexes
CREATE INDEX idx_status ON orders (status);
CREATE INDEX idx_date ON orders (order_date);

-- Database can combine indexes for this query
SELECT * FROM orders 
WHERE status = 'PENDING' AND order_date > '2023-01-01';

-- May use bitmap index scan combining both indexes
```

### 3. Index Skip Scan

```sql
-- Composite index
CREATE INDEX idx_category_date ON products (category, created_date);

-- Oracle can use skip scan for this query (skipping category)
SELECT * FROM products WHERE created_date > '2023-01-01';
-- Even though category is not specified
```

## Index Monitoring and Optimization

### 1. Index Usage Analysis

```sql
-- PostgreSQL: Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as size
FROM pg_stat_user_indexes 
WHERE idx_scan < 50  -- Low usage threshold
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- MySQL: Index usage statistics
SELECT 
    object_schema,
    object_name,
    index_name,
    count_star,
    count_read,
    count_insert,
    count_update,
    count_delete
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE object_schema = 'your_database'
ORDER BY count_star DESC;
```

### 2. Index Fragmentation

```sql
-- SQL Server: Check index fragmentation
SELECT 
    DB_NAME(database_id) AS DatabaseName,
    OBJECT_NAME(object_id) AS TableName,
    i.name AS IndexName,
    avg_fragmentation_in_percent,
    page_count
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED') ps
INNER JOIN sys.indexes i ON ps.object_id = i.object_id 
                         AND ps.index_id = i.index_id
WHERE avg_fragmentation_in_percent > 10
ORDER BY avg_fragmentation_in_percent DESC;

-- Rebuild fragmented indexes
ALTER INDEX idx_last_name ON employees REBUILD;
```

### 3. Missing Index Analysis

```sql
-- SQL Server: Find missing indexes
SELECT 
    mid.statement AS TableName,
    migs.avg_total_user_cost * (migs.avg_user_impact / 100.0) * (migs.user_seeks + migs.user_scans) AS ImprovementMeasure,
    'CREATE INDEX idx_' + REPLACE(REPLACE(REPLACE(mid.statement, '[', ''), ']', ''), '.', '_') + 
    ' ON ' + mid.statement + ' (' + ISNULL(mid.equality_columns, '') + 
    CASE WHEN mid.inequality_columns IS NOT NULL THEN 
        CASE WHEN mid.equality_columns IS NOT NULL THEN ',' ELSE '' END + mid.inequality_columns 
    ELSE '' END + ')' + 
    CASE WHEN mid.included_columns IS NOT NULL THEN ' INCLUDE (' + mid.included_columns + ')' ELSE '' END AS CreateIndexStatement
FROM sys.dm_db_missing_index_groups mig
INNER JOIN sys.dm_db_missing_index_group_stats migs ON migs.group_handle = mig.index_group_handle
INNER JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
ORDER BY ImprovementMeasure DESC;
```

## Common Index Anti-Patterns

### 1. Over-Indexing

```sql
-- ✗ Anti-pattern: Too many indexes
CREATE INDEX idx_first_name ON employees (first_name);
CREATE INDEX idx_last_name ON employees (last_name);
CREATE INDEX idx_email ON employees (email);
CREATE INDEX idx_department ON employees (department);
CREATE INDEX idx_hire_date ON employees (hire_date);
CREATE INDEX idx_salary ON employees (salary);
CREATE INDEX idx_status ON employees (status);

-- ✓ Better approach: Analyze query patterns first
-- Create only indexes that support actual query patterns
```

### 2. Wrong Column Order in Composite Indexes

```sql
-- ✗ Anti-pattern: Low selectivity column first
CREATE INDEX idx_bad ON orders (status, customer_id, order_date);
-- status has only 3-4 values, poor selectivity

-- ✓ Better approach: High selectivity column first
CREATE INDEX idx_good ON orders (customer_id, order_date, status);
-- customer_id has high selectivity
```

### 3. Redundant Indexes

```sql
-- ✗ Anti-pattern: Redundant indexes
CREATE INDEX idx_customer ON orders (customer_id);
CREATE INDEX idx_customer_date ON orders (customer_id, order_date);
-- First index is redundant (covered by second)

-- ✓ Better approach: Remove redundant index
DROP INDEX idx_customer;  -- Keep only the composite index
```

## Platform-Specific Considerations

### PostgreSQL

```sql
-- Partial indexes
CREATE INDEX idx_active_orders ON orders (customer_id) 
WHERE status IN ('PENDING', 'PROCESSING');

-- Expression indexes
CREATE INDEX idx_lower_email ON users (LOWER(email));

-- GIN indexes for full-text search
CREATE INDEX idx_product_search ON products 
USING GIN (to_tsvector('english', name || ' ' || description));
```

### MySQL

```sql
-- Full-text indexes
CREATE FULLTEXT INDEX idx_article_content ON articles (title, content);

-- Hash indexes (memory engine)
CREATE TABLE sessions (
    session_id CHAR(32) PRIMARY KEY,
    data TEXT,
    INDEX USING HASH (session_id)
) ENGINE=MEMORY;

-- Invisible indexes (MySQL 8.0+)
CREATE INDEX idx_test ON products (category) INVISIBLE;
```

### SQL Server

```sql
-- Included columns
CREATE INDEX idx_order_details ON orders (customer_id) 
INCLUDE (order_date, total_amount, status);

-- Filtered indexes
CREATE INDEX idx_recent_orders ON orders (customer_id) 
WHERE order_date >= '2023-01-01';

-- Columnstore indexes for analytics
CREATE COLUMNSTORE INDEX idx_analytics ON sales_fact;
```

## Future of Database Indexing

### 1. AI-Driven Index Recommendations

```python
class AIIndexAdvisor:
    def __init__(self, query_log, table_stats):
        self.query_log = query_log
        self.table_stats = table_stats
        
    def analyze_query_patterns(self):
        """Analyze query patterns to recommend indexes"""
        patterns = {}
        
        for query in self.query_log:
            # Extract WHERE clauses, JOIN conditions, ORDER BY
            conditions = self.extract_conditions(query)
            
            for condition in conditions:
                key = (condition.table, tuple(condition.columns))
                patterns[key] = patterns.get(key, 0) + 1
        
        return patterns
    
    def recommend_indexes(self):
        """Use ML to recommend optimal index configuration"""
        patterns = self.analyze_query_patterns()
        
        # ML model to predict index effectiveness
        recommendations = []
        
        for (table, columns), frequency in patterns.items():
            if frequency > self.threshold and self.predict_effectiveness(table, columns) > 0.8:
                recommendations.append({
                    'table': table,
                    'columns': columns,
                    'expected_improvement': self.calculate_improvement(table, columns),
                    'frequency': frequency
                })
        
        return sorted(recommendations, key=lambda x: x['expected_improvement'], reverse=True)
```

### 2. Adaptive Indexes

```sql
-- Oracle Automatic Indexing (Oracle 19c+)
ALTER DATABASE SET AUTO_INDEX = ON;

-- SQL Server Automatic Tuning
ALTER DATABASE CURRENT SET AUTOMATIC_TUNING (FORCE_LAST_GOOD_PLAN = ON);
```

## Conclusion

Database indexes are powerful tools for query optimization, but they require careful design and management:

### Key Takeaways

1. **Understand Your Queries**: Analyze query patterns before creating indexes
2. **Choose Appropriate Index Types**: Different index types serve different purposes
3. **Consider Column Selectivity**: High-selectivity columns make better index candidates
4. **Monitor Index Usage**: Remove unused indexes to reduce overhead
5. **Balance Read vs Write Performance**: More indexes improve reads but slow writes
6. **Use Composite Indexes Wisely**: Column order matters significantly
7. **Regular Maintenance**: Monitor fragmentation and rebuild when necessary

### Decision Framework

```python
def should_create_index(column_info, query_patterns, table_stats):
    """
    Decision framework for index creation
    """
    score = 0
    
    # Selectivity score
    if column_info['selectivity'] > 0.8:
        score += 3
    elif column_info['selectivity'] > 0.5:
        score += 2
    elif column_info['selectivity'] > 0.2:
        score += 1
    
    # Query frequency score
    if query_patterns['frequency'] > 1000:  # queries per day
        score += 3
    elif query_patterns['frequency'] > 100:
        score += 2
    elif query_patterns['frequency'] > 10:
        score += 1
    
    # Table size score
    if table_stats['row_count'] > 1000000:
        score += 2
    elif table_stats['row_count'] > 100000:
        score += 1
    
    # Write frequency penalty
    if table_stats['write_frequency'] > 1000:  # writes per day
        score -= 2
    elif table_stats['write_frequency'] > 100:
        score -= 1
    
    return score >= 5  # Threshold for index creation
```

Remember: indexes are not a silver bullet. They should be part of a comprehensive performance optimization strategy that includes proper database design, query optimization, and system architecture considerations.

The best indexing strategy is one that's continuously monitored, measured, and adapted to changing application requirements and data patterns.