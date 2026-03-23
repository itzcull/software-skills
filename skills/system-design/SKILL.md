---
name: system-design
description: Distributed systems design covering CAP theorem, load balancing, caching strategies, message queues, database sharding, consistency patterns, circuit breakers, architectural patterns (microservices, event-driven, serverless), and 12 key tradeoffs. Use when designing distributed systems, evaluating infrastructure tradeoffs, choosing databases, or understanding scalability patterns.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Provide comprehensive reference material on system design concepts. Covers building blocks, architectural patterns, key concepts, and tradeoffs for designing reliable distributed systems.

## When to use

- Designing a new distributed system or service
- Choosing between architectural patterns (microservices, event-driven, serverless)
- Evaluating database choices (SQL vs NoSQL, sharding, replication)
- Understanding caching strategies and consistency models
- Making scalability decisions (vertical vs horizontal, sync vs async)
- Evaluating tradeoffs (latency vs throughput, strong vs eventual consistency)

## Key concepts

- **CAP Theorem** - consistency, availability, partition tolerance tradeoff
- **Idempotency** - operations safe to retry
- **Circuit Breakers** - prevent cascade failures
- **Eventual Consistency** - temporary inconsistency for availability
- **Design for failure** - distributed systems fail in partial, unpredictable ways

## Related

- Use the `system-designer` agent for interactive architectural decisions

## Reference files

### Architectural Patterns
- [Client-Server](references/architectural-patterns/client-server-architecture.md)
- [Event-Driven](references/architectural-patterns/event-driven-architecture.md)
- [Microservices](references/architectural-patterns/microservices-architecture.md)
- [Peer-to-Peer](references/architectural-patterns/peer-to-peer-architecture.md)
- [Serverless](references/architectural-patterns/serverless-architecture.md)

### Building Blocks
- [API Gateway](references/building-blocks/api-gateway.md)
- [APIs](references/building-blocks/apis.md)
- [Bloom Filters](references/building-blocks/bloom-filters.md)
- [Caching](references/building-blocks/caching.md)
- [Caching Strategies](references/building-blocks/caching-strategies.md)
- [Checksums](references/building-blocks/checksums.md)
- [Circuit Breaker](references/building-blocks/circuit-breaker.md)
- [CDN](references/building-blocks/content-delivery-network.md)
- [Consistency Patterns](references/building-blocks/consistency-patterns.md)
- [Data Redundancy](references/building-blocks/data-redundancy.md)
- [Data Replication](references/building-blocks/data-replication.md)
- [Database Architectures](references/building-blocks/database-architectures.md)
- [Database Indexes](references/building-blocks/database-indexes.md)
- [Database Scaling](references/building-blocks/database-scaling.md)
- [Database Sharding](references/building-blocks/database-sharding.md)
- [Database Types](references/building-blocks/database-types.md)
- [Distributed Caching](references/building-blocks/distributed-caching.md)
- [Distributed Locking](references/building-blocks/distributed-locking.md)
- [DNS](references/building-blocks/domain-name-system.md)
- [Failover](references/building-blocks/failover.md)
- [Heartbeats](references/building-blocks/heartbeats.md)
- [Idempotency](references/building-blocks/idempotency.md)
- [Load Balancing](references/building-blocks/load-balancing.md)
- [Message Queues](references/building-blocks/message-queues.md)
- [Microservices Guidelines](references/building-blocks/microservices-guidelines.md)
- [Proxy vs Reverse Proxy](references/building-blocks/proxy-vs-reverse-proxy.md)
- [SQL vs NoSQL](references/building-blocks/sql-vs-nosql.md)
- [WebSockets](references/building-blocks/websockets.md)

### Key Concepts
- [ACID Transactions](references/key-concepts/acid-transactions.md)
- [API Design](references/key-concepts/api-design.md)
- [Availability](references/key-concepts/availability.md)
- [CAP Theorem](references/key-concepts/cap-theorem.md)
- [Consensus Algorithms](references/key-concepts/consensus-algorithms.md)
- [Consistent Hashing](references/key-concepts/consistent-hashing.md)
- [Disaster Recovery](references/key-concepts/disaster-recovery.md)
- [Distributed Tracing](references/key-concepts/distributed-tracing.md)
- [Fault Tolerance](references/key-concepts/fault-tolerance.md)
- [Gossip Protocol](references/key-concepts/gossip-protocol.md)
- [Rate Limiting](references/key-concepts/rate-limiting.md)
- [Scalability](references/key-concepts/scalability.md)
- [Service Discovery](references/key-concepts/service-discovery.md)
- [Single Point of Failure](references/key-concepts/single-point-of-failure.md)

### Tradeoffs
- [Batch vs Stream Processing](references/tradeoffs/batch-vs-stream-processing.md)
- [Concurrency vs Parallelism](references/tradeoffs/concurrency-vs-parallelism.md)
- [Latency vs Throughput](references/tradeoffs/latency-vs-throughput.md)
- [Long Polling vs WebSockets](references/tradeoffs/long-polling-vs-websockets.md)
- [Push vs Pull Architecture](references/tradeoffs/push-vs-pull-architecture.md)
- [Read-Through vs Write-Through Cache](references/tradeoffs/read-through-vs-write-through-cache.md)
- [REST vs RPC](references/tradeoffs/rest-vs-rpc.md)
- [Stateful vs Stateless](references/tradeoffs/stateful-vs-stateless-design.md)
- [Strong vs Eventual Consistency](references/tradeoffs/strong-vs-eventual-consistency.md)
- [Sync vs Async](references/tradeoffs/synchronous-vs-asynchronous-communications.md)
- [Top 15 Tradeoffs](references/tradeoffs/top-15-tradeoffs.md)
- [Vertical vs Horizontal Scaling](references/tradeoffs/vertical-vs-horizontal-scaling.md)
