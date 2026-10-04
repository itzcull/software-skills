# Feature-driven development

## Source and scope

- [Planview: What is FDD in Agile?](https://www.planview.com/resources/articles/fdd-agile/) — a secondary overview, not an original methodology specification.

The overview describes developing an overall model, building a feature list, planning by feature, designing by feature, and building by feature. Features are client-valued outcomes rather than technical tasks. Design review, testing, inspection, and promotion to the main build provide checkpoints.

## Mapping to the abstract procedure

This is our interpretation using the [contract and evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Partial:** gather context, understand the audience and goals, and develop a shared domain model. Explicit exclusions and decision limits need further definition. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Supported:** derive a feature list from the model; break oversized features into smaller client-valued outcomes. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** plan ordering and ownership, then design and review the selected feature. Define the precise acceptance evidence in the concrete implementation. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Supported:** feature teams build the components needed to realise the design. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Partial:** testing, inspection, and approval precede promotion to the main build. The overview does not fully specify fitness or regression evidence. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Partial:** the model gains detail as learning occurs, and oversized features are split. Replanning after failed checks needs a concrete protocol. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Partial:** promotion marks a feature checkpoint. Acceptance of the combined feature set and incomplete-work accounting need an enclosing closure policy. |

## What remains implementation-specific

The described class ownership, chief-programmer role, design reviews, and feature-size limit belong to FDD, not the abstract contract. Do not infer that those roles cover every decision-authority or escalation requirement.

**Lesson for the abstraction:** organise progress around meaningful outcomes while allowing modelling, design, and technical tasks to support those outcomes.
