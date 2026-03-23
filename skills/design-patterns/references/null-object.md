# Null Object Pattern

## Intent
Reduce the need for null checks by creating a special "null" instance that provides default behavior.

## Description
The Null Object Pattern was first described in the "Pattern Languages of Program Design" book by James Coplien in 1995. The pattern aims to "reduce the need to add checks and special behavior for handling null instances".

## Problem
Typical code often requires extensive null checking, which leads to verbose and error-prone code:

```typescript
interface Customer {
    phoneNumber: string;
    orderCount: number;
    totalPurchase: number;
}

function getByPhoneNumber(phoneNumber: string): Customer | null {
    return customerRepository
        .list((c: Customer) => c.phoneNumber === phoneNumber)
        .find(() => true) || null;
}

// Requires null checks
const customer = getByPhoneNumber(phone);
const orderCount = customer !== null ? customer.orderCount : 0;
const totalPurchase = customer !== null ? customer.totalPurchase : 0;
```

## Solution
Implement a Null Object with default behavior:

### Static Instance Approach
```typescript
class Customer {
    public orderCount: number = 0;
    public totalSales: number = 0;
    public phoneNumber: string = '';
    
    public static readonly notFound = new Customer();
}

function getByPhoneNumber(phoneNumber: string): Customer {
    const customer = customerRepository
        .list((c: Customer) => c.phoneNumber === phoneNumber)
        .find(() => true);
    
    if (customer === undefined) {
        return Customer.notFound;
    }
    return customer;
}
```

### Inheritance Approach
```typescript
class NullObjectCustomer extends Customer {
    constructor() {
        super();
        this.orderCount = 0;
        this.totalSales = 0;
    }
}
```

## Benefits
- Eliminates null checks
- Simplifies client code
- Avoids null reference exceptions
- Follows the Liskov Substitution Principle

## References
- [Nulls Break Polymorphism](https://ardalis.com/nulls-break-polymorphism/)
- [Wikipedia Null Object Pattern](https://en.wikipedia.org/wiki/Null_object_pattern)