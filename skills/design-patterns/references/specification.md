# Specification Pattern

## Overview

The Specification pattern is a design pattern in Domain-Driven Design that encapsulates querying, sorting, and paging logic into a specification object. 

## Key Characteristics

- Describes a query as an object
- Allows for reusable and testable query logic
- Can be used with repositories to filter and load data
- Helps eliminate complex query logic in repositories

## Core Benefits

1. Provides a named query that can be reasoned about
2. Enables unit testing of query logic in isolation
3. Supports reuse across different application layers
4. Helps eliminate lazy loading in web applications

## Generic Specification Interface

```typescript
interface ISpecification<T> {
    criteria: (item: T) => boolean;
    includes: Array<(item: T) => any>;
    includeStrings: string[];
}
```

## Base Specification Implementation

```typescript
abstract class BaseSpecification<T> implements ISpecification<T> {
    public readonly criteria: (item: T) => boolean;
    public readonly includes: Array<(item: T) => any> = [];
    public readonly includeStrings: string[] = [];

    constructor(criteria: (item: T) => boolean) {
        this.criteria = criteria;
    }

    protected addInclude(includeExpression: (item: T) => any): void {
        this.includes.push(includeExpression);
    }

    protected addIncludeString(includeString: string): void {
        this.includeStrings.push(includeString);
    }
}
```

## Example Specification

```typescript
interface Basket {
    id: number;
    items: any[];
}

class BasketWithItemsSpecification extends BaseSpecification<Basket> {
    constructor(basketId: number) {
        super(b => b.id === basketId);
        this.addInclude(b => b.items);
    }
}
```