# Spiral development

## Source and scope

- [Software Engineering Institute: Spiral Development—Experience, Principles, and Refinements](https://www.sei.cmu.edu/library/spiral-development-experience-principles-and-refinements-spiral-development-workshop-february-9-2000/).

The reviewed report abstract describes a family of development processes characterised by repeated development activities and active risk reduction. It distinguishes invariant properties from permitted variants and hazardous look-alikes, and discusses incremental commitment and anchor-point milestones.

This mapping is deliberately limited to the public report abstract. It is not a reading of the full report or an enumeration of its formal invariants.

## Mapping to the abstract procedure

This is our interpretation using the [contract and evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Not established:** the abstract does not detail how objectives, constraints, or authority are established. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Partial:** repeated development activities supply an iterative structure. Behaviour or feature decomposition is not specified in the abstract. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** risk reduction and incremental commitment inform selection. Concrete scope and evaluation criteria need further specification. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Partial:** a family of process variants is explicitly permitted. The selected variant must define the actual execution protocol. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Partial:** active risk reduction is a stated concern. Software correctness and fitness checks are not detailed in the abstract. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Partial:** iteration and incremental commitment support repeated decisions. Exact replanning and escalation rules require fuller guidance. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Partial:** anchor-point milestones are mentioned, but their criteria and their relation to final acceptance are not established by the abstract. |

## Loops and concern placement

- **Supported — recurrence:** the report abstract describes repeated development activities and incremental commitment, with active risk reduction.
- **Not established — nesting:** recurrence does not demonstrate a particular hierarchy of product, feature, or behaviour loops. The abstract does not specify such levels, their authority, or how evidence crosses their boundaries.
- **Partial — concern placement:** risk is an explicit concern of the repeated process, but its precise decisions, checks, and milestones are not detailed in the reviewed abstract. **Not established:** specific placements for operational observability or behavioural analytics. An adaptation must supply them where relevant, rather than assuming that a general commitment to risk reduction covers them.

## What remains implementation-specific

Spiral development is itself a process family, not a ready-to-execute protocol in the reviewed material. A concrete adaptation must specify its risk assessment, commitment decisions, engineering practices, and evidence requirements.

**Lesson for the abstraction:** define a family through obligations that variants preserve, and identify superficially similar procedures that fail those obligations. The structured-development contract takes inspiration from this distinction; it does not claim to reproduce Spiral's invariants.
