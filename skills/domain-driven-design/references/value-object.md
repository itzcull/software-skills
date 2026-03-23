# Value Object

A Value Object is an immutable type distinguished only by its properties. Key characteristics include:

## Definition
- Immutable type where two objects with identical properties are considered equal
- Introduced in Eric Evans' "Domain-Driven Design" book
- Unlike [Entities](./entity.md), Value Objects lack unique identifiers

## Implementation Example (TypeScript)
```typescript
class SomeValue {
    constructor(
        private readonly value1: number,
        private readonly value2: string
    ) {}
    
    public get getValue1(): number {
        return this.value1;
    }
    
    public get getValue2(): string {
        return this.value2;
    }

    public equals(other: SomeValue): boolean {
        return this.value1 === other.value1 && this.value2 === other.value2;
    }
}
```

## Key Principles
- Immutability: Cannot be changed after creation
- Comparison based on collective state
- Validation typically done via factory methods, not constructors
- Useful for describing concepts with intrinsic rules

## Important Distinctions
- Not the same as "value types" in programming
- Different from C# records, which have some limitations for Value Objects

## Practical Example
A shipping address could be a Value Object, where two addresses with identical details are considered equal.

## References
- [Domain-Driven Design Fundamentals (Pluralsight)](https://www.pluralsight.com/courses/domain-driven-design-fundamentals)
- [Microsoft Learn: Implement Value Objects](https://learn.microsoft.com/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/implement-value-objects)