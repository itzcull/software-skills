# Repository Pattern

## Overview

The Repository Pattern is an abstraction of data persistence that provides a collection-like interface for working with domain objects, helping to achieve loose coupling and [persistence ignorance](../principles/persistence-ignorance.md).

## Key Characteristics

- Provides an abstraction layer for data access
- Allows working with data through a simple collection-like interface
- Helps decouple domain logic from data persistence concerns

## Implementation Approaches

### 1. Repository Per Entity

- Create a repository for each business object
- Implement only the specific methods needed
- Focus on aggregate root objects
- Follows [YAGNI](../principles/yagni.md) principle

### 2. Generic Repository Interface

Example interface in C#:

```typescript
interface EntityBase {
    id: number;
}

interface IRepository<T extends EntityBase> {
    getByIdAsync(id: number): Promise<T | null>;
    listAsync(): Promise<T[]>;
    listAsync(predicate: (entity: T) => boolean): Promise<T[]>;
    addAsync(entity: T): Promise<void>;
    deleteAsync(entity: T): Promise<void>;
    editAsync(entity: T): Promise<void>;
}
```

### 3. Generic Repository Implementation

Example implementation using Entity Framework Core:

```typescript
class Repository<T extends EntityBase> implements IRepository<T> {
    private readonly dbContext: ApplicationDbContext;

    constructor(dbContext: ApplicationDbContext) {
        this.dbContext = dbContext;
    }

    public async getByIdAsync(id: number): Promise<T | null> {
        return await this.dbContext.set<T>().findAsync(id);
    }

    public async listAsync(predicate?: (entity: T) => boolean): Promise<T[]> {
        const allEntities = await this.dbContext.set<T>().findAll();
        return predicate ? allEntities.filter(predicate) : allEntities;
    }

    public async addAsync(entity: T): Promise<void> {
        await this.dbContext.set<T>().add(entity);
    }

    public async deleteAsync(entity: T): Promise<void> {
        await this.dbContext.set<T>().remove(entity);
    }

    public async editAsync(entity: T): Promise<void> {
        await this.dbContext.set<T>().update(entity);
    }
}
```

## Advanced Considerations

### Specification Pattern

- Separate queries into their own types
- Helps maintain [Single Responsibility Principle](../principles/single-responsibility.md)
- Allows for more flexible and maintainable query logic

### Recommended Library

[Ardalis.Specification](https://github.com/ardalis/Specification) provides robust implementation support for repositories and specifications in .NET applications.

## Best Practices

- Only implement methods you actually need
- Avoid exposing IQueryable directly
- Encapsulate query logic within repositories