---
name: domain-driven-design
description: Domain-Driven Design concepts including ubiquitous language, bounded contexts, entities, value objects, aggregates, strategic and tactical design, context mapping, EventStorming, and domain storytelling. Use when modeling domains, defining bounded contexts, applying DDD patterns, or understanding strategic vs tactical design.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Provide comprehensive reference material on Domain-Driven Design. Covers the strategic patterns for organising complex domains and the tactical patterns for implementing domain models in code.

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
- Use the `domain-designer` agent for interactive DDD modeling

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
