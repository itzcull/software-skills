# Domain Events Pattern

## What are Domain Events?

Domain events are events that signify a state change in the domain. They serve as a mechanism to communicate between different parts of the domain model without tightly coupling them.

### Pre-Persistence vs Post-Persistence Events

There are two types of domain events:

- **Pre-Persistence Events**: Triggered before the state change is persisted to the database
- **Post-Persistence Events**: Triggered after the state change is saved to the database

## Code Example

### Defining a Domain Event

```typescript
interface INotification {
    // Base interface for events
}

class NewOrderPlacedEvent implements INotification {
    public readonly orderId: number;
    
    constructor(orderId: number) {
        this.orderId = orderId;
    }
}
```

### Publishing a Domain Event

```typescript
interface Order {
    id: number;
    // other order properties
}

interface IMediator {
    publish(event: INotification): Promise<void>;
}

class OrderService {
    private readonly mediator: IMediator;
    
    constructor(mediator: IMediator) {
        this.mediator = mediator;
    }
    
    public async placeOrderAsync(order: Order): Promise<void> {
        // Logic to place order and save changes
        await this.mediator.publish(new NewOrderPlacedEvent(order.id));
    }
}
```

### Handling a Domain Event

```typescript
interface INotificationHandler<T extends INotification> {
    handle(notification: T): Promise<void>;
}

class SendEmailHandler implements INotificationHandler<NewOrderPlacedEvent> {
    public async handle(notification: NewOrderPlacedEvent): Promise<void> {
        // Logic to send email about the new order
        console.log(`Sending email for order ${notification.orderId}`);
    }
}
```

## Conclusion

The Domain Events pattern helps decouple different aspects of domain logic. Using libraries like MediatR makes implementation in C#/.NET straightforward and clean.

## References

- [Martin Fowler - Domain Event](https://martinfowler.com/eaaDev/DomainEvent.html)
- [Pre-Persistence Domain Events](https://www.youtube.com/watch?v=95CxduH1b8A)
- [Post-Persistence Domain Events](https://www.youtube.com/watch?v=j2oLda