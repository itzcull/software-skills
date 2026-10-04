---
name: refactorings
description: Refactoring catalog based on Martin Fowler's work. Covers composing methods (extract/inline function, extract variable), moving features (move function/field), organising data (split variable, encapsulate record/collection), simplifying conditionals (decompose/consolidate conditional, replace with polymorphism), dealing with inheritance (pull up/push down, replace superclass with delegate), and more. Use when refactoring code, choosing specific refactoring techniques, or during code review.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Provide a comprehensive catalog of refactoring operations that improve code structure without changing external behaviour. Each refactoring describes a specific, mechanical transformation with clear motivation and mechanics.

## Relationship to structured development

Within [structured development](../structured-development/SKILL.md), this catalog supplies behavior-preserving transformations during an increment or as explicitly selected maintenance work. A TDD REFACTOR phase is one use, not the only place structural improvement may occur.

Start from a concrete design problem, the agreed change boundary, compatibility constraints, and available behavioral verification. Return a recommended transformation or a justified no-change decision. When changes are authorized, return the changed scope and verification evidence, separating demonstrated preservation from assumptions or checks not run.

A cleaner structure is not proof that behavior was preserved. If the change requires new behavior, incompatible interfaces, or work beyond the selected scope, return it to the enclosing procedure for a separate decision rather than presenting it as routine cleanup.

## When to use

- Refactoring code during the REFACTOR step of TDD
- Choosing the right refactoring technique for a code smell
- Code review discussions about structural improvements
- Learning specific refactoring mechanics
- Teaching refactoring techniques to team members

## Categories

### Composing methods
Extract Function, Inline Function, Extract Variable, Inline Variable, Change Function Declaration, Encapsulate Variable, Rename Variable, Introduce Parameter Object, Combine Functions into Class/Transform, Split Phase

### Moving features
Move Function, Move Field, Move Statements into/out of Function, Replace Inline Code with Function Call, Slide Statements, Split Loop, Replace Loop with Pipeline

### Organising data
Split Variable, Rename Field, Replace Derived Variable with Query, Change Reference to Value (and reverse), Encapsulate Record, Encapsulate Collection, Replace Primitive with Object

### Simplifying conditionals
Decompose Conditional, Consolidate Conditional Expression, Replace Conditional with Polymorphism, Introduce Special Case, Introduce Assertion, Remove Flag Argument

### Dealing with generalisation
Pull Up Method/Field/Constructor Body, Push Down Method/Field, Replace Type Code with Subclasses, Remove Subclass, Extract Superclass, Collapse Hierarchy, Replace Superclass with Delegate

### Other
Parameterize Function, Preserve Whole Object, Remove Dead Code, Remove Middle Man, Remove Setting Method, Replace Constructor with Factory Function, Replace Function with Command, Replace Parameter with Query (and reverse), Replace Query with Parameter, Substitute Algorithm, Hide Delegate, Inline Class, Extract Class

## Reference files

- [Overview and full catalog](references/overview.md)
- Individual refactorings documented in [references/](references/)
