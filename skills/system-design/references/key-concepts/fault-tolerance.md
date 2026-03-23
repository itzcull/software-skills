---
title: Fault Tolerance
description: Understanding fault tolerance in distributed systems, types of faults, and comprehensive strategies for building resilient systems that can handle failures gracefully
source: https://www.cockroachlabs.com/blog/what-is-fault-tolerance/
tags: [fault-tolerance, resilience, distributed-systems, reliability, error-recovery, redundancy, high-availability]
category: key-concepts
---

# Fault Tolerance

## Definition

> Fault tolerance describes a system's ability to handle errors and outages without any loss of functionality.

Fault tolerance is a critical property of distributed systems that ensures continuous operation even when components fail. It encompasses the system's capability to detect, isolate, and recover from failures while maintaining acceptable levels of service quality and data integrity.

## Why Fault Tolerance Matters

### Business Impact of Downtime

**Revenue Loss**
- E-commerce sites can lose thousands of dollars per minute of downtime
- SaaS platforms face immediate subscription and usage-based revenue loss
- Financial services risk regulatory penalties and customer churn

**Reputation Damage**
- Customer trust erodes with each outage
- Negative social media coverage amplifies impact
- Competitor advantage during service disruptions

**Operational Costs**
- Emergency response and incident management
- Engineering time diverted from feature development
- Potential legal and compliance consequences

### The Economics of Fault Tolerance

```python
class DowntimeCostCalculator:
    def __init__(self, hourly_revenue, customer_count, reputation_factor=1.5):
        self.hourly_revenue = hourly_revenue
        self.customer_count = customer_count
        self.reputation_factor = reputation_factor
    
    def calculate_downtime_cost(self, downtime_hours):
        """Calculate total cost of downtime"""
        
        # Direct revenue loss
        direct_loss = self.hourly_revenue * downtime_hours
        
        # Customer acquisition cost impact
        # Assume 2% customer churn per hour of downtime
        churn_rate = 0.02 * downtime_hours
        customer_acquisition_cost = 100  # Average cost to acquire new customer
        churn_cost = self.customer_count * churn_rate * customer_acquisition_cost
        
        # Reputation and future business impact
        reputation_cost = direct_loss * (self.reputation_factor - 1)
        
        # Engineering response cost
        incident_response_cost = 500 * downtime_hours  # $500/hour for incident response
        
        total_cost = direct_loss + churn_cost + reputation_cost + incident_response_cost
        
        return {
            'direct_revenue_loss': direct_loss,
            'customer_churn_cost': churn_cost,
            'reputation_impact': reputation_cost,
            'incident_response_cost': incident_response_cost,
            'total_cost': total_cost
        }

# Example: E-commerce site with $10K/hour revenue, 100K customers
cost_calculator = DowntimeCostCalculator(
    hourly_revenue=10000,
    customer_count=100000,
    reputation_factor=2.0
)

# Cost of 2-hour outage
outage_cost = cost_calculator.calculate_downtime_cost(2)
print(f"Total cost of 2-hour outage: ${outage_cost['total_cost']:,.2f}")
```

## Types of Faults

### 1. Hardware Faults

**Characteristics**:
- Physical component failures (CPU, memory, storage, network interfaces)
- Power supply failures and electrical issues
- Environmental factors (cooling, humidity, physical damage)

**Examples**:
```python
class HardwareFaultSimulator:
    def __init__(self):
        self.fault_types = {
            'disk_failure': {'probability': 0.001, 'impact': 'data_loss'},
            'memory_error': {'probability': 0.0005, 'impact': 'process_crash'},
            'network_interface_failure': {'probability': 0.0002, 'impact': 'connectivity_loss'},
            'power_supply_failure': {'probability': 0.0001, 'impact': 'system_shutdown'},
            'cpu_overheating': {'probability': 0.00005, 'impact': 'performance_degradation'}
        }
    
    def simulate_hardware_fault(self, server_id):
        """Simulate random hardware fault"""
        import random
        
        for fault_type, properties in self.fault_types.items():
            if random.random() < properties['probability']:
                return {
                    'server_id': server_id,
                    'fault_type': fault_type,
                    'impact': properties['impact'],
                    'timestamp': time.time(),
                    'recovery_strategy': self.get_recovery_strategy(fault_type)
                }
        
        return None  # No fault occurred
    
    def get_recovery_strategy(self, fault_type):
        """Get recommended recovery strategy for fault type"""
        strategies = {
            'disk_failure': 'Replace disk, restore from backup',
            'memory_error': 'Restart process, check memory modules',
            'network_interface_failure': 'Switch to backup interface, replace NIC',
            'power_supply_failure': 'Switch to backup power, replace PSU',
            'cpu_overheating': 'Improve cooling, reduce load'
        }
        return strategies.get(fault_type, 'Contact hardware support')
```

### 2. Software Faults

**Characteristics**:
- Application bugs and logic errors
- Memory leaks and resource exhaustion
- Deadlocks and race conditions
- Configuration errors

**Examples**:
```python
class SoftwareFaultHandler:
    def __init__(self):
        self.error_patterns = {
            'memory_leak': self.handle_memory_leak,
            'deadlock': self.handle_deadlock,
            'null_pointer': self.handle_null_pointer,
            'configuration_error': self.handle_config_error,
            'dependency_failure': self.handle_dependency_failure
        }
        self.circuit_breakers = {}
    
    def handle_software_fault(self, error_type, error_details):
        """Handle different types of software faults"""
        if error_type in self.error_patterns:
            return self.error_patterns[error_type](error_details)
        else:
            return self.handle_unknown_error(error_type, error_details)
    
    def handle_memory_leak(self, error_details):
        """Handle memory leak detection"""
        return {
            'action': 'restart_process',
            'monitoring': 'increase_memory_monitoring',
            'prevention': 'enable_memory_profiling',
            'escalation': 'alert_development_team'
        }
    
    def handle_deadlock(self, error_details):
        """Handle deadlock scenarios"""
        return {
            'action': 'kill_deadlocked_processes',
            'monitoring': 'enable_deadlock_detection',
            'prevention': 'implement_timeout_mechanisms',
            'code_review': 'review_locking_strategy'
        }
    
    def handle_dependency_failure(self, error_details):
        """Handle external dependency failures"""
        dependency = error_details.get('dependency')
        
        # Implement circuit breaker pattern
        if dependency not in self.circuit_breakers:
            self.circuit_breakers[dependency] = CircuitBreaker(
                failure_threshold=5,
                recovery_timeout=60
            )
        
        return {
            'action': 'enable_circuit_breaker',
            'fallback': 'use_cached_data_or_degraded_service',
            'monitoring': 'track_dependency_health',
            'alerting': 'notify_dependency_team'
        }

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def is_request_allowed(self):
        """Check if request should be allowed through circuit breaker"""
        if self.state == 'CLOSED':
            return True
        elif self.state == 'OPEN':
            if self.should_attempt_reset():
                self.state = 'HALF_OPEN'
                return True
            return False
        else:  # HALF_OPEN
            return True
    
    def record_success(self):
        """Record successful request"""
        if self.state == 'HALF_OPEN':
            self.state = 'CLOSED'
            self.failure_count = 0
    
    def record_failure(self):
        """Record failed request"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
```

### 3. Network Faults

**Characteristics**:
- Network partitions and connectivity loss
- Packet loss and high latency
- DNS resolution failures
- Load balancer failures

**Examples**:
```python
class NetworkFaultTolerance:
    def __init__(self):
        self.retry_config = {
            'max_retries': 3,
            'base_delay': 1,
            'max_delay': 30,
            'backoff_multiplier': 2
        }
        self.timeout_config = {
            'connection_timeout': 10,
            'read_timeout': 30,
            'total_timeout': 60
        }
    
    def make_network_request(self, url, data=None, method='GET'):
        """Make network request with fault tolerance"""
        for attempt in range(self.retry_config['max_retries'] + 1):
            try:
                response = self.execute_request(url, data, method)
                return response
                
            except NetworkError as e:
                if attempt == self.retry_config['max_retries']:
                    # Final attempt failed
                    raise FinalNetworkError(f"Request failed after {attempt + 1} attempts: {e}")
                
                # Calculate delay for next retry
                delay = min(
                    self.retry_config['base_delay'] * (
                        self.retry_config['backoff_multiplier'] ** attempt
                    ),
                    self.retry_config['max_delay']
                )
                
                print(f"Request attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
    
    def execute_request(self, url, data, method):
        """Execute HTTP request with timeouts"""
        import requests
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                timeout=(
                    self.timeout_config['connection_timeout'],
                    self.timeout_config['read_timeout']
                )
            )
            
            if response.status_code >= 500:
                raise NetworkError(f"Server error: {response.status_code}")
            
            return response
            
        except requests.exceptions.Timeout:
            raise NetworkError("Request timeout")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Connection failed")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request error: {e}")

class NetworkPartitionHandler:
    def __init__(self, nodes):
        self.nodes = nodes
        self.partition_detector = PartitionDetector()
        self.consensus_algorithm = RaftConsensus()
    
    def handle_network_partition(self):
        """Handle network partition scenarios"""
        partitions = self.partition_detector.detect_partitions(self.nodes)
        
        if len(partitions) > 1:
            # Network partition detected
            majority_partition = self.find_majority_partition(partitions)
            
            if majority_partition:
                # Continue operating with majority partition
                self.enable_majority_partition_mode(majority_partition)
                self.disable_minority_partitions(partitions, majority_partition)
            else:
                # No majority - enter read-only mode
                self.enter_read_only_mode()
    
    def find_majority_partition(self, partitions):
        """Find partition with majority of nodes"""
        total_nodes = sum(len(partition) for partition in partitions)
        majority_threshold = total_nodes // 2 + 1
        
        for partition in partitions:
            if len(partition) >= majority_threshold:
                return partition
        
        return None
```

### 4. Byzantine Faults

**Characteristics**:
- Malicious or corrupted nodes providing incorrect information
- Nodes that appear to be working but produce wrong results
- Security breaches and compromised systems

**Examples**:
```python
class ByzantineFaultTolerance:
    def __init__(self, total_nodes):
        self.total_nodes = total_nodes
        self.max_byzantine_nodes = (total_nodes - 1) // 3
        self.consensus_threshold = 2 * self.max_byzantine_nodes + 1
    
    def byzantine_consensus(self, proposals):
        """Achieve consensus despite Byzantine faults"""
        # Practical Byzantine Fault Tolerance (PBFT) simulation
        
        # Phase 1: Pre-prepare
        primary_proposal = self.select_primary_proposal(proposals)
        pre_prepare_votes = self.collect_pre_prepare_votes(primary_proposal)
        
        if len(pre_prepare_votes) < self.consensus_threshold:
            return None  # Cannot achieve consensus
        
        # Phase 2: Prepare
        prepare_votes = self.collect_prepare_votes(primary_proposal)
        
        if len(prepare_votes) < self.consensus_threshold:
            return None  # Cannot achieve consensus
        
        # Phase 3: Commit
        commit_votes = self.collect_commit_votes(primary_proposal)
        
        if len(commit_votes) < self.consensus_threshold:
            return None  # Cannot achieve consensus
        
        return primary_proposal  # Consensus achieved
    
    def detect_byzantine_behavior(self, node_responses):
        """Detect potentially Byzantine nodes"""
        response_counts = {}
        
        # Count identical responses
        for node_id, response in node_responses.items():
            response_hash = hash(str(response))
            if response_hash not in response_counts:
                response_counts[response_hash] = []
            response_counts[response_hash].append(node_id)
        
        # Find responses with insufficient support
        suspicious_nodes = []
        for response_hash, supporting_nodes in response_counts.items():
            if len(supporting_nodes) < self.consensus_threshold:
                suspicious_nodes.extend(supporting_nodes)
        
        return suspicious_nodes
    
    def quarantine_byzantine_nodes(self, suspicious_nodes):
        """Quarantine nodes showing Byzantine behavior"""
        for node_id in suspicious_nodes:
            # Remove node from active consensus
            # Investigate node behavior
            # Alert security team
            self.remove_from_consensus(node_id)
            self.log_security_incident(node_id)

class SecurityFaultHandler:
    def __init__(self):
        self.security_monitors = {}
        self.threat_detector = ThreatDetector()
    
    def handle_security_fault(self, fault_type, fault_details):
        """Handle security-related faults"""
        
        security_responses = {
            'unauthorized_access': self.handle_unauthorized_access,
            'data_corruption': self.handle_data_corruption,
            'malicious_input': self.handle_malicious_input,
            'insider_threat': self.handle_insider_threat,
            'denial_of_service': self.handle_dos_attack
        }
        
        if fault_type in security_responses:
            return security_responses[fault_type](fault_details)
        else:
            return self.handle_unknown_security_threat(fault_type, fault_details)
    
    def handle_unauthorized_access(self, details):
        """Handle unauthorized access attempts"""
        return {
            'immediate_action': 'revoke_access_tokens',
            'investigation': 'audit_access_logs',
            'prevention': 'strengthen_authentication',
            'monitoring': 'increase_access_monitoring'
        }
    
    def handle_data_corruption(self, details):
        """Handle data corruption incidents"""
        return {
            'immediate_action': 'isolate_corrupted_data',
            'recovery': 'restore_from_verified_backup',
            'validation': 'implement_data_integrity_checks',
            'investigation': 'trace_corruption_source'
        }
```

## Fault Tolerance Strategies

### 1. Redundancy and Replication

#### Hardware Redundancy

```python
class HardwareRedundancyManager:
    def __init__(self):
        self.redundancy_configs = {
            'servers': {'type': 'N+1', 'minimum_spares': 1},
            'power_supplies': {'type': 'N+1', 'dual_supply': True},
            'network_interfaces': {'type': 'active_active', 'bonding': True},
            'storage': {'type': 'RAID', 'level': 'RAID10'}
        }
    
    def design_redundant_architecture(self, requirements):
        """Design hardware architecture with redundancy"""
        
        architecture = {
            'compute_nodes': self.calculate_server_redundancy(requirements),
            'storage_nodes': self.design_storage_redundancy(requirements),
            'network_infrastructure': self.design_network_redundancy(requirements),
            'power_infrastructure': self.design_power_redundancy(requirements)
        }
        
        return architecture
    
    def calculate_server_redundancy(self, requirements):
        """Calculate required server redundancy"""
        base_capacity = requirements['peak_load']
        redundancy_factor = self.redundancy_configs['servers']['minimum_spares']
        
        required_servers = base_capacity + redundancy_factor
        
        return {
            'total_servers': required_servers,
            'active_servers': base_capacity,
            'spare_servers': redundancy_factor,
            'availability_zones': 3,  # Distribute across AZs
            'failover_strategy': 'automatic'
        }
    
    def design_storage_redundancy(self, requirements):
        """Design storage with redundancy"""
        storage_config = self.redundancy_configs['storage']
        
        return {
            'raid_level': storage_config['level'],
            'replication_factor': 3,
            'cross_zone_replication': True,
            'backup_strategy': {
                'local_snapshots': 'hourly',
                'cross_region_backup': 'daily',
                'retention_policy': '30_days'
            }
        }

class DataReplicationManager:
    def __init__(self):
        self.replication_strategies = {
            'synchronous': SynchronousReplication(),
            'asynchronous': AsynchronousReplication(),
            'semi_synchronous': SemiSynchronousReplication()
        }
    
    def setup_replication(self, primary_node, replica_nodes, strategy='synchronous'):
        """Setup data replication between nodes"""
        
        replication_handler = self.replication_strategies[strategy]
        
        replication_config = {
            'primary': primary_node,
            'replicas': replica_nodes,
            'consistency_level': self.get_consistency_level(strategy),
            'conflict_resolution': self.get_conflict_resolution_strategy(strategy),
            'monitoring': self.setup_replication_monitoring()
        }
        
        return replication_handler.configure(replication_config)
    
    def handle_replication_failure(self, failed_replica):
        """Handle replica failure scenarios"""
        
        # Remove failed replica from active set
        self.remove_replica(failed_replica)
        
        # Provision new replica
        new_replica = self.provision_new_replica()
        
        # Sync new replica with primary
        self.sync_replica(new_replica)
        
        # Add to active replica set
        self.add_replica(new_replica)
        
        return new_replica

class SynchronousReplication:
    def replicate_write(self, primary, replicas, data):
        """Synchronously replicate write to all replicas"""
        
        # Write to primary first
        primary_result = primary.write(data)
        
        replica_results = []
        failed_replicas = []
        
        # Write to all replicas
        for replica in replicas:
            try:
                result = replica.write(data)
                replica_results.append(result)
            except Exception as e:
                failed_replicas.append({'replica': replica, 'error': e})
        
        # Check if majority succeeded
        total_nodes = 1 + len(replicas)  # Primary + replicas
        successful_writes = 1 + len(replica_results)  # Primary + successful replicas
        
        if successful_writes >= (total_nodes // 2 + 1):
            return {'status': 'success', 'failed_replicas': failed_replicas}
        else:
            # Rollback primary write
            primary.rollback(data)
            raise ReplicationError("Failed to achieve majority consensus")

class AsynchronousReplication:
    def __init__(self):
        self.replication_queue = Queue()
        self.replication_worker = ReplicationWorker(self.replication_queue)
    
    def replicate_write(self, primary, replicas, data):
        """Asynchronously replicate write to replicas"""
        
        # Write to primary immediately
        primary_result = primary.write(data)
        
        # Queue replication to replicas
        for replica in replicas:
            self.replication_queue.put({
                'replica': replica,
                'data': data,
                'timestamp': time.time()
            })
        
        return {'status': 'success', 'replication': 'queued'}

class ReplicationWorker:
    def __init__(self, queue):
        self.queue = queue
        self.running = True
        self.worker_thread = threading.Thread(target=self.process_replications)
        self.worker_thread.start()
    
    def process_replications(self):
        """Process replication queue"""
        while self.running:
            try:
                replication_task = self.queue.get(timeout=1)
                
                replica = replication_task['replica']
                data = replication_task['data']
                
                replica.write(data)
                
                self.queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                # Handle replication failure
                self.handle_replication_failure(replication_task, e)
```

### 2. Graceful Degradation

```python
class GracefulDegradationManager:
    def __init__(self):
        self.service_dependencies = {}
        self.degradation_strategies = {}
        self.feature_flags = FeatureFlags()
    
    def register_service_dependency(self, service_name, dependency_config):
        """Register service dependencies for degradation planning"""
        self.service_dependencies[service_name] = {
            'critical_dependencies': dependency_config.get('critical', []),
            'optional_dependencies': dependency_config.get('optional', []),
            'degradation_mode': dependency_config.get('degradation_mode', 'disable'),
            'fallback_strategy': dependency_config.get('fallback', None)
        }
    
    def handle_dependency_failure(self, failed_dependency):
        """Handle failure of a service dependency"""
        
        affected_services = self.find_affected_services(failed_dependency)
        
        for service_name in affected_services:
            dependency_config = self.service_dependencies[service_name]
            
            if failed_dependency in dependency_config['critical_dependencies']:
                # Critical dependency failed - major degradation
                self.apply_major_degradation(service_name, failed_dependency)
            else:
                # Optional dependency failed - minor degradation
                self.apply_minor_degradation(service_name, failed_dependency)
    
    def apply_major_degradation(self, service_name, failed_dependency):
        """Apply major degradation when critical dependency fails"""
        
        config = self.service_dependencies[service_name]
        
        if config['degradation_mode'] == 'disable':
            # Disable service entirely
            self.disable_service(service_name)
            
        elif config['degradation_mode'] == 'fallback':
            # Switch to fallback implementation
            self.enable_fallback_mode(service_name, config['fallback_strategy'])
            
        elif config['degradation_mode'] == 'cache_only':
            # Serve only cached data
            self.enable_cache_only_mode(service_name)
    
    def apply_minor_degradation(self, service_name, failed_dependency):
        """Apply minor degradation when optional dependency fails"""
        
        # Disable non-essential features
        self.feature_flags.disable_features_for_dependency(failed_dependency)
        
        # Log degradation for monitoring
        self.log_service_degradation(service_name, failed_dependency, 'minor')

class FeatureFlags:
    def __init__(self):
        self.flags = {}
        self.dependency_mappings = {}
    
    def define_feature_flag(self, flag_name, default_value, dependencies=None):
        """Define a feature flag with dependencies"""
        self.flags[flag_name] = {
            'enabled': default_value,
            'dependencies': dependencies or [],
            'degradation_fallback': None
        }
    
    def is_enabled(self, flag_name):
        """Check if feature flag is enabled"""
        if flag_name not in self.flags:
            return False
        
        flag_config = self.flags[flag_name]
        
        # Check if all dependencies are healthy
        for dependency in flag_config['dependencies']:
            if not self.is_dependency_healthy(dependency):
                return False
        
        return flag_config['enabled']
    
    def disable_features_for_dependency(self, failed_dependency):
        """Disable features that depend on a failed dependency"""
        for flag_name, flag_config in self.flags.items():
            if failed_dependency in flag_config['dependencies']:
                flag_config['enabled'] = False
                
                # Enable fallback if available
                if flag_config['degradation_fallback']:
                    self.enable_fallback_feature(flag_name, flag_config['degradation_fallback'])

# Example usage
degradation_manager = GracefulDegradationManager()

# Register service dependencies
degradation_manager.register_service_dependency('user_recommendations', {
    'critical': ['user_database'],
    'optional': ['ml_service', 'external_api'],
    'degradation_mode': 'fallback',
    'fallback': 'basic_recommendations'
})

degradation_manager.register_service_dependency('search_service', {
    'critical': ['search_index'],
    'optional': ['autocomplete_service', 'spell_checker'],
    'degradation_mode': 'cache_only'
})

# Define feature flags
feature_flags = FeatureFlags()
feature_flags.define_feature_flag('advanced_search', True, ['search_index', 'ml_service'])
feature_flags.define_feature_flag('real_time_notifications', True, ['websocket_service'])
```

### 3. Consensus Algorithms

```python
class RaftConsensus:
    def __init__(self, node_id, cluster_nodes):
        self.node_id = node_id
        self.cluster_nodes = cluster_nodes
        self.state = 'FOLLOWER'  # FOLLOWER, CANDIDATE, LEADER
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        
        # Leader state
        self.next_index = {}
        self.match_index = {}
        
        # Election timeout
        self.election_timeout = random.uniform(150, 300)  # milliseconds
        self.last_heartbeat = time.time()
    
    def start_election(self):
        """Start leader election process"""
        self.state = 'CANDIDATE'
        self.current_term += 1
        self.voted_for = self.node_id
        
        votes_received = 1  # Vote for self
        
        # Request votes from other nodes
        for node in self.cluster_nodes:
            if node != self.node_id:
                vote_response = self.request_vote(node)
                if vote_response and vote_response.get('vote_granted'):
                    votes_received += 1
        
        # Check if majority achieved
        majority_threshold = len(self.cluster_nodes) // 2 + 1
        
        if votes_received >= majority_threshold:
            self.become_leader()
        else:
            self.become_follower()
    
    def become_leader(self):
        """Transition to leader state"""
        self.state = 'LEADER'
        
        # Initialize leader state
        for node in self.cluster_nodes:
            if node != self.node_id:
                self.next_index[node] = len(self.log) + 1
                self.match_index[node] = 0
        
        # Send initial heartbeat
        self.send_heartbeat()
    
    def append_entries(self, term, leader_id, prev_log_index, prev_log_term, entries, leader_commit):
        """Handle append entries RPC"""
        
        # Reply false if term < currentTerm
        if term < self.current_term:
            return {'term': self.current_term, 'success': False}
        
        # Update term and become follower if necessary
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.become_follower()
        
        self.last_heartbeat = time.time()
        
        # Reply false if log doesn't contain an entry at prevLogIndex whose term matches prevLogTerm
        if prev_log_index > 0:
            if len(self.log) < prev_log_index or self.log[prev_log_index - 1]['term'] != prev_log_term:
                return {'term': self.current_term, 'success': False}
        
        # If an existing entry conflicts with a new one, delete the existing entry and all that follow
        if entries:
            for i, entry in enumerate(entries):
                log_index = prev_log_index + i + 1
                if len(self.log) >= log_index:
                    if self.log[log_index - 1]['term'] != entry['term']:
                        # Delete conflicting entry and all following entries
                        self.log = self.log[:log_index - 1]
                        break
        
        # Append new entries
        for entry in entries:
            self.log.append(entry)
        
        # Update commit index
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log))
        
        return {'term': self.current_term, 'success': True}
    
    def replicate_log_entry(self, entry):
        """Replicate log entry to followers (leader only)"""
        if self.state != 'LEADER':
            return False
        
        # Add entry to local log
        entry['term'] = self.current_term
        self.log.append(entry)
        
        # Replicate to followers
        successful_replications = 1  # Count self
        
        for node in self.cluster_nodes:
            if node != self.node_id:
                if self.send_append_entries(node, [entry]):
                    successful_replications += 1
        
        # Check if majority achieved
        majority_threshold = len(self.cluster_nodes) // 2 + 1
        
        if successful_replications >= majority_threshold:
            # Commit the entry
            self.commit_index = len(self.log)
            return True
        
        return False

class ByzantineFaultTolerantConsensus:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.byzantine_threshold = (total_nodes - 1) // 3
        self.view_number = 0
        self.sequence_number = 0
        self.state = 'NORMAL'
        
        # Message logs
        self.pre_prepare_log = {}
        self.prepare_log = {}
        self.commit_log = {}
    
    def pbft_consensus(self, request):
        """Practical Byzantine Fault Tolerance consensus"""
        
        if self.is_primary():
            # Primary node initiates consensus
            return self.primary_consensus(request)
        else:
            # Backup node participates in consensus
            return self.backup_consensus(request)
    
    def primary_consensus(self, request):
        """Primary node consensus process"""
        
        # Phase 1: Pre-prepare
        pre_prepare_msg = {
            'view': self.view_number,
            'sequence': self.sequence_number,
            'digest': self.compute_digest(request),
            'request': request
        }
        
        # Broadcast pre-prepare to all backups
        self.broadcast_pre_prepare(pre_prepare_msg)
        
        # Wait for prepare messages
        prepare_count = self.wait_for_prepare_messages(pre_prepare_msg)
        
        if prepare_count >= 2 * self.byzantine_threshold:
            # Phase 2: Commit
            commit_msg = {
                'view': self.view_number,
                'sequence': self.sequence_number,
                'digest': pre_prepare_msg['digest']
            }
            
            self.broadcast_commit(commit_msg)
            
            # Wait for commit messages
            commit_count = self.wait_for_commit_messages(commit_msg)
            
            if commit_count >= 2 * self.byzantine_threshold:
                # Execute request
                result = self.execute_request(request)
                self.sequence_number += 1
                return result
        
        return None  # Consensus failed
    
    def backup_consensus(self, pre_prepare_msg):
        """Backup node consensus process"""
        
        # Validate pre-prepare message
        if self.validate_pre_prepare(pre_prepare_msg):
            # Send prepare message
            prepare_msg = {
                'view': pre_prepare_msg['view'],
                'sequence': pre_prepare_msg['sequence'],
                'digest': pre_prepare_msg['digest'],
                'node_id': self.node_id
            }
            
            self.broadcast_prepare(prepare_msg)
            
            # Wait for enough prepare messages
            if self.has_enough_prepare_messages(prepare_msg):
                # Send commit message
                commit_msg = {
                    'view': pre_prepare_msg['view'],
                    'sequence': pre_prepare_msg['sequence'],
                    'digest': pre_prepare_msg['digest'],
                    'node_id': self.node_id
                }
                
                self.broadcast_commit(commit_msg)
                
                # Wait for enough commit messages
                if self.has_enough_commit_messages(commit_msg):
                    # Execute request
                    return self.execute_request(pre_prepare_msg['request'])
        
        return None
```

### 4. Error Detection and Recovery

```python
class ErrorDetectionSystem:
    def __init__(self):
        self.detectors = {
            'health_check': HealthCheckDetector(),
            'performance_anomaly': PerformanceAnomalyDetector(),
            'error_rate': ErrorRateDetector(),
            'resource_exhaustion': ResourceExhaustionDetector(),
            'network_partition': NetworkPartitionDetector()
        }
        self.recovery_strategies = RecoveryStrategyManager()
    
    def monitor_system_health(self):
        """Continuously monitor system health"""
        while True:
            detected_issues = []
            
            for detector_name, detector in self.detectors.items():
                try:
                    issues = detector.detect()
                    if issues:
                        detected_issues.extend(issues)
                except Exception as e:
                    print(f"Error in detector {detector_name}: {e}")
            
            # Process detected issues
            for issue in detected_issues:
                self.handle_detected_issue(issue)
            
            time.sleep(30)  # Check every 30 seconds
    
    def handle_detected_issue(self, issue):
        """Handle detected system issue"""
        
        # Classify issue severity
        severity = self.classify_issue_severity(issue)
        
        # Select appropriate recovery strategy
        recovery_strategy = self.recovery_strategies.get_strategy(issue['type'], severity)
        
        # Execute recovery
        recovery_result = recovery_strategy.execute(issue)
        
        # Log and alert
        self.log_issue_and_recovery(issue, recovery_result)
        
        if severity == 'critical':
            self.send_critical_alert(issue, recovery_result)

class HealthCheckDetector:
    def __init__(self):
        self.endpoints = [
            {'url': '/health', 'timeout': 5, 'critical': True},
            {'url': '/metrics', 'timeout': 10, 'critical': False},
            {'url': '/ready', 'timeout': 3, 'critical': True}
        ]
    
    def detect(self):
        """Detect health check failures"""
        issues = []
        
        for endpoint in self.endpoints:
            try:
                response = requests.get(
                    f"http://localhost:8080{endpoint['url']}",
                    timeout=endpoint['timeout']
                )
                
                if response.status_code != 200:
                    issues.append({
                        'type': 'health_check_failure',
                        'endpoint': endpoint['url'],
                        'status_code': response.status_code,
                        'critical': endpoint['critical'],
                        'timestamp': time.time()
                    })
                    
            except requests.exceptions.RequestException as e:
                issues.append({
                    'type': 'health_check_timeout',
                    'endpoint': endpoint['url'],
                    'error': str(e),
                    'critical': endpoint['critical'],
                    'timestamp': time.time()
                })
        
        return issues

class PerformanceAnomalyDetector:
    def __init__(self):
        self.response_time_threshold = 1000  # milliseconds
        self.error_rate_threshold = 0.05  # 5%
        self.cpu_threshold = 0.8  # 80%
        self.memory_threshold = 0.9  # 90%
    
    def detect(self):
        """Detect performance anomalies"""
        issues = []
        
        # Check response times
        avg_response_time = self.get_average_response_time()
        if avg_response_time > self.response_time_threshold:
            issues.append({
                'type': 'high_response_time',
                'value': avg_response_time,
                'threshold': self.response_time_threshold,
                'critical': True,
                'timestamp': time.time()
            })
        
        # Check error rates
        error_rate = self.get_error_rate()
        if error_rate > self.error_rate_threshold:
            issues.append({
                'type': 'high_error_rate',
                'value': error_rate,
                'threshold': self.error_rate_threshold,
                'critical': True,
                'timestamp': time.time()
            })
        
        # Check resource usage
        cpu_usage = self.get_cpu_usage()
        if cpu_usage > self.cpu_threshold:
            issues.append({
                'type': 'high_cpu_usage',
                'value': cpu_usage,
                'threshold': self.cpu_threshold,
                'critical': False,
                'timestamp': time.time()
            })
        
        memory_usage = self.get_memory_usage()
        if memory_usage > self.memory_threshold:
            issues.append({
                'type': 'high_memory_usage',
                'value': memory_usage,
                'threshold': self.memory_threshold,
                'critical': True,
                'timestamp': time.time()
            })
        
        return issues

class AutoRecoveryManager:
    def __init__(self):
        self.recovery_actions = {
            'service_restart': self.restart_service,
            'scale_up': self.scale_up_service,
            'failover': self.perform_failover,
            'circuit_breaker': self.enable_circuit_breaker,
            'cache_warming': self.warm_cache,
            'traffic_rerouting': self.reroute_traffic
        }
    
    def execute_recovery_plan(self, issue, recovery_plan):
        """Execute automated recovery plan"""
        
        recovery_results = []
        
        for action in recovery_plan['actions']:
            try:
                result = self.recovery_actions[action['type']](action['parameters'])
                recovery_results.append({
                    'action': action['type'],
                    'success': True,
                    'result': result,
                    'timestamp': time.time()
                })
                
                # Check if issue is resolved
                if self.verify_issue_resolved(issue):
                    break
                    
            except Exception as e:
                recovery_results.append({
                    'action': action['type'],
                    'success': False,
                    'error': str(e),
                    'timestamp': time.time()
                })
        
        return recovery_results
    
    def restart_service(self, parameters):
        """Restart a service"""
        service_name = parameters['service_name']
        
        # Graceful shutdown
        self.send_shutdown_signal(service_name)
        
        # Wait for graceful shutdown
        if not self.wait_for_shutdown(service_name, timeout=30):
            # Force kill if graceful shutdown fails
            self.force_kill_service(service_name)
        
        # Restart service
        self.start_service(service_name)
        
        # Verify service is healthy
        return self.verify_service_health(service_name)
    
    def scale_up_service(self, parameters):
        """Scale up service instances"""
        service_name = parameters['service_name']
        scale_factor = parameters.get('scale_factor', 2)
        
        current_instances = self.get_current_instances(service_name)
        target_instances = current_instances * scale_factor
        
        # Deploy additional instances
        new_instances = self.deploy_instances(service_name, target_instances - current_instances)
        
        # Wait for instances to become healthy
        for instance in new_instances:
            self.wait_for_instance_health(instance)
        
        # Update load balancer configuration
        self.update_load_balancer(service_name, new_instances)
        
        return f"Scaled {service_name} from {current_instances} to {target_instances} instances"
```

## Survival Goals and Architecture

### Progressive Fault Tolerance Levels

```python
class FaultToleranceArchitect:
    def __init__(self):
        self.survival_goals = {
            'level_1': 'Survive single node failure',
            'level_2': 'Survive availability zone failure', 
            'level_3': 'Survive region failure',
            'level_4': 'Survive cloud provider failure'
        }
    
    def design_fault_tolerant_architecture(self, requirements):
        """Design architecture based on fault tolerance requirements"""
        
        target_level = requirements.get('fault_tolerance_level', 'level_2')
        
        if target_level == 'level_1':
            return self.design_node_fault_tolerance(requirements)
        elif target_level == 'level_2':
            return self.design_zone_fault_tolerance(requirements)
        elif target_level == 'level_3':
            return self.design_region_fault_tolerance(requirements)
        elif target_level == 'level_4':
            return self.design_multi_cloud_fault_tolerance(requirements)
    
    def design_node_fault_tolerance(self, requirements):
        """Design for single node failure survival"""
        return {
            'compute': {
                'min_instances': 2,
                'load_balancer': True,
                'health_checks': True,
                'auto_scaling': True
            },
            'data': {
                'replication': 'master_slave',
                'backup_frequency': 'hourly',
                'backup_retention': '7_days'
            },
            'network': {
                'redundant_connections': False,
                'cdn': True
            }
        }
    
    def design_zone_fault_tolerance(self, requirements):
        """Design for availability zone failure survival"""
        return {
            'compute': {
                'min_instances': 3,
                'distribution': 'multi_az',
                'load_balancer': 'multi_az',
                'health_checks': True,
                'auto_scaling': True
            },
            'data': {
                'replication': 'multi_az_sync',
                'backup_frequency': 'every_4_hours',
                'backup_retention': '30_days',
                'cross_az_backup': True
            },
            'network': {
                'redundant_connections': True,
                'cdn': 'multi_region',
                'dns_failover': True
            }
        }
    
    def design_region_fault_tolerance(self, requirements):
        """Design for region failure survival"""
        return {
            'compute': {
                'min_instances': 6,
                'distribution': 'multi_region',
                'load_balancer': 'global',
                'health_checks': True,
                'auto_scaling': True,
                'cross_region_failover': True
            },
            'data': {
                'replication': 'multi_region_async',
                'backup_frequency': 'hourly',
                'backup_retention': '90_days',
                'cross_region_backup': True,
                'disaster_recovery_site': True
            },
            'network': {
                'redundant_connections': True,
                'cdn': 'global',
                'dns_failover': True,
                'anycast_routing': True
            }
        }
    
    def design_multi_cloud_fault_tolerance(self, requirements):
        """Design for cloud provider failure survival"""
        return {
            'compute': {
                'min_instances': 9,
                'distribution': 'multi_cloud',
                'load_balancer': 'cloud_agnostic',
                'health_checks': True,
                'auto_scaling': True,
                'cross_cloud_failover': True
            },
            'data': {
                'replication': 'multi_cloud_async',
                'backup_frequency': 'hourly',
                'backup_retention': '365_days',
                'cross_cloud_backup': True,
                'vendor_agnostic_storage': True
            },
            'network': {
                'redundant_connections': True,
                'cdn': 'multi_vendor',
                'dns_failover': True,
                'anycast_routing': True,
                'vpn_interconnect': True
            }
        }
```

## Monitoring and Observability

```python
class FaultToleranceMonitoring:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alerting_system = AlertingSystem()
        self.dashboard = FaultToleranceDashboard()
    
    def setup_monitoring(self, architecture):
        """Setup comprehensive monitoring for fault tolerant system"""
        
        # System health metrics
        self.metrics_collector.add_metrics([
            'system_availability',
            'component_health_status',
            'failure_rate_by_component',
            'mean_time_to_recovery',
            'mean_time_between_failures'
        ])
        
        # Performance metrics
        self.metrics_collector.add_metrics([
            'response_time_percentiles',
            'throughput',
            'error_rate',
            'resource_utilization'
        ])
        
        # Fault tolerance specific metrics
        self.metrics_collector.add_metrics([
            'replication_lag',
            'consensus_success_rate',
            'circuit_breaker_state',
            'failover_frequency',
            'recovery_success_rate'
        ])
        
        # Setup alerts
        self.setup_fault_tolerance_alerts()
        
        # Create dashboard
        self.dashboard.create_fault_tolerance_dashboard()
    
    def setup_fault_tolerance_alerts(self):
        """Setup alerts for fault tolerance events"""
        
        alerts = [
            {
                'name': 'High Failure Rate',
                'condition': 'failure_rate > 0.05',
                'severity': 'critical',
                'action': 'trigger_recovery_procedure'
            },
            {
                'name': 'Replication Lag High',
                'condition': 'replication_lag > 60',
                'severity': 'warning',
                'action': 'investigate_replication_health'
            },
            {
                'name': 'Circuit Breaker Open',
                'condition': 'circuit_breaker_state == "OPEN"',
                'severity': 'warning',
                'action': 'check_dependency_health'
            },
            {
                'name': 'Recovery Failed',
                'condition': 'recovery_success_rate < 0.8',
                'severity': 'critical',
                'action': 'escalate_to_engineering'
            }
        ]
        
        for alert in alerts:
            self.alerting_system.create_alert(alert)
    
    def generate_fault_tolerance_report(self):
        """Generate comprehensive fault tolerance report"""
        
        report = {
            'availability_metrics': self.calculate_availability_metrics(),
            'reliability_metrics': self.calculate_reliability_metrics(),
            'recovery_metrics': self.calculate_recovery_metrics(),
            'cost_analysis': self.calculate_fault_tolerance_costs(),
            'recommendations': self.generate_recommendations()
        }
        
        return report
    
    def calculate_availability_metrics(self):
        """Calculate system availability metrics"""
        
        uptime_data = self.metrics_collector.get_uptime_data()
        
        return {
            'availability_percentage': uptime_data['uptime'] / (uptime_data['uptime'] + uptime_data['downtime']) * 100,
            'mtbf': uptime_data['total_operational_time'] / uptime_data['failure_count'],
            'mttr': uptime_data['total_recovery_time'] / uptime_data['failure_count'],
            'downtime_breakdown': uptime_data['downtime_by_cause']
        }
```

Fault tolerance is essential for building reliable distributed systems. By implementing redundancy, graceful degradation, consensus mechanisms, and comprehensive monitoring, systems can continue operating effectively even when individual components fail. The key is to design for failure from the beginning and continuously test and improve fault tolerance mechanisms.