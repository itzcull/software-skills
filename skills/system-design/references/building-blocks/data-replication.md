---
title: "Data Replication in Distributed Systems"
description: "Comprehensive guide to data replication strategies, types, implementation approaches, and best practices for distributed systems"
category: "Building Blocks"
tags: ["data-replication", "distributed-systems", "consistency", "availability", "fault-tolerance"]
difficulty: "intermediate"
last_updated: "2025-07-27"
---

# Data Replication in Distributed Systems

Data replication is a method of copying data to ensure that all information stays identical in real-time between all data resources. It's a fundamental technique for building reliable, available, and performant distributed systems.

## What is Data Replication?

Data replication involves maintaining multiple copies of data across different nodes, locations, or systems to achieve:

- **High Availability**: System continues operating even when some nodes fail
- **Fault Tolerance**: Protection against data loss from hardware failures
- **Performance**: Reduced latency by serving data from geographically closer replicas
- **Load Distribution**: Spread read operations across multiple replicas

### Basic Replication Architecture

```
Primary Database ─────┐
       │              │
       │              ▼
   Write Ops      Replication
       │              │
       ▼              ▼
┌─────────────────────────────────┐
│        Replica 1                │
├─────────────────────────────────┤
│        Replica 2                │
├─────────────────────────────────┤
│        Replica 3                │
└─────────────────────────────────┘
       ▲              ▲
       │              │
   Read Ops       Read Ops
```

## Types of Data Replication

### 1. Full Database Replication

Complete replication of the entire database to all replica instances.

```python
import asyncio
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class ReplicationStatus(Enum):
    SYNCED = "synced"
    SYNCING = "syncing"
    LAGGING = "lagging"
    FAILED = "failed"

@dataclass
class ReplicaNode:
    node_id: str
    host: str
    port: int
    status: ReplicationStatus
    last_sync_time: float
    lag_seconds: float = 0.0

class FullDatabaseReplicator:
    def __init__(self, primary_node: str, replica_nodes: List[ReplicaNode]):
        self.primary_node = primary_node
        self.replica_nodes = {node.node_id: node for node in replica_nodes}
        self.replication_log = []
        self.max_lag_threshold = 10.0  # seconds
        
    async def replicate_full_database(self, target_replica: str):
        """Perform full database replication to target replica"""
        
        replica = self.replica_nodes[target_replica]
        replica.status = ReplicationStatus.SYNCING
        
        try:
            # Step 1: Create database snapshot
            snapshot_id = await self._create_database_snapshot()
            
            # Step 2: Transfer snapshot to replica
            await self._transfer_snapshot(replica, snapshot_id)
            
            # Step 3: Apply snapshot to replica
            await self._apply_snapshot(replica, snapshot_id)
            
            # Step 4: Start incremental sync from snapshot point
            await self._start_incremental_sync(replica, snapshot_id)
            
            replica.status = ReplicationStatus.SYNCED
            replica.last_sync_time = time.time()
            replica.lag_seconds = 0.0
            
            print(f"Full replication to {target_replica} completed successfully")
            
        except Exception as e:
            replica.status = ReplicationStatus.FAILED
            print(f"Full replication to {target_replica} failed: {e}")
            raise
    
    async def _create_database_snapshot(self) -> str:
        """Create consistent database snapshot"""
        import time
        import uuid
        
        snapshot_id = f"snapshot_{int(time.time())}_{str(uuid.uuid4())[:8]}"
        
        # Lock database for consistent snapshot
        await self._execute_on_primary("SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ")
        await self._execute_on_primary("START TRANSACTION")
        
        try:
            # Export all tables
            tables = await self._get_all_tables()
            
            for table in tables:
                await self._export_table_data(table, snapshot_id)
            
            # Export schema
            await self._export_database_schema(snapshot_id)
            
            await self._execute_on_primary("COMMIT")
            
        except Exception as e:
            await self._execute_on_primary("ROLLBACK")
            raise e
        
        return snapshot_id
    
    async def _transfer_snapshot(self, replica: ReplicaNode, snapshot_id: str):
        """Transfer snapshot files to replica node"""
        
        # In production, this would use secure file transfer
        # like scp, rsync, or cloud storage
        
        snapshot_files = await self._get_snapshot_files(snapshot_id)
        
        for file_path in snapshot_files:
            await self._secure_copy_file(file_path, replica.host)
        
        print(f"Transferred {len(snapshot_files)} files to {replica.node_id}")
    
    async def _apply_snapshot(self, replica: ReplicaNode, snapshot_id: str):
        """Apply snapshot to replica database"""
        
        # Connect to replica
        replica_connection = await self._connect_to_replica(replica)
        
        try:
            # Drop existing database (careful!)
            await self._execute_on_replica(replica_connection, "DROP DATABASE IF EXISTS replica_db")
            
            # Create new database
            await self._execute_on_replica(replica_connection, "CREATE DATABASE replica_db")
            
            # Import schema
            await self._import_schema(replica_connection, snapshot_id)
            
            # Import data
            tables = await self._get_snapshot_tables(snapshot_id)
            for table in tables:
                await self._import_table_data(replica_connection, table, snapshot_id)
            
            print(f"Applied snapshot {snapshot_id} to {replica.node_id}")
            
        finally:
            await replica_connection.close()
    
    async def _start_incremental_sync(self, replica: ReplicaNode, from_snapshot: str):
        """Start incremental synchronization from snapshot point"""
        
        # Get binary log position from snapshot
        log_position = await self._get_snapshot_log_position(from_snapshot)
        
        # Start reading binary log from that position
        await self._start_binlog_replication(replica, log_position)
```

### 2. Partial Replication

Replicate only specific data subsets, tables, or recently updated records.

```python
class PartialReplicator:
    def __init__(self, primary_node: str, replication_rules: Dict):
        self.primary_node = primary_node
        self.replication_rules = replication_rules
        
    async def setup_table_filtering(self, replica_id: str, tables: List[str]):
        """Setup replication for specific tables only"""
        
        self.replication_rules[replica_id] = {
            'type': 'table_filter',
            'tables': tables,
            'filters': {}
        }
        
        # Configure replication stream
        await self._configure_filtered_replication(replica_id)
    
    async def setup_column_filtering(self, replica_id: str, table_columns: Dict[str, List[str]]):
        """Setup replication for specific columns in tables"""
        
        self.replication_rules[replica_id] = {
            'type': 'column_filter',
            'table_columns': table_columns,
            'filters': {}
        }
        
        await self._configure_filtered_replication(replica_id)
    
    async def setup_row_filtering(self, replica_id: str, filters: Dict[str, str]):
        """Setup replication with row-level filtering"""
        
        # filters format: {'table_name': 'WHERE condition'}
        self.replication_rules[replica_id] = {
            'type': 'row_filter',
            'filters': filters
        }
        
        await self._configure_filtered_replication(replica_id)
    
    async def replicate_recent_changes(self, replica_id: str, time_window_hours: int = 24):
        """Replicate only recent changes within time window"""
        
        time_filter = f"updated_at >= NOW() - INTERVAL {time_window_hours} HOUR"
        
        rules = self.replication_rules.get(replica_id, {})
        
        # Get tables with timestamp columns
        timestamped_tables = await self._get_timestamped_tables()
        
        for table in timestamped_tables:
            # Extract recent changes
            recent_changes = await self._extract_recent_changes(table, time_filter)
            
            # Apply to replica
            await self._apply_changes_to_replica(replica_id, table, recent_changes)
    
    async def _extract_recent_changes(self, table: str, time_filter: str) -> List[Dict]:
        """Extract recent changes from table"""
        
        query = f"""
        SELECT * FROM {table}
        WHERE {time_filter}
        ORDER BY updated_at ASC
        """
        
        results = await self._execute_on_primary(query)
        return [dict(row) for row in results]
    
    async def _apply_changes_to_replica(self, replica_id: str, table: str, changes: List[Dict]):
        """Apply changes to replica using upsert logic"""
        
        if not changes:
            return
        
        replica_connection = await self._get_replica_connection(replica_id)
        
        for change in changes:
            # Use INSERT ... ON DUPLICATE KEY UPDATE for MySQL
            # or INSERT ... ON CONFLICT for PostgreSQL
            
            columns = list(change.keys())
            values = list(change.values())
            placeholders = ', '.join(['?' for _ in values])
            
            # Example for MySQL
            upsert_query = f"""
            INSERT INTO {table} ({', '.join(columns)})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE
            {', '.join([f"{col} = VALUES({col})" for col in columns if col != 'id'])}
            """
            
            await replica_connection.execute(upsert_query, values)

# Usage example
async def setup_partial_replication():
    replicator = PartialReplicator("primary.db.com", {})
    
    # Replicate only user and order tables to analytics replica
    await replicator.setup_table_filtering("analytics_replica", ["users", "orders", "order_items"])
    
    # Replicate only recent user activity to cache replica
    await replicator.setup_row_filtering("cache_replica", {
        "user_sessions": "last_activity >= NOW() - INTERVAL 1 DAY",
        "user_preferences": "updated_at >= NOW() - INTERVAL 7 DAY"
    })
    
    # Replicate only essential user columns to public API replica
    await replicator.setup_column_filtering("api_replica", {
        "users": ["id", "username", "email", "created_at"],
        "profiles": ["user_id", "display_name", "avatar_url"]
    })
```

## Replication Strategies

### 1. Synchronous Replication

All replicas must acknowledge writes before the transaction is considered complete.

```python
import asyncio
from typing import List, Dict, Any, Optional

class SynchronousReplicator:
    def __init__(self, primary_node: str, replica_nodes: List[str]):
        self.primary_node = primary_node
        self.replica_nodes = replica_nodes
        self.timeout_seconds = 30.0
        self.min_replicas_for_success = len(replica_nodes) // 2 + 1  # Majority
        
    async def write_with_sync_replication(self, operation: Dict) -> bool:
        """Execute write operation with synchronous replication"""
        
        transaction_id = f"txn_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        try:
            # Phase 1: Prepare on all replicas
            prepare_results = await self._prepare_transaction_on_replicas(
                transaction_id, operation
            )
            
            if len(prepare_results) < self.min_replicas_for_success:
                await self._abort_transaction(transaction_id)
                return False
            
            # Phase 2: Execute on primary
            primary_result = await self._execute_on_primary(operation)
            
            if not primary_result:
                await self._abort_transaction(transaction_id)
                return False
            
            # Phase 3: Commit on all prepared replicas
            commit_results = await self._commit_transaction_on_replicas(
                transaction_id, operation
            )
            
            if len(commit_results) < self.min_replicas_for_success:
                # This is a serious condition - primary committed but replicas failed
                await self._handle_partial_commit_failure(transaction_id)
                return False
            
            return True
            
        except asyncio.TimeoutError:
            await self._abort_transaction(transaction_id)
            raise Exception("Synchronous replication timeout")
        except Exception as e:
            await self._abort_transaction(transaction_id)
            raise e
    
    async def _prepare_transaction_on_replicas(self, transaction_id: str, operation: Dict) -> List[str]:
        """Prepare transaction on all replicas (2PC Phase 1)"""
        
        prepare_tasks = []
        
        for replica in self.replica_nodes:
            task = asyncio.create_task(
                self._prepare_on_replica(replica, transaction_id, operation)
            )
            prepare_tasks.append((replica, task))
        
        # Wait for all with timeout
        prepared_replicas = []
        
        try:
            for replica, task in prepare_tasks:
                result = await asyncio.wait_for(task, timeout=self.timeout_seconds)
                if result:
                    prepared_replicas.append(replica)
        except asyncio.TimeoutError:
            # Cancel remaining tasks
            for replica, task in prepare_tasks:
                if not task.done():
                    task.cancel()
        
        return prepared_replicas
    
    async def _prepare_on_replica(self, replica: str, transaction_id: str, operation: Dict) -> bool:
        """Prepare transaction on single replica"""
        try:
            connection = await self._get_replica_connection(replica)
            
            # Start transaction
            await connection.execute("BEGIN")
            
            # Validate operation can be applied
            validation_result = await self._validate_operation(connection, operation)
            
            if validation_result:
                # Store prepared transaction info
                await self._store_prepared_transaction(connection, transaction_id, operation)
                return True
            else:
                await connection.execute("ROLLBACK")
                return False
                
        except Exception as e:
            print(f"Prepare failed on replica {replica}: {e}")
            return False
    
    async def _commit_transaction_on_replicas(self, transaction_id: str, operation: Dict) -> List[str]:
        """Commit prepared transactions on replicas (2PC Phase 2)"""
        
        commit_tasks = []
        
        for replica in self.replica_nodes:
            task = asyncio.create_task(
                self._commit_on_replica(replica, transaction_id, operation)
            )
            commit_tasks.append((replica, task))
        
        committed_replicas = []
        
        for replica, task in commit_tasks:
            try:
                result = await asyncio.wait_for(task, timeout=self.timeout_seconds)
                if result:
                    committed_replicas.append(replica)
            except asyncio.TimeoutError:
                print(f"Commit timeout on replica {replica}")
            except Exception as e:
                print(f"Commit failed on replica {replica}: {e}")
        
        return committed_replicas
    
    async def _commit_on_replica(self, replica: str, transaction_id: str, operation: Dict) -> bool:
        """Commit prepared transaction on single replica"""
        try:
            connection = await self._get_replica_connection(replica)
            
            # Apply the operation
            await self._apply_operation(connection, operation)
            
            # Commit transaction
            await connection.execute("COMMIT")
            
            # Clean up prepared transaction info
            await self._cleanup_prepared_transaction(connection, transaction_id)
            
            return True
            
        except Exception as e:
            print(f"Commit failed on replica {replica}: {e}")
            try:
                await connection.execute("ROLLBACK")
            except:
                pass
            return False

# Advantages: Strong consistency, immediate durability
# Disadvantages: Higher latency, reduced availability during network issues
```

### 2. Asynchronous Replication

Primary commits immediately; replicas are updated eventually.

```python
import asyncio
import queue
from dataclasses import dataclass
from typing import Queue

@dataclass
class ReplicationEvent:
    event_id: str
    timestamp: float
    operation_type: str  # INSERT, UPDATE, DELETE
    table: str
    data: Dict
    conditions: Dict = None  # For UPDATE/DELETE

class AsynchronousReplicator:
    def __init__(self, primary_node: str, replica_nodes: List[str]):
        self.primary_node = primary_node
        self.replica_nodes = replica_nodes
        self.replication_queue: Queue[ReplicationEvent] = queue.Queue()
        self.batch_size = 100
        self.batch_timeout = 5.0  # seconds
        self.worker_tasks = []
        
    async def start_async_replication(self):
        """Start asynchronous replication workers"""
        
        for replica in self.replica_nodes:
            worker_task = asyncio.create_task(
                self._replication_worker(replica)
            )
            self.worker_tasks.append(worker_task)
        
        print(f"Started {len(self.worker_tasks)} replication workers")
    
    async def write_with_async_replication(self, operation: Dict) -> bool:
        """Execute write operation with asynchronous replication"""
        
        try:
            # Execute on primary immediately
            result = await self._execute_on_primary(operation)
            
            if result:
                # Queue for asynchronous replication
                event = ReplicationEvent(
                    event_id=f"{int(time.time())}_{uuid.uuid4().hex[:8]}",
                    timestamp=time.time(),
                    operation_type=operation['type'],
                    table=operation['table'],
                    data=operation.get('data', {}),
                    conditions=operation.get('conditions', {})
                )
                
                # Non-blocking queue add
                await self._add_to_replication_queue(event)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Primary write failed: {e}")
            return False
    
    async def _replication_worker(self, replica: str):
        """Worker process for replicating to specific replica"""
        
        batch = []
        last_batch_time = time.time()
        
        while True:
            try:
                # Try to get event from queue
                try:
                    event = await asyncio.wait_for(
                        self._get_from_replication_queue(), 
                        timeout=1.0
                    )
                    batch.append(event)
                except asyncio.TimeoutError:
                    # Timeout - check if we should process current batch
                    pass
                
                # Process batch if it's full or timeout reached
                current_time = time.time()
                should_process = (
                    len(batch) >= self.batch_size or
                    (batch and current_time - last_batch_time >= self.batch_timeout)
                )
                
                if should_process and batch:
                    await self._process_replication_batch(replica, batch)
                    batch = []
                    last_batch_time = current_time
                
            except Exception as e:
                print(f"Replication worker error for {replica}: {e}")
                await asyncio.sleep(1.0)  # Brief pause before retry
    
    async def _process_replication_batch(self, replica: str, batch: List[ReplicationEvent]):
        """Process batch of replication events for replica"""
        
        try:
            connection = await self._get_replica_connection(replica)
            
            # Start transaction for batch
            await connection.execute("BEGIN")
            
            for event in batch:
                await self._apply_replication_event(connection, event)
            
            # Commit batch
            await connection.execute("COMMIT")
            
            print(f"Replicated batch of {len(batch)} events to {replica}")
            
        except Exception as e:
            print(f"Batch replication failed for {replica}: {e}")
            try:
                await connection.execute("ROLLBACK")
            except:
                pass
            
            # Re-queue failed events for retry
            for event in batch:
                await self._add_to_replication_queue(event)
    
    async def _apply_replication_event(self, connection, event: ReplicationEvent):
        """Apply single replication event to connection"""
        
        if event.operation_type == "INSERT":
            await self._apply_insert(connection, event)
        elif event.operation_type == "UPDATE":
            await self._apply_update(connection, event)
        elif event.operation_type == "DELETE":
            await self._apply_delete(connection, event)
        else:
            raise ValueError(f"Unknown operation type: {event.operation_type}")
    
    async def _apply_insert(self, connection, event: ReplicationEvent):
        """Apply INSERT operation"""
        columns = list(event.data.keys())
        values = list(event.data.values())
        placeholders = ', '.join(['?' for _ in values])
        
        query = f"""
        INSERT INTO {event.table} ({', '.join(columns)})
        VALUES ({placeholders})
        """
        
        await connection.execute(query, values)
    
    async def _apply_update(self, connection, event: ReplicationEvent):
        """Apply UPDATE operation"""
        set_clauses = [f"{col} = ?" for col in event.data.keys()]
        where_clauses = [f"{col} = ?" for col in event.conditions.keys()]
        
        query = f"""
        UPDATE {event.table}
        SET {', '.join(set_clauses)}
        WHERE {' AND '.join(where_clauses)}
        """
        
        values = list(event.data.values()) + list(event.conditions.values())
        await connection.execute(query, values)
    
    async def _apply_delete(self, connection, event: ReplicationEvent):
        """Apply DELETE operation"""
        where_clauses = [f"{col} = ?" for col in event.conditions.keys()]
        
        query = f"""
        DELETE FROM {event.table}
        WHERE {' AND '.join(where_clauses)}
        """
        
        values = list(event.conditions.values())
        await connection.execute(query, values)

# Advantages: Low latency, high availability
# Disadvantages: Eventual consistency, potential data loss
```

### 3. Semi-Synchronous Replication

Waits for acknowledgment from at least one replica before committing.

```python
class SemiSynchronousReplicator:
    def __init__(self, primary_node: str, replica_nodes: List[str]):
        self.primary_node = primary_node
        self.replica_nodes = replica_nodes
        self.sync_replica_count = 1  # Wait for at least 1 replica
        self.sync_timeout = 10.0  # seconds
        
    async def write_with_semi_sync_replication(self, operation: Dict) -> bool:
        """Execute write with semi-synchronous replication"""
        
        try:
            # Execute on primary
            primary_result = await self._execute_on_primary(operation)
            
            if not primary_result:
                return False
            
            # Replicate to replicas in parallel
            replication_tasks = []
            
            for replica in self.replica_nodes:
                task = asyncio.create_task(
                    self._replicate_to_replica(replica, operation)
                )
                replication_tasks.append(task)
            
            # Wait for at least sync_replica_count to complete
            completed_count = 0
            
            for task in asyncio.as_completed(replication_tasks, timeout=self.sync_timeout):
                try:
                    result = await task
                    if result:
                        completed_count += 1
                        
                        if completed_count >= self.sync_replica_count:
                            # We have enough synchronous confirmations
                            break
                except Exception as e:
                    print(f"Replica replication failed: {e}")
            
            if completed_count >= self.sync_replica_count:
                # Continue async replication for remaining replicas
                remaining_tasks = [task for task in replication_tasks if not task.done()]
                if remaining_tasks:
                    asyncio.create_task(self._complete_async_replication(remaining_tasks))
                
                return True
            else:
                # Not enough replicas confirmed - this is a serious condition
                print(f"Only {completed_count} replicas confirmed, needed {self.sync_replica_count}")
                return False
                
        except asyncio.TimeoutError:
            print("Semi-synchronous replication timeout")
            return False
        except Exception as e:
            print(f"Semi-synchronous replication failed: {e}")
            return False
    
    async def _complete_async_replication(self, remaining_tasks: List[asyncio.Task]):
        """Complete replication to remaining replicas asynchronously"""
        
        for task in remaining_tasks:
            try:
                await task
            except Exception as e:
                print(f"Async replication completion failed: {e}")

# Advantages: Balance between consistency and performance
# Disadvantages: More complex than pure sync/async approaches
```

## Conflict Resolution Strategies

### 1. Last Writer Wins

```python
import time
from typing import Dict, Any, Optional

class LastWriterWinsResolver:
    def __init__(self):
        self.conflict_log = []
        
    def resolve_conflict(self, local_record: Dict, remote_record: Dict) -> Dict:
        """Resolve conflict using Last Writer Wins strategy"""
        
        local_timestamp = local_record.get('updated_at', 0)
        remote_timestamp = remote_record.get('updated_at', 0)
        
        if remote_timestamp > local_timestamp:
            winner = remote_record
            source = 'remote'
        elif local_timestamp > remote_timestamp:
            winner = local_record
            source = 'local'
        else:
            # Same timestamp - use other criteria (e.g., node ID)
            local_node = local_record.get('last_modified_by', '')
            remote_node = remote_record.get('last_modified_by', '')
            
            if remote_node > local_node:  # Lexicographic comparison
                winner = remote_record
                source = 'remote'
            else:
                winner = local_record
                source = 'local'
        
        # Log the conflict resolution
        self.conflict_log.append({
            'timestamp': time.time(),
            'record_id': local_record.get('id'),
            'resolution': 'last_writer_wins',
            'winner_source': source,
            'local_timestamp': local_timestamp,
            'remote_timestamp': remote_timestamp
        })
        
        return winner
```

### 2. Vector Clock Resolution

```python
class VectorClock:
    def __init__(self, node_id: str, nodes: List[str]):
        self.node_id = node_id
        self.clocks = {node: 0 for node in nodes}
        
    def increment(self):
        """Increment own clock"""
        self.clocks[self.node_id] += 1
        return self.clocks.copy()
    
    def update(self, other_clocks: Dict[str, int]):
        """Update clocks based on received vector clock"""
        for node, clock in other_clocks.items():
            if node in self.clocks:
                self.clocks[node] = max(self.clocks[node], clock)
        
        # Increment own clock
        self.clocks[self.node_id] += 1
    
    def compare(self, other_clocks: Dict[str, int]) -> str:
        """Compare with another vector clock"""
        
        less_than = all(
            self.clocks[node] <= other_clocks.get(node, 0) 
            for node in self.clocks
        )
        greater_than = all(
            self.clocks[node] >= other_clocks.get(node, 0) 
            for node in self.clocks
        )
        
        if less_than and any(
            self.clocks[node] < other_clocks.get(node, 0) 
            for node in self.clocks
        ):
            return "before"
        elif greater_than and any(
            self.clocks[node] > other_clocks.get(node, 0) 
            for node in self.clocks
        ):
            return "after"
        else:
            return "concurrent"

class VectorClockResolver:
    def __init__(self, node_id: str, nodes: List[str]):
        self.vector_clock = VectorClock(node_id, nodes)
        
    def resolve_conflict(self, local_record: Dict, remote_record: Dict) -> Optional[Dict]:
        """Resolve conflict using vector clocks"""
        
        local_vclock = local_record.get('vector_clock', {})
        remote_vclock = remote_record.get('vector_clock', {})
        
        comparison = self.vector_clock.compare(remote_vclock)
        
        if comparison == "before":
            # Remote is newer
            return remote_record
        elif comparison == "after":
            # Local is newer
            return local_record
        else:
            # Concurrent updates - need application-specific resolution
            return self.resolve_concurrent_update(local_record, remote_record)
    
    def resolve_concurrent_update(self, local_record: Dict, remote_record: Dict) -> Dict:
        """Resolve concurrent updates using application logic"""
        
        # Example: Merge strategy for user profiles
        if local_record.get('table') == 'user_profiles':
            return self._merge_user_profiles(local_record, remote_record)
        
        # Default: Use last writer wins as fallback
        local_timestamp = local_record.get('updated_at', 0)
        remote_timestamp = remote_record.get('updated_at', 0)
        
        return remote_record if remote_timestamp > local_timestamp else local_record
    
    def _merge_user_profiles(self, local: Dict, remote: Dict) -> Dict:
        """Merge user profile updates"""
        
        merged = local.copy()
        
        # Merge non-conflicting fields
        for field, value in remote.items():
            if field not in local or local[field] is None:
                merged[field] = value
        
        # Handle specific field conflicts
        if 'preferences' in local and 'preferences' in remote:
            # Merge preferences dictionaries
            merged['preferences'] = {**local['preferences'], **remote['preferences']}
        
        # Update vector clock
        merged['vector_clock'] = self.vector_clock.clocks.copy()
        
        return merged
```

### 3. Application-Specific Resolution

```python
class ApplicationSpecificResolver:
    def __init__(self):
        self.resolution_rules = {}
        
    def register_resolution_rule(self, table: str, field: str, strategy: str):
        """Register resolution strategy for specific table/field"""
        
        if table not in self.resolution_rules:
            self.resolution_rules[table] = {}
        
        self.resolution_rules[table][field] = strategy
    
    def resolve_conflict(self, table: str, local_record: Dict, remote_record: Dict) -> Dict:
        """Resolve conflict using application-specific rules"""
        
        table_rules = self.resolution_rules.get(table, {})
        resolved_record = {}
        
        # Get all fields from both records
        all_fields = set(local_record.keys()) | set(remote_record.keys())
        
        for field in all_fields:
            local_value = local_record.get(field)
            remote_value = remote_record.get(field)
            
            if local_value == remote_value:
                # No conflict
                resolved_record[field] = local_value
                continue
            
            # Apply resolution strategy
            strategy = table_rules.get(field, 'last_writer_wins')
            
            if strategy == 'sum':
                resolved_record[field] = (local_value or 0) + (remote_value or 0)
            elif strategy == 'max':
                resolved_record[field] = max(local_value or 0, remote_value or 0)
            elif strategy == 'min':
                resolved_record[field] = min(local_value or 0, remote_value or 0)
            elif strategy == 'concat':
                resolved_record[field] = f"{local_value or ''},{remote_value or ''}"
            elif strategy == 'local_wins':
                resolved_record[field] = local_value
            elif strategy == 'remote_wins':
                resolved_record[field] = remote_value
            else:  # last_writer_wins
                local_ts = local_record.get('updated_at', 0)
                remote_ts = remote_record.get('updated_at', 0)
                resolved_record[field] = remote_value if remote_ts > local_ts else local_value
        
        return resolved_record

# Usage example
resolver = ApplicationSpecificResolver()

# Configure resolution strategies
resolver.register_resolution_rule('user_stats', 'login_count', 'max')
resolver.register_resolution_rule('user_stats', 'total_spent', 'sum')
resolver.register_resolution_rule('user_profile', 'bio', 'last_writer_wins')
resolver.register_resolution_rule('user_preferences', 'themes', 'local_wins')
```

## Multi-Master Replication

### Active-Active Configuration

```python
class ActiveActiveReplicator:
    def __init__(self, nodes: List[str], node_id: str):
        self.nodes = nodes
        self.node_id = node_id
        self.peer_connections = {}
        self.conflict_resolver = VectorClockResolver(node_id, nodes)
        
    async def setup_active_active_replication(self):
        """Setup bidirectional replication between all nodes"""
        
        # Establish connections to all peer nodes
        for node in self.nodes:
            if node != self.node_id:
                connection = await self._establish_peer_connection(node)
                self.peer_connections[node] = connection
        
        # Start replication listeners
        await self._start_replication_listeners()
        
        print(f"Active-active replication setup complete for node {self.node_id}")
    
    async def write_with_active_active_replication(self, operation: Dict) -> bool:
        """Execute write operation in active-active setup"""
        
        try:
            # Add vector clock to operation
            operation['vector_clock'] = self.conflict_resolver.vector_clock.increment()
            operation['originating_node'] = self.node_id
            
            # Execute locally first
            local_success = await self._execute_locally(operation)
            
            if local_success:
                # Propagate to all peers asynchronously
                await self._propagate_to_peers(operation)
                return True
            
            return False
            
        except Exception as e:
            print(f"Active-active write failed: {e}")
            return False
    
    async def _propagate_to_peers(self, operation: Dict):
        """Propagate operation to all peer nodes"""
        
        propagation_tasks = []
        
        for node, connection in self.peer_connections.items():
            task = asyncio.create_task(
                self._send_operation_to_peer(node, connection, operation)
            )
            propagation_tasks.append(task)
        
        # Wait for all propagations (with timeout)
        try:
            await asyncio.wait_for(
                asyncio.gather(*propagation_tasks, return_exceptions=True),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            print("Some peer propagations timed out")
    
    async def _send_operation_to_peer(self, node: str, connection, operation: Dict):
        """Send operation to specific peer node"""
        
        try:
            await connection.send_replication_event(operation)
        except Exception as e:
            print(f"Failed to send operation to peer {node}: {e}")
            # Implement retry logic or queue for later retry
    
    async def handle_incoming_replication(self, operation: Dict):
        """Handle replication event from peer node"""
        
        # Check if we've already processed this operation
        if await self._is_duplicate_operation(operation):
            return
        
        # Check for conflicts with local data
        conflict = await self._detect_conflict(operation)
        
        if conflict:
            # Resolve conflict
            resolved_operation = self.conflict_resolver.resolve_conflict(
                conflict['local_record'],
                operation
            )
            
            if resolved_operation:
                await self._apply_resolved_operation(resolved_operation)
        else:
            # No conflict, apply directly
            await self._apply_operation(operation)
        
        # Update vector clock
        self.conflict_resolver.vector_clock.update(operation['vector_clock'])
    
    async def _detect_conflict(self, incoming_operation: Dict) -> Optional[Dict]:
        """Detect if incoming operation conflicts with local data"""
        
        table = incoming_operation['table']
        record_id = incoming_operation.get('record_id')
        
        if not record_id:
            return None
        
        # Get current local record
        local_record = await self._get_local_record(table, record_id)
        
        if not local_record:
            return None  # No conflict, record doesn't exist locally
        
        # Check if both records have been modified since last sync
        local_vclock = local_record.get('vector_clock', {})
        incoming_vclock = incoming_operation.get('vector_clock', {})
        
        comparison = self.conflict_resolver.vector_clock.compare(incoming_vclock)
        
        if comparison == "concurrent":
            return {
                'local_record': local_record,
                'incoming_operation': incoming_operation,
                'conflict_type': 'concurrent_modification'
            }
        
        return None
```

## Monitoring and Management

### Replication Lag Monitoring

```python
class ReplicationMonitor:
    def __init__(self, primary_node: str, replica_nodes: List[str]):
        self.primary_node = primary_node
        self.replica_nodes = replica_nodes
        self.lag_thresholds = {
            'warning': 10.0,  # seconds
            'critical': 60.0   # seconds
        }
        self.monitoring_interval = 30.0  # seconds
        
    async def start_monitoring(self):
        """Start continuous replication monitoring"""
        
        monitoring_task = asyncio.create_task(self._monitoring_loop())
        return monitoring_task
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        
        while True:
            try:
                await self._collect_replication_metrics()
                await asyncio.sleep(self.monitoring_interval)
            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(5.0)  # Brief pause on error
    
    async def _collect_replication_metrics(self):
        """Collect replication metrics from all nodes"""
        
        primary_position = await self._get_primary_log_position()
        
        for replica in self.replica_nodes:
            try:
                replica_metrics = await self._get_replica_metrics(replica)
                lag_seconds = await self._calculate_lag(primary_position, replica_metrics)
                
                await self._record_lag_metric(replica, lag_seconds)
                await self._check_lag_alerts(replica, lag_seconds)
                
            except Exception as e:
                print(f"Failed to collect metrics for replica {replica}: {e}")
    
    async def _get_primary_log_position(self) -> Dict:
        """Get current log position from primary"""
        
        # MySQL example
        query = "SHOW MASTER STATUS"
        result = await self._execute_on_primary(query)
        
        return {
            'log_file': result['File'],
            'log_position': result['Position'],
            'timestamp': time.time()
        }
    
    async def _get_replica_metrics(self, replica: str) -> Dict:
        """Get replication metrics from replica"""
        
        # MySQL example
        query = "SHOW SLAVE STATUS"
        result = await self._execute_on_replica(replica, query)
        
        return {
            'master_log_file': result['Master_Log_File'],
            'read_master_log_pos': result['Read_Master_Log_Pos'],
            'exec_master_log_pos': result['Exec_Master_Log_Pos'],
            'seconds_behind_master': result['Seconds_Behind_Master'],
            'slave_io_running': result['Slave_IO_Running'],
            'slave_sql_running': result['Slave_SQL_Running']
        }
    
    async def _calculate_lag(self, primary_pos: Dict, replica_metrics: Dict) -> float:
        """Calculate replication lag in seconds"""
        
        # Use built-in lag calculation if available
        if 'seconds_behind_master' in replica_metrics:
            return float(replica_metrics['seconds_behind_master'] or 0)
        
        # Calculate based on log positions
        # This is a simplified calculation
        primary_timestamp = primary_pos['timestamp']
        current_time = time.time()
        
        # Estimate lag based on position difference and time
        # In practice, this would be more sophisticated
        return current_time - primary_timestamp
    
    async def _check_lag_alerts(self, replica: str, lag_seconds: float):
        """Check if lag exceeds alert thresholds"""
        
        if lag_seconds >= self.lag_thresholds['critical']:
            await self._send_alert('critical', replica, lag_seconds)
        elif lag_seconds >= self.lag_thresholds['warning']:
            await self._send_alert('warning', replica, lag_seconds)
    
    async def _send_alert(self, severity: str, replica: str, lag_seconds: float):
        """Send replication lag alert"""
        
        alert = {
            'severity': severity,
            'replica': replica,
            'lag_seconds': lag_seconds,
            'timestamp': time.time(),
            'message': f"Replication lag on {replica}: {lag_seconds:.1f}s"
        }
        
        # Send to monitoring system
        print(f"ALERT [{severity.upper()}]: {alert['message']}")
```

### Automated Failover

```python
class ReplicationFailoverManager:
    def __init__(self, primary_node: str, replica_nodes: List[str]):
        self.primary_node = primary_node
        self.replica_nodes = replica_nodes
        self.failover_in_progress = False
        self.primary_healthy = True
        
    async def monitor_primary_health(self):
        """Monitor primary node health and trigger failover if needed"""
        
        consecutive_failures = 0
        failure_threshold = 3
        
        while True:
            try:
                is_healthy = await self._check_primary_health()
                
                if is_healthy:
                    consecutive_failures = 0
                    self.primary_healthy = True
                else:
                    consecutive_failures += 1
                    
                    if consecutive_failures >= failure_threshold:
                        if not self.failover_in_progress:
                            await self._trigger_failover()
                
                await asyncio.sleep(10.0)  # Check every 10 seconds
                
            except Exception as e:
                print(f"Health monitoring error: {e}")
                await asyncio.sleep(5.0)
    
    async def _check_primary_health(self) -> bool:
        """Check if primary node is healthy"""
        
        try:
            # Simple health check query
            result = await asyncio.wait_for(
                self._execute_on_primary("SELECT 1"),
                timeout=5.0
            )
            return result is not None
            
        except (asyncio.TimeoutError, Exception):
            return False
    
    async def _trigger_failover(self):
        """Trigger automatic failover to replica"""
        
        self.failover_in_progress = True
        self.primary_healthy = False
        
        try:
            print("Primary failure detected, starting failover...")
            
            # Step 1: Select best replica for promotion
            new_primary = await self._select_failover_candidate()
            
            if not new_primary:
                raise Exception("No suitable replica found for failover")
            
            # Step 2: Promote replica to primary
            await self._promote_replica_to_primary(new_primary)
            
            # Step 3: Redirect traffic to new primary
            await self._redirect_traffic_to_new_primary(new_primary)
            
            # Step 4: Update replication topology
            await self._update_replication_topology(new_primary)
            
            print(f"Failover completed successfully. New primary: {new_primary}")
            
        except Exception as e:
            print(f"Failover failed: {e}")
            # Implement rollback or manual intervention alert
        finally:
            self.failover_in_progress = False
    
    async def _select_failover_candidate(self) -> Optional[str]:
        """Select the best replica to promote to primary"""
        
        candidates = []
        
        for replica in self.replica_nodes:
            try:
                metrics = await self._get_replica_metrics(replica)
                
                # Check if replica is healthy and up-to-date
                if (metrics['slave_io_running'] == 'Yes' and
                    metrics['slave_sql_running'] == 'Yes' and
                    metrics['seconds_behind_master'] < 10):  # Less than 10 seconds behind
                    
                    candidates.append({
                        'replica': replica,
                        'lag': metrics['seconds_behind_master'],
                        'log_position': metrics['exec_master_log_pos']
                    })
                    
            except Exception as e:
                print(f"Failed to evaluate replica {replica}: {e}")
        
        if not candidates:
            return None
        
        # Select replica with least lag and highest log position
        best_candidate = min(candidates, key=lambda x: (x['lag'], -x['log_position']))
        return best_candidate['replica']
    
    async def _promote_replica_to_primary(self, replica: str):
        """Promote replica to become new primary"""
        
        # Stop replication on the replica
        await self._execute_on_replica(replica, "STOP SLAVE")
        
        # Reset master info
        await self._execute_on_replica(replica, "RESET MASTER")
        
        # Enable binary logging (if not already enabled)
        # This might require restart depending on configuration
        
        print(f"Promoted {replica} to primary")
    
    async def _redirect_traffic_to_new_primary(self, new_primary: str):
        """Redirect application traffic to new primary"""
        
        # Update load balancer configuration
        # Update DNS records
        # Update application connection strings
        
        # This is highly dependent on your infrastructure setup
        print(f"Redirected traffic to new primary: {new_primary}")
    
    async def _update_replication_topology(self, new_primary: str):
        """Update remaining replicas to replicate from new primary"""
        
        remaining_replicas = [r for r in self.replica_nodes if r != new_primary]
        
        for replica in remaining_replicas:
            try:
                # Stop current replication
                await self._execute_on_replica(replica, "STOP SLAVE")
                
                # Change master to new primary
                change_master_query = f"""
                CHANGE MASTER TO
                MASTER_HOST='{new_primary}',
                MASTER_USER='replication_user',
                MASTER_PASSWORD='replication_password',
                MASTER_LOG_FILE='',
                MASTER_LOG_POS=0
                """
                
                await self._execute_on_replica(replica, change_master_query)
                
                # Start replication
                await self._execute_on_replica(replica, "START SLAVE")
                
                print(f"Updated {replica} to replicate from new primary")
                
            except Exception as e:
                print(f"Failed to update replica {replica}: {e}")
```

## Best Practices

### 1. Replication Strategy Selection

```python
class ReplicationStrategySelector:
    def __init__(self):
        self.strategy_matrix = {
            'consistency_requirement': {
                'strong': ['synchronous', 'semi_synchronous'],
                'eventual': ['asynchronous', 'semi_synchronous'],
                'weak': ['asynchronous']
            },
            'performance_requirement': {
                'low_latency': ['asynchronous', 'semi_synchronous'],
                'high_throughput': ['asynchronous'],
                'balanced': ['semi_synchronous', 'asynchronous']
            },
            'availability_requirement': {
                'high': ['asynchronous', 'semi_synchronous'],
                'medium': ['semi_synchronous', 'synchronous'],
                'low': ['synchronous']
            }
        }
    
    def recommend_strategy(self, requirements: Dict) -> str:
        """Recommend replication strategy based on requirements"""
        
        scores = {}
        
        for requirement, value in requirements.items():
            if requirement in self.strategy_matrix:
                strategies = self.strategy_matrix[requirement].get(value, [])
                
                for strategy in strategies:
                    scores[strategy] = scores.get(strategy, 0) + 1
        
        # Return strategy with highest score
        if scores:
            return max(scores, key=scores.get)
        else:
            return 'semi_synchronous'  # Default balanced approach

# Usage example
selector = ReplicationStrategySelector()

requirements = {
    'consistency_requirement': 'eventual',
    'performance_requirement': 'low_latency',
    'availability_requirement': 'high'
}

recommended_strategy = selector.recommend_strategy(requirements)
print(f"Recommended strategy: {recommended_strategy}")
```

### 2. Operational Best Practices

1. **Monitor Replication Lag**
   - Set up automated monitoring and alerting
   - Define SLAs for acceptable lag levels
   - Implement lag-based traffic routing

2. **Plan for Failure Scenarios**
   - Document failover procedures
   - Test failover processes regularly
   - Implement automated failover where appropriate

3. **Optimize Network Usage**
   - Use compression for replication streams
   - Implement batching for asynchronous replication
   - Consider bandwidth limitations

4. **Security Considerations**
   - Encrypt replication traffic
   - Use dedicated replication users with minimal privileges
   - Implement certificate-based authentication

5. **Capacity Planning**
   - Monitor storage growth on all nodes
   - Plan for peak load scenarios
   - Consider geographic distribution requirements

## Conclusion

Data replication is essential for building robust distributed systems. Key takeaways:

### Strategy Selection
- **Synchronous**: Use for strong consistency requirements
- **Asynchronous**: Use for high performance and availability
- **Semi-synchronous**: Use for balanced consistency and performance

### Implementation Considerations
- Choose appropriate conflict resolution strategies
- Implement comprehensive monitoring and alerting
- Plan for failure scenarios and automated recovery
- Consider operational complexity and expertise requirements

### Best Practices
- Start with simpler strategies and evolve as needed
- Monitor replication lag and performance continuously
- Test failover procedures regularly
- Design for your specific consistency and availability requirements

Data replication involves fundamental trade-offs between consistency, availability, and performance. Understanding these trade-offs and choosing the right approach for your specific use case is crucial for building successful distributed systems.