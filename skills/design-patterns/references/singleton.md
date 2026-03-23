# Singleton Design Pattern

## Overview

The Singleton design pattern ensures an application never contains more than a single instance of a given type. However, it is often considered an antipattern due to several key issues:

- Violates the [Single Responsibility Principle](../principles/single-responsibility.md)
- Creates tight coupling through static references
- Introduces [Static Cling](../antipatterns/static-cling.md)

## Example Implementation (Not Recommended)

```typescript
// Bad code! Do not use!
class Singleton {
    private static instance: Singleton | null = null;
    
    private constructor() {
        // Private constructor to prevent direct instantiation
    }
    
    public static getInstance(): Singleton {
        if (Singleton.instance === null) {
            Singleton.instance = new Singleton();
        }
        return Singleton.instance;
    }
}
```

## Recommended Alternative

Instead of using the Singleton pattern, the recommended approach is to:

1. Follow the [Explicit Dependencies Principle](../principles/explicit-dependencies.md)
2. Use [dependency injection](../practices/dependency-injection.md)
3. Configure services/IOC container to manage object lifetime

## References

- [Singleton Design Pattern in C#](https://www.pluralsight.com/courses/c-sharp-design-patterns-singleton)
- [Jon Skeet's Implementation Guide](http://csharpindepth.com/Articles/General/Singleton.aspx)