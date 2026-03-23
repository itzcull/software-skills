# Entity in Domain-Driven Design

An Entity is an object with a unique identity, distinct from its state. Key characteristics include:

## Definition

"An Entity is an object that has some intrinsic identity, apart from the rest of its state. Even if its properties are the same as another instance of the same type, it remains distinct because of its unique identity."

## Example

Consider a `Person` class where two individuals could have the same name and birth date, but remain different people. In contrast, a mailing address could be a [Value Object](./value-object.md) if its properties are identical.

## Sample Code: ToDoItem Entity

```typescript
abstract class EntityBase {
    public abstract id: string;
    protected registerDomainEvent(event: any): void {
        // Implementation for domain event registration
    }
}

class ToDoItemCompletedEvent {
    constructor(public readonly item: ToDoItem) {}
}

class ToDoItem extends EntityBase {
    public id: string = '';
    public title: string = '';
    public description: string = '';
    private contributorId?: number;
    private isDone: boolean = false;

    public markComplete(): void {
        if (!this.isDone) {
            this.isDone = true;
            this.registerDomainEvent(new ToDoItemCompletedEvent(this));
        }
    }

    public get getIsDone(): boolean {
        return this.isDone;
    }

    public get getContributorId(): number | undefined {
        return this.contributorId;
    }

    // Additional methods for managing contributors and state
}
```

## Key Responsibilities

Entities are responsible for:
- Encapsulating state and behavior
- Ensuring consistent domain logic
- Maintaining data integrity

## References

- [Domain-Driven Design Fundamentals (Pluralsight)](https://www.pluralsight.com/courses/domain-driven-design-fundamentals)
- [Ardalis' CleanArchitecture template](https://github.com/ardalis/CleanArchitecture/)