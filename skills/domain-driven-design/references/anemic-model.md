# Anemic Model

In object-oriented programming and Domain-Driven Design (DDD), an anemic model refers to objects that have state but lack behavior. Key characteristics include:

## Definition
- Objects primarily contain properties
- Behaviors are extracted to separate service objects
- Fails to follow the [Tell, Don't Ask principle](../principles/tell-dont-ask.md)
- Lacks encapsulation of internal state and behavior

## Characteristics
- Primarily contains data properties
- Behaviors are typically moved to a business layer
- More focused on technical implementation than business domain

## When Anemic Models Occur
- Technical focus overshadows business domain
- Less suitable in object-oriented approaches
- More acceptable in functional programming paradigms

## Avoiding Anemic Models
- Focus on complex business models
- Implement behaviors within domain models
- Use encapsulation to manage state and behavior
- Prioritize business domain over technical implementation

## Functional vs. Object-Oriented Approaches
- Object-Oriented: Anemic models are less desirable
- Functional Programming: Anemic models are expected
  - Uses immutable data structures
  - Behaviors implemented as functions operating on records

## References
- [Domain-Driven Design Fundamentals](https://www.pluralsight.com/courses/domain-driven-design-fundamentals)
- [Anemic Domain Model](http://www.martinfowler.com/bliki/AnemicDomainModel.html) by Martin Fowler
- [SOLID - The Next Step is Functional](http://blog.ploeh.dk/2014/03/10/solid-the-next-step-is-functional/) by Mark Seemann