# Facade Pattern

## Overview

The Facade Pattern provides a simplified interface for a complex subsystem, reducing complexity and improving usability. It helps address code smells like [the big ball of mud](../antipatterns/big-ball-of-mud.md) and [the blob](../antipatterns/blob.md).

## Key Characteristics

- Creates a simplified interface for a complex system
- The subsystem does not know the facade exists
- Ties exist from the facade to the subsystem, but not vice versa

## Example Scenario: eCommerce API

### Original Complex System
An eCommerce monolithic API with multiple endpoints:
- Orders
- Invoices
- Customer Profiles
- Products
- Product Categories
- Store Locations

### Facade Solution
Create a focused facade for product management that only exposes necessary product-related endpoints:
- GetAllProducts()
- GetProduct(productId)
- GetAllProductCategories()
- GetProductCategory(categoryId)

## Domain-Driven Design (DDD) Perspective

- The domain (eCommerce) is too large for a single API
- Subdomains like Orders, Invoices, and Products suggest potential facade opportunities
- Bounded contexts provide limitations for facades

## Benefits

- Embraces [KISS](../principles/keep-it-simple.md) principle
- Supports [separation of concerns](../principles/separation-of-concerns.md)
- Simplifies client interactions with complex systems

## Related Patterns

- [Strangler Fig Pattern](strangler-fig.md)

## References

- "Design Patterns: Elements of Reusable Object-Oriented Software" - Gang of Four
- Pluralsight - C# Design Patterns: Facade course