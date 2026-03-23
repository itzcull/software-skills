---
title: Consistent Hashing
description: Understanding consistent hashing algorithm for distributed systems, load balancing, and efficient data distribution
source: https://blog.algomaster.io/p/consistent-hashing-explained
tags: [consistent-hashing, distributed-systems, load-balancing, data-distribution, hash-ring, virtual-nodes]
category: key-concepts
---

# Consistent Hashing

## Definition

> Consistent hashing is a distributed hashing scheme that operates independently of the number of servers or objects in a distributed hash table by assigning them a position on an abstract circle.

Consistent hashing is a technique used in distributed systems to distribute data across multiple servers while minimizing the amount of data that needs to be redistributed when servers are added or removed. It was popularized by Amazon's Dynamo paper and has become fundamental in modern distributed systems design.

## The Problem with Traditional Hashing

### Simple Hash Function Approach

Traditional hashing in distributed systems uses the formula:
```
server_index = hash(key) mod N
```

Where N is the number of servers.

### Example of Traditional Hashing Issues

```python
# Traditional hashing with 3 servers
def traditional_hash(key, num_servers):
    return hash(key) % num_servers

# Initial setup with 3 servers
servers = ['Server1', 'Server2', 'Server3']
keys = ['user1', 'user2', 'user3', 'user4', 'user5']

print("With 3 servers:")
for key in keys:
    server_idx = traditional_hash(key, 3)
    print(f"{key} -> {servers[server_idx]}")

# Adding a 4th server
print("\nWith 4 servers (after adding Server4):")
servers.append('Server4')
for key in keys:
    server_idx = traditional_hash(key, 4)
    print(f"{key} -> {servers[server_idx]}")
```

### Problems with Traditional Hashing:

1. **Massive Redistribution**: When a server is added or removed, most keys need to be reassigned
2. **Cache Invalidation**: In caching systems, this leads to widespread cache misses
3. **Data Movement**: Large amounts of data need to be moved between servers
4. **Performance Impact**: System performance degrades during redistribution
5. **Unpredictable Scaling**: Adding one server can affect the entire key distribution

**Example Impact**: With 1000 keys and 10 servers, adding one server (making it 11) could require redistributing up to 909 keys (90.9%).

## How Consistent Hashing Works

### The Hash Ring Concept

1. **Create a Hash Space**: Use a large hash space (typically 0 to 2^32 - 1)
2. **Form a Ring**: Connect the end of the hash space to the beginning, creating a circular ring
3. **Place Servers**: Hash server identifiers to positions on the ring
4. **Place Keys**: Hash keys to positions on the ring
5. **Assignment Rule**: Each key is assigned to the first server found when moving clockwise from the key's position

### Basic Implementation

```python
import hashlib
import bisect

class ConsistentHash:
    def __init__(self, replicas=3):
        self.replicas = replicas  # Number of virtual nodes per server
        self.ring = {}  # Hash ring: hash_value -> server
        self.sorted_hashes = []  # Sorted list of hash values
        
    def _hash(self, key):
        """Generate hash for a key"""
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
    
    def add_server(self, server):
        """Add a server to the hash ring"""
        for i in range(self.replicas):
            # Create virtual nodes
            virtual_key = f"{server}:{i}"
            hash_value = self._hash(virtual_key)
            
            self.ring[hash_value] = server
            bisect.insort(self.sorted_hashes, hash_value)
    
    def remove_server(self, server):
        """Remove a server from the hash ring"""
        for i in range(self.replicas):
            virtual_key = f"{server}:{i}"
            hash_value = self._hash(virtual_key)
            
            if hash_value in self.ring:
                del self.ring[hash_value]
                self.sorted_hashes.remove(hash_value)
    
    def get_server(self, key):
        """Get the server responsible for a key"""
        if not self.ring:
            return None
            
        hash_value = self._hash(key)
        
        # Find the first server clockwise from the key
        idx = bisect.bisect_right(self.sorted_hashes, hash_value)
        
        # Wrap around to the beginning if needed
        if idx == len(self.sorted_hashes):
            idx = 0
            
        return self.ring[self.sorted_hashes[idx]]

# Example usage
ch = ConsistentHash(replicas=3)

# Add servers
servers = ['Server1', 'Server2', 'Server3']
for server in servers:
    ch.add_server(server)

# Test key distribution
keys = ['user1', 'user2', 'user3', 'user4', 'user5']
print("Initial distribution:")
for key in keys:
    server = ch.get_server(key)
    print(f"{key} -> {server}")

# Add a new server
ch.add_server('Server4')
print("\nAfter adding Server4:")
for key in keys:
    server = ch.get_server(key)
    print(f"{key} -> {server}")
```

### Key Benefits

1. **Minimal Redistribution**: Only `k/n` keys need to be reassigned, where `k` is total keys and `n` is total nodes
2. **Predictable Impact**: Adding/removing servers affects only adjacent ranges
3. **Scalability**: Easy to add or remove servers without major disruption
4. **Load Distribution**: More even distribution of load across servers

## Virtual Nodes (Replicas)

### The Problem with Basic Consistent Hashing

Without virtual nodes, servers might be unevenly distributed around the ring, leading to:
- **Hot Spots**: Some servers handle much more data than others
- **Uneven Load**: Poor load balancing across the cluster
- **Poor Fault Tolerance**: Losing a server with a large range affects many keys

### Virtual Nodes Solution

Each physical server is assigned multiple positions (virtual nodes) on the hash ring.

```python
class ImprovedConsistentHash:
    def __init__(self, virtual_nodes=150):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_hashes = []
        
    def add_server(self, server):
        """Add server with multiple virtual nodes"""
        for i in range(self.virtual_nodes):
            # Create unique virtual node identifiers
            virtual_key = f"{server}:vnode:{i}"
            hash_value = self._hash(virtual_key)
            
            self.ring[hash_value] = server
            bisect.insort(self.sorted_hashes, hash_value)
    
    def get_load_distribution(self):
        """Analyze load distribution across servers"""
        server_ranges = {}
        ring_size = 2**32
        
        for i, hash_val in enumerate(self.sorted_hashes):
            server = self.ring[hash_val]
            
            # Calculate range size for this virtual node
            if i == 0:
                # First node handles wrap-around
                range_size = hash_val + (ring_size - self.sorted_hashes[-1])
            else:
                range_size = hash_val - self.sorted_hashes[i-1]
            
            if server not in server_ranges:
                server_ranges[server] = 0
            server_ranges[server] += range_size
        
        return server_ranges

# Example with better load distribution
ch_improved = ImprovedConsistentHash(virtual_nodes=100)

servers = ['Server1', 'Server2', 'Server3']
for server in servers:
    ch_improved.add_server(server)

# Analyze load distribution
distribution = ch_improved.get_load_distribution()
total_space = sum(distribution.values())

print("Load distribution with virtual nodes:")
for server, range_size in distribution.items():
    percentage = (range_size / total_space) * 100
    print(f"{server}: {percentage:.2f}%")
```

### Benefits of Virtual Nodes:

1. **Better Load Balancing**: More uniform distribution of data
2. **Improved Fault Tolerance**: Load from failed server is distributed among many others
3. **Smoother Scaling**: Adding servers affects smaller, more distributed ranges
4. **Configurable Granularity**: Can tune the number of virtual nodes for optimal balance

## Real-World Applications

### 1. Distributed Databases

**Amazon DynamoDB**
```python
# DynamoDB-style partitioning
class DynamoDBPartitioner:
    def __init__(self):
        self.consistent_hash = ConsistentHash(replicas=3)
        self.replication_factor = 3
    
    def get_partition_nodes(self, key):
        """Get N nodes for storing replicas"""
        nodes = []
        primary_node = self.consistent_hash.get_server(key)
        
        # Get the next N-1 nodes clockwise for replicas
        hash_value = self.consistent_hash._hash(key)
        idx = bisect.bisect_right(self.consistent_hash.sorted_hashes, hash_value)
        
        for i in range(self.replication_factor):
            if idx >= len(self.consistent_hash.sorted_hashes):
                idx = 0
            node = self.consistent_hash.ring[self.consistent_hash.sorted_hashes[idx]]
            if node not in nodes:
                nodes.append(node)
            idx += 1
            
        return nodes
```

**Apache Cassandra**
- Uses consistent hashing for data distribution
- Each node is responsible for a range of token values
- Automatic rebalancing when nodes join or leave

### 2. Load Balancing

```python
class LoadBalancer:
    def __init__(self):
        self.consistent_hash = ConsistentHash()
        self.server_weights = {}
    
    def add_server(self, server, weight=1):
        """Add server with weight-based virtual nodes"""
        # More virtual nodes for higher weight servers
        virtual_nodes = weight * 50
        
        for i in range(virtual_nodes):
            virtual_key = f"{server}:weight:{weight}:vnode:{i}"
            hash_value = self.consistent_hash._hash(virtual_key)
            self.consistent_hash.ring[hash_value] = server
            bisect.insort(self.consistent_hash.sorted_hashes, hash_value)
        
        self.server_weights[server] = weight
    
    def route_request(self, session_id):
        """Route request based on session ID"""
        return self.consistent_hash.get_server(session_id)

# Example: Weighted load balancing
lb = LoadBalancer()
lb.add_server('High-Capacity-Server', weight=3)
lb.add_server('Medium-Server', weight=2)
lb.add_server('Low-Server', weight=1)
```

### 3. Distributed Caching

```python
class DistributedCache:
    def __init__(self):
        self.consistent_hash = ConsistentHash()
        self.cache_nodes = {}
    
    def add_cache_node(self, node_id, node_instance):
        """Add a cache node to the ring"""
        self.consistent_hash.add_server(node_id)
        self.cache_nodes[node_id] = node_instance
    
    def get(self, key):
        """Get value from appropriate cache node"""
        node_id = self.consistent_hash.get_server(key)
        if node_id in self.cache_nodes:
            return self.cache_nodes[node_id].get(key)
        return None
    
    def put(self, key, value):
        """Store value in appropriate cache node"""
        node_id = self.consistent_hash.get_server(key)
        if node_id in self.cache_nodes:
            self.cache_nodes[node_id].put(key, value)
    
    def remove_cache_node(self, node_id):
        """Remove cache node and redistribute its data"""
        # Get all keys that were stored on this node
        affected_keys = self.get_keys_for_node(node_id)
        
        # Remove the node
        self.consistent_hash.remove_server(node_id)
        del self.cache_nodes[node_id]
        
        # Redistribute affected keys
        for key in affected_keys:
            # Keys will automatically map to new nodes
            # Application needs to handle cache misses
            pass
```

### 4. Content Delivery Networks (CDNs)

```python
class CDNRouter:
    def __init__(self):
        self.consistent_hash = ConsistentHash()
        self.edge_servers = {}
    
    def add_edge_server(self, location, server_info):
        """Add edge server in a geographic location"""
        self.consistent_hash.add_server(location)
        self.edge_servers[location] = server_info
    
    def route_content_request(self, content_id, user_location=None):
        """Route content request to appropriate edge server"""
        # Primary routing based on content ID
        primary_server = self.consistent_hash.get_server(content_id)
        
        # Could add geographic optimization here
        if user_location:
            # Find geographically closer server if available
            return self.find_closest_server(primary_server, user_location)
        
        return primary_server
```

## Advanced Consistent Hashing Techniques

### 1. Weighted Consistent Hashing

```python
class WeightedConsistentHash:
    def __init__(self):
        self.ring = {}
        self.sorted_hashes = []
        
    def add_server(self, server, weight):
        """Add server with proportional virtual nodes based on weight"""
        # Base virtual nodes, scaled by weight
        virtual_nodes = int(weight * 100)  # 100 virtual nodes per weight unit
        
        for i in range(virtual_nodes):
            virtual_key = f"{server}:weight:{weight}:vnode:{i}"
            hash_value = self._hash(virtual_key)
            
            self.ring[hash_value] = server
            bisect.insort(self.sorted_hashes, hash_value)
```

### 2. Hierarchical Consistent Hashing

```python
class HierarchicalConsistentHash:
    def __init__(self):
        self.datacenter_ring = ConsistentHash()
        self.datacenter_servers = {}
    
    def add_datacenter(self, datacenter_id):
        """Add a datacenter to the top-level ring"""
        self.datacenter_ring.add_server(datacenter_id)
        self.datacenter_servers[datacenter_id] = ConsistentHash()
    
    def add_server(self, datacenter_id, server_id):
        """Add server to specific datacenter"""
        if datacenter_id in self.datacenter_servers:
            self.datacenter_servers[datacenter_id].add_server(server_id)
    
    def get_server(self, key):
        """Two-level lookup: datacenter then server"""
        datacenter = self.datacenter_ring.get_server(key)
        if datacenter in self.datacenter_servers:
            return self.datacenter_servers[datacenter].get_server(key)
        return None
```

## Performance Considerations

### Time Complexity
- **Adding/Removing Servers**: O(V log N), where V is virtual nodes and N is total servers
- **Key Lookup**: O(log N)
- **Space Complexity**: O(N × V)

### Optimization Techniques

```python
class OptimizedConsistentHash:
    def __init__(self, virtual_nodes=150):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_hashes = []
        self.server_to_hashes = {}  # Cache for faster removal
        
    def add_server(self, server):
        """Optimized server addition with caching"""
        hashes = []
        for i in range(self.virtual_nodes):
            virtual_key = f"{server}:vnode:{i}"
            hash_value = self._hash(virtual_key)
            
            self.ring[hash_value] = server
            bisect.insort(self.sorted_hashes, hash_value)
            hashes.append(hash_value)
        
        self.server_to_hashes[server] = hashes
    
    def remove_server(self, server):
        """Optimized server removal using cached hashes"""
        if server in self.server_to_hashes:
            for hash_value in self.server_to_hashes[server]:
                if hash_value in self.ring:
                    del self.ring[hash_value]
                    self.sorted_hashes.remove(hash_value)
            
            del self.server_to_hashes[server]
```

## Monitoring and Metrics

### Key Metrics to Track

```python
class ConsistentHashMetrics:
    def __init__(self, consistent_hash):
        self.ch = consistent_hash
    
    def calculate_load_balance(self):
        """Calculate how evenly load is distributed"""
        distribution = self.ch.get_load_distribution()
        values = list(distribution.values())
        
        mean_load = sum(values) / len(values)
        variance = sum((x - mean_load) ** 2 for x in values) / len(values)
        std_deviation = variance ** 0.5
        
        # Coefficient of variation (lower is better)
        cv = std_deviation / mean_load if mean_load > 0 else 0
        
        return {
            'mean_load': mean_load,
            'std_deviation': std_deviation,
            'coefficient_of_variation': cv,
            'min_load': min(values),
            'max_load': max(values)
        }
    
    def calculate_redistribution_impact(self, new_server):
        """Calculate impact of adding a new server"""
        # Get current key distribution
        keys = [f"key_{i}" for i in range(1000)]  # Sample keys
        original_distribution = {}
        
        for key in keys:
            server = self.ch.get_server(key)
            original_distribution[key] = server
        
        # Add new server and check redistribution
        self.ch.add_server(new_server)
        redistributed_keys = 0
        
        for key in keys:
            new_server_assigned = self.ch.get_server(key)
            if new_server_assigned != original_distribution[key]:
                redistributed_keys += 1
        
        redistribution_percentage = (redistributed_keys / len(keys)) * 100
        return redistribution_percentage
```

## Best Practices

### 1. Choosing Virtual Node Count
```python
def optimal_virtual_nodes(num_servers, target_balance=0.1):
    """
    Calculate optimal virtual nodes for target load balance
    target_balance: acceptable coefficient of variation
    """
    # Rule of thumb: 100-200 virtual nodes per server
    # More virtual nodes = better balance but more memory
    
    base_virtual_nodes = max(100, 500 // num_servers)
    return min(base_virtual_nodes, 200)
```

### 2. Hash Function Selection
```python
import hashlib

def robust_hash(key):
    """Use cryptographically strong hash for better distribution"""
    # SHA-1 provides good distribution
    return int(hashlib.sha1(key.encode('utf-8')).hexdigest(), 16)

def fast_hash(key):
    """Use fast hash for performance-critical applications"""
    # FNV hash - faster but less cryptographically secure
    hash_value = 2166136261
    for byte in key.encode('utf-8'):
        hash_value ^= byte
        hash_value *= 16777619
        hash_value &= 0xffffffff
    return hash_value
```

### 3. Handling Server Failures
```python
class FailureAwareConsistentHash(ConsistentHash):
    def __init__(self, replicas=3):
        super().__init__(replicas)
        self.failed_servers = set()
    
    def mark_server_failed(self, server):
        """Mark server as failed without removing from ring"""
        self.failed_servers.add(server)
    
    def get_server(self, key):
        """Get server, skipping failed ones"""
        if not self.ring:
            return None
            
        hash_value = self._hash(key)
        idx = bisect.bisect_right(self.sorted_hashes, hash_value)
        
        # Find next available server
        attempts = 0
        while attempts < len(self.sorted_hashes):
            if idx >= len(self.sorted_hashes):
                idx = 0
            
            server = self.ring[self.sorted_hashes[idx]]
            if server not in self.failed_servers:
                return server
                
            idx += 1
            attempts += 1
        
        return None  # All servers failed
```

## Common Pitfalls and Solutions

### 1. Poor Hash Function
```python
# BAD: Poor distribution
def bad_hash(key):
    return len(key)  # Will cluster keys by length

# GOOD: Uniform distribution
def good_hash(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16)
```

### 2. Too Few Virtual Nodes
```python
# BAD: Hot spots with few virtual nodes
ch_bad = ConsistentHash(replicas=1)

# GOOD: Balanced load with sufficient virtual nodes
ch_good = ConsistentHash(replicas=150)
```

### 3. Ignoring Geographic Distribution
```python
# Consider geographic constraints
class GeoAwareConsistentHash:
    def __init__(self):
        self.global_ring = ConsistentHash()
        self.regional_rings = {}
    
    def add_server(self, server, region):
        self.global_ring.add_server(server)
        if region not in self.regional_rings:
            self.regional_rings[region] = ConsistentHash()
        self.regional_rings[region].add_server(server)
```

Consistent hashing is a powerful technique that enables scalable, fault-tolerant distributed systems. By understanding its principles and implementation details, you can build systems that handle growth and failures gracefully while maintaining good performance characteristics.