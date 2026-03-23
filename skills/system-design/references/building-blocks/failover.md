---
title: "Failover Systems"
description: "Comprehensive guide to failover mechanisms, strategies, and implementation patterns for ensuring high availability and business continuity"
category: "Building Blocks"
date: "2025-07-27"
tags: ["failover", "high-availability", "disaster-recovery", "fault-tolerance", "business-continuity"]
complexity: "intermediate"
---

# Failover Systems

Failover is the ability to switch automatically and seamlessly to a reliable backup system when a primary component fails. It's a critical mechanism for ensuring high availability, business continuity, and fault tolerance in distributed systems.

## Core Concepts

### What is Failover?

Failover is an operational procedure where a secondary system automatically takes over the functions of a primary system when the primary system becomes unavailable due to failure, maintenance, or other issues. The goal is to maintain service continuity with minimal downtime and user impact.

### Key Components

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio
import logging

class FailoverState(Enum):
    ACTIVE = "active"
    STANDBY = "standby"
    FAILED = "failed"
    MAINTENANCE = "maintenance"
    RECOVERING = "recovering"

class FailoverMode(Enum):
    ACTIVE_PASSIVE = "active_passive"
    ACTIVE_ACTIVE = "active_active"
    HOT_STANDBY = "hot_standby"
    COLD_STANDBY = "cold_standby"
    WARM_STANDBY = "warm_standby"

@dataclass
class SystemNode:
    node_id: str
    host: str
    port: int
    state: FailoverState
    last_heartbeat: datetime
    health_score: float = 1.0
    load_percentage: float = 0.0
    is_primary: bool = False
    capabilities: List[str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []

class HealthChecker(ABC):
    """Abstract health checker interface"""
    
    @abstractmethod
    async def check_health(self, node: SystemNode) -> bool:
        """Check if node is healthy"""
        pass
    
    @abstractmethod
    def get_health_score(self, node: SystemNode) -> float:
        """Get health score between 0.0 and 1.0"""
        pass

class HeartbeatMonitor:
    """Monitor node heartbeats for failure detection"""
    
    def __init__(self, timeout_seconds: int = 30, check_interval: int = 5):
        self.timeout_seconds = timeout_seconds
        self.check_interval = check_interval
        self.running = False
        self.heartbeat_callbacks: List[Callable] = []
    
    def add_heartbeat_callback(self, callback: Callable):
        """Add callback for heartbeat events"""
        self.heartbeat_callbacks.append(callback)
    
    async def start_monitoring(self, nodes: List[SystemNode]):
        """Start heartbeat monitoring"""
        self.running = True
        
        while self.running:
            for node in nodes:
                if self._is_heartbeat_expired(node):
                    await self._handle_heartbeat_timeout(node)
            
            await asyncio.sleep(self.check_interval)
    
    def stop_monitoring(self):
        """Stop heartbeat monitoring"""
        self.running = False
    
    def update_heartbeat(self, node_id: str, nodes: List[SystemNode]):
        """Update heartbeat for a node"""
        for node in nodes:
            if node.node_id == node_id:
                node.last_heartbeat = datetime.now()
                break
    
    def _is_heartbeat_expired(self, node: SystemNode) -> bool:
        """Check if heartbeat has expired"""
        if node.state == FailoverState.FAILED:
            return False
        
        time_since_heartbeat = datetime.now() - node.last_heartbeat
        return time_since_heartbeat.total_seconds() > self.timeout_seconds
    
    async def _handle_heartbeat_timeout(self, node: SystemNode):
        """Handle heartbeat timeout"""
        logging.warning(f"Heartbeat timeout for node {node.node_id}")
        node.state = FailoverState.FAILED
        
        # Notify callbacks
        for callback in self.heartbeat_callbacks:
            try:
                await callback(node, "heartbeat_timeout")
            except Exception as e:
                logging.error(f"Error in heartbeat callback: {e}")

class BasicHealthChecker(HealthChecker):
    """Basic health checker implementation"""
    
    def __init__(self):
        self.timeout = 10  # seconds
    
    async def check_health(self, node: SystemNode) -> bool:
        """Basic health check via HTTP or TCP"""
        try:
            # Simulate health check (in practice, this would be HTTP/TCP check)
            await asyncio.sleep(0.1)  # Simulate network delay
            
            # Check if node is responding
            if node.state == FailoverState.FAILED:
                return False
            
            # Simulate occasional health check failures
            import random
            return random.random() > 0.1  # 90% success rate
            
        except Exception as e:
            logging.error(f"Health check failed for {node.node_id}: {e}")
            return False
    
    def get_health_score(self, node: SystemNode) -> float:
        """Calculate health score based on various metrics"""
        score = 1.0
        
        # Reduce score based on load
        if node.load_percentage > 80:
            score -= 0.3
        elif node.load_percentage > 60:
            score -= 0.1
        
        # Reduce score if in recovering state
        if node.state == FailoverState.RECOVERING:
            score -= 0.2
        
        # Failed nodes get 0 score
        if node.state == FailoverState.FAILED:
            score = 0.0
        
        return max(0.0, min(1.0, score))
```

## Failover Configurations

### 1. Active-Passive Failover

In active-passive configuration, one node handles all traffic while backup nodes remain on standby.

```python
class ActivePassiveFailover:
    """Active-Passive failover implementation"""
    
    def __init__(self, health_checker: HealthChecker):
        self.health_checker = health_checker
        self.nodes: List[SystemNode] = []
        self.primary_node: Optional[SystemNode] = None
        self.failover_in_progress = False
        self.heartbeat_monitor = HeartbeatMonitor()
        self.failover_callbacks: List[Callable] = []
        
        # Set up heartbeat callback
        self.heartbeat_monitor.add_heartbeat_callback(self._handle_node_failure)
    
    def add_node(self, node: SystemNode):
        """Add node to failover cluster"""
        self.nodes.append(node)
        
        # First node becomes primary
        if not self.primary_node and node.state == FailoverState.ACTIVE:
            self.primary_node = node
            node.is_primary = True
        else:
            node.state = FailoverState.STANDBY
            node.is_primary = False
    
    def add_failover_callback(self, callback: Callable):
        """Add callback for failover events"""
        self.failover_callbacks.append(callback)
    
    async def start_monitoring(self):
        """Start monitoring cluster health"""
        await self.heartbeat_monitor.start_monitoring(self.nodes)
    
    async def _handle_node_failure(self, failed_node: SystemNode, failure_type: str):
        """Handle node failure"""
        if failed_node.is_primary and not self.failover_in_progress:
            await self._initiate_failover()
    
    async def _initiate_failover(self):
        """Initiate failover to backup node"""
        if self.failover_in_progress:
            return
        
        self.failover_in_progress = True
        logging.info("Initiating failover from primary node")
        
        try:
            # Find best standby node
            best_standby = await self._select_best_standby()
            
            if best_standby:
                await self._promote_to_primary(best_standby)
                logging.info(f"Failover completed: {best_standby.node_id} is now primary")
            else:
                logging.error("No suitable standby node found for failover")
        
        except Exception as e:
            logging.error(f"Failover failed: {e}")
        
        finally:
            self.failover_in_progress = False
    
    async def _select_best_standby(self) -> Optional[SystemNode]:
        """Select best standby node for promotion"""
        standby_nodes = [
            node for node in self.nodes 
            if node.state == FailoverState.STANDBY
        ]
        
        if not standby_nodes:
            return None
        
        # Check health of all standby nodes
        healthy_standbys = []
        for node in standby_nodes:
            if await self.health_checker.check_health(node):
                node.health_score = self.health_checker.get_health_score(node)
                healthy_standbys.append(node)
        
        if not healthy_standbys:
            return None
        
        # Select node with highest health score
        return max(healthy_standbys, key=lambda n: n.health_score)
    
    async def _promote_to_primary(self, standby_node: SystemNode):
        """Promote standby node to primary"""
        
        # Update old primary
        if self.primary_node:
            self.primary_node.is_primary = False
            self.primary_node.state = FailoverState.FAILED
        
        # Promote new primary
        standby_node.state = FailoverState.ACTIVE
        standby_node.is_primary = True
        self.primary_node = standby_node
        
        # Notify callbacks
        for callback in self.failover_callbacks:
            try:
                await callback(standby_node, "promoted_to_primary")
            except Exception as e:
                logging.error(f"Error in failover callback: {e}")
    
    async def manual_failover(self, target_node_id: str) -> bool:
        """Manually trigger failover to specific node"""
        target_node = None
        for node in self.nodes:
            if node.node_id == target_node_id:
                target_node = node
                break
        
        if not target_node:
            logging.error(f"Target node {target_node_id} not found")
            return False
        
        if target_node.state != FailoverState.STANDBY:
            logging.error(f"Target node {target_node_id} is not in standby state")
            return False
        
        # Check health of target node
        if not await self.health_checker.check_health(target_node):
            logging.error(f"Target node {target_node_id} failed health check")
            return False
        
        await self._promote_to_primary(target_node)
        return True
    
    async def get_cluster_status(self) -> Dict[str, Any]:
        """Get current cluster status"""
        status = {
            'primary_node': self.primary_node.node_id if self.primary_node else None,
            'failover_in_progress': self.failover_in_progress,
            'total_nodes': len(self.nodes),
            'nodes': []
        }
        
        for node in self.nodes:
            node_status = {
                'node_id': node.node_id,
                'state': node.state.value,
                'is_primary': node.is_primary,
                'health_score': node.health_score,
                'load_percentage': node.load_percentage,
                'last_heartbeat': node.last_heartbeat.isoformat()
            }
            status['nodes'].append(node_status)
        
        return status

# Example usage of Active-Passive failover
async def active_passive_example():
    health_checker = BasicHealthChecker()
    failover = ActivePassiveFailover(health_checker)
    
    # Add nodes
    primary = SystemNode(
        node_id="primary",
        host="10.0.1.10",
        port=8080,
        state=FailoverState.ACTIVE,
        last_heartbeat=datetime.now()
    )
    
    standby1 = SystemNode(
        node_id="standby1",
        host="10.0.1.11",
        port=8080,
        state=FailoverState.STANDBY,
        last_heartbeat=datetime.now()
    )
    
    standby2 = SystemNode(
        node_id="standby2",
        host="10.0.1.12",
        port=8080,
        state=FailoverState.STANDBY,
        last_heartbeat=datetime.now()
    )
    
    failover.add_node(primary)
    failover.add_node(standby1)
    failover.add_node(standby2)
    
    # Add failover callback
    async def on_failover(node, event_type):
        print(f"Failover event: {event_type} for node {node.node_id}")
    
    failover.add_failover_callback(on_failover)
    
    # Start monitoring
    await failover.start_monitoring()
    
    # Get status
    status = await failover.get_cluster_status()
    print(f"Cluster status: {status}")
```

### 2. Active-Active Failover

In active-active configuration, multiple nodes handle traffic simultaneously with load balancing.

```python
class ActiveActiveFailover:
    """Active-Active failover implementation"""
    
    def __init__(self, health_checker: HealthChecker, load_balancer_type: str = "round_robin"):
        self.health_checker = health_checker
        self.nodes: List[SystemNode] = []
        self.active_nodes: List[SystemNode] = []
        self.load_balancer_type = load_balancer_type
        self.current_node_index = 0
        self.heartbeat_monitor = HeartbeatMonitor()
        self.rebalance_callbacks: List[Callable] = []
        
        # Set up heartbeat callback
        self.heartbeat_monitor.add_heartbeat_callback(self._handle_node_failure)
    
    def add_node(self, node: SystemNode):
        """Add node to active-active cluster"""
        self.nodes.append(node)
        
        if node.state == FailoverState.ACTIVE:
            self.active_nodes.append(node)
    
    def add_rebalance_callback(self, callback: Callable):
        """Add callback for rebalancing events"""
        self.rebalance_callbacks.append(callback)
    
    async def start_monitoring(self):
        """Start monitoring cluster health"""
        await self.heartbeat_monitor.start_monitoring(self.nodes)
    
    async def _handle_node_failure(self, failed_node: SystemNode, failure_type: str):
        """Handle node failure in active-active setup"""
        if failed_node in self.active_nodes:
            await self._remove_from_active_pool(failed_node)
            await self._rebalance_load()
    
    async def _remove_from_active_pool(self, failed_node: SystemNode):
        """Remove failed node from active pool"""
        if failed_node in self.active_nodes:
            self.active_nodes.remove(failed_node)
            logging.info(f"Removed failed node {failed_node.node_id} from active pool")
            
            # Try to add standby node to maintain capacity
            await self._promote_standby_if_needed()
    
    async def _promote_standby_if_needed(self):
        """Promote standby node to active if needed"""
        standby_nodes = [
            node for node in self.nodes 
            if node.state == FailoverState.STANDBY
        ]
        
        if standby_nodes:
            # Find best standby node
            best_standby = None
            best_score = 0
            
            for node in standby_nodes:
                if await self.health_checker.check_health(node):
                    score = self.health_checker.get_health_score(node)
                    if score > best_score:
                        best_score = score
                        best_standby = node
            
            if best_standby:
                best_standby.state = FailoverState.ACTIVE
                self.active_nodes.append(best_standby)
                logging.info(f"Promoted standby node {best_standby.node_id} to active")
    
    async def _rebalance_load(self):
        """Rebalance load across active nodes"""
        if not self.active_nodes:
            logging.error("No active nodes available for load balancing")
            return
        
        # Redistribute load evenly
        target_load = 100.0 / len(self.active_nodes)
        
        for node in self.active_nodes:
            node.load_percentage = target_load
        
        # Notify callbacks
        for callback in self.rebalance_callbacks:
            try:
                await callback(self.active_nodes, "load_rebalanced")
            except Exception as e:
                logging.error(f"Error in rebalance callback: {e}")
    
    def get_next_node(self) -> Optional[SystemNode]:
        """Get next node for load balancing"""
        if not self.active_nodes:
            return None
        
        if self.load_balancer_type == "round_robin":
            return self._round_robin_selection()
        elif self.load_balancer_type == "least_loaded":
            return self._least_loaded_selection()
        elif self.load_balancer_type == "weighted":
            return self._weighted_selection()
        else:
            return self._round_robin_selection()
    
    def _round_robin_selection(self) -> SystemNode:
        """Round robin node selection"""
        node = self.active_nodes[self.current_node_index]
        self.current_node_index = (self.current_node_index + 1) % len(self.active_nodes)
        return node
    
    def _least_loaded_selection(self) -> SystemNode:
        """Select least loaded node"""
        return min(self.active_nodes, key=lambda n: n.load_percentage)
    
    def _weighted_selection(self) -> SystemNode:
        """Weighted selection based on health score"""
        import random
        
        weights = [node.health_score for node in self.active_nodes]
        total_weight = sum(weights)
        
        if total_weight == 0:
            return self.active_nodes[0]
        
        normalized_weights = [w / total_weight for w in weights]
        return random.choices(self.active_nodes, weights=normalized_weights)[0]
    
    async def add_node_to_cluster(self, node: SystemNode):
        """Dynamically add node to cluster"""
        self.nodes.append(node)
        
        # Check if node is healthy
        if await self.health_checker.check_health(node):
            node.state = FailoverState.ACTIVE
            self.active_nodes.append(node)
            await self._rebalance_load()
            logging.info(f"Added node {node.node_id} to active cluster")
        else:
            node.state = FailoverState.STANDBY
            logging.warning(f"Added node {node.node_id} as standby (failed health check)")
    
    async def remove_node_from_cluster(self, node_id: str):
        """Gracefully remove node from cluster"""
        node_to_remove = None
        for node in self.nodes:
            if node.node_id == node_id:
                node_to_remove = node
                break
        
        if not node_to_remove:
            logging.error(f"Node {node_id} not found in cluster")
            return
        
        # Remove from active pool if present
        if node_to_remove in self.active_nodes:
            self.active_nodes.remove(node_to_remove)
            await self._rebalance_load()
        
        # Remove from nodes list
        self.nodes.remove(node_to_remove)
        
        logging.info(f"Removed node {node_id} from cluster")
    
    async def get_cluster_status(self) -> Dict[str, Any]:
        """Get current cluster status"""
        return {
            'total_nodes': len(self.nodes),
            'active_nodes': len(self.active_nodes),
            'standby_nodes': len([n for n in self.nodes if n.state == FailoverState.STANDBY]),
            'failed_nodes': len([n for n in self.nodes if n.state == FailoverState.FAILED]),
            'load_balancer_type': self.load_balancer_type,
            'nodes': [
                {
                    'node_id': node.node_id,
                    'state': node.state.value,
                    'health_score': node.health_score,
                    'load_percentage': node.load_percentage,
                    'last_heartbeat': node.last_heartbeat.isoformat()
                }
                for node in self.nodes
            ]
        }

# Example usage of Active-Active failover
async def active_active_example():
    health_checker = BasicHealthChecker()
    failover = ActiveActiveFailover(health_checker, "least_loaded")
    
    # Add nodes
    nodes = [
        SystemNode(f"node{i}", f"10.0.1.{10+i}", 8080, FailoverState.ACTIVE, datetime.now())
        for i in range(3)
    ]
    
    for node in nodes:
        failover.add_node(node)
    
    # Add rebalance callback
    async def on_rebalance(active_nodes, event_type):
        print(f"Rebalance event: {event_type}, active nodes: {len(active_nodes)}")
    
    failover.add_rebalance_callback(on_rebalance)
    
    # Simulate load balancing
    for _ in range(10):
        selected_node = failover.get_next_node()
        if selected_node:
            print(f"Selected node: {selected_node.node_id}")
    
    # Get cluster status
    status = await failover.get_cluster_status()
    print(f"Cluster status: {status}")
```

## Standby Types

### Hot Standby

```python
class HotStandbyFailover:
    """Hot standby with real-time data replication"""
    
    def __init__(self, primary_node: SystemNode, standby_node: SystemNode):
        self.primary_node = primary_node
        self.standby_node = standby_node
        self.replication_lag_ms = 0
        self.max_acceptable_lag_ms = 1000  # 1 second
        self.replication_monitor = ReplicationMonitor()
    
    async def start_replication(self):
        """Start real-time replication to standby"""
        await self.replication_monitor.start_monitoring(
            self.primary_node, 
            self.standby_node
        )
    
    async def failover_to_standby(self) -> bool:
        """Failover to hot standby"""
        
        # Check replication lag
        current_lag = await self.replication_monitor.get_replication_lag()
        
        if current_lag > self.max_acceptable_lag_ms:
            logging.warning(f"High replication lag: {current_lag}ms")
        
        # Promote standby
        self.standby_node.state = FailoverState.ACTIVE
        self.standby_node.is_primary = True
        
        # Demote primary
        self.primary_node.state = FailoverState.FAILED
        self.primary_node.is_primary = False
        
        logging.info("Hot standby failover completed")
        return True

class ReplicationMonitor:
    """Monitor replication between primary and standby"""
    
    async def start_monitoring(self, primary: SystemNode, standby: SystemNode):
        """Start monitoring replication lag"""
        while True:
            lag = await self._measure_replication_lag(primary, standby)
            await asyncio.sleep(1)
    
    async def _measure_replication_lag(self, primary: SystemNode, standby: SystemNode) -> int:
        """Measure replication lag in milliseconds"""
        # Simulate replication lag measurement
        import random
        return random.randint(10, 100)  # 10-100ms lag
    
    async def get_replication_lag(self) -> int:
        """Get current replication lag"""
        return 50  # Mock value
```

### Warm Standby

```python
class WarmStandbyFailover:
    """Warm standby with periodic data synchronization"""
    
    def __init__(self, primary_node: SystemNode, standby_node: SystemNode, 
                 sync_interval_minutes: int = 15):
        self.primary_node = primary_node
        self.standby_node = standby_node
        self.sync_interval_minutes = sync_interval_minutes
        self.last_sync_time = None
        self.sync_in_progress = False
    
    async def start_periodic_sync(self):
        """Start periodic synchronization"""
        while True:
            await self._sync_data()
            await asyncio.sleep(self.sync_interval_minutes * 60)
    
    async def _sync_data(self):
        """Synchronize data from primary to standby"""
        if self.sync_in_progress:
            return
        
        self.sync_in_progress = True
        try:
            logging.info("Starting warm standby data sync")
            
            # Simulate data synchronization
            await asyncio.sleep(2)  # Simulate sync time
            
            self.last_sync_time = datetime.now()
            logging.info("Warm standby sync completed")
            
        except Exception as e:
            logging.error(f"Warm standby sync failed: {e}")
        finally:
            self.sync_in_progress = False
    
    async def failover_to_standby(self) -> bool:
        """Failover to warm standby"""
        
        # Check if recent sync is available
        if self.last_sync_time:
            time_since_sync = datetime.now() - self.last_sync_time
            data_age_minutes = time_since_sync.total_seconds() / 60
            
            logging.info(f"Data age: {data_age_minutes:.1f} minutes")
        
        # Final sync before failover
        await self._sync_data()
        
        # Start standby node
        self.standby_node.state = FailoverState.ACTIVE
        self.standby_node.is_primary = True
        
        # Update primary
        self.primary_node.state = FailoverState.FAILED
        self.primary_node.is_primary = False
        
        logging.info("Warm standby failover completed")
        return True
```

### Cold Standby

```python
class ColdStandbyFailover:
    """Cold standby requiring manual intervention"""
    
    def __init__(self, primary_node: SystemNode, standby_node: SystemNode):
        self.primary_node = primary_node
        self.standby_node = standby_node
        self.backup_location = "/backups/database"
        self.recovery_time_estimate = timedelta(hours=2)
    
    async def create_backup(self):
        """Create backup for cold standby"""
        logging.info("Creating backup for cold standby")
        
        # Simulate backup creation
        await asyncio.sleep(5)
        
        backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        logging.info(f"Backup created: {backup_file}")
        
        return backup_file
    
    async def failover_to_standby(self, backup_file: str) -> bool:
        """Manual failover to cold standby"""
        
        logging.info("Starting cold standby failover")
        
        # Step 1: Start standby node
        logging.info("Starting standby node...")
        await asyncio.sleep(30)  # Simulate node startup
        
        # Step 2: Restore from backup
        logging.info(f"Restoring from backup: {backup_file}")
        await asyncio.sleep(60)  # Simulate backup restoration
        
        # Step 3: Verify data integrity
        logging.info("Verifying data integrity...")
        await asyncio.sleep(10)
        
        # Step 4: Activate standby
        self.standby_node.state = FailoverState.ACTIVE
        self.standby_node.is_primary = True
        
        # Step 5: Deactivate primary
        self.primary_node.state = FailoverState.FAILED
        self.primary_node.is_primary = False
        
        logging.info("Cold standby failover completed")
        return True
    
    def get_recovery_estimate(self) -> timedelta:
        """Get estimated recovery time"""
        return self.recovery_time_estimate
```

## Failover Testing and Validation

### Disaster Recovery Testing

```python
class FailoverTestSuite:
    """Comprehensive failover testing suite"""
    
    def __init__(self, failover_system):
        self.failover_system = failover_system
        self.test_results: List[Dict] = []
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run complete failover test suite"""
        
        test_methods = [
            self.test_primary_node_failure,
            self.test_network_partition,
            self.test_gradual_degradation,
            self.test_simultaneous_failures,
            self.test_manual_failover,
            self.test_failback_process,
            self.test_split_brain_prevention
        ]
        
        results = {
            'total_tests': len(test_methods),
            'passed': 0,
            'failed': 0,
            'test_details': []
        }
        
        for test_method in test_methods:
            try:
                test_result = await test_method()
                if test_result['passed']:
                    results['passed'] += 1
                else:
                    results['failed'] += 1
                results['test_details'].append(test_result)
            except Exception as e:
                results['failed'] += 1
                results['test_details'].append({
                    'test_name': test_method.__name__,
                    'passed': False,
                    'error': str(e),
                    'duration_seconds': 0
                })
        
        return results
    
    async def test_primary_node_failure(self) -> Dict[str, Any]:
        """Test primary node failure scenario"""
        start_time = datetime.now()
        
        try:
            # Get initial state
            initial_status = await self.failover_system.get_cluster_status()
            initial_primary = initial_status.get('primary_node')
            
            # Simulate primary node failure
            for node in self.failover_system.nodes:
                if node.node_id == initial_primary:
                    node.state = FailoverState.FAILED
                    break
            
            # Wait for failover
            await asyncio.sleep(5)
            
            # Check if failover occurred
            final_status = await self.failover_system.get_cluster_status()
            final_primary = final_status.get('primary_node')
            
            passed = (final_primary != initial_primary and 
                     final_primary is not None)
            
            return {
                'test_name': 'primary_node_failure',
                'passed': passed,
                'initial_primary': initial_primary,
                'final_primary': final_primary,
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
            
        except Exception as e:
            return {
                'test_name': 'primary_node_failure',
                'passed': False,
                'error': str(e),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
    
    async def test_network_partition(self) -> Dict[str, Any]:
        """Test network partition scenario"""
        start_time = datetime.now()
        
        try:
            # Simulate network partition by stopping heartbeats
            original_timeout = self.failover_system.heartbeat_monitor.timeout_seconds
            self.failover_system.heartbeat_monitor.timeout_seconds = 1
            
            # Stop updating heartbeats for primary node
            primary_node = self.failover_system.primary_node
            if primary_node:
                # Simulate old heartbeat
                primary_node.last_heartbeat = datetime.now() - timedelta(seconds=10)
            
            # Wait for detection
            await asyncio.sleep(3)
            
            # Check if failover occurred
            status = await self.failover_system.get_cluster_status()
            
            # Restore original timeout
            self.failover_system.heartbeat_monitor.timeout_seconds = original_timeout
            
            passed = status.get('primary_node') != primary_node.node_id if primary_node else False
            
            return {
                'test_name': 'network_partition',
                'passed': passed,
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
            
        except Exception as e:
            return {
                'test_name': 'network_partition',
                'passed': False,
                'error': str(e),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
    
    async def test_gradual_degradation(self) -> Dict[str, Any]:
        """Test gradual performance degradation"""
        start_time = datetime.now()
        
        try:
            # Gradually increase load on primary node
            primary_node = self.failover_system.primary_node
            if primary_node:
                primary_node.load_percentage = 95
                primary_node.health_score = 0.2
            
            # Check if system responds appropriately
            await asyncio.sleep(2)
            
            # For active-active, check if load is rebalanced
            # For active-passive, check if failover threshold is respected
            
            status = await self.failover_system.get_cluster_status()
            
            passed = True  # Implementation depends on specific logic
            
            return {
                'test_name': 'gradual_degradation',
                'passed': passed,
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
            
        except Exception as e:
            return {
                'test_name': 'gradual_degradation',
                'passed': False,
                'error': str(e),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
    
    async def test_simultaneous_failures(self) -> Dict[str, Any]:
        """Test multiple simultaneous node failures"""
        start_time = datetime.now()
        
        try:
            # Fail multiple nodes simultaneously
            nodes_to_fail = self.failover_system.nodes[:2]  # Fail first 2 nodes
            
            for node in nodes_to_fail:
                node.state = FailoverState.FAILED
            
            await asyncio.sleep(3)
            
            # Check if system maintains availability
            status = await self.failover_system.get_cluster_status()
            active_nodes = [n for n in status['nodes'] if n['state'] == 'active']
            
            passed = len(active_nodes) > 0
            
            return {
                'test_name': 'simultaneous_failures',
                'passed': passed,
                'active_nodes_remaining': len(active_nodes),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
            
        except Exception as e:
            return {
                'test_name': 'simultaneous_failures',
                'passed': False,
                'error': str(e),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
    
    async def test_manual_failover(self) -> Dict[str, Any]:
        """Test manual failover functionality"""
        start_time = datetime.now()
        
        try:
            # Get initial state
            initial_status = await self.failover_system.get_cluster_status()
            initial_primary = initial_status.get('primary_node')
            
            # Find a standby node for manual failover
            target_node = None
            for node_info in initial_status['nodes']:
                if node_info['state'] == 'standby':
                    target_node = node_info['node_id']
                    break
            
            if not target_node:
                return {
                    'test_name': 'manual_failover',
                    'passed': False,
                    'error': 'No standby node available',
                    'duration_seconds': (datetime.now() - start_time).total_seconds()
                }
            
            # Perform manual failover
            success = await self.failover_system.manual_failover(target_node)
            
            # Verify failover
            final_status = await self.failover_system.get_cluster_status()
            final_primary = final_status.get('primary_node')
            
            passed = success and final_primary == target_node
            
            return {
                'test_name': 'manual_failover',
                'passed': passed,
                'initial_primary': initial_primary,
                'target_node': target_node,
                'final_primary': final_primary,
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
            
        except Exception as e:
            return {
                'test_name': 'manual_failover',
                'passed': False,
                'error': str(e),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
    
    async def test_failback_process(self) -> Dict[str, Any]:
        """Test failback to original primary"""
        start_time = datetime.now()
        
        try:
            # This test assumes previous failover occurred
            # Simulate original primary recovery
            
            for node in self.failover_system.nodes:
                if node.state == FailoverState.FAILED:
                    # Simulate node recovery
                    node.state = FailoverState.STANDBY
                    node.health_score = 1.0
                    node.last_heartbeat = datetime.now()
                    break
            
            # Wait for system to detect recovery
            await asyncio.sleep(2)
            
            # Check if failback can be performed
            status = await self.failover_system.get_cluster_status()
            standby_nodes = [n for n in status['nodes'] if n['state'] == 'standby']
            
            passed = len(standby_nodes) > 0
            
            return {
                'test_name': 'failback_process',
                'passed': passed,
                'standby_nodes_available': len(standby_nodes),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
            
        except Exception as e:
            return {
                'test_name': 'failback_process',
                'passed': False,
                'error': str(e),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
    
    async def test_split_brain_prevention(self) -> Dict[str, Any]:
        """Test split-brain scenario prevention"""
        start_time = datetime.now()
        
        try:
            # Simulate split-brain scenario
            # This is a complex test that would involve network partitioning
            
            # For now, check that only one primary exists
            status = await self.failover_system.get_cluster_status()
            primary_nodes = [n for n in status['nodes'] if n.get('is_primary', False)]
            
            passed = len(primary_nodes) <= 1
            
            return {
                'test_name': 'split_brain_prevention',
                'passed': passed,
                'primary_nodes_count': len(primary_nodes),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }
            
        except Exception as e:
            return {
                'test_name': 'split_brain_prevention',
                'passed': False,
                'error': str(e),
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            }

# Example usage
async def failover_testing_example():
    # Set up failover system
    health_checker = BasicHealthChecker()
    failover = ActivePassiveFailover(health_checker)
    
    # Add test nodes
    nodes = [
        SystemNode(f"node{i}", f"10.0.1.{10+i}", 8080, 
                  FailoverState.ACTIVE if i == 0 else FailoverState.STANDBY, 
                  datetime.now())
        for i in range(3)
    ]
    
    for node in nodes:
        failover.add_node(node)
    
    # Run tests
    test_suite = FailoverTestSuite(failover)
    results = await test_suite.run_all_tests()
    
    print(f"Test Results: {results['passed']}/{results['total_tests']} passed")
    for test in results['test_details']:
        status = "PASS" if test['passed'] else "FAIL"
        print(f"  {test['test_name']}: {status} ({test['duration_seconds']:.2f}s)")
```

## Best Practices and Considerations

### Monitoring and Alerting

```python
class FailoverMonitoring:
    """Comprehensive monitoring for failover systems"""
    
    def __init__(self, failover_system):
        self.failover_system = failover_system
        self.metrics = {
            'failover_count': 0,
            'total_downtime_seconds': 0,
            'last_failover_time': None,
            'average_failover_time': 0,
            'false_positive_count': 0
        }
        self.alert_thresholds = {
            'max_failover_time_seconds': 30,
            'max_failovers_per_hour': 3,
            'min_healthy_nodes': 1
        }
    
    async def start_monitoring(self):
        """Start continuous monitoring"""
        while True:
            await self._collect_metrics()
            await self._check_alert_conditions()
            await asyncio.sleep(10)  # Check every 10 seconds
    
    async def _collect_metrics(self):
        """Collect system metrics"""
        status = await self.failover_system.get_cluster_status()
        
        # Update node health metrics
        for node_info in status['nodes']:
            if node_info['state'] == 'failed':
                # Track failed nodes
                pass
        
        # Calculate uptime
        active_nodes = [n for n in status['nodes'] if n['state'] == 'active']
        self.metrics['healthy_nodes'] = len(active_nodes)
    
    async def _check_alert_conditions(self):
        """Check alert conditions and send notifications"""
        
        # Check minimum healthy nodes
        if self.metrics['healthy_nodes'] < self.alert_thresholds['min_healthy_nodes']:
            await self._send_alert("CRITICAL", "Insufficient healthy nodes")
        
        # Check failover frequency
        if self._get_recent_failover_count() > self.alert_thresholds['max_failovers_per_hour']:
            await self._send_alert("WARNING", "High failover frequency detected")
    
    def _get_recent_failover_count(self) -> int:
        """Get failover count in last hour"""
        # Implementation would track recent failovers
        return 0
    
    async def _send_alert(self, severity: str, message: str):
        """Send alert notification"""
        timestamp = datetime.now().isoformat()
        alert = f"[{severity}] {timestamp}: {message}"
        
        # In practice, this would send to alerting system
        logging.warning(alert)
    
    def record_failover_event(self, duration_seconds: float):
        """Record failover event for metrics"""
        self.metrics['failover_count'] += 1
        self.metrics['total_downtime_seconds'] += duration_seconds
        self.metrics['last_failover_time'] = datetime.now()
        
        # Update average
        self.metrics['average_failover_time'] = (
            self.metrics['total_downtime_seconds'] / self.metrics['failover_count']
        )
    
    def get_monitoring_dashboard(self) -> Dict[str, Any]:
        """Get monitoring dashboard data"""
        return {
            'system_status': 'healthy' if self.metrics['healthy_nodes'] > 0 else 'degraded',
            'total_failovers': self.metrics['failover_count'],
            'average_failover_time': self.metrics['average_failover_time'],
            'last_failover': self.metrics['last_failover_time'].isoformat() if self.metrics['last_failover_time'] else None,
            'healthy_nodes': self.metrics['healthy_nodes'],
            'uptime_percentage': self._calculate_uptime_percentage()
        }
    
    def _calculate_uptime_percentage(self) -> float:
        """Calculate system uptime percentage"""
        # Simplified calculation
        total_time = 86400  # 24 hours in seconds
        downtime = self.metrics['total_downtime_seconds']
        uptime_percentage = ((total_time - downtime) / total_time) * 100
        return max(0, min(100, uptime_percentage))
```

### Configuration Management

```python
class FailoverConfiguration:
    """Manage failover system configuration"""
    
    def __init__(self):
        self.config = {
            'heartbeat_timeout_seconds': 30,
            'health_check_interval_seconds': 5,
            'failover_timeout_seconds': 60,
            'max_failover_attempts': 3,
            'enable_automatic_failback': False,
            'require_manual_intervention': False,
            'notification_endpoints': [],
            'backup_retention_days': 30,
            'split_brain_prevention': True
        }
    
    def load_config(self, config_file: str):
        """Load configuration from file"""
        # Implementation would load from JSON/YAML file
        pass
    
    def save_config(self, config_file: str):
        """Save configuration to file"""
        # Implementation would save to JSON/YAML file
        pass
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return errors"""
        errors = []
        
        if self.config['heartbeat_timeout_seconds'] < 5:
            errors.append("Heartbeat timeout too low (minimum 5 seconds)")
        
        if self.config['failover_timeout_seconds'] < 30:
            errors.append("Failover timeout too low (minimum 30 seconds)")
        
        return errors
    
    def get_config(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
```

## Conclusion

Failover systems are essential for maintaining high availability and business continuity in distributed systems. Key considerations include:

### Failover Strategy Selection
- **Active-Passive**: Simple but with resource waste and longer failover times
- **Active-Active**: Better resource utilization but more complex implementation
- **Hot Standby**: Minimal downtime but requires real-time replication
- **Warm/Cold Standby**: Lower cost but longer recovery times

### Implementation Best Practices
- **Comprehensive Monitoring**: Monitor all components with appropriate alerting
- **Regular Testing**: Conduct regular disaster recovery tests
- **Clear Procedures**: Document manual intervention procedures
- **Split-Brain Prevention**: Implement mechanisms to prevent multiple primaries
- **Gradual Rollout**: Test failover procedures in non-production environments first

### Success Factors
- **Recovery Time Objective (RTO)**: Define acceptable downtime
- **Recovery Point Objective (RPO)**: Define acceptable data loss
- **Automated vs Manual**: Balance automation with human oversight
- **Testing and Validation**: Regular testing ensures procedures work when needed

Effective failover systems require careful planning, thorough testing, and ongoing maintenance to ensure they provide the expected level of reliability and availability when failures occur.