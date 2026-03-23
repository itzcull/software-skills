---
title: "Database Sharding: Horizontal Scaling Strategy"
description: "Comprehensive guide to database sharding including strategies, implementation approaches, challenges, and best practices"
category: "Building Blocks"
tags: ["database-sharding", "horizontal-scaling", "distributed-systems", "partitioning", "performance"]
difficulty: "advanced"
last_updated: "2025-07-27"
---

# Database Sharding: Horizontal Scaling Strategy

Database sharding is a horizontal scaling technique that splits a large database into smaller, independent pieces called "shards" distributed across multiple servers. Each shard handles a specific subset of data, enabling systems to scale beyond the limitations of a single database server.

## What is Database Sharding?

Sharding is a database architecture pattern that involves partitioning data across multiple database instances (shards) so that each shard contains a subset of the total data. Unlike vertical scaling (adding more power to a single server), sharding allows horizontal scaling by distributing the load across multiple servers.

### Sharding vs. Partitioning

```
Traditional Partitioning (Single Server):
┌─────────────────────────────────────┐
│           Database Server           │
├─────────────────────────────────────┤
│ Partition 1 │ Partition 2 │ Part 3 │
│ Users A-H   │ Users I-P   │ Users Q-Z│
└─────────────────────────────────────┘

Sharding (Multiple Servers):
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Shard 1   │  │   Shard 2   │  │   Shard 3   │
│ Users A-H   │  │ Users I-P   │  │ Users Q-Z   │
│ Server 1    │  │ Server 2    │  │ Server 3    │
└─────────────┘  └─────────────┘  └─────────────┘
```

## Core Components of Sharding

### 1. Shard Key

The shard key determines how data is distributed across shards. It's crucial for balanced distribution and query performance.

```python
import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ShardKeyType(Enum):
    HASH_BASED = "hash_based"
    RANGE_BASED = "range_based"
    DIRECTORY_BASED = "directory_based"
    GEOGRAPHIC = "geographic"

@dataclass
class ShardConfig:
    shard_id: str
    connection_string: str
    weight: float = 1.0
    is_active: bool = True
    min_range: Optional[Any] = None
    max_range: Optional[Any] = None

class ShardKeyManager:
    def __init__(self, shard_key_type: ShardKeyType, shards: List[ShardConfig]):
        self.shard_key_type = shard_key_type
        self.shards = {shard.shard_id: shard for shard in shards}
        self.total_weight = sum(shard.weight for shard in shards if shard.is_active)
        
    def get_shard_for_key(self, shard_key: Any) -> str:
        """Determine which shard should handle the given key"""
        
        if self.shard_key_type == ShardKeyType.HASH_BASED:
            return self._hash_based_sharding(shard_key)
        elif self.shard_key_type == ShardKeyType.RANGE_BASED:
            return self._range_based_sharding(shard_key)
        elif self.shard_key_type == ShardKeyType.DIRECTORY_BASED:
            return self._directory_based_sharding(shard_key)
        elif self.shard_key_type == ShardKeyType.GEOGRAPHIC:
            return self._geographic_sharding(shard_key)
        else:
            raise ValueError(f"Unknown shard key type: {self.shard_key_type}")
    
    def _hash_based_sharding(self, shard_key: Any) -> str:
        """Hash-based sharding for even distribution"""
        
        # Convert key to string and hash
        key_str = str(shard_key)
        hash_value = int(hashlib.md5(key_str.encode()).hexdigest(), 16)
        
        # Use consistent hashing with weights
        active_shards = [shard for shard in self.shards.values() if shard.is_active]
        
        if not active_shards:
            raise Exception("No active shards available")
        
        # Calculate weighted hash ranges
        range_size = 2**32 / self.total_weight
        current_position = 0
        
        for shard in active_shards:
            shard_range = range_size * shard.weight
            if hash_value % (2**32) < current_position + shard_range:
                return shard.shard_id
            current_position += shard_range
        
        # Fallback to first shard
        return active_shards[0].shard_id
    
    def _range_based_sharding(self, shard_key: Any) -> str:
        """Range-based sharding based on key value ranges"""
        
        for shard in self.shards.values():
            if not shard.is_active:
                continue
                
            if (shard.min_range is not None and shard_key < shard.min_range):
                continue
            if (shard.max_range is not None and shard_key >= shard.max_range):
                continue
                
            return shard.shard_id
        
        raise ValueError(f"No shard found for key {shard_key}")
    
    def _directory_based_sharding(self, shard_key: Any) -> str:
        """Directory-based sharding using lookup table"""
        
        # This would typically query a directory service
        # For demonstration, we'll use a simple mapping
        
        directory_mapping = {
            'premium_users': 'shard_premium',
            'standard_users': 'shard_standard',
            'trial_users': 'shard_trial'
        }
        
        # Extract category from shard key (implementation-specific)
        if isinstance(shard_key, dict) and 'user_category' in shard_key:
            category = shard_key['user_category']
            shard_id = directory_mapping.get(category, 'shard_standard')
            
            if shard_id in self.shards and self.shards[shard_id].is_active:
                return shard_id
        
        # Fallback to first active shard
        active_shards = [s for s in self.shards.values() if s.is_active]
        return active_shards[0].shard_id if active_shards else list(self.shards.keys())[0]
    
    def _geographic_sharding(self, shard_key: Any) -> str:
        """Geographic-based sharding"""
        
        geographic_mapping = {
            'US': 'shard_us',
            'EU': 'shard_eu',
            'ASIA': 'shard_asia'
        }
        
        # Extract region from shard key
        if isinstance(shard_key, dict) and 'region' in shard_key:
            region = shard_key['region']
            shard_id = geographic_mapping.get(region, 'shard_us')
            
            if shard_id in self.shards and self.shards[shard_id].is_active:
                return shard_id
        
        # Fallback
        active_shards = [s for s in self.shards.values() if s.is_active]
        return active_shards[0].shard_id if active_shards else list(self.shards.keys())[0]

# Example usage
def setup_shard_key_manager():
    # Hash-based sharding setup
    shards = [
        ShardConfig("shard_1", "postgresql://db1:5432/shard1", weight=1.0),
        ShardConfig("shard_2", "postgresql://db2:5432/shard2", weight=1.5),
        ShardConfig("shard_3", "postgresql://db3:5432/shard3", weight=1.0),
    ]
    
    hash_manager = ShardKeyManager(ShardKeyType.HASH_BASED, shards)
    
    # Range-based sharding setup
    range_shards = [
        ShardConfig("shard_1", "postgresql://db1:5432/shard1", min_range=0, max_range=1000),
        ShardConfig("shard_2", "postgresql://db2:5432/shard2", min_range=1000, max_range=2000),
        ShardConfig("shard_3", "postgresql://db3:5432/shard3", min_range=2000, max_range=None),
    ]
    
    range_manager = ShardKeyManager(ShardKeyType.RANGE_BASED, range_shards)
    
    return hash_manager, range_manager
```

### 2. Shard Router

The shard router directs queries to the appropriate shard(s) based on the shard key.

```python
import asyncio
from typing import Dict, List, Any, Optional, Union
import asyncpg

class QueryType(Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

class ShardRouter:
    def __init__(self, shard_key_manager: ShardKeyManager):
        self.shard_key_manager = shard_key_manager
        self.connections: Dict[str, asyncpg.Pool] = {}
        self.query_cache = {}
        
    async def initialize_connections(self):
        """Initialize connection pools for all shards"""
        
        for shard_id, shard_config in self.shard_key_manager.shards.items():
            if shard_config.is_active:
                try:
                    pool = await asyncpg.create_pool(
                        shard_config.connection_string,
                        min_size=5,
                        max_size=20
                    )
                    self.connections[shard_id] = pool
                    print(f"Connected to shard {shard_id}")
                except Exception as e:
                    print(f"Failed to connect to shard {shard_id}: {e}")
    
    async def execute_query(self, query: str, params: tuple = (), 
                          shard_key: Any = None, 
                          query_type: QueryType = QueryType.SELECT) -> Any:
        """Execute query on appropriate shard(s)"""
        
        if shard_key is not None:
            # Single shard query
            shard_id = self.shard_key_manager.get_shard_for_key(shard_key)
            return await self._execute_on_shard(shard_id, query, params, query_type)
        else:
            # Cross-shard query - execute on all shards
            return await self._execute_cross_shard_query(query, params, query_type)
    
    async def _execute_on_shard(self, shard_id: str, query: str, 
                              params: tuple, query_type: QueryType) -> Any:
        """Execute query on specific shard"""
        
        if shard_id not in self.connections:
            raise Exception(f"No connection to shard {shard_id}")
        
        pool = self.connections[shard_id]
        
        async with pool.acquire() as connection:
            if query_type == QueryType.SELECT:
                return await connection.fetch(query, *params)
            else:
                return await connection.execute(query, *params)
    
    async def _execute_cross_shard_query(self, query: str, params: tuple, 
                                       query_type: QueryType) -> Any:
        """Execute query across all active shards"""
        
        if query_type != QueryType.SELECT:
            raise Exception("Cross-shard queries only supported for SELECT")
        
        # Execute on all shards in parallel
        tasks = []
        for shard_id in self.connections.keys():
            task = asyncio.create_task(
                self._execute_on_shard(shard_id, query, params, query_type)
            )
            tasks.append((shard_id, task))
        
        # Collect results
        all_results = []
        for shard_id, task in tasks:
            try:
                result = await task
                # Add shard information to each row
                for row in result:
                    row_dict = dict(row)
                    row_dict['_shard_id'] = shard_id
                    all_results.append(row_dict)
            except Exception as e:
                print(f"Query failed on shard {shard_id}: {e}")
        
        return all_results
    
    async def insert_record(self, table: str, data: Dict[str, Any], 
                          shard_key_field: str) -> bool:
        """Insert record into appropriate shard"""
        
        shard_key = data[shard_key_field]
        shard_id = self.shard_key_manager.get_shard_for_key(shard_key)
        
        # Build INSERT query
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join(['$' + str(i+1) for i in range(len(values))])
        
        query = f"""
        INSERT INTO {table} ({', '.join(columns)})
        VALUES ({placeholders})
        """
        
        try:
            await self._execute_on_shard(shard_id, query, tuple(values), QueryType.INSERT)
            return True
        except Exception as e:
            print(f"Insert failed: {e}")
            return False
    
    async def update_record(self, table: str, data: Dict[str, Any], 
                          conditions: Dict[str, Any], 
                          shard_key_field: str) -> int:
        """Update record in appropriate shard"""
        
        # Determine shard from conditions or data
        shard_key = conditions.get(shard_key_field) or data.get(shard_key_field)
        
        if not shard_key:
            raise ValueError(f"Shard key {shard_key_field} not found in update conditions or data")
        
        shard_id = self.shard_key_manager.get_shard_for_key(shard_key)
        
        # Build UPDATE query
        set_clauses = [f"{col} = ${i+1}" for i, col in enumerate(data.keys())]
        where_clauses = [f"{col} = ${len(data)+i+1}" for i, col in enumerate(conditions.keys())]
        
        query = f"""
        UPDATE {table}
        SET {', '.join(set_clauses)}
        WHERE {' AND '.join(where_clauses)}
        """
        
        params = tuple(list(data.values()) + list(conditions.values()))
        
        try:
            result = await self._execute_on_shard(shard_id, query, params, QueryType.UPDATE)
            # Parse result to get affected row count
            return int(result.split()[-1]) if result else 0
        except Exception as e:
            print(f"Update failed: {e}")
            return 0
    
    async def delete_record(self, table: str, conditions: Dict[str, Any], 
                          shard_key_field: str) -> int:
        """Delete record from appropriate shard"""
        
        shard_key = conditions.get(shard_key_field)
        
        if not shard_key:
            raise ValueError(f"Shard key {shard_key_field} not found in delete conditions")
        
        shard_id = self.shard_key_manager.get_shard_for_key(shard_key)
        
        # Build DELETE query
        where_clauses = [f"{col} = ${i+1}" for i, col in enumerate(conditions.keys())]
        
        query = f"""
        DELETE FROM {table}
        WHERE {' AND '.join(where_clauses)}
        """
        
        params = tuple(conditions.values())
        
        try:
            result = await self._execute_on_shard(shard_id, query, params, QueryType.DELETE)
            return int(result.split()[-1]) if result else 0
        except Exception as e:
            print(f"Delete failed: {e}")
            return 0
    
    async def get_shard_statistics(self) -> Dict[str, Dict]:
        """Get statistics from all shards"""
        
        stats = {}
        
        for shard_id in self.connections.keys():
            try:
                # Get basic table statistics
                query = """
                SELECT 
                    schemaname,
                    tablename,
                    n_tup_ins as inserts,
                    n_tup_upd as updates,
                    n_tup_del as deletes,
                    n_live_tup as live_tuples,
                    n_dead_tup as dead_tuples
                FROM pg_stat_user_tables
                ORDER BY n_live_tup DESC
                """
                
                result = await self._execute_on_shard(shard_id, query, (), QueryType.SELECT)
                
                stats[shard_id] = {
                    'tables': [dict(row) for row in result],
                    'total_tuples': sum(row['live_tuples'] for row in result),
                    'connection_status': 'active'
                }
                
            except Exception as e:
                stats[shard_id] = {
                    'error': str(e),
                    'connection_status': 'error'
                }
        
        return stats

# Example usage
async def demonstrate_shard_router():
    # Setup shard key manager
    shards = [
        ShardConfig("shard_1", "postgresql://localhost:5432/shard1"),
        ShardConfig("shard_2", "postgresql://localhost:5432/shard2"),
        ShardConfig("shard_3", "postgresql://localhost:5432/shard3"),
    ]
    
    shard_manager = ShardKeyManager(ShardKeyType.HASH_BASED, shards)
    router = ShardRouter(shard_manager)
    
    # Initialize connections
    await router.initialize_connections()
    
    # Insert user
    user_data = {
        'user_id': '12345',
        'name': 'John Doe',
        'email': 'john@example.com',
        'created_at': '2023-07-27'
    }
    
    success = await router.insert_record('users', user_data, 'user_id')
    print(f"Insert success: {success}")
    
    # Query user (single shard)
    query = "SELECT * FROM users WHERE user_id = $1"
    result = await router.execute_query(query, ('12345',), shard_key='12345')
    print(f"Query result: {result}")
    
    # Cross-shard query
    all_users = await router.execute_query("SELECT user_id, name FROM users LIMIT 10")
    print(f"All users across shards: {len(all_users)}")
    
    # Get shard statistics
    stats = await router.get_shard_statistics()
    print(f"Shard statistics: {stats}")
```

### 3. Cross-Shard Query Coordination

```python
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
import asyncio

@dataclass
class QueryPlan:
    query_id: str
    original_query: str
    shard_queries: Dict[str, str]  # shard_id -> query
    aggregation_function: Optional[Callable] = None
    requires_sorting: bool = False
    sort_column: Optional[str] = None
    limit: Optional[int] = None

class CrossShardQueryCoordinator:
    def __init__(self, shard_router: ShardRouter):
        self.shard_router = shard_router
        self.query_planner = QueryPlanner()
    
    async def execute_distributed_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute distributed query across shards"""
        
        # Parse and plan the query
        query_plan = self.query_planner.create_query_plan(query, params)
        
        # Execute on relevant shards
        shard_results = await self._execute_shard_queries(query_plan)
        
        # Merge and process results
        final_result = await self._merge_shard_results(query_plan, shard_results)
        
        return final_result
    
    async def _execute_shard_queries(self, query_plan: QueryPlan) -> Dict[str, List[Dict]]:
        """Execute queries on shards in parallel"""
        
        tasks = []
        
        for shard_id, shard_query in query_plan.shard_queries.items():
            task = asyncio.create_task(
                self._execute_shard_query(shard_id, shard_query)
            )
            tasks.append((shard_id, task))
        
        results = {}
        
        for shard_id, task in tasks:
            try:
                result = await task
                results[shard_id] = result
            except Exception as e:
                print(f"Query failed on shard {shard_id}: {e}")
                results[shard_id] = []
        
        return results
    
    async def _execute_shard_query(self, shard_id: str, query: str) -> List[Dict]:
        """Execute query on specific shard"""
        
        result = await self.shard_router._execute_on_shard(
            shard_id, query, (), QueryType.SELECT
        )
        
        return [dict(row) for row in result]
    
    async def _merge_shard_results(self, query_plan: QueryPlan, 
                                 shard_results: Dict[str, List[Dict]]) -> List[Dict]:
        """Merge results from multiple shards"""
        
        # Combine all results
        all_results = []
        for shard_id, results in shard_results.items():
            for row in results:
                row['_shard_id'] = shard_id
                all_results.append(row)
        
        # Apply aggregation if needed
        if query_plan.aggregation_function:
            all_results = query_plan.aggregation_function(all_results)
        
        # Apply sorting if needed
        if query_plan.requires_sorting and query_plan.sort_column:
            all_results.sort(key=lambda x: x.get(query_plan.sort_column, 0))
        
        # Apply limit if needed
        if query_plan.limit:
            all_results = all_results[:query_plan.limit]
        
        return all_results

class QueryPlanner:
    def __init__(self):
        self.supported_patterns = {
            'COUNT': self._plan_count_query,
            'SUM': self._plan_sum_query,
            'AVG': self._plan_avg_query,
            'ORDER BY': self._plan_ordered_query,
            'GROUP BY': self._plan_group_by_query
        }
    
    def create_query_plan(self, query: str, params: tuple) -> QueryPlan:
        """Create execution plan for distributed query"""
        
        query_upper = query.upper()
        query_id = f"query_{hash(query)}_{int(time.time())}"
        
        # Determine query type and create appropriate plan
        if 'COUNT(' in query_upper:
            return self._plan_count_query(query_id, query, params)
        elif 'SUM(' in query_upper:
            return self._plan_sum_query(query_id, query, params)
        elif 'AVG(' in query_upper:
            return self._plan_avg_query(query_id, query, params)
        elif 'ORDER BY' in query_upper:
            return self._plan_ordered_query(query_id, query, params)
        elif 'GROUP BY' in query_upper:
            return self._plan_group_by_query(query_id, query, params)
        else:
            return self._plan_simple_query(query_id, query, params)
    
    def _plan_count_query(self, query_id: str, query: str, params: tuple) -> QueryPlan:
        """Plan COUNT aggregation query"""
        
        # Extract table name and conditions
        # This is a simplified parser - production would use proper SQL parsing
        
        def sum_counts(results: List[Dict]) -> List[Dict]:
            total_count = sum(row.get('count', 0) for row in results)
            return [{'count': total_count}]
        
        return QueryPlan(
            query_id=query_id,
            original_query=query,
            shard_queries={'all': query},  # Execute on all shards
            aggregation_function=sum_counts
        )
    
    def _plan_sum_query(self, query_id: str, query: str, params: tuple) -> QueryPlan:
        """Plan SUM aggregation query"""
        
        def sum_values(results: List[Dict]) -> List[Dict]:
            # Find the SUM column (simplified)
            sum_column = None
            for row in results:
                for key in row.keys():
                    if 'sum' in key.lower():
                        sum_column = key
                        break
                if sum_column:
                    break
            
            if sum_column:
                total_sum = sum(row.get(sum_column, 0) for row in results)
                return [{sum_column: total_sum}]
            
            return results
        
        return QueryPlan(
            query_id=query_id,
            original_query=query,
            shard_queries={'all': query},
            aggregation_function=sum_values
        )
    
    def _plan_avg_query(self, query_id: str, query: str, params: tuple) -> QueryPlan:
        """Plan AVG aggregation query"""
        
        # Convert AVG to SUM and COUNT for proper distribution
        modified_query = query.replace('AVG(', 'SUM(').replace(')', '), COUNT(*)')
        
        def calculate_average(results: List[Dict]) -> List[Dict]:
            total_sum = 0
            total_count = 0
            
            for row in results:
                for key, value in row.items():
                    if 'sum' in key.lower():
                        total_sum += value or 0
                    elif 'count' in key.lower():
                        total_count += value or 0
            
            avg = total_sum / total_count if total_count > 0 else 0
            return [{'avg': avg}]
        
        return QueryPlan(
            query_id=query_id,
            original_query=query,
            shard_queries={'all': modified_query},
            aggregation_function=calculate_average
        )
    
    def _plan_ordered_query(self, query_id: str, query: str, params: tuple) -> QueryPlan:
        """Plan query with ORDER BY clause"""
        
        # Extract sort column and direction
        order_by_index = query.upper().find('ORDER BY')
        if order_by_index != -1:
            order_clause = query[order_by_index:].split()[2]  # Get column name
            sort_column = order_clause.replace(',', '').strip()
        else:
            sort_column = None
        
        return QueryPlan(
            query_id=query_id,
            original_query=query,
            shard_queries={'all': query},
            requires_sorting=True,
            sort_column=sort_column
        )
    
    def _plan_group_by_query(self, query_id: str, query: str, params: tuple) -> QueryPlan:
        """Plan GROUP BY query"""
        
        def merge_groups(results: List[Dict]) -> List[Dict]:
            # Group results by the GROUP BY column
            groups = {}
            
            for row in results:
                # Find group key (simplified)
                group_key = None
                for key, value in row.items():
                    if not key.startswith('_') and not any(agg in key.lower() 
                                                          for agg in ['count', 'sum', 'avg']):
                        group_key = value
                        break
                
                if group_key not in groups:
                    groups[group_key] = []
                groups[group_key].append(row)
            
            # Aggregate each group
            result = []
            for group_key, group_rows in groups.items():
                merged_row = {'group_key': group_key}
                
                # Sum numeric columns
                for key in group_rows[0].keys():
                    if any(agg in key.lower() for agg in ['count', 'sum']):
                        merged_row[key] = sum(row.get(key, 0) for row in group_rows)
                
                result.append(merged_row)
            
            return result
        
        return QueryPlan(
            query_id=query_id,
            original_query=query,
            shard_queries={'all': query},
            aggregation_function=merge_groups
        )
    
    def _plan_simple_query(self, query_id: str, query: str, params: tuple) -> QueryPlan:
        """Plan simple query without aggregation"""
        
        return QueryPlan(
            query_id=query_id,
            original_query=query,
            shard_queries={'all': query}
        )

# Example usage
async def demonstrate_cross_shard_queries():
    # Setup (assuming shard_router is already configured)
    coordinator = CrossShardQueryCoordinator(shard_router)
    
    # Execute distributed COUNT query
    count_result = await coordinator.execute_distributed_query(
        "SELECT COUNT(*) FROM users WHERE status = 'active'"
    )
    print(f"Total active users across all shards: {count_result}")
    
    # Execute distributed SUM query
    sum_result = await coordinator.execute_distributed_query(
        "SELECT SUM(order_amount) FROM orders WHERE order_date >= '2023-01-01'"
    )
    print(f"Total order amount: {sum_result}")
    
    # Execute distributed query with ORDER BY
    top_users = await coordinator.execute_distributed_query(
        "SELECT user_id, total_spent FROM user_stats ORDER BY total_spent DESC LIMIT 10"
    )
    print(f"Top 10 users by spending: {top_users}")
```

## Sharding Strategies

### 1. Hash-Based Sharding

Best for even distribution and simple implementation.

```python
class HashBasedSharding:
    def __init__(self, num_shards: int):
        self.num_shards = num_shards
        self.shard_ring = self._create_consistent_hash_ring()
    
    def _create_consistent_hash_ring(self) -> Dict[int, str]:
        """Create consistent hash ring for better distribution"""
        
        virtual_nodes_per_shard = 150  # Number of virtual nodes per physical shard
        ring = {}
        
        for shard_id in range(self.num_shards):
            for virtual_node in range(virtual_nodes_per_shard):
                # Create virtual node identifier
                virtual_node_key = f"shard_{shard_id}_vnode_{virtual_node}"
                
                # Hash the virtual node key
                hash_value = int(hashlib.md5(virtual_node_key.encode()).hexdigest(), 16)
                
                # Add to ring
                ring[hash_value] = f"shard_{shard_id}"
        
        return ring
    
    def get_shard(self, key: str) -> str:
        """Get shard for key using consistent hashing"""
        
        # Hash the key
        key_hash = int(hashlib.md5(key.encode()).hexdigest(), 16)
        
        # Find the first node in the ring that is >= key_hash
        sorted_hashes = sorted(self.shard_ring.keys())
        
        for ring_hash in sorted_hashes:
            if ring_hash >= key_hash:
                return self.shard_ring[ring_hash]
        
        # Wrap around to the first node
        return self.shard_ring[sorted_hashes[0]]
    
    def add_shard(self, new_shard_count: int):
        """Add new shards and rebalance"""
        
        old_ring = self.shard_ring.copy()
        self.num_shards = new_shard_count
        self.shard_ring = self._create_consistent_hash_ring()
        
        # Calculate data migration needed
        migration_plan = self._calculate_migration_plan(old_ring, self.shard_ring)
        return migration_plan
    
    def _calculate_migration_plan(self, old_ring: Dict, new_ring: Dict) -> Dict:
        """Calculate what data needs to be migrated"""
        
        migration_plan = {}
        
        # For each hash position, check if shard assignment changed
        all_hashes = set(old_ring.keys()) | set(new_ring.keys())
        
        for hash_value in all_hashes:
            old_shard = old_ring.get(hash_value)
            new_shard = new_ring.get(hash_value)
            
            if old_shard != new_shard:
                if old_shard not in migration_plan:
                    migration_plan[old_shard] = {}
                
                if new_shard not in migration_plan[old_shard]:
                    migration_plan[old_shard][new_shard] = []
                
                migration_plan[old_shard][new_shard].append(hash_value)
        
        return migration_plan

# Example: Implementing user sharding
class UserShardingService:
    def __init__(self, num_shards: int):
        self.hash_sharding = HashBasedSharding(num_shards)
        
    async def create_user(self, user_data: Dict) -> str:
        """Create user in appropriate shard"""
        
        user_id = user_data['user_id']
        shard = self.hash_sharding.get_shard(user_id)
        
        # Route to appropriate shard
        # Implementation would use actual database connections
        print(f"Creating user {user_id} in {shard}")
        
        return user_id
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user from appropriate shard"""
        
        shard = self.hash_sharding.get_shard(user_id)
        
        # Query specific shard
        print(f"Querying user {user_id} from {shard}")
        
        # Return mock user data
        return {'user_id': user_id, 'shard': shard}
    
    async def scale_out(self, new_shard_count: int):
        """Scale out by adding new shards"""
        
        migration_plan = self.hash_sharding.add_shard(new_shard_count)
        
        # Execute migration
        await self._execute_migration(migration_plan)
    
    async def _execute_migration(self, migration_plan: Dict):
        """Execute data migration between shards"""
        
        for source_shard, destinations in migration_plan.items():
            for dest_shard, hash_ranges in destinations.items():
                print(f"Migrating data from {source_shard} to {dest_shard}")
                
                # In production, this would:
                # 1. Lock the data being migrated
                # 2. Copy data to destination shard
                # 3. Verify data integrity
                # 4. Update routing table
                # 5. Delete data from source shard
```

### 2. Range-Based Sharding

Best for range queries but can create hotspots.

```python
class RangeBasedSharding:
    def __init__(self, range_boundaries: List[Any]):
        self.range_boundaries = sorted(range_boundaries)
        self.shard_stats = {}
        
    def get_shard(self, key: Any) -> str:
        """Get shard based on key range"""
        
        for i, boundary in enumerate(self.range_boundaries):
            if key < boundary:
                return f"shard_{i}"
        
        # Last shard for keys >= last boundary
        return f"shard_{len(self.range_boundaries)}"
    
    def get_shards_for_range(self, start_key: Any, end_key: Any) -> List[str]:
        """Get all shards that might contain keys in the given range"""
        
        shards = set()
        
        # Find all boundaries within the range
        for i, boundary in enumerate(self.range_boundaries):
            if start_key <= boundary <= end_key:
                shards.add(f"shard_{i}")
                shards.add(f"shard_{i+1}")
        
        # Add shards for start and end keys
        shards.add(self.get_shard(start_key))
        shards.add(self.get_shard(end_key))
        
        return sorted(list(shards))
    
    async def optimize_ranges(self, shard_stats: Dict[str, Dict]):
        """Optimize range boundaries based on data distribution"""
        
        # Analyze shard load and data distribution
        load_imbalance = self._calculate_load_imbalance(shard_stats)
        
        if load_imbalance > 0.3:  # 30% imbalance threshold
            new_boundaries = self._calculate_optimal_boundaries(shard_stats)
            migration_plan = self._plan_range_migration(self.range_boundaries, new_boundaries)
            
            return migration_plan
        
        return None
    
    def _calculate_load_imbalance(self, shard_stats: Dict[str, Dict]) -> float:
        """Calculate load imbalance across shards"""
        
        loads = [stats.get('row_count', 0) for stats in shard_stats.values()]
        
        if not loads:
            return 0.0
        
        avg_load = sum(loads) / len(loads)
        max_deviation = max(abs(load - avg_load) for load in loads)
        
        return max_deviation / avg_load if avg_load > 0 else 0.0
    
    def _calculate_optimal_boundaries(self, shard_stats: Dict[str, Dict]) -> List[Any]:
        """Calculate optimal range boundaries for balanced load"""
        
        # This is a simplified version
        # Production implementation would use more sophisticated algorithms
        
        total_rows = sum(stats.get('row_count', 0) for stats in shard_stats.values())
        target_rows_per_shard = total_rows / len(shard_stats)
        
        # Calculate new boundaries to achieve target distribution
        # Implementation would analyze actual data distribution
        
        return self.range_boundaries  # Placeholder

# Example: Date-based sharding for time-series data
class TimeSeriesSharding:
    def __init__(self, start_date: str, shard_duration_days: int = 30):
        self.start_date = datetime.fromisoformat(start_date)
        self.shard_duration_days = shard_duration_days
        self.range_sharding = self._setup_date_ranges()
    
    def _setup_date_ranges(self) -> RangeBasedSharding:
        """Setup date-based range boundaries"""
        
        # Create monthly boundaries for 2 years
        boundaries = []
        current_date = self.start_date
        
        for _ in range(24):  # 24 months
            current_date += timedelta(days=self.shard_duration_days)
            boundaries.append(current_date.isoformat())
        
        return RangeBasedSharding(boundaries)
    
    def get_shard_for_date(self, date_str: str) -> str:
        """Get shard for specific date"""
        return self.range_sharding.get_shard(date_str)
    
    def get_shards_for_date_range(self, start_date: str, end_date: str) -> List[str]:
        """Get all shards for date range"""
        return self.range_sharding.get_shards_for_range(start_date, end_date)
    
    async def query_time_range(self, start_date: str, end_date: str, 
                             query_template: str) -> List[Dict]:
        """Query across time range shards"""
        
        relevant_shards = self.get_shards_for_date_range(start_date, end_date)
        
        # Execute query on relevant shards only
        results = []
        for shard in relevant_shards:
            query = query_template.format(
                start_date=start_date,
                end_date=end_date
            )
            
            # Execute on shard (mock implementation)
            shard_result = await self._execute_on_time_shard(shard, query)
            results.extend(shard_result)
        
        return results
    
    async def _execute_on_time_shard(self, shard: str, query: str) -> List[Dict]:
        """Execute query on time-based shard"""
        
        # Mock implementation
        print(f"Executing time-series query on {shard}: {query}")
        return [{'shard': shard, 'data': 'mock_time_series_data'}]
```

## Shard Management and Operations

### 1. Shard Rebalancing

```python
class ShardRebalancer:
    def __init__(self, shard_router: ShardRouter):
        self.shard_router = shard_router
        self.rebalancing_in_progress = False
        
    async def analyze_shard_balance(self) -> Dict[str, Any]:
        """Analyze current shard balance"""
        
        stats = await self.shard_router.get_shard_statistics()
        
        # Calculate balance metrics
        shard_loads = {}
        total_load = 0
        
        for shard_id, shard_stats in stats.items():
            if shard_stats.get('connection_status') == 'active':
                load = shard_stats.get('total_tuples', 0)
                shard_loads[shard_id] = load
                total_load += load
        
        if not shard_loads:
            return {'balanced': True, 'reason': 'No active shards'}
        
        avg_load = total_load / len(shard_loads)
        
        # Calculate imbalance
        imbalances = {}
        max_imbalance = 0
        
        for shard_id, load in shard_loads.items():
            imbalance = abs(load - avg_load) / avg_load if avg_load > 0 else 0
            imbalances[shard_id] = imbalance
            max_imbalance = max(max_imbalance, imbalance)
        
        is_balanced = max_imbalance < 0.2  # 20% threshold
        
        return {
            'balanced': is_balanced,
            'max_imbalance': max_imbalance,
            'shard_loads': shard_loads,
            'avg_load': avg_load,
            'imbalances': imbalances,
            'recommendations': self._generate_rebalancing_recommendations(imbalances, avg_load)
        }
    
    def _generate_rebalancing_recommendations(self, imbalances: Dict[str, float], 
                                           avg_load: float) -> List[Dict]:
        """Generate rebalancing recommendations"""
        
        recommendations = []
        
        # Find overloaded and underloaded shards
        overloaded = [(shard, imbalance) for shard, imbalance in imbalances.items() if imbalance > 0.2]
        underloaded = [(shard, imbalance) for shard, imbalance in imbalances.items() if imbalance < -0.1]
        
        for overloaded_shard, _ in overloaded:
            for underloaded_shard, _ in underloaded:
                recommendations.append({
                    'action': 'migrate_data',
                    'source_shard': overloaded_shard,
                    'target_shard': underloaded_shard,
                    'estimated_benefit': 'Improve load distribution'
                })
        
        if len(overloaded) > len(underloaded):
            recommendations.append({
                'action': 'add_shard',
                'reason': 'More overloaded shards than underloaded',
                'estimated_benefit': 'Distribute load across more shards'
            })
        
        return recommendations
    
    async def execute_rebalancing(self, rebalancing_plan: List[Dict]) -> bool:
        """Execute rebalancing plan"""
        
        if self.rebalancing_in_progress:
            return False
        
        self.rebalancing_in_progress = True
        
        try:
            for action in rebalancing_plan:
                if action['action'] == 'migrate_data':
                    await self._migrate_shard_data(
                        action['source_shard'],
                        action['target_shard']
                    )
                elif action['action'] == 'add_shard':
                    await self._add_new_shard()
            
            return True
            
        except Exception as e:
            print(f"Rebalancing failed: {e}")
            return False
        finally:
            self.rebalancing_in_progress = False
    
    async def _migrate_shard_data(self, source_shard: str, target_shard: str):
        """Migrate data between shards"""
        
        print(f"Starting data migration from {source_shard} to {target_shard}")
        
        # Step 1: Identify data to migrate
        # This would typically involve analyzing key ranges or hash ranges
        
        # Step 2: Set up replication stream
        # Replicate ongoing changes to both shards during migration
        
        # Step 3: Copy historical data
        # Copy existing data in batches
        
        # Step 4: Verify data integrity
        # Ensure all data was copied correctly
        
        # Step 5: Update routing table
        # Update shard routing to point to new locations
        
        # Step 6: Clean up source data
        # Remove migrated data from source shard
        
        print(f"Completed data migration from {source_shard} to {target_shard}")
    
    async def _add_new_shard(self):
        """Add new shard to the cluster"""
        
        print("Adding new shard to cluster")
        
        # Step 1: Provision new database instance
        # Set up new database server/container
        
        # Step 2: Configure replication
        # Set up replication from existing shards
        
        # Step 3: Update shard configuration
        # Add new shard to routing configuration
        
        # Step 4: Rebalance data
        # Migrate appropriate data to new shard
        
        print("New shard added successfully")

# Monitoring and alerting for shard health
class ShardMonitor:
    def __init__(self, shard_router: ShardRouter, rebalancer: ShardRebalancer):
        self.shard_router = shard_router
        self.rebalancer = rebalancer
        self.monitoring_interval = 300  # 5 minutes
        
    async def start_monitoring(self):
        """Start continuous shard monitoring"""
        
        while True:
            try:
                await self._check_shard_health()
                await asyncio.sleep(self.monitoring_interval)
            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _check_shard_health(self):
        """Check health of all shards"""
        
        # Check connection health
        stats = await self.shard_router.get_shard_statistics()
        
        failed_shards = []
        for shard_id, shard_stats in stats.items():
            if shard_stats.get('connection_status') != 'active':
                failed_shards.append(shard_id)
        
        if failed_shards:
            await self._handle_shard_failures(failed_shards)
        
        # Check load balance
        balance_analysis = await self.rebalancer.analyze_shard_balance()
        
        if not balance_analysis['balanced']:
            await self._handle_load_imbalance(balance_analysis)
    
    async def _handle_shard_failures(self, failed_shards: List[str]):
        """Handle shard failures"""
        
        for shard_id in failed_shards:
            print(f"ALERT: Shard {shard_id} is not responding")
            
            # Try to reconnect
            # Implement failover to replica
            # Alert operations team
    
    async def _handle_load_imbalance(self, balance_analysis: Dict):
        """Handle load imbalance"""
        
        if balance_analysis['max_imbalance'] > 0.5:  # 50% imbalance
            print("ALERT: Severe load imbalance detected")
            
            # Consider automatic rebalancing for severe imbalances
            recommendations = balance_analysis['recommendations']
            
            if any(rec['action'] == 'add_shard' for rec in recommendations):
                print("Recommendation: Add new shard to cluster")
```

## Best Practices and Common Pitfalls

### 1. Shard Key Selection

```python
class ShardKeyAnalyzer:
    def __init__(self):
        self.analysis_criteria = {
            'cardinality': 'High cardinality provides better distribution',
            'immutability': 'Shard key should not change frequently',
            'query_patterns': 'Should align with common query patterns',
            'hotspots': 'Should avoid creating hotspots'
        }
    
    def analyze_shard_key_candidates(self, table_schema: Dict, 
                                   query_patterns: List[str]) -> Dict[str, Dict]:
        """Analyze potential shard key candidates"""
        
        candidates = {}
        
        for column, column_info in table_schema.items():
            score = self._score_shard_key_candidate(column, column_info, query_patterns)
            candidates[column] = score
        
        return sorted(candidates.items(), key=lambda x: x[1]['total_score'], reverse=True)
    
    def _score_shard_key_candidate(self, column: str, column_info: Dict, 
                                 query_patterns: List[str]) -> Dict:
        """Score a shard key candidate"""
        
        score = {
            'cardinality_score': 0,
            'immutability_score': 0,
            'query_alignment_score': 0,
            'hotspot_risk_score': 0,
            'total_score': 0
        }
        
        # Cardinality score (higher is better)
        if column_info.get('unique_values', 0) > 1000:
            score['cardinality_score'] = 10
        elif column_info.get('unique_values', 0) > 100:
            score['cardinality_score'] = 7
        else:
            score['cardinality_score'] = 3
        
        # Immutability score
        if column_info.get('immutable', False):
            score['immutability_score'] = 10
        elif column_info.get('rarely_updated', False):
            score['immutability_score'] = 7
        else:
            score['immutability_score'] = 3
        
        # Query alignment score
        query_usage_count = sum(1 for pattern in query_patterns if column in pattern)
        score['query_alignment_score'] = min(query_usage_count * 2, 10)
        
        # Hotspot risk score (lower risk is better)
        if column_info.get('data_type') == 'timestamp':
            score['hotspot_risk_score'] = 3  # Time-based can create hotspots
        elif column_info.get('data_type') in ['uuid', 'hash']:
            score['hotspot_risk_score'] = 10  # Good distribution
        else:
            score['hotspot_risk_score'] = 7
        
        # Calculate total score
        score['total_score'] = sum(score.values()) - score['total_score']  # Exclude self
        
        return score

# Common anti-patterns and solutions
class ShardingAntiPatterns:
    @staticmethod
    def demonstrate_anti_patterns():
        """Demonstrate common sharding anti-patterns and solutions"""
        
        print("Anti-Pattern 1: Using auto-incrementing ID as shard key")
        print("Problem: Creates hotspots as new records go to same shard")
        print("Solution: Use UUID or hash of business key")
        print()
        
        print("Anti-Pattern 2: Cross-shard JOINs in application code")
        print("Problem: Expensive cross-shard operations")
        print("Solution: Denormalize data or redesign schema")
        print()
        
        print("Anti-Pattern 3: Ignoring shard rebalancing")
        print("Problem: Load imbalance over time")
        print("Solution: Implement automated monitoring and rebalancing")
        print()
        
        print("Anti-Pattern 4: No fallback for shard failures")
        print("Problem: Data unavailability during shard failures")
        print("Solution: Implement read replicas and failover mechanisms")

# Comprehensive sharding checklist
class ShardingReadinessChecker:
    def __init__(self):
        self.checklist = {
            'data_volume': 'Database size > 100GB or growth rate requires scaling',
            'query_performance': 'Single database cannot handle query load',
            'write_throughput': 'Write throughput exceeds single database capacity',
            'shard_key_identified': 'Appropriate shard key has been identified',
            'application_ready': 'Application can handle sharded queries',
            'monitoring_setup': 'Monitoring and alerting systems in place',
            'backup_strategy': 'Backup and recovery strategy for sharded data',
            'operational_expertise': 'Team has expertise to manage sharded system'
        }
    
    def assess_sharding_readiness(self, current_state: Dict[str, bool]) -> Dict:
        """Assess readiness for implementing sharding"""
        
        readiness_score = 0
        missing_requirements = []
        
        for requirement, description in self.checklist.items():
            if current_state.get(requirement, False):
                readiness_score += 1
            else:
                missing_requirements.append({
                    'requirement': requirement,
                    'description': description
                })
        
        total_requirements = len(self.checklist)
        readiness_percentage = (readiness_score / total_requirements) * 100
        
        return {
            'readiness_percentage': readiness_percentage,
            'ready_for_sharding': readiness_percentage >= 80,
            'missing_requirements': missing_requirements,
            'recommendations': self._generate_readiness_recommendations(missing_requirements)
        }
    
    def _generate_readiness_recommendations(self, missing_requirements: List[Dict]) -> List[str]:
        """Generate recommendations for sharding readiness"""
        
        recommendations = []
        
        for req in missing_requirements:
            if req['requirement'] == 'shard_key_identified':
                recommendations.append("Conduct thorough analysis of data access patterns to identify optimal shard key")
            elif req['requirement'] == 'application_ready':
                recommendations.append("Modify application to support sharded queries and cross-shard operations")
            elif req['requirement'] == 'monitoring_setup':
                recommendations.append("Implement comprehensive monitoring for shard health and performance")
            elif req['requirement'] == 'operational_expertise':
                recommendations.append("Train team on sharded database operations and troubleshooting")
        
        return recommendations
```

## Conclusion

Database sharding is a powerful technique for achieving horizontal scalability, but it comes with significant complexity. Key takeaways include:

### When to Shard
- Database size exceeds single server capacity (>100GB)
- Query load cannot be handled by single database
- Write throughput requirements exceed single database limits
- Geographic distribution requirements

### Sharding Strategy Selection
- **Hash-based**: Best for even distribution, simple implementation
- **Range-based**: Good for range queries, but watch for hotspots  
- **Directory-based**: Flexible but requires additional infrastructure
- **Geographic**: Essential for global applications with data locality requirements

### Critical Success Factors
1. **Proper Shard Key Selection**: High cardinality, immutable, aligns with query patterns
2. **Application Design**: Support for cross-shard queries and distributed transactions
3. **Monitoring and Operations**: Comprehensive monitoring, automated rebalancing
4. **Data Management**: Backup, recovery, and migration strategies

### Common Challenges and Solutions
- **Cross-shard queries**: Implement query coordination layer
- **Load imbalance**: Automated monitoring and rebalancing
- **Shard failures**: Read replicas and failover mechanisms
- **Data migration**: Plan for resharding and rebalancing operations

### Best Practices
- Start with thorough analysis and planning
- Implement comprehensive monitoring from day one
- Design for operational simplicity where possible
- Plan for growth and rebalancing scenarios
- Maintain expertise in sharded system operations

Sharding transforms a database scaling problem into a distributed systems problem. While it provides virtually unlimited horizontal scalability, it requires careful planning, robust operational procedures, and ongoing management to be successful. Consider sharding only when simpler scaling approaches (read replicas, caching, vertical scaling) are insufficient for your requirements.