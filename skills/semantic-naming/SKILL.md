---
name: semantic-naming
description: Semantic naming and categorisation for programming language constructs. Use when naming or reviewing classes, functions, modules, services, commands, queries, handlers, DTOs, use cases, interactors, domain objects, adapters, workflows, state machines, or when replacing vague names like Manager, Helper, Util, Logic, Processor, Data, Info, or Wrapper with precise architectural vocabulary.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Choose names for programming constructs that reveal their semantic role, architectural boundary, lifecycle, and behavioural responsibility. This skill helps agents categorise a construct before naming it, so names communicate domain meaning rather than implementation trivia.

## Relationship to structured development

Within [structured development](../structured-development/SKILL.md), this skill makes domain meaning and design responsibilities explicit while [executing](../structured-development/SKILL.md#4-execute-the-increment) and [evaluating](../structured-development/SKILL.md#5-evaluate-the-result) changes, including refactoring. It supports readable, reviewable increments rather than adding a separate naming stage.

Use the construct's actual behavior, domain vocabulary, ownership boundary, and nearby naming conventions. Return proposed names with their semantic rationale and any mismatch between the claimed role and observed responsibilities. For an authorized rename, report affected references and verification results.

A better name does not repair an incorrect abstraction. If the analysis requires changing responsibilities, public compatibility, or agreed boundaries, return that design question to the enclosing procedure rather than hiding a redesign inside a rename.

## When to use

- Naming a new class, function, type, module, package, directory, or test helper
- Deciding whether something is an Entity, Value Object, Command, Query, Handler, Service, UseCase, Interactor, Adapter, Repository, Saga, or Process Manager
- Reviewing names for ambiguity, misleading semantics, or architectural drift
- Replacing vague suffixes such as `Manager`, `Helper`, `Util`, `Logic`, `Processor`, `Data`, `Info`, or `Wrapper`
- Aligning code with Domain-Driven Design, CQRS, Clean Architecture, request pipelines, state machines, or distributed workflows
- Choosing between active names for behaviour and passive names for data carriers

## Core principles

- Categorise before naming: identify what the construct is responsible for, then choose vocabulary that fits that role.
- Prefer domain language over technical convenience: use the team's ubiquitous language when naming business concepts.
- Names should encode intent, not implementation detail: `BookHotelRoomCommand` is better than `SetReservationStatusCommand` when the user intent is booking.
- Active constructs use verb-oriented names: commands, use cases, interactors, functions, and workflows should describe the action they perform.
- Passive constructs use noun-oriented names: DTOs, results, value objects, events, and records should describe the information they carry.
- Suffixes are contracts: `Command`, `Query`, `Handler`, `Repository`, `Decorator`, and `Presenter` imply behavioural constraints, not just naming style.
- Avoid semantic sinkholes: vague names usually signal unclear responsibility or missing domain concepts.
- Follow local conventions when they are clear and intentional; introduce taxonomy only where it improves comprehension.

## Related skills

- Load `domain-driven-design` for ubiquitous language, bounded contexts, entities, value objects, aggregates, and tactical modeling.
- Load `design-patterns` for Factory, Builder, Adapter, Decorator, Facade, Proxy, Repository, Specification, and Strategy details.
- Load `system-design` for distributed workflow, messaging, CQRS, and consistency tradeoffs.
- Load `code-review` when evaluating naming as part of a review.
- Load `refactorings` when renaming or reshaping poorly named constructs.

## Reference files

- [Naming Decision Process](references/naming-decision-process.md) - Step-by-step questions for categorising a construct before choosing a name
- [Construct Taxonomy](references/construct-taxonomy.md) - Reference table of common semantic archetypes and their naming implications
- [Architectural Naming Patterns](references/architectural-naming-patterns.md) - DDD, CQRS, Clean Architecture, distributed workflow, state machine, and request pipeline naming
- [Naming Antipatterns](references/naming-antipatterns.md) - Vague suffixes to avoid and precise alternatives
