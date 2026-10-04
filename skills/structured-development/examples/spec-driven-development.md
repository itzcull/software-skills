# Spec-driven development with GitHub Spec Kit

## Source and scope

- [GitHub Spec Kit documentation](https://github.github.com/spec-kit/).

The reviewed overview presents a core sequence of Specify → Plan → Tasks → Implement → Converge. Markdown artifacts carry information between steps. It also describes customisable processes and independent entry points for feature development, bug fixing, and idea assessment.

This is one tool-supported approach to spec-driven development, not a definition of every methodology using that name. The mapping reflects the reviewed overview; consult the linked workflow documentation before implementing its individual commands.

## Mapping to the abstract procedure

This is our interpretation using the [contract and evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Partial:** specify what to build before implementation. The overview does not fully establish decision authority or treatment of unresolved scope. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Supported:** turn the specification into a technical plan and actionable tasks. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** plans and tasks provide execution inputs. Increment boundaries, prioritisation, and readiness checks need the detailed workflow or explicit adaptation. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Supported:** implementation consumes the preceding artifacts, with step-by-step or automated execution available. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Partial:** the overview describes quality checklists, cross-artifact analysis, and convergence. It does not establish every runtime verification or fitness check. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Partial:** convergence provides a named reconciliation step. Its exact handling of changed requirements and failed checks needs the detailed protocol. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Not established:** the overview alone does not define sufficient acceptance, unresolved-work accounting, or release criteria. |

## What remains implementation-specific

Markdown artifacts, command names, and the core sequence belong to this implementation. They are not required by the abstract contract. An assessment's decision to proceed also does not automatically authorise implementation.

**Lesson for the abstraction:** preserve intent across planning and execution through explicit information handoffs, without standardising a particular tool or file layout.
