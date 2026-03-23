---
title: CAP Theorem
description: Understanding the fundamental trade-offs in distributed systems between consistency, availability, and partition tolerance
source: https://blog.algomaster.io/p/cap-theorem-explained
tags: [cap-theorem, distributed-systems, consistency, availability, partition-tolerance, trade-offs]
category: key-concepts
---

# CAP Theorem

## Definition

> The CAP theorem states that a distributed data store cannot simultaneously provide all three of the following guarantees: Consistency, Availability, and Partition Tolerance.

The CAP theorem, introduced by computer scientist Eric Brewer in 2000, describes fundamental trade-offs that must be made when designing distributed systems. It forces architects to understand that in the presence of network partitions, they must choose between consistency and availability.

## The Three Properties

### 1. Consistency (C)

**Definition**: Every read receives the most recent write or an error.

**Characteristics**:
- All nodes in the system return identical data at any given time
- When data is updated, all subsequent reads return the updated value
- No stale or outdated data is ever returned to clients
- Strong guarantee that the system appears as a single, coherent data store

**Example**: In a banking system, if you transfer $100 from Account A to Account B, all subsequent balance queries must reflect this change immediately across all nodes.

### 2. Availability (A)

**Definition**: Every request receives a non-error response, without guaranteeing that it contains the most recent write.

**Characteristics**:
- System remains operational and responsive to requests
- Requests never fail due to system unavailability
- Response may not contain the most recent data
- System prioritizes uptime over data freshness

**Example**: Amazon's shopping cart continues to function even if some servers are down, allowing users to add items even if the cart contents might not be perfectly synchronized across all regions.

### 3. Partition Tolerance (P)

**Definition**: The system continues to operate despite an arbitrary number of messages being dropped or delayed by the network between nodes.

**Characteristics**:
- System remains functional when network communication fails
- Nodes can become isolated but continue processing requests
- Essential for geographically distributed systems
- Network failures are inevitable in distributed systems

**Example**: A system deployed across multiple data centers continues working even if the network connection between data centers is severed.

## The Fundamental Trade-off

### Why You Can't Have All Three

In a distributed system, network partitions are inevitable. When a partition occurs, you must choose:

1. **Maintain Consistency**: Reject requests that could lead to inconsistent data
2. **Maintain Availability**: Continue serving requests but risk returning stale data

This leads to three possible combinations:

## System Categories

### 1. CP Systems (Consistency + Partition Tolerance)

**Characteristics**:
- Prioritize data accuracy over availability
- May reject requests during network partitions
- Ensure all nodes have identical data
- Accept temporary unavailability to maintain consistency

**Use Cases**:
- Financial systems
- Inventory management
- Systems requiring ACID transactions

**Examples**:
- **MongoDB**: Sacrifices availability during partition by failing reads/writes to ensure consistency
- **HBase**: Stops serving requests when it cannot guarantee consistency
- **Redis Cluster**: Stops accepting writes when it loses majority of master nodes

**Trade-off**: System may become unavailable but data remains accurate and consistent.

### 2. AP Systems (Availability + Partition Tolerance)

**Characteristics**:
- Prioritize system uptime over data consistency
- Continue serving requests during partitions
- Accept temporary data inconsistencies
- Use eventual consistency models

**Use Cases**:
- Social media platforms
- Content delivery systems
- Shopping carts and catalogs

**Examples**:
- **Cassandra**: Continues serving reads/writes during partitions, allowing eventual consistency
- **DynamoDB**: Remains available during network issues, with eventual consistency guarantees
- **CouchDB**: Accepts conflicting updates during partitions, resolving them later

**Trade-off**: System remains available but may serve stale or inconsistent data.

### 3. CA Systems (Consistency + Availability)

**Characteristics**:
- Work perfectly in the absence of network partitions
- Cannot handle network failures gracefully
- Essentially single-node systems or systems with perfect networks

**Reality Check**: True CA systems don't exist in practice for distributed systems, as network partitions are inevitable. However, some systems behave as CA within a single data center:

**Examples**:
- **RDBMS systems** (MySQL, PostgreSQL) within a single node
- **Two-phase commit protocols** (work only when all nodes can communicate)

## Advanced Concepts

### Eventual Consistency

**Definition**: The system will become consistent over time, given that the system stops receiving input.

**Characteristics**:
- Temporary inconsistencies are acceptable
- All replicas will converge to the same state eventually
- Conflicts are resolved through various strategies (timestamps, vector clocks, application logic)

**Example**: DNS propagation - changes to DNS records eventually propagate to all nameservers worldwide.

### Strong Consistency

**Definition**: All accesses are seen by all parallel processes in the same order.

**Implementation Techniques**:
- Synchronous replication
- Consensus algorithms (Raft, Paxos)
- Two-phase commit protocols
- Quorum-based systems

### Quorum-Based Approaches

**Concept**: Require a majority of nodes to agree before completing operations.

**Formula**: For N replicas, require:
- Write Quorum: W > N/2
- Read Quorum: R > N/2
- Consistency guarantee when: R + W > N

**Example**: In a 5-node system, require 3 nodes for writes and 3 nodes for reads to guarantee consistency.

## Extended Framework: PACELC Theorem

The PACELC theorem extends CAP by considering what happens during normal operation (no partitions):

**PACELC**: "If there is a Partition, how does the system trade off Availability and Consistency; Else, when the system is running normally in the absence of partitions, how does the system trade off Latency and Consistency?"

### PAC/ELC Trade-offs

**During Partitions** (PAC):
- Choose between Availability and Consistency

**During Normal Operation** (ELC):
- Choose between Latency and Consistency
- Lower latency often means weaker consistency guarantees

## Real-World Examples

### Google Spanner
- **Approach**: CP system with high availability through sophisticated infrastructure
- **Trade-off**: Uses atomic clocks and GPS to achieve strong consistency with minimal availability impact
- **Cost**: Requires specialized hardware and global infrastructure

### Amazon DynamoDB
- **Approach**: AP system with tunable consistency
- **Options**: Eventually consistent reads (higher availability) vs. strongly consistent reads (lower availability)
- **Flexibility**: Developers choose consistency level per operation

### Apache Kafka
- **Approach**: Configurable based on use case
- **Settings**: Acknowledge levels determine consistency vs. availability trade-offs
- **Flexibility**: Can behave as CP or AP based on configuration

## Design Strategies

### 1. Hybrid Approaches

**Strategy**: Different parts of the system make different CAP choices.

**Example**: 
- User profile data (CP): Strong consistency for critical information
- Activity feeds (AP): High availability for social interactions
- Analytics data (AP): Eventual consistency acceptable for reporting

### 2. Tunable Consistency

**Strategy**: Allow applications to choose consistency levels per operation.

**Implementation**:
- Read/write with different consistency requirements
- Client specifies desired consistency level
- System adjusts behavior accordingly

### 3. Compensation Patterns

**Strategy**: Design systems to handle and recover from inconsistencies.

**Techniques**:
- Saga patterns for distributed transactions
- Event sourcing for audit trails
- Compensating transactions for rollbacks

## Best Practices

### 1. Understand Your Requirements

**Questions to Ask**:
- How critical is data consistency for your use case?
- What is the cost of system downtime?
- Can your business logic handle eventual consistency?
- What are the regulatory or compliance requirements?

### 2. Design for Your Trade-offs

**CP Systems**:
- Implement robust monitoring and alerting
- Design graceful degradation strategies
- Plan for partition scenarios

**AP Systems**:
- Design conflict resolution strategies
- Implement effective monitoring for consistency lag
- Plan for eventual consistency scenarios

### 3. Test Partition Scenarios

**Chaos Engineering**:
- Simulate network partitions in testing
- Verify system behavior during failures
- Test recovery procedures

**Tools**:
- Chaos Monkey for random failures
- Network partition simulators
- Load testing during simulated partitions

## Common Misconceptions

### 1. "NoSQL is Always AP"
**Reality**: Many NoSQL databases offer tunable consistency and can behave as CP systems.

### 2. "SQL Databases are Always CP"
**Reality**: Distributed SQL systems face the same CAP trade-offs and may choose availability in some scenarios.

### 3. "You Must Choose Only Two"
**Reality**: Systems can make different choices for different operations or data types.

### 4. "CAP is Binary"
**Reality**: Consistency and availability exist on spectrums, not as binary choices.

## Measuring CAP Properties

### Consistency Metrics
- **Staleness**: Time delay between write and consistent read
- **Conflict Rate**: Frequency of data conflicts
- **Convergence Time**: Time for all replicas to become consistent

### Availability Metrics
- **Uptime Percentage**: Time system is responsive
- **Response Time**: Latency of successful requests
- **Error Rate**: Percentage of failed requests

### Partition Tolerance Metrics
- **Network Failure Recovery Time**: Time to detect and recover from partitions
- **Partition Duration Tolerance**: Maximum partition time system can handle
- **Split-brain Detection**: Ability to identify and resolve network partitions

The CAP theorem provides a fundamental framework for understanding distributed systems design. While it presents hard trade-offs, modern systems use sophisticated techniques to minimize these trade-offs while still respecting the theorem's fundamental constraints. The key is to choose the right trade-offs for your specific use case and requirements.