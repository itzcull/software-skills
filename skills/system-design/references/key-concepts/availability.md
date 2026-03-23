---
title: Availability
description: Understanding system availability, measurement, and techniques for achieving high availability
source: https://blog.algomaster.io/p/system-design-what-is-availability
tags: [availability, system-design, reliability, uptime, SLA]
category: key-concepts
---

# Availability

## Definition

> Availability is the proportion of time a system is operational and accessible when required.

**Formal Definition**: `Availability = Uptime / (Uptime + Downtime)`

Where:
- **Uptime**: Period when a system is functional and accessible to users
- **Downtime**: Period when a system is unavailable due to failures, maintenance, or outages

## Availability Measurement

### The "Nines" System

Availability is commonly expressed in "nines," representing the percentage of uptime:

| Availability | Downtime per Year | Downtime per Month | Downtime per Week |
|--------------|-------------------|-------------------|-------------------|
| 90% (1 nine) | 36.53 days | 73 hours | 16.8 hours |
| 99% (2 nines) | 3.65 days | 7.3 hours | 1.68 hours |
| 99.9% (3 nines) | 8.76 hours | 43.8 minutes | 10.1 minutes |
| 99.99% (4 nines) | 52.56 minutes | 4.38 minutes | 1.01 minutes |
| 99.999% (5 nines) | 5.26 minutes | 26.3 seconds | 6.05 seconds |
| 99.9999% (6 nines) | 31.56 seconds | 2.63 seconds | 0.605 seconds |

### Key Insight
Each additional "nine" represents a **10-fold improvement** in uptime, becoming exponentially more difficult and expensive to achieve.

## Strategies for Improving Availability

### 1. Redundancy

**Concept**: Eliminating single points of failure by having backup components.

#### Types of Redundancy:

**Server Redundancy**
- Multiple servers handling identical requests
- If one server fails, others continue serving traffic
- **Example**: Netflix uses thousands of servers across multiple regions

**Database Redundancy**
- Creating replica databases for backup and load distribution
- Master-slave or master-master configurations
- **Example**: MySQL master-slave replication

**Geographic Redundancy**
- Distributing resources across multiple geographical locations
- Protects against regional disasters or connectivity issues
- **Example**: AWS availability zones across different regions

### 2. Load Balancing

**Purpose**: Distribute incoming requests across multiple servers to prevent overload.

#### Load Balancing Methods:

**Hardware Load Balancers**
- Dedicated physical devices
- High performance and reliability
- More expensive solution

**Software Load Balancers**
- Applications running on standard servers
- More flexible and cost-effective
- **Examples**: HAProxy, Nginx, AWS Elastic Load Balancer

#### Load Balancing Algorithms:
- Round Robin
- Least Connections
- Weighted Round Robin
- IP Hash
- Least Response Time

### 3. Failover Mechanisms

**Definition**: Automatic switching to backup systems when primary systems fail.

#### Types of Failover:

**Active-Passive Failover**
- Primary system handles all traffic
- Backup system remains idle until needed
- Faster recovery but resource inefficient

**Active-Active Failover**
- Multiple systems handle traffic simultaneously
- Better resource utilization
- More complex to implement

### 4. Data Replication

**Purpose**: Maintain multiple copies of data across different systems.

#### Replication Approaches:

**Synchronous Replication**
- Data written to all replicas simultaneously
- Ensures consistency but higher latency
- Better for critical data integrity

**Asynchronous Replication**
- Data written to primary first, then replicated
- Lower latency but potential data loss
- Better for performance-critical applications

### 5. Monitoring and Alerting

**Importance**: Early detection and response to potential issues.

#### Monitoring Techniques:

**Heartbeat Signals**
- Regular "alive" messages between system components
- Detect component failures quickly

**Health Checks**
- Regular verification of system functionality
- Check database connections, service responses, resource usage

**Alerting Systems**
- Automated notifications for system issues
- Integration with communication tools (Slack, PagerDuty)
- Escalation procedures for critical issues

## Best Practices for High Availability

### 1. Design for Failure
- Assume components will fail
- Build systems that gracefully handle failures
- Implement circuit breakers and timeout mechanisms

### 2. Use Multiple Availability Zones
- Distribute resources across different data centers
- Protect against localized failures
- Maintain service even during facility issues

### 3. Implement Circuit Breakers
- Prevent cascading failures
- Automatically stop requests to failing services
- Allow time for recovery

### 4. Strategic Caching
- Reduce load on primary systems
- Serve cached content during outages
- Multiple cache layers (CDN, application, database)

### 5. Capacity Management
- Plan for peak load scenarios
- Auto-scaling capabilities
- Resource monitoring and optimization

### 6. Chaos Engineering
- Deliberately introduce failures to test resilience
- Identify weaknesses before they cause outages
- **Example**: Netflix's Chaos Monkey

### 7. Regular Testing
- Disaster recovery drills
- Failover testing
- Load testing under peak conditions

## Common Availability Patterns

### 1. Circuit Breaker Pattern
- Monitor service calls for failures
- "Open" circuit to prevent further calls when threshold exceeded
- Periodically test if service has recovered

### 2. Bulkhead Pattern
- Isolate critical resources
- Prevent failures in one area from affecting others
- Separate thread pools, connection pools, or services

### 3. Timeout Pattern
- Set maximum wait times for operations
- Prevent indefinite blocking
- Fail fast and try alternatives

## Availability vs. Other Concepts

### Availability vs. Reliability
- **Availability**: System is accessible when needed
- **Reliability**: System performs correctly over time

### Availability vs. Scalability
- **Availability**: System remains operational
- **Scalability**: System handles increased load

### Availability vs. Performance
- **Availability**: System is reachable
- **Performance**: System responds quickly and efficiently

## Challenges in Achieving High Availability

1. **Cost**: Each additional "nine" significantly increases infrastructure costs
2. **Complexity**: More components and failover mechanisms increase system complexity
3. **Testing**: Difficult to test all failure scenarios
4. **Trade-offs**: Balance between availability, consistency, and performance (CAP theorem)
5. **Human Error**: Often the leading cause of outages

High availability is not just about technology—it requires careful planning, monitoring, testing, and organizational processes to maintain systems that users can rely on 24/7.