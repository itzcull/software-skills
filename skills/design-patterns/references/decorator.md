# Decorator Design Pattern

## Overview

The Decorator Design Pattern is a structural pattern that allows "adding new functionalities to objects dynamically without altering their structure."

## Intent

The primary goals of the Decorator pattern are to:
- Add responsibilities to objects dynamically
- Provide a flexible alternative to subclassing
- Follow the Single Responsibility Principle
- Adhere to the Open-Closed Principle

## When to Use

Use the Decorator pattern when you want to:
- Add responsibilities to objects at runtime
- Create modular and reusable extensions
- Avoid creating numerous subclasses
- Extend functionality without modifying existing code
- Add conditional behaviors
- Enhance legacy code
- Implement cross-cutting concerns like logging, validation, or security

## TypeScript Example Structure

### Core Components
1. Base Interface (`IBookService`)
2. Concrete Implementation (`BookService`)
3. Decorators:
   - Logging Decorator
   - Validation Decorator

### Key Code Example

```typescript
interface Book {
    id: number;
    title: string;
    author: string;
}

interface IBookService {
    addBook(book: Book): void;
}

interface ILogger {
    logInformation(message: string): void;
}

class LoggingBookServiceDecorator implements IBookService {
    private readonly decoratedBookService: IBookService;
    private readonly logger: ILogger;

    constructor(decoratedBookService: IBookService, logger: ILogger) {
        this.decoratedBookService = decoratedBookService;
        this.logger = logger;
    }

    public addBook(book: Book): void {
        this.logger.logInformation(`Adding a book: ${JSON.stringify(book)}`);
        const startTime = performance.now();
        this.decoratedBookService.addBook(book);
        const endTime = performance.now();
        this.logger.logInformation(`Book added in ${(endTime - startTime).toFixed(2)} ms`);
    }
}
```

## Related Patterns

### Proxy
- Similar structure to Decorator
- Different intent: controls access vs. adds behavior

### Chain of Responsibility
- Breaks responsibilities into individual classes
- Requires specific service interface
- More rigid compared to Decorator

## Conclusion

The Decorator pattern provides a flexible way to extend object behavior dynamically, allowing developers to add functionality without modifying existing code.

## References
- "Design Patterns: Elements of Reusable Object-Oriented Software" by Gang of Four
- Pluralsight Design Patterns courses