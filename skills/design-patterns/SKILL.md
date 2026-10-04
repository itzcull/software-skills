---
name: design-patterns
description: Software design patterns catalog including creational (Abstract Factory, Builder, Factory Method, Singleton), structural (Adapter, Decorator, Facade, Proxy), behavioural (Chain of Responsibility, Mediator, Observer, Strategy, Specification), and architectural patterns (Repository, Strangler Fig, Domain Events, Rules Engine). Use when choosing patterns, implementing specific designs, or evaluating pattern trade-offs.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Provide a reference catalog of software design patterns with implementation guidance, trade-offs, and practical examples. Based on the Gang of Four patterns and extended with modern architectural patterns.

## Relationship to structured development

Within [structured development](../structured-development/SKILL.md), this catalog supplies design options while [preparing](../structured-development/SKILL.md#3-select-and-prepare-the-next-increment), [executing](../structured-development/SKILL.md#4-execute-the-increment), or [evaluating](../structured-development/SKILL.md#5-evaluate-the-result) an increment. Consult it for an observed design problem, not to introduce a pattern as a goal in itself.

Use the intended behavior, existing structure, constraints, and concrete change pressure to compare a pattern with simpler alternatives. Return a recommendation and its trade-offs, or an explanation of why no pattern is warranted. When implementation is requested, keep changes within the agreed scope and return verification evidence to the enclosing procedure.

Pattern selection is not architectural approval or proof of correctness. If an option changes public behavior, ownership, or inherited design decisions beyond the increment, return that choice for authorization rather than expanding the work silently.

## When to use

- Choosing a design pattern for a recurring problem
- Implementing a specific pattern
- Evaluating whether a pattern is appropriate for a situation
- Understanding trade-offs between similar patterns
- Refactoring code to use established patterns
- Code review discussions about pattern usage

## Pattern catalog

### Creational
Abstract Factory, Builder, Factory Method, Singleton, Object Mother

### Structural
Adapter, Decorator, Facade, Proxy

### Behavioural
Chain of Responsibility, Mediator, Memento, Null Object, Observer, Specification, Strategy

### Architectural / Domain
Domain Events, Repository, Rules Engine, Strangler Fig

## Reference files

- [Overview and full catalog](references/overview.md)
- Individual patterns documented in [references/](references/)
