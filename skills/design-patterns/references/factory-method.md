# Factory Method Pattern

## Overview

The Factory Method pattern is an object creation pattern from the Gang of Four Design Patterns book that enables defining an interface or abstract class for creating objects while leaving specific implementation details to subclasses.

## Key Characteristics

- Allows for loose coupling and enhanced flexibility in object creation
- Encapsulates the complexity of object creation
- Enables swapping implementations as needed

## Implementation Steps

1. Create an interface or abstract base class with a method for creating an object
2. Implement the interface or inherit from the abstract base class
3. Define the abstract methods
4. Swap implementations as needed

## Example Code

```typescript
interface IProductFactory {
    createProduct(): IProduct;
}

class MentoringFactory implements IProductFactory {
    public createProduct(): IProduct {
        return new MentoringOpportunity();
    }
}

class TrainingFactory implements IProductFactory {
    public createProduct(): IProduct {
        return new TrainingOffering();
    }
}

interface IProduct {
    displayDetails(): void;
}

class MentoringOpportunity implements IProduct {
    public displayDetails(): void {
        console.log("This is a mentoring opportunity.");
    }
}

class TrainingOffering implements IProduct {
    public displayDetails(): void {
        console.log("This is a training offering.");
    }
}
```

## Usage Example

```typescript
class Program {
    public static main(): void {
        const productFactory: IProductFactory = new MentoringFactory();
        const productItem: IProduct = productFactory.createProduct();
        productItem.displayDetails();

        const productFactory2: IProductFactory = new TrainingFactory();
        const productItem2: IProduct = productFactory2.createProduct();
        productItem2.displayDetails();
    }
}
```

## Dependency Injection Integration

The pattern works well with dependency injection, allowing you to:
- Inject `IProductFactory` interfaces where needed
- Pass specific factory implementations as required

## Practical Application

For example, in a web application with multiple product display pages:
- A base `BaseProduct