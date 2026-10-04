# OpenUP

## Source and scope

- [Eclipse: Introduction to OpenUP](https://archive.eclipse.org/epf/downloads/OpenUP/published/openup_published_1.5.1.5_20121212/openup/publish.openup.base/guidances/supportingmaterials/introduction_to_openup_EFA29EF3.html).

**Type:** development process. **Contract assessed:** `7c10199`.

The reviewed introduction comes from the archived OpenUP 1.5.1.5 distribution. It explicitly distinguishes micro-increments, an iteration lifecycle, and a project lifecycle with stakeholder decision points. This assessment covers that overview, not its linked detailed protocols, a configured team procedure, or current adoption.

## Mapping to the abstract procedure

This is our interpretation using the [source-evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Partial:** iteration objectives and a project plan frame stakeholder value. Full constraints, exclusions, and decision limits are not established. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Supported:** teams pull fine-grained work items to accomplish iteration objectives within the project lifecycle. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** iteration planning establishes a delivery commitment. Exact selection and evaluation criteria require more detailed provisions. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Supported:** collaborative micro-increments incrementally develop the system. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Partial:** stable, cohesive builds and rapid feedback are intended results; the overview does not establish the checks demonstrating them. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Partial:** micro-increment feedback drives adaptive iteration decisions, and project milestones support go/no-go decisions. Escalation and resumption rules are not established. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Partial:** iterations produce demonstrable or shippable builds; the project produces a released application. Acceptance evidence and outstanding handoffs are not specified in this overview. |

## Loops and concern placement

- **Supported:** the source explicitly connects short feedback loops to iteration objectives and distinguishes project oversight from local work. These are stronger evidence of level relationships than phase names alone.
- **Partial:** the four project phases do not themselves establish four nested loops. Local authority, milestone criteria, and how discoveries reopen project decisions need the detailed protocols.
- **Not established:** placement of operational observability, analytics, and acceptance of relevant operational handoffs. Their absence from the introduction is not proof of omission by OpenUP.

## Additional criteria to establish conformance

Findings use the [evaluation classifications](../references/evaluating-procedures.md#3-classify-findings). No actual contradiction is established.

| Original contract criterion | Finding | What the concrete implementation must establish |
| --- | --- | --- |
| [6. Loop structure](../SKILL.md#development-loops) | **Unknown** | Entry, completion, authority, and feedback routing at the declared levels, including which decisions and evidence are inherited. |
| [2. Progression conditions and 3. Exception handling](../SKILL.md#conformance-requirements) | **Unknown** | Checks for accepting an iteration or milestone, and what happens when checks fail or commitments change. |
| [7. Concern coverage](../SKILL.md#concern-placement) | **Unknown** | Placement and ownership of relevant concerns, including operational handoffs where applicable. |
| [5. Traceability](../SKILL.md#conformance-requirements) and [scope closure](../SKILL.md#7-close-the-agreed-scope) | **Unknown** | How work-item and iteration evidence support project completion, and how deferred or unverified work affects the claim. |

## What remains implementation-specific

Do not require every micro-increment to independently perform project acceptance. The contract permits allocation across levels; it forbids assuming that completed child work automatically proves enclosing completion.

**Lesson for the abstraction:** nested development levels need explicit evidence and decision relationships, not duplicated ceremonies. The reviewed overview is a useful structural example, not a full conformance demonstration.
