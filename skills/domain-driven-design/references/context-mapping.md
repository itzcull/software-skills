# Context Mapping in Domain-Driven Design

## Definition

Context Mapping enables understanding how [bounded contexts](./bounded-context.md) integrate with each other. It shows the relationships between bounded contexts and may indicate the relationships of teams maintaining those contexts.

## Team Relationships

There are three primary team relationship types:

### 1. Partnership
- Teams are aligned with common goals
- Requires close collaboration and communication
- Mutual success is interdependent

### 2. Upstream/Downstream
- One team (Upstream) significantly impacts another team (Downstream)
- Changes by the Upstream team affect Downstream teams
- Similar to a Publisher/Subscriber relationship

### 3. Nonrelated (Free)
- Teams and bounded contexts are independent
- No significant relationship or dependencies exist

## Context Map Patterns

### Positive Patterns
- [Anti-Corruption Layer](./anti-corruption-layer.md)
- Open Host Service
- Partnership
- Published Language
- Customer-Supplier

### Problematic Patterns
- [Big Ball of Mud](../antipatterns/big-ball-of-mud.md)
- Conformist

### Key Patterns Explained

#### Anti-Corruption Layer
- Serves as a translation layer between upstream and downstream teams
- Implemented using Facades and Adapters

#### Big Ball of Mud
- Characterized by tightly-coupled code
- No clear bounded context boundaries
- Debugging is extremely challenging

#### Shared Kernel
- Represents the intersection between bounded contexts
- Requires establishing a shared [ubiquitous language](./ubiquitous-language.md)

## Recommendations

- Clearly define boundaries between bounded contexts
- Establish clear communication between teams
- Use appropriate context mapping patterns
- Minimize tight coupling between contexts

## References

- "Domain-Driven Design Distilled" by Vaughn Vernon
- Eric Evans' DDD Reference

## See Also

- [Bounded Context](./bounded-context.md)
- [Shared Kernel](./shared-kernel.md)
- [Strategic Design](./strategic-design.md)