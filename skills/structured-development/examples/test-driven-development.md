# Test-driven development

## Source and scope

- [Agile Alliance: Test-Driven Development](https://agilealliance.org/glossary/tdd/).

The source describes a programming protocol: write a single test, observe its failure, write enough code to pass, refactor, and repeat. It also describes maintaining and revising a roadmap of tests for larger features. This is an increment-level protocol, not a complete delivery procedure.

## Mapping to the abstract procedure

This is our interpretation using the [contract and evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Partial:** a test expresses an intended aspect of behaviour. Beneficiaries, overall scope, and decision authority need an enclosing procedure. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Supported:** compound features can be decomposed into a sequence of tests; the test roadmap can be revised. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** selecting a single test establishes a narrow target and evaluation criterion. Value, dependencies, and risk need an explicit selection policy. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Supported:** write the simplest code that passes the failing test, then refactor. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Partial:** test execution supplies repeatable evidence. Passing a test alone does not establish overall fitness or adequate integration coverage. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Partial:** repeat the cycle and revise the roadmap as necessary. Scope changes and escalation need explicit authority. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Not established:** the reviewed definition does not provide a complete feature acceptance or handoff protocol. |

## Loops and concern placement

- **Supported — local loop:** the test–implementation–refactoring cycle repeats for successive aspects of behaviour. A revisable test roadmap connects those cycles to larger features.
- **Partial — enclosing relationships:** interpreting the roadmap as input to a feature-delivery loop is our mapping. The source does not specify that loop's authority, completion criteria, or escalation rules.
- **Partial — concern placement:** correctness checks and internal design improvement occur within the programming cycle. **Not established:** placement of operational observability or behavioural analytics, including when diagnostic needs or learning questions are defined. An adaptation must declare those placements and any external handoffs rather than equating passing tests with readiness.

## What remains implementation-specific

Test-first ordering, single-test cycles, and refactoring are TDD rules, not requirements of the abstract contract. An enclosing implementation must supply outcome selection, broader evaluation, exception handling, and closure.

**Lesson for the abstraction:** separate an implementation cycle from the procedure that selects and accepts the work it performs.
