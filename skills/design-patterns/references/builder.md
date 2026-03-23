# Builder Design Pattern

## Overview

The Builder design pattern is a creational pattern that provides a flexible way to construct complex objects step by step. Unlike factory patterns that typically offer a single method for object creation, the Builder pattern allows gradual definition of an object's characteristics through multiple methods.

## Key Characteristics

- Named with a `SomeTypeBuilder` convention
- Initializes a private instance of the target type
- Provides methods that:
  - Set properties on the private instance
  - Return the builder instance (method chaining)
- Includes a `Build()` or `Create()` method to return the final object

## Example in TypeScript

```typescript
interface Address {
    street?: string;
    state?: string;
}

class AddressBuilder {
    private address: Address = {};

    public withStreet(street: string): AddressBuilder {
        this.address.street = street;
        return this;
    }

    public withState(state: string): AddressBuilder {
        this.address.state = state;
        return this;
    }

    public build(): Address {
        return { ...this.address };
    }
}
```

## Benefits

- More flexible than constructors with multiple parameters
- Allows step-by-step object construction
- Supports method chaining
- Can implement complex object creation logic

## References

- [Design Patterns Library (Pluralsight)](https://www.pluralsight.com/courses/patterns-library)
- [Applying Builder Pattern to Angular Service](https://ardalis.com/applying-the-builder-pattern-to-improve-an-angular-service)
- [Builder Pattern in Unit Tests Kata](https://github.com/ardalis/BuilderTestSample)

## Learn More

- [On-Demand Webinar: Exploring Design Patterns for Testing](https://mailchi.mp/nimblepros/design-patterns-testing-recording)