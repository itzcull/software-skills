---
title: Consensus Algorithms
description: Algorithms that enable distributed systems to agree on a single value or state
source: Manual creation due to inaccessible source URL
tags: [consensus, distributed-systems, algorithms, raft, pbft, paxos, system-design]
category: key-concepts
---

# Consensus Algorithms

## Definition

> Consensus algorithms are protocols that enable distributed systems to agree on a single value or state, even in the presence of failures and network partitions.

In distributed systems, achieving consensus is fundamental for maintaining consistency and coordination among multiple nodes. Consensus algorithms ensure that all participating nodes agree on the same value, operation order, or system state.

## The Consensus Problem

### Core Challenge
- Multiple nodes need to agree on a single value
- Nodes may fail or become unreachable
- Network messages can be lost, delayed, or duplicated
- Some nodes might behave maliciously (Byzantine failures)

### FLP Impossibility Result
- **Fischer-Lynch-Paterson Theorem**: In an asynchronous network with even one node failure, no consensus algorithm can guarantee termination
- **Implication**: Consensus algorithms must choose between safety and liveness
- **Practical Solution**: Use timeouts and assumptions about network behavior

## Types of Consensus

### 1. Byzantine Fault Tolerant (BFT)
- **Handles**: Arbitrary failures including malicious behavior
- **Assumption**: Up to f Byzantine nodes out of 3f+1 total nodes
- **Use Cases**: Blockchain, critical safety systems
- **Examples**: PBFT, Tendermint, HotStuff

### 2. Crash Fault Tolerant (CFT)
- **Handles**: Node crashes and network partitions
- **Assumption**: Nodes fail by stopping (fail-stop model)
- **Use Cases**: Distributed databases, coordination services
- **Examples**: Raft, Multi-Paxos, Viewstamped Replication

## Popular Consensus Algorithms

### Raft Algorithm

**Overview:**
Raft is designed to be understandable while providing the same guarantees as Paxos. It separates consensus into leader election, log replication, and safety.

**Core Components:**

1. **Leader Election**
   - Nodes can be followers, candidates, or leaders
   - Terms are used to detect stale leaders
   - Majority vote required to become leader

2. **Log Replication**
   - Leader receives client requests and replicates to followers
   - Entries committed once replicated to majority
   - Log consistency maintained through term numbers and indices

3. **Safety Properties**
   - Election Safety: At most one leader per term
   - Leader Append-Only: Leaders never overwrite log entries
   - Log Matching: Identical entries at same index across logs
   - Leader Completeness: All committed entries present in future leaders

**Algorithm Flow:**
```
1. Client sends request to leader
2. Leader appends entry to local log
3. Leader sends AppendEntries RPC to followers
4. Followers append entry and respond
5. Once majority responds, leader commits entry
6. Leader responds to client
7. Leader notifies followers of commitment
```

**Advantages:**
- Easier to understand than Paxos
- Strong leadership model simplifies operation
- Efficient in normal operation
- Good performance characteristics

**Disadvantages:**
- Single leader can become bottleneck
- Leader election can cause temporary unavailability
- Not Byzantine fault tolerant

### Paxos Algorithm

**Overview:**
Paxos is a family of protocols for achieving consensus in unreliable networks. It's known for being difficult to understand but provides strong theoretical foundations.

**Basic Paxos Phases:**

1. **Prepare Phase**
   - Proposer sends prepare(n) to acceptors
   - Acceptors respond with promise not to accept proposals < n
   - Acceptors include highest-numbered proposal already accepted

2. **Accept Phase**
   - Proposer sends accept(n, v) to acceptors
   - Acceptors accept if they haven't promised to ignore
   - Value v chosen if majority accepts

**Multi-Paxos:**
- Optimizes Basic Paxos for multiple rounds
- Stable leader reduces message complexity
- More practical for real-world implementations

**Advantages:**
- Theoretically proven correct
- Works in asynchronous networks
- Forms basis for many other algorithms
- Can handle arbitrary message delays

**Disadvantages:**
- Complex to understand and implement correctly
- Can suffer from dueling proposers
- Higher message complexity than Raft

### Practical Byzantine Fault Tolerance (PBFT)

**Overview:**
PBFT provides Byzantine fault tolerance for asynchronous networks. It can handle up to f Byzantine failures out of 3f+1 total nodes.

**Three-Phase Protocol:**

1. **Pre-Prepare Phase**
   - Primary assigns sequence number to request
   - Broadcasts pre-prepare message to backups
   - Backups verify and accept if valid

2. **Prepare Phase**
   - Backups broadcast prepare messages
   - Nodes collect 2f matching prepare messages
   - Ensures agreement on sequence number

3. **Commit Phase**
   - Nodes broadcast commit messages
   - After receiving 2f+1 commits, execute request
   - Ensures all honest nodes execute in same order

**View Changes:**
- Triggered when primary suspected of failure
- New primary selected through view change protocol
- Ensures liveness despite primary failures

**Advantages:**
- Handles Byzantine (malicious) failures
- Proven safe and live in asynchronous networks
- Used in real-world blockchain systems
- Provides strong safety guarantees

**Disadvantages:**
- High message complexity O(n²)
- Requires 3f+1 nodes for f failures
- Performance degrades with network size
- Complex implementation

### Tendermint

**Overview:**
Tendermint is a Byzantine fault-tolerant consensus algorithm optimized for blockchain applications. It provides instant finality and focuses on simplicity.

**Key Features:**
- **Instant Finality**: No forks or reorganizations
- **Accountability**: Byzantine validators can be identified and punished
- **Fast Finality**: Blocks finalized in ~1-3 seconds
- **Validator Set Changes**: Dynamic validator membership

**Three-Phase Consensus:**

1. **Propose**: Designated proposer broadcasts block proposal
2. **Prevote**: Validators vote on proposed block
3. **Precommit**: Validators commit to block if 2/3+ prevotes received

**Advantages:**
- Instant finality for applications
- Accountability for Byzantine behavior
- Good performance for blockchain use cases
- Active development and real-world usage

**Disadvantages:**
- Optimized specifically for blockchain
- Less general-purpose than other algorithms
- Requires 2/3+ honest validators
- Lock-step progression can slow down fast nodes

## Consensus in Practice

### etcd (Raft)
- **Use Case**: Kubernetes cluster coordination
- **Implementation**: CoreOS's Raft implementation
- **Features**: Strong consistency, linearizable reads
- **Scale**: Typically 3-5 node clusters

### Apache Kafka (ISR)
- **Use Case**: Message broker replication
- **Implementation**: In-Sync Replica (ISR) based consensus
- **Features**: High throughput, configurable consistency
- **Scale**: Hundreds of brokers, millions of messages/sec

### CockroachDB (Raft)
- **Use Case**: Distributed SQL database
- **Implementation**: Raft for replication and consistency
- **Features**: Serializable isolation, geo-distribution
- **Scale**: Multi-region deployments

### Hyperledger Fabric (PBFT/Raft)
- **Use Case**: Enterprise blockchain platform
- **Implementation**: Pluggable consensus (PBFT, Raft, Solo)
- **Features**: Permissioned networks, smart contracts
- **Scale**: Enterprise consortium networks

## Implementation Considerations

### Performance Characteristics

**Raft:**
- **Latency**: 1-2 network round trips for normal operation
- **Throughput**: Limited by leader and network bandwidth
- **Scalability**: Typically 3-7 nodes for best performance
- **Resource Usage**: Moderate CPU and memory requirements

**PBFT:**
- **Latency**: 2-3 network round trips minimum
- **Throughput**: O(n²) message complexity limits scalability
- **Scalability**: Practical for 4-20 nodes
- **Resource Usage**: High CPU due to cryptographic operations

### Network Requirements

**Partial Synchrony:**
- Most practical consensus algorithms assume partial synchrony
- Network has periods of bounded message delay
- Enables liveness while maintaining safety

**Message Authentication:**
- Digital signatures prevent message tampering
- MAC (Message Authentication Code) for performance
- Public key cryptography for Byzantine fault tolerance

### Failure Models

**Crash Failures:**
- Nodes stop responding but don't send incorrect messages
- Easier to handle, requires fewer replicas (2f+1 for f failures)
- Examples: Power failures, software crashes, network partitions

**Byzantine Failures:**
- Nodes may behave arbitrarily or maliciously
- Requires more replicas (3f+1 for f failures)
- Examples: Software bugs, hardware corruption, malicious attacks

## Best Practices

### 1. Choose Appropriate Algorithm
- **CFT algorithms** (Raft, Multi-Paxos) for trusted environments
- **BFT algorithms** (PBFT, Tendermint) for untrusted environments
- Consider performance requirements and failure assumptions

### 2. Configure Timeouts Carefully
- Balance between false failure detection and slow recovery
- Consider network latency and load characteristics
- Use adaptive timeouts based on historical performance

### 3. Monitor Consensus Health
- Track consensus round duration and success rates
- Monitor leader stability and election frequency
- Alert on consensus failures or performance degradation

### 4. Handle Network Partitions
- Design for partition tolerance
- Implement proper quorum requirements
- Plan for partition healing and reconciliation

### 5. Test Failure Scenarios
- Simulate various failure modes
- Test network partitions and message loss
- Validate recovery behavior and data consistency

## Common Pitfalls

### Split-Brain Scenarios
- **Problem**: Multiple leaders due to network partition
- **Solution**: Require majority quorum for leadership and commits
- **Prevention**: Proper quorum configuration and monitoring

### Configuration Errors
- **Problem**: Incorrect quorum sizes or node configurations
- **Solution**: Automated configuration management and validation
- **Prevention**: Infrastructure as code and testing

### Clock Skew Issues
- **Problem**: Node clocks significantly out of sync
- **Solution**: NTP synchronization and clock skew monitoring
- **Prevention**: Regular time synchronization and monitoring

### Performance Degradation
- **Problem**: Consensus becomes bottleneck under high load
- **Solution**: Batching, pipelining, and load balancing
- **Prevention**: Capacity planning and performance testing

## Emerging Trends

### Hybrid Consensus
- **Approach**: Combine different consensus algorithms
- **Example**: Use CFT for normal operation, BFT for recovery
- **Benefits**: Balance performance with fault tolerance

### Leaderless Consensus
- **Approach**: Consensus without designated leaders
- **Examples**: Stellar Consensus Protocol, Hashgraph
- **Benefits**: Better fault tolerance and performance distribution

### Proof-of-Stake (PoS)
- **Approach**: Economic incentives instead of computational work
- **Examples**: Ethereum 2.0, Cosmos, Polkadot
- **Benefits**: Energy efficiency and economic security

### Sharded Consensus
- **Approach**: Parallel consensus across multiple shards
- **Examples**: Ethereum 2.0 beacon chain, Cosmos zones
- **Benefits**: Horizontal scalability while maintaining consistency

Consensus algorithms are fundamental building blocks for distributed systems, enabling coordination and consistency in the face of failures and network issues. The choice of algorithm depends on specific requirements for performance, fault tolerance, and trust assumptions.