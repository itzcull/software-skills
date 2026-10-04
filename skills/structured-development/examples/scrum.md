# Scrum

## Source and scope

- [The Scrum Guide, November 2020](https://scrumguides.org/scrum-guide.html).

**Type:** product-development framework. **Contract assessed:** `7c10199`.

The Guide describes Scrum as deliberately incomplete. It supplies goals, accountabilities, events, artifacts, and commitments, while leaving detailed engineering practices to the concrete implementation. This example assesses the Guide, not an observed team.

## Mapping to the abstract procedure

This is our interpretation using the [source-evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Partial:** the Product Goal, product boundaries, stakeholders, and Product Owner accountability establish direction. Full constraints and handoffs need local provisions. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Supported:** the ordered Product Backlog is refined into work selected and planned in the Sprint Backlog. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Supported:** Sprint Planning establishes a goal, selects work with capacity and the Definition of Done in mind, and plans delivery. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Partial:** Developers control implementation and negotiate scope as they learn. Specific engineering protocols are supplied by the team. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Partial:** usable, verified Increments meet a Definition of Done; Sprint Review inspects outcomes. Actual quality measures and concern evidence depend on the configured procedure. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Supported:** Daily Scrum adjusts plans, Sprint Review informs future work, and Retrospective improves practices. An obsolete Sprint can be cancelled by the Product Owner. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Partial:** unfinished items return to the backlog and Product Goals are fulfilled or abandoned. Detailed acceptance evidence and lifecycle handoffs need local provisions. |

## Loops and concern placement

- **Supported:** successive Sprints inspect progress towards a Product Goal, with shorter planning feedback inside each Sprint. The source distinguishes Product Goal, Sprint Goal, and Increment quality.
- **Partial:** an Increment is an outcome with a quality boundary, not automatically another development loop. Product-goal fulfilment evidence and complete escalation paths remain implementation questions.
- **Partial:** the Definition of Done carries product quality measures and applicable organizational minima. The Scrum Team's remit includes operation and maintenance, but individual concern placements and handoffs are not fully specified.

## Additional criteria to establish conformance

Findings use the [evaluation classifications](../references/evaluating-procedures.md#3-classify-findings). No actual contradiction is established.

| Original contract criterion | Finding | What the concrete implementation must establish |
| --- | --- | --- |
| [1. Responsibility coverage](../SKILL.md#conformance-requirements) and [execution](../SKILL.md#4-execute-the-increment) | **Scope mismatch** | The engineering protocols used within Scrum and their connection to the framework's commitments. The Guide is not a complete engineering procedure. |
| [2. Progression conditions](../SKILL.md#conformance-requirements) and [evaluation](../SKILL.md#5-evaluate-the-result) | **Unknown** | The actual Definition of Done, release-specific checks, and evidence needed for Product Goal fulfilment. |
| [3. Exception handling and 4. Decision authority](../SKILL.md#conformance-requirements) | **Unknown** | Authority for release, residual-risk decisions, external approvals, and blocked work beyond the Guide's explicit accountabilities. |
| [7. Concern coverage](../SKILL.md#concern-placement) | **Unknown** | Who handles each relevant concern, when its evidence is due, and which obligations are handed to collaborating processes. |

## What remains implementation-specific

The Guide explicitly says Sprint Review is not a gate to releasing value. Releasing a qualifying Increment before the Sprint finishes is compatible with distinct completion boundaries. Conversely, timebox expiry does not turn unfinished work into an accepted Increment.

**Lesson for the abstraction:** a framework can define feedback and accountability without specifying every engineering obligation. Conformance belongs to the configured procedure, not the framework name.
