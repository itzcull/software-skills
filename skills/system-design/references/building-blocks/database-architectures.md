---
title: "Database Architectures"
description: "Comprehensive guide to database architecture patterns including active-active, master-slave, multi-master, and distributed database designs"
category: "Building Blocks"
date: "2025-07-27"
tags: ["database-architecture", "active-active", "multi-master", "distributed-systems", "high-availability"]
complexity: "advanced"
---

# Database Architectures

Database architecture patterns define how data is stored, replicated, and accessed across distributed systems. Understanding different architectural approaches is crucial for building scalable, highly available, and consistent database systems that meet varying business requirements.

## Core Database Architecture Patterns

### 1. Single Database Architecture

The simplest architecture where all data resides in a single database instance.

```python
from typing import Dict, Any, Optional
import asyncio
import asyncpg

class SingleDatabaseArchitecture:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize database connection pool"""
        self.pool = await asyncpg.create_pool(
            self.connection_string,
            min_size=10,
            max_size=50,
            command_timeout=60
        )
    
    async def execute_query(self, query: str, params: tuple = ()) -> Any:
        """Execute query on single database"""
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *params)
    
    async def execute_transaction(self, operations: list) -> bool:
        """Execute multiple operations in a transaction"""
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    for operation in operations:
                        await connection.execute(operation['query'], *operation.get('params', ()))
                    return True
                except Exception as e:
                    print(f"Transaction failed: {e}")
                    return False

# Example usage
async def single_db_example():
    db = SingleDatabaseArchitecture("postgresql://localhost:5432/myapp")
    await db.initialize()
    
    # Simple query
    users = await db.execute_query("SELECT * FROM users WHERE active = $1", (True,))
    
    # Transaction
    operations = [
        {"query": "INSERT INTO orders (user_id, amount) VALUES ($1, $2)", "params": (1, 100.00)},
        {"query": "UPDATE users SET last_order_date = NOW() WHERE id = $1", "params": (1,)}
    ]
    success = await db.execute_transaction(operations)
```

**Advantages:**
- Simple to implement and maintain
- ACID transactions guaranteed
- No data consistency concerns
- Lower operational complexity

**Disadvantages:**
- Single point of failure
- Limited scalability
- Performance bottlenecks
- No geographic distribution

### 2. Master-Slave (Primary-Secondary) Architecture

One primary database handles writes while multiple read replicas serve read traffic.

```python
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any

class DatabaseRole(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"

@dataclass
class DatabaseNode:
    node_id: str
    connection_string: str
    role: DatabaseRole
    is_healthy: bool = True
    lag_ms: int = 0
    weight: float = 1.0

class MasterSlaveArchitecture:
    def __init__(self):
        self.nodes: Dict[str, DatabaseNode] = {}
        self.connections: Dict[str, asyncpg.Pool] = {}
        self.primary_node: Optional[str] = None
        self.secondary_nodes: List[str] = []
    
    async def add_node(self, node: DatabaseNode):
        """Add database node to cluster"""
        self.nodes[node.node_id] = node
        
        # Create connection pool
        pool = await asyncpg.create_pool(
            node.connection_string,
            min_size=5,
            max_size=20
        )
        self.connections[node.node_id] = pool
        
        if node.role == DatabaseRole.PRIMARY:
            self.primary_node = node.node_id
        else:
            self.secondary_nodes.append(node.node_id)
    
    async def execute_write(self, query: str, params: tuple = ()) -> Any:
        """Execute write operation on primary node"""
        if not self.primary_node:
            raise Exception("No primary node available")
        
        if not self.nodes[self.primary_node].is_healthy:
            raise Exception("Primary node is unhealthy")
        
        pool = self.connections[self.primary_node]
        async with pool.acquire() as connection:
            return await connection.execute(query, *params)
    
    async def execute_read(self, query: str, params: tuple = (), 
                          read_preference: str = "secondary_preferred") -> Any:
        """Execute read operation with read preference"""
        
        target_node = self._select_read_node(read_preference)
        
        if not target_node:
            raise Exception("No healthy nodes available for read")
        
        pool = self.connections[target_node]
        async with pool.acquire() as connection:
            return await connection.fetch(query, *params)
    
    def _select_read_node(self, read_preference: str) -> Optional[str]:
        """Select appropriate node for read operation"""
        
        healthy_secondaries = [
            node_id for node_id in self.secondary_nodes
            if self.nodes[node_id].is_healthy
        ]
        
        if read_preference == "primary":
            return self.primary_node if self.nodes[self.primary_node].is_healthy else None
        
        elif read_preference == "secondary":
            if healthy_secondaries:
                return self._weighted_random_selection(healthy_secondaries)
            return None
        
        elif read_preference == "secondary_preferred":
            if healthy_secondaries:
                return self._weighted_random_selection(healthy_secondaries)
            return self.primary_node if self.nodes[self.primary_node].is_healthy else None
        
        elif read_preference == "primary_preferred":
            if self.nodes[self.primary_node].is_healthy:
                return self.primary_node
            return self._weighted_random_selection(healthy_secondaries)
        
        else:  # nearest
            all_healthy = [self.primary_node] + healthy_secondaries
            all_healthy = [node for node in all_healthy if self.nodes[node].is_healthy]
            return min(all_healthy, key=lambda n: self.nodes[n].lag_ms) if all_healthy else None
    
    def _weighted_random_selection(self, node_ids: List[str]) -> str:
        """Select node using weighted random selection"""
        weights = [self.nodes[node_id].weight for node_id in node_ids]
        return random.choices(node_ids, weights=weights)[0]
    
    async def promote_secondary_to_primary(self, secondary_node_id: str) -> bool:
        """Promote secondary to primary (failover)"""
        
        if secondary_node_id not in self.secondary_nodes:
            return False
        
        if not self.nodes[secondary_node_id].is_healthy:
            return False
        
        # Update roles
        if self.primary_node:
            self.nodes[self.primary_node].role = DatabaseRole.SECONDARY
            self.secondary_nodes.append(self.primary_node)
        
        self.nodes[secondary_node_id].role = DatabaseRole.PRIMARY
        self.secondary_nodes.remove(secondary_node_id)
        self.primary_node = secondary_node_id
        
        print(f"Promoted {secondary_node_id} to primary")
        return True
    
    async def check_replication_lag(self) -> Dict[str, int]:
        """Check replication lag for all secondary nodes"""
        lag_info = {}
        
        for node_id in self.secondary_nodes:
            if self.nodes[node_id].is_healthy:
                # Query replication lag (PostgreSQL example)
                try:
                    pool = self.connections[node_id]
                    async with pool.acquire() as connection:
                        result = await connection.fetchrow("""
                            SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))::int as lag_seconds
                        """)
                        lag_seconds = result['lag_seconds'] if result['lag_seconds'] else 0
                        lag_info[node_id] = lag_seconds * 1000  # Convert to milliseconds
                        self.nodes[node_id].lag_ms = lag_seconds * 1000
                except Exception as e:
                    print(f"Error checking lag for {node_id}: {e}")
                    lag_info[node_id] = -1
        
        return lag_info

# Example setup
async def master_slave_example():
    architecture = MasterSlaveArchitecture()
    
    # Add primary node
    primary = DatabaseNode(
        node_id="primary",
        connection_string="postgresql://primary:5432/myapp",
        role=DatabaseRole.PRIMARY
    )
    await architecture.add_node(primary)
    
    # Add secondary nodes
    secondary1 = DatabaseNode(
        node_id="secondary1",
        connection_string="postgresql://secondary1:5432/myapp",
        role=DatabaseRole.SECONDARY,
        weight=1.0
    )
    await architecture.add_node(secondary1)
    
    secondary2 = DatabaseNode(
        node_id="secondary2", 
        connection_string="postgresql://secondary2:5432/myapp",
        role=DatabaseRole.SECONDARY,
        weight=1.5  # Higher weight for better hardware
    )
    await architecture.add_node(secondary2)
    
    # Write to primary
    await architecture.execute_write(
        "INSERT INTO users (name, email) VALUES ($1, $2)",
        ("John Doe", "john@example.com")
    )
    
    # Read from secondary (preferred)
    users = await architecture.execute_read(
        "SELECT * FROM users WHERE active = $1",
        (True,),
        read_preference="secondary_preferred"
    )
    
    # Check replication lag
    lag_info = await architecture.check_replication_lag()
    print(f"Replication lag: {lag_info}")
```

### 3. Active-Active (Multi-Master) Architecture

Multiple database nodes can accept both read and write operations, with conflict resolution mechanisms.

```python
from enum import Enum
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
import uuid
import json

class ConflictResolutionStrategy(Enum):
    LAST_WRITE_WINS = "last_write_wins"
    FIRST_WRITE_WINS = "first_write_wins"
    MANUAL_RESOLUTION = "manual_resolution"
    CUSTOM_FUNCTION = "custom_function"

@dataclass
class WriteOperation:
    operation_id: str
    node_id: str
    table_name: str
    operation_type: str  # INSERT, UPDATE, DELETE
    data: Dict[str, Any]
    timestamp: datetime
    version_vector: Dict[str, int]

class VectorClock:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.clock: Dict[str, int] = {node_id: 0}
    
    def increment(self) -> Dict[str, int]:
        """Increment local counter"""
        self.clock[self.node_id] += 1
        return self.clock.copy()
    
    def update(self, other_clock: Dict[str, int]) -> None:
        """Update clock with received vector clock"""
        for node, count in other_clock.items():
            self.clock[node] = max(self.clock.get(node, 0), count)
        # Increment local counter
        self.clock[self.node_id] += 1
    
    def compare(self, other_clock: Dict[str, int]) -> str:
        """Compare vector clocks"""
        # Returns: "before", "after", "concurrent"
        
        self_dominates = False
        other_dominates = False
        
        all_nodes = set(self.clock.keys()) | set(other_clock.keys())
        
        for node in all_nodes:
            self_count = self.clock.get(node, 0)
            other_count = other_clock.get(node, 0)
            
            if self_count > other_count:
                self_dominates = True
            elif self_count < other_count:
                other_dominates = True
        
        if self_dominates and not other_dominates:
            return "after"
        elif other_dominates and not self_dominates:
            return "before"
        else:
            return "concurrent"

class ActiveActiveArchitecture:
    def __init__(self, node_id: str, conflict_resolution: ConflictResolutionStrategy):
        self.node_id = node_id
        self.conflict_resolution = conflict_resolution
        self.vector_clock = VectorClock(node_id)
        self.nodes: Dict[str, DatabaseNode] = {}
        self.connections: Dict[str, asyncpg.Pool] = {}
        self.pending_operations: List[WriteOperation] = []
        self.operation_log: List[WriteOperation] = []
        self.conflict_queue: List[Tuple[WriteOperation, WriteOperation]] = []
    
    async def add_node(self, node: DatabaseNode):
        """Add node to active-active cluster"""
        self.nodes[node.node_id] = node
        
        pool = await asyncpg.create_pool(
            node.connection_string,
            min_size=5,
            max_size=20
        )
        self.connections[node.node_id] = pool
        
        # Initialize vector clock entry
        self.vector_clock.clock[node.node_id] = 0
    
    async def execute_write(self, table_name: str, operation_type: str, 
                          data: Dict[str, Any]) -> str:
        """Execute write operation with conflict detection"""
        
        # Create operation with vector clock
        operation_id = str(uuid.uuid4())
        version_vector = self.vector_clock.increment()
        
        operation = WriteOperation(
            operation_id=operation_id,
            node_id=self.node_id,
            table_name=table_name,
            operation_type=operation_type,
            data=data,
            timestamp=datetime.now(timezone.utc),
            version_vector=version_vector
        )
        
        # Execute locally
        await self._execute_local_write(operation)
        
        # Add to operation log
        self.operation_log.append(operation)
        
        # Replicate to other nodes
        await self._replicate_operation(operation)
        
        return operation_id
    
    async def _execute_local_write(self, operation: WriteOperation):
        """Execute write operation on local node"""
        
        pool = self.connections[self.node_id]
        async with pool.acquire() as connection:
            
            if operation.operation_type == "INSERT":
                # Add metadata for conflict resolution
                operation.data['_operation_id'] = operation.operation_id
                operation.data['_node_id'] = operation.node_id
                operation.data['_timestamp'] = operation.timestamp
                operation.data['_version_vector'] = json.dumps(operation.version_vector)
                
                columns = list(operation.data.keys())
                values = list(operation.data.values())
                placeholders = ', '.join(['$' + str(i+1) for i in range(len(values))])
                
                query = f"""
                INSERT INTO {operation.table_name} ({', '.join(columns)})
                VALUES ({placeholders})
                ON CONFLICT DO NOTHING
                """
                
                await connection.execute(query, *values)
            
            elif operation.operation_type == "UPDATE":
                # Handle update with conflict detection
                await self._execute_update_with_conflict_detection(connection, operation)
            
            elif operation.operation_type == "DELETE":
                # Soft delete with tombstone
                await self._execute_soft_delete(connection, operation)
    
    async def _execute_update_with_conflict_detection(self, connection, operation: WriteOperation):
        """Execute update with conflict detection"""
        
        # Get current version vector
        primary_key = operation.data.get('id')
        current_record = await connection.fetchrow(
            f"SELECT _version_vector FROM {operation.table_name} WHERE id = $1",
            primary_key
        )
        
        if current_record:
            current_vector = json.loads(current_record['_version_vector'])
            comparison = self.vector_clock.compare(current_vector)
            
            if comparison == "after":
                # Our operation is newer, proceed with update
                set_clauses = []
                values = []
                param_count = 1
                
                for key, value in operation.data.items():
                    if key != 'id':  # Skip primary key
                        set_clauses.append(f"{key} = ${param_count}")
                        values.append(value)
                        param_count += 1
                
                # Add metadata
                set_clauses.extend([
                    f"_operation_id = ${param_count}",
                    f"_node_id = ${param_count + 1}",
                    f"_timestamp = ${param_count + 2}",
                    f"_version_vector = ${param_count + 3}"
                ])
                values.extend([
                    operation.operation_id,
                    operation.node_id,
                    operation.timestamp,
                    json.dumps(operation.version_vector)
                ])
                
                query = f"""
                UPDATE {operation.table_name}
                SET {', '.join(set_clauses)}
                WHERE id = ${param_count + 4}
                """
                values.append(primary_key)
                
                await connection.execute(query, *values)
            
            elif comparison == "concurrent":
                # Conflict detected, queue for resolution
                existing_operation = WriteOperation(
                    operation_id=current_record.get('_operation_id', ''),
                    node_id=current_record.get('_node_id', ''),
                    table_name=operation.table_name,
                    operation_type="UPDATE",
                    data=dict(current_record),
                    timestamp=current_record.get('_timestamp', datetime.now(timezone.utc)),
                    version_vector=current_vector
                )
                
                self.conflict_queue.append((existing_operation, operation))
                await self._resolve_conflict(existing_operation, operation)
    
    async def _execute_soft_delete(self, connection, operation: WriteOperation):
        """Execute soft delete with tombstone"""
        
        primary_key = operation.data.get('id')
        
        query = f"""
        UPDATE {operation.table_name}
        SET _deleted = true,
            _operation_id = $1,
            _node_id = $2,
            _timestamp = $3,
            _version_vector = $4
        WHERE id = $5
        """
        
        await connection.execute(
            query,
            operation.operation_id,
            operation.node_id,
            operation.timestamp,
            json.dumps(operation.version_vector),
            primary_key
        )
    
    async def _replicate_operation(self, operation: WriteOperation):
        """Replicate operation to other nodes"""
        
        replication_tasks = []
        
        for node_id in self.nodes.keys():
            if node_id != self.node_id:
                task = asyncio.create_task(
                    self._send_operation_to_node(node_id, operation)
                )
                replication_tasks.append(task)
        
        # Wait for all replications
        results = await asyncio.gather(*replication_tasks, return_exceptions=True)
        
        # Log any replication failures
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                node_id = list(self.nodes.keys())[i]
                print(f"Replication to {node_id} failed: {result}")
    
    async def _send_operation_to_node(self, target_node_id: str, operation: WriteOperation):
        """Send operation to specific node"""
        
        # In a real implementation, this would use message queues or HTTP APIs
        # For this example, we'll simulate by calling receive_operation
        
        if target_node_id in self.connections:
            # Simulate network delay
            await asyncio.sleep(0.1)
            
            # This would be an API call in practice
            await self._receive_operation_from_peer(operation)
    
    async def _receive_operation_from_peer(self, operation: WriteOperation):
        """Receive and process operation from peer node"""
        
        # Update vector clock
        self.vector_clock.update(operation.version_vector)
        
        # Check if we need to apply this operation
        if not await self._operation_already_applied(operation):
            await self._execute_local_write(operation)
            self.operation_log.append(operation)
    
    async def _operation_already_applied(self, operation: WriteOperation) -> bool:
        """Check if operation was already applied"""
        
        for existing_op in self.operation_log:
            if existing_op.operation_id == operation.operation_id:
                return True
        
        return False
    
    async def _resolve_conflict(self, operation1: WriteOperation, operation2: WriteOperation):
        """Resolve conflict between two operations"""
        
        if self.conflict_resolution == ConflictResolutionStrategy.LAST_WRITE_WINS:
            winning_operation = operation1 if operation1.timestamp > operation2.timestamp else operation2
            await self._apply_winning_operation(winning_operation)
        
        elif self.conflict_resolution == ConflictResolutionStrategy.FIRST_WRITE_WINS:
            winning_operation = operation1 if operation1.timestamp < operation2.timestamp else operation2
            await self._apply_winning_operation(winning_operation)
        
        elif self.conflict_resolution == ConflictResolutionStrategy.MANUAL_RESOLUTION:
            # Queue for manual resolution
            print(f"Conflict requires manual resolution: {operation1.operation_id} vs {operation2.operation_id}")
        
        else:
            # Custom resolution logic would go here
            pass
    
    async def _apply_winning_operation(self, winning_operation: WriteOperation):
        """Apply the winning operation from conflict resolution"""
        
        pool = self.connections[self.node_id]
        async with pool.acquire() as connection:
            # Force apply the winning operation
            await self._execute_local_write(winning_operation)
    
    async def execute_read(self, query: str, params: tuple = ()) -> Any:
        """Execute read operation on local node"""
        
        pool = self.connections[self.node_id]
        async with pool.acquire() as connection:
            # Add filter to exclude soft-deleted records
            if "WHERE" in query.upper():
                query = query.replace("WHERE", "WHERE (_deleted IS NULL OR _deleted = false) AND")
            else:
                query = query.replace("FROM", "FROM").replace(" ORDER", " WHERE (_deleted IS NULL OR _deleted = false) ORDER")
            
            return await connection.fetch(query, *params)
    
    async def get_conflict_summary(self) -> Dict[str, Any]:
        """Get summary of conflicts and their resolution status"""
        
        return {
            'total_conflicts': len(self.conflict_queue),
            'pending_manual_resolution': len([
                c for c in self.conflict_queue 
                if self.conflict_resolution == ConflictResolutionStrategy.MANUAL_RESOLUTION
            ]),
            'conflict_resolution_strategy': self.conflict_resolution.value,
            'node_id': self.node_id,
            'vector_clock': self.vector_clock.clock
        }

# Example usage
async def active_active_example():
    # Create two active-active nodes
    node1 = ActiveActiveArchitecture("node1", ConflictResolutionStrategy.LAST_WRITE_WINS)
    node2 = ActiveActiveArchitecture("node2", ConflictResolutionStrategy.LAST_WRITE_WINS)
    
    # Add database nodes
    db_node1 = DatabaseNode("node1", "postgresql://node1:5432/myapp", DatabaseRole.PRIMARY)
    db_node2 = DatabaseNode("node2", "postgresql://node2:5432/myapp", DatabaseRole.PRIMARY)
    
    await node1.add_node(db_node1)
    await node1.add_node(db_node2)
    await node2.add_node(db_node1)
    await node2.add_node(db_node2)
    
    # Concurrent writes on different nodes
    await node1.execute_write("users", "INSERT", {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    })
    
    await node2.execute_write("users", "UPDATE", {
        "id": 1,
        "email": "john.doe@example.com"
    })
    
    # Check conflict status
    conflicts1 = await node1.get_conflict_summary()
    conflicts2 = await node2.get_conflict_summary()
    
    print(f"Node1 conflicts: {conflicts1}")
    print(f"Node2 conflicts: {conflicts2}")
```

### 4. Federated Database Architecture

Distributes data across multiple independent database systems with a unified query interface.

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import asyncio

class DatabaseAdapter(ABC):
    """Abstract adapter for different database types"""
    
    @abstractmethod
    async def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        pass
    
    @abstractmethod
    async def get_schema(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def translate_query(self, query: str) -> str:
        pass

class PostgreSQLAdapter(DatabaseAdapter):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool = None
    
    async def initialize(self):
        self.pool = await asyncpg.create_pool(self.connection_string)
    
    async def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        async with self.pool.acquire() as connection:
            result = await connection.fetch(query, *params)
            return [dict(row) for row in result]
    
    async def get_schema(self) -> Dict[str, Any]:
        schema_query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position
        """
        result = await self.execute_query(schema_query)
        
        schema = {}
        for row in result:
            table = row['table_name']
            if table not in schema:
                schema[table] = []
            schema[table].append({
                'column': row['column_name'],
                'type': row['data_type']
            })
        
        return schema
    
    def translate_query(self, query: str) -> str:
        # PostgreSQL doesn't need translation
        return query

class MongoDBAdapter(DatabaseAdapter):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.client = None
        self.db = None
    
    async def initialize(self):
        # Mock MongoDB initialization
        print(f"Connecting to MongoDB: {self.connection_string}")
    
    async def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        # Translate SQL-like query to MongoDB operations
        # This is simplified - real implementation would be more complex
        
        if "SELECT * FROM users" in query:
            # Mock result
            return [
                {"_id": "1", "name": "John Doe", "email": "john@example.com"},
                {"_id": "2", "name": "Jane Smith", "email": "jane@example.com"}
            ]
        
        return []
    
    async def get_schema(self) -> Dict[str, Any]:
        # Mock schema for MongoDB
        return {
            "users": [
                {"column": "_id", "type": "ObjectId"},
                {"column": "name", "type": "String"},
                {"column": "email", "type": "String"}
            ]
        }
    
    def translate_query(self, query: str) -> str:
        # Translate SQL to MongoDB query language
        # Simplified implementation
        return query

@dataclass
class FederatedDataSource:
    source_id: str
    adapter: DatabaseAdapter
    tables: List[str]
    priority: int = 1
    is_active: bool = True

class FederatedDatabaseArchitecture:
    def __init__(self):
        self.data_sources: Dict[str, FederatedDataSource] = {}
        self.global_schema: Dict[str, Dict] = {}
        self.query_planner = FederatedQueryPlanner()
    
    async def add_data_source(self, source: FederatedDataSource):
        """Add data source to federation"""
        
        await source.adapter.initialize()
        self.data_sources[source.source_id] = source
        
        # Update global schema
        source_schema = await source.adapter.get_schema()
        for table_name, columns in source_schema.items():
            if table_name not in self.global_schema:
                self.global_schema[table_name] = {
                    'sources': [],
                    'columns': columns
                }
            self.global_schema[table_name]['sources'].append(source.source_id)
    
    async def execute_federated_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute query across federated data sources"""
        
        # Parse query to determine required tables
        required_tables = self._extract_tables_from_query(query)
        
        # Create execution plan
        execution_plan = self.query_planner.create_execution_plan(
            query, required_tables, self.global_schema, self.data_sources
        )
        
        # Execute plan
        return await self._execute_plan(execution_plan)
    
    def _extract_tables_from_query(self, query: str) -> List[str]:
        """Extract table names from SQL query"""
        # Simplified parser - production would use proper SQL parsing
        import re
        
        # Find FROM clauses
        from_matches = re.findall(r'FROM\s+(\w+)', query, re.IGNORECASE)
        
        # Find JOIN clauses
        join_matches = re.findall(r'JOIN\s+(\w+)', query, re.IGNORECASE)
        
        return list(set(from_matches + join_matches))
    
    async def _execute_plan(self, execution_plan: Dict) -> List[Dict]:
        """Execute federated query plan"""
        
        if execution_plan['type'] == 'single_source':
            # Query against single data source
            source_id = execution_plan['source_id']
            source = self.data_sources[source_id]
            
            translated_query = source.adapter.translate_query(execution_plan['query'])
            return await source.adapter.execute_query(translated_query, execution_plan.get('params', ()))
        
        elif execution_plan['type'] == 'union':
            # Union queries from multiple sources
            all_results = []
            
            for sub_plan in execution_plan['sub_plans']:
                results = await self._execute_plan(sub_plan)
                all_results.extend(results)
            
            return all_results
        
        elif execution_plan['type'] == 'join':
            # Join data from multiple sources
            return await self._execute_federated_join(execution_plan)
        
        else:
            raise ValueError(f"Unknown execution plan type: {execution_plan['type']}")
    
    async def _execute_federated_join(self, execution_plan: Dict) -> List[Dict]:
        """Execute join across federated data sources"""
        
        # Execute sub-queries
        left_results = await self._execute_plan(execution_plan['left_plan'])
        right_results = await self._execute_plan(execution_plan['right_plan'])
        
        # Perform join in memory (simplified)
        join_column = execution_plan['join_column']
        joined_results = []
        
        for left_row in left_results:
            for right_row in right_results:
                if left_row.get(join_column) == right_row.get(join_column):
                    # Merge rows
                    merged_row = {**left_row, **right_row}
                    joined_results.append(merged_row)
        
        return joined_results
    
    async def get_federation_status(self) -> Dict[str, Any]:
        """Get status of all federated data sources"""
        
        status = {
            'total_sources': len(self.data_sources),
            'active_sources': sum(1 for s in self.data_sources.values() if s.is_active),
            'global_tables': len(self.global_schema),
            'sources': {}
        }
        
        for source_id, source in self.data_sources.items():
            try:
                # Test connectivity
                await source.adapter.execute_query("SELECT 1")
                connection_status = "healthy"
            except Exception as e:
                connection_status = f"error: {str(e)}"
            
            status['sources'][source_id] = {
                'is_active': source.is_active,
                'connection_status': connection_status,
                'tables': source.tables,
                'priority': source.priority
            }
        
        return status

class FederatedQueryPlanner:
    def create_execution_plan(self, query: str, required_tables: List[str], 
                            global_schema: Dict, data_sources: Dict) -> Dict:
        """Create execution plan for federated query"""
        
        # Determine which sources contain required tables
        relevant_sources = self._find_relevant_sources(required_tables, global_schema)
        
        if len(relevant_sources) == 1:
            # Single source query
            source_id = relevant_sources[0]
            return {
                'type': 'single_source',
                'source_id': source_id,
                'query': query,
                'params': ()
            }
        
        elif len(required_tables) == 1:
            # Single table, multiple sources - union
            return self._create_union_plan(query, required_tables[0], relevant_sources)
        
        else:
            # Multiple tables - join
            return self._create_join_plan(query, required_tables, relevant_sources, global_schema)
    
    def _find_relevant_sources(self, required_tables: List[str], 
                             global_schema: Dict) -> List[str]:
        """Find data sources that contain required tables"""
        
        relevant_sources = set()
        
        for table in required_tables:
            if table in global_schema:
                relevant_sources.update(global_schema[table]['sources'])
        
        return list(relevant_sources)
    
    def _create_union_plan(self, query: str, table: str, sources: List[str]) -> Dict:
        """Create union plan for single table across multiple sources"""
        
        sub_plans = []
        for source_id in sources:
            sub_plans.append({
                'type': 'single_source',
                'source_id': source_id,
                'query': query,
                'params': ()
            })
        
        return {
            'type': 'union',
            'sub_plans': sub_plans
        }
    
    def _create_join_plan(self, query: str, tables: List[str], 
                         sources: List[str], global_schema: Dict) -> Dict:
        """Create join plan for multiple tables"""
        
        # Simplified join planning
        # In practice, this would be much more sophisticated
        
        left_table = tables[0]
        right_table = tables[1] if len(tables) > 1 else tables[0]
        
        left_source = global_schema[left_table]['sources'][0]
        right_source = global_schema[right_table]['sources'][0]
        
        return {
            'type': 'join',
            'join_column': 'id',  # Simplified assumption
            'left_plan': {
                'type': 'single_source',
                'source_id': left_source,
                'query': f"SELECT * FROM {left_table}",
                'params': ()
            },
            'right_plan': {
                'type': 'single_source',
                'source_id': right_source,
                'query': f"SELECT * FROM {right_table}",
                'params': ()
            }
        }

# Example usage
async def federated_example():
    federation = FederatedDatabaseArchitecture()
    
    # Add PostgreSQL source
    pg_adapter = PostgreSQLAdapter("postgresql://pg:5432/main")
    pg_source = FederatedDataSource(
        source_id="postgres_main",
        adapter=pg_adapter,
        tables=["users", "orders"],
        priority=1
    )
    await federation.add_data_source(pg_source)
    
    # Add MongoDB source
    mongo_adapter = MongoDBAdapter("mongodb://mongo:27017/analytics")
    mongo_source = FederatedDataSource(
        source_id="mongo_analytics",
        adapter=mongo_adapter,
        tables=["user_analytics"],
        priority=2
    )
    await federation.add_data_source(mongo_source)
    
    # Execute federated query
    results = await federation.execute_federated_query(
        "SELECT * FROM users WHERE active = true"
    )
    
    print(f"Federated query results: {results}")
    
    # Get federation status
    status = await federation.get_federation_status()
    print(f"Federation status: {status}")
```

## Architecture Selection Guidelines

### Choosing the Right Architecture

```python
class ArchitectureDecisionFramework:
    def __init__(self):
        self.decision_criteria = {
            'data_volume': 'Amount of data to be stored and processed',
            'read_write_ratio': 'Ratio of read operations to write operations',
            'consistency_requirements': 'ACID vs eventual consistency needs',
            'availability_requirements': 'Uptime and fault tolerance needs',
            'scalability_requirements': 'Growth projections and scaling needs',
            'geographic_distribution': 'Global vs regional deployment needs',
            'operational_complexity': 'Team expertise and operational overhead',
            'budget_constraints': 'Infrastructure and operational costs'
        }
    
    def recommend_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend database architecture based on requirements"""
        
        recommendations = []
        scores = {}
        
        # Single Database
        single_db_score = self._score_single_database(requirements)
        scores['single_database'] = single_db_score
        
        # Master-Slave
        master_slave_score = self._score_master_slave(requirements)
        scores['master_slave'] = master_slave_score
        
        # Active-Active
        active_active_score = self._score_active_active(requirements)
        scores['active_active'] = active_active_score
        
        # Federated
        federated_score = self._score_federated(requirements)
        scores['federated'] = federated_score
        
        # Sort by score
        sorted_architectures = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'recommended_architecture': sorted_architectures[0][0],
            'all_scores': scores,
            'recommendations': self._generate_recommendations(requirements, sorted_architectures[0])
        }
    
    def _score_single_database(self, req: Dict[str, Any]) -> float:
        """Score single database architecture"""
        score = 10.0
        
        # Penalty for high data volume
        if req.get('data_volume', 'small') in ['large', 'very_large']:
            score -= 5.0
        
        # Penalty for high read load
        if req.get('read_write_ratio', 1) > 10:
            score -= 3.0
        
        # Bonus for strong consistency needs
        if req.get('consistency_requirements') == 'strong':
            score += 2.0
        
        # Penalty for high availability needs
        if req.get('availability_requirements', 'standard') == 'high':
            score -= 4.0
        
        # Bonus for operational simplicity
        if req.get('operational_complexity', 'medium') == 'low':
            score += 3.0
        
        return max(0, score)
    
    def _score_master_slave(self, req: Dict[str, Any]) -> float:
        """Score master-slave architecture"""
        score = 7.0
        
        # Bonus for read-heavy workloads
        if req.get('read_write_ratio', 1) > 5:
            score += 3.0
        
        # Bonus for medium data volumes
        if req.get('data_volume', 'small') == 'medium':
            score += 2.0
        
        # Good for eventual consistency
        if req.get('consistency_requirements') == 'eventual':
            score += 1.0
        
        # Good availability improvement
        if req.get('availability_requirements') == 'high':
            score += 2.0
        
        return max(0, score)
    
    def _score_active_active(self, req: Dict[str, Any]) -> float:
        """Score active-active architecture"""
        score = 5.0
        
        # Bonus for very high availability needs
        if req.get('availability_requirements') == 'very_high':
            score += 4.0
        
        # Bonus for geographic distribution
        if req.get('geographic_distribution') == 'global':
            score += 3.0
        
        # Penalty for strong consistency needs
        if req.get('consistency_requirements') == 'strong':
            score -= 3.0
        
        # Bonus for write-heavy workloads
        if req.get('read_write_ratio', 1) < 2:
            score += 2.0
        
        # Penalty for operational complexity concerns
        if req.get('operational_complexity') == 'low':
            score -= 2.0
        
        return max(0, score)
    
    def _score_federated(self, req: Dict[str, Any]) -> float:
        """Score federated architecture"""
        score = 4.0
        
        # Bonus for heterogeneous data sources
        if req.get('heterogeneous_sources', False):
            score += 4.0
        
        # Bonus for data integration needs
        if req.get('data_integration_needs', False):
            score += 3.0
        
        # Penalty for performance requirements
        if req.get('performance_requirements', 'medium') == 'high':
            score -= 2.0
        
        # Works with various consistency models
        score += 1.0
        
        return max(0, score)
    
    def _generate_recommendations(self, requirements: Dict, top_choice: Tuple) -> List[str]:
        """Generate specific recommendations"""
        
        architecture, score = top_choice
        recommendations = []
        
        if architecture == 'single_database':
            recommendations.extend([
                "Start with single database for simplicity",
                "Implement proper indexing and query optimization", 
                "Plan for vertical scaling initially",
                "Monitor performance and plan migration path"
            ])
        
        elif architecture == 'master_slave':
            recommendations.extend([
                "Implement read replicas for read scaling",
                "Use connection pooling and read/write splitting",
                "Monitor replication lag",
                "Plan for automatic failover"
            ])
        
        elif architecture == 'active_active':
            recommendations.extend([
                "Design application for eventual consistency",
                "Implement robust conflict resolution",
                "Use vector clocks for causality tracking",
                "Plan for complex operational procedures"
            ])
        
        elif architecture == 'federated':
            recommendations.extend([
                "Design unified data access layer",
                "Implement query optimization across sources",
                "Plan for data governance and security",
                "Consider performance implications of joins"
            ])
        
        return recommendations

# Example usage
def architecture_decision_example():
    framework = ArchitectureDecisionFramework()
    
    # Example requirements for a growing e-commerce platform
    requirements = {
        'data_volume': 'large',
        'read_write_ratio': 8,  # Read-heavy
        'consistency_requirements': 'eventual',
        'availability_requirements': 'high',
        'scalability_requirements': 'high',
        'geographic_distribution': 'regional',
        'operational_complexity': 'medium',
        'budget_constraints': 'medium'
    }
    
    recommendation = framework.recommend_architecture(requirements)
    
    print(f"Recommended architecture: {recommendation['recommended_architecture']}")
    print(f"Architecture scores: {recommendation['all_scores']}")
    print("Recommendations:")
    for rec in recommendation['recommendations']:
        print(f"- {rec}")
```

## Migration Strategies

### Database Architecture Migration

```python
class ArchitectureMigrationPlanner:
    def __init__(self):
        self.migration_strategies = {
            'blue_green': BlueGreenMigration(),
            'rolling': RollingMigration(),
            'shadow_write': ShadowWriteMigration(),
            'gradual_cutover': GradualCutoverMigration()
        }
    
    def plan_migration(self, source_arch: str, target_arch: str, 
                      constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Plan migration between database architectures"""
        
        migration_complexity = self._assess_migration_complexity(source_arch, target_arch)
        recommended_strategy = self._recommend_migration_strategy(migration_complexity, constraints)
        
        return {
            'source_architecture': source_arch,
            'target_architecture': target_arch,
            'complexity': migration_complexity,
            'recommended_strategy': recommended_strategy,
            'estimated_timeline': self._estimate_timeline(migration_complexity),
            'risk_factors': self._identify_risk_factors(source_arch, target_arch),
            'rollback_plan': self._create_rollback_plan(source_arch, target_arch)
        }
    
    def _assess_migration_complexity(self, source: str, target: str) -> str:
        """Assess complexity of migration between architectures"""
        
        complexity_matrix = {
            ('single_database', 'master_slave'): 'low',
            ('single_database', 'active_active'): 'high',
            ('single_database', 'federated'): 'medium',
            ('master_slave', 'active_active'): 'medium',
            ('master_slave', 'federated'): 'high',
            ('active_active', 'federated'): 'very_high'
        }
        
        return complexity_matrix.get((source, target), 'unknown')
    
    def _recommend_migration_strategy(self, complexity: str, constraints: Dict) -> str:
        """Recommend migration strategy based on complexity and constraints"""
        
        downtime_tolerance = constraints.get('downtime_tolerance', 'low')
        data_volume = constraints.get('data_volume', 'medium')
        
        if complexity == 'low' and downtime_tolerance == 'high':
            return 'blue_green'
        elif complexity in ['medium', 'high'] and downtime_tolerance == 'low':
            return 'shadow_write'
        elif data_volume == 'large':
            return 'gradual_cutover'
        else:
            return 'rolling'
    
    def _estimate_timeline(self, complexity: str) -> Dict[str, str]:
        """Estimate migration timeline"""
        
        timelines = {
            'low': {'planning': '1-2 weeks', 'execution': '1 day', 'total': '2-3 weeks'},
            'medium': {'planning': '2-4 weeks', 'execution': '1 week', 'total': '1-2 months'},
            'high': {'planning': '1-2 months', 'execution': '2-4 weeks', 'total': '2-4 months'},
            'very_high': {'planning': '2-3 months', 'execution': '1-2 months', 'total': '4-6 months'}
        }
        
        return timelines.get(complexity, timelines['medium'])
    
    def _identify_risk_factors(self, source: str, target: str) -> List[str]:
        """Identify risk factors for migration"""
        
        common_risks = [
            "Data consistency during migration",
            "Application compatibility with new architecture",
            "Performance degradation during transition"
        ]
        
        if target == 'active_active':
            common_risks.extend([
                "Conflict resolution complexity",
                "Vector clock implementation challenges",
                "Eventual consistency handling"
            ])
        
        if target == 'federated':
            common_risks.extend([
                "Query performance across heterogeneous sources",
                "Schema mapping complexity",
                "Cross-source transaction handling"
            ])
        
        return common_risks
    
    def _create_rollback_plan(self, source: str, target: str) -> Dict[str, Any]:
        """Create rollback plan for migration"""
        
        return {
            'rollback_triggers': [
                "Performance degradation > 50%",
                "Data loss detected",
                "Application errors > 5%",
                "Migration timeline exceeded by 100%"
            ],
            'rollback_steps': [
                "Stop writes to new architecture",
                "Redirect traffic to original architecture",
                "Sync any missing data",
                "Verify data integrity",
                "Resume normal operations"
            ],
            'rollback_time_estimate': "1-4 hours",
            'data_protection_measures': [
                "Continuous backup during migration",
                "Point-in-time recovery capability",
                "Change data capture for rollback"
            ]
        }

class ShadowWriteMigration:
    """Shadow write migration strategy implementation"""
    
    def __init__(self):
        self.shadow_write_active = False
        self.consistency_checker = DataConsistencyChecker()
    
    async def start_shadow_writes(self, source_db, target_db):
        """Start writing to both old and new architectures"""
        
        self.shadow_write_active = True
        print("Starting shadow writes to target architecture")
        
        # Implement dual-write logic
        # All writes go to both source and target
        
    async def verify_data_consistency(self, source_db, target_db) -> bool:
        """Verify data consistency between source and target"""
        
        return await self.consistency_checker.compare_databases(source_db, target_db)
    
    async def cutover_reads(self, percentage: float):
        """Gradually cut over read traffic"""
        
        print(f"Cutting over {percentage}% of read traffic to target architecture")
        
        # Implement gradual read traffic migration
        
    async def complete_migration(self):
        """Complete migration and stop shadow writes"""
        
        self.shadow_write_active = False
        print("Migration completed, stopping shadow writes")

class DataConsistencyChecker:
    """Check data consistency between different database architectures"""
    
    async def compare_databases(self, db1, db2) -> bool:
        """Compare data between two database instances"""
        
        # Implementation would depend on specific databases
        # This is a simplified example
        
        tables = await self._get_common_tables(db1, db2)
        
        for table in tables:
            if not await self._compare_table_data(db1, db2, table):
                print(f"Data inconsistency found in table: {table}")
                return False
        
        return True
    
    async def _get_common_tables(self, db1, db2) -> List[str]:
        """Get list of common tables between databases"""
        
        # Mock implementation
        return ["users", "orders", "products"]
    
    async def _compare_table_data(self, db1, db2, table: str) -> bool:
        """Compare data in specific table"""
        
        # Mock implementation - would use checksums, row counts, sampling
        print(f"Comparing table {table} between databases")
        return True

# Example migration planning
def migration_example():
    planner = ArchitectureMigrationPlanner()
    
    # Plan migration from single database to master-slave
    migration_plan = planner.plan_migration(
        source_arch='single_database',
        target_arch='master_slave',
        constraints={
            'downtime_tolerance': 'low',
            'data_volume': 'large',
            'performance_requirements': 'high'
        }
    )
    
    print(f"Migration plan: {migration_plan}")
```

## Best Practices and Considerations

### Performance Optimization

1. **Connection Pooling**: Use connection pools to manage database connections efficiently
2. **Query Optimization**: Implement proper indexing and query optimization
3. **Caching Strategies**: Use application-level and database-level caching
4. **Load Balancing**: Distribute queries efficiently across available nodes

### High Availability

1. **Health Monitoring**: Implement comprehensive health checks
2. **Automatic Failover**: Design automatic failover mechanisms
3. **Backup Strategies**: Ensure proper backup and recovery procedures
4. **Geographic Distribution**: Consider cross-region deployment for disaster recovery

### Data Consistency

1. **Transaction Design**: Design transactions to work with chosen consistency model
2. **Conflict Resolution**: Implement robust conflict resolution for multi-master setups
3. **Monitoring**: Monitor data consistency across nodes
4. **Testing**: Test consistency under various failure scenarios

### Operational Excellence

1. **Monitoring and Alerting**: Comprehensive monitoring of all database nodes
2. **Capacity Planning**: Plan for growth and scaling requirements
3. **Security**: Implement proper authentication, authorization, and encryption
4. **Documentation**: Maintain detailed operational procedures and runbooks

## Conclusion

Database architecture selection is a critical decision that impacts scalability, availability, consistency, and operational complexity. Key considerations include:

### Architecture Selection Criteria
- **Data Volume and Growth**: Choose architectures that can handle current and projected data volumes
- **Read/Write Patterns**: Match architecture to application access patterns
- **Consistency Requirements**: Balance consistency needs with availability and performance
- **Operational Capabilities**: Consider team expertise and operational overhead

### Implementation Guidelines
- **Start Simple**: Begin with simpler architectures and evolve as requirements grow
- **Plan for Growth**: Design migration paths for future scaling needs
- **Monitor Everything**: Implement comprehensive monitoring from day one
- **Test Thoroughly**: Test failure scenarios and recovery procedures

### Success Factors
- **Clear Requirements**: Understand business and technical requirements
- **Gradual Migration**: Use incremental migration strategies to reduce risk
- **Operational Readiness**: Ensure team is prepared for operational complexity
- **Continuous Improvement**: Regularly review and optimize architecture decisions

Each database architecture pattern serves specific use cases and comes with trade-offs. Success depends on matching the right architecture to your specific requirements, implementing it correctly, and maintaining operational excellence throughout the system's lifecycle.