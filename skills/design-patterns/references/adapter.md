# Adapter Design Pattern

## Overview

The Adapter Design Pattern (also known as the Wrapper) allows two classes with incompatible interfaces to work together. It's analogous to a real-world electrical power adapter that enables devices to connect to different power sources.

## Intent

"Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces."

## Key Characteristics

- Provides a way to make incompatible interfaces work together
- Creates a middle-layer abstraction that translates between different interfaces
- Enables the [Open-Closed Principle](../principles/open-closed.md)
- Frequently used in [Domain-Driven Design](../domain-driven-design/ddd-overview.md) as part of Anti-Corruption Layers

## Example

### Notification Adapter Interface

```typescript
interface User {
    emailAddress: string;
    allowEmailNotifications: boolean;
}

interface Message {
    title: string;
    details: string;
}

interface INotificationAdapter {
    notify(user: User, message: Message): void;
}
```

### Specific Adapter Implementation

```typescript
interface IEmailSender {
    send(to: string, from: string, subject: string, body: string): void;
}

interface EmailSettings {
    defaultFromAddress: string;
}

class EmailNotificationAdapter implements INotificationAdapter {
    private readonly emailSender: IEmailSender;
    private readonly settings: EmailSettings;
    
    constructor(emailSender: IEmailSender, settings: EmailSettings) {
        this.emailSender = emailSender;
        this.settings = settings;
    }
    
    public notify(user: User, message: Message): void {
        if (!user.allowEmailNotifications) return;
        const fromEmail = this.settings.defaultFromAddress;
        this.emailSender.send(user.emailAddress, fromEmail, message.title, message.details);
    }
}
```

## Use Cases

- When you need to integrate systems with different interfaces
- To create a reusable solution for connecting incompatible components
- In scenarios involving legacy code or third-party libraries

## References

- [Pluralsight - C# Design Patterns: Adapter](https://www.pluralsight.com/courses/c-sharp-design-patterns-adapter)
- [Design Patterns: Elements of Reusable Object-Oriented Software](http://amzn.to/vep3BT)