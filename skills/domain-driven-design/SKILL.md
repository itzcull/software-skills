---
name: domain-driven-design
description: Domain-Driven Design concepts including ubiquitous language, bounded contexts, entities, value objects, aggregates, strategic and tactical design, context mapping, EventStorming, and domain storytelling. Use when modeling domains, defining bounded contexts, applying DDD patterns, or understanding strategic vs tactical design.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Provide comprehensive reference material on Domain-Driven Design. Covers the strategic patterns for organising complex domains and the tactical patterns for implementing domain models in code.

## Relationship to structured development

Within [structured development](../structured-development/SKILL.md), this skill supports [intent clarification](../structured-development/SKILL.md#1-establish-intent-and-boundaries), [work structuring](../structured-development/SKILL.md#2-structure-the-work), and [implementation decisions](../structured-development/SKILL.md#4-execute-the-increment) through domain language and models. Use strategic guidance when boundaries or ownership are uncertain, and tactical guidance when implementing behavior within an understood context. Bounded contexts are domain boundaries, not mandatory development loops.

Start from stakeholder examples, business rules, existing terminology, and known ownership constraints. Return a proposed or revised model with its supporting examples, boundary relationships, and unresolved domain questions. The enclosing procedure uses that understanding to select behaviors and evaluation criteria.

A plausible model is not evidence that domain experts agree or that implementation preserves its rules. Return conflicting meanings and decisions that change scope to the user or domain decision-maker before treating them as settled. This skill does not require every procedure to adopt DDD.

## When to use

- Modeling a new domain or bounded context
- Deciding between entities and value objects
- Defining ubiquitous language for a team
- Applying strategic design (context mapping, subdomains)
- Implementing tactical patterns (aggregates, repositories)
- Running EventStorming or domain storytelling sessions
- Identifying and avoiding anemic domain models

## Key concepts

- **Ubiquitous Language** - consistent terminology across code and business
- **Bounded Context** - explicit boundary with consistent language
- **Entity** - identity-based objects
- **Value Object** - immutable, equality by attributes
- **Strategic Design** - contexts, mapping, language first
- **Tactical Design** - entities, value objects, aggregates within contexts

## Related skills

- Load `design-patterns` for Repository and Specification patterns
- Domain modeling can be performed directly. Use an available advisor only when delegation is explicitly authorized; no particular agent is required.

## Reference files

- [Overview](references/overview.md) - Index of all DDD concepts
- [DDD Overview](references/ddd-overview.md) - Comprehensive DDD introduction
- [Ubiquitous Language](references/ubiquitous-language.md)
- [Bounded Context](references/bounded-context.md)
- [Domain](references/domain.md)
- [Subdomain](references/subdomain.md)
- [Entity](references/entity.md)
- [Value Object](references/value-object.md)
- [Domain Model](references/domain-model.md)
- [Strategic Design](references/strategic-design.md)
- [Tactical Design](references/tactical-design.md)
- [Anti-Corruption Layer](references/anti-corruption-layer.md)
- [Anemic Model](references/anemic-model.md)
- [Shared Kernel](references/shared-kernel.md)
- [Context Mapping](references/context-mapping.md)
- [Domain Storytelling](references/domain-storytelling.md)
- [EventStorming](references/eventstorming.md)
