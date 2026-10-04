# Continuous Discovery

## Sources and scope

- [Teresa Torres: Getting Started with Discovery](https://www.producttalk.org/getting-started-with-discovery/).
- [Teresa Torres: Opportunity Solution Trees](https://www.producttalk.org/opportunity-solution-trees/).

**Type:** product-discovery approach. **Contract assessed:** `7c10199`.

The reviewed author material describes regular customer contact and small research activities directed towards a product outcome. Opportunity solution trees connect outcomes, customer opportunities, solutions, and assumption tests. The book and linked detailed testing protocols were not reviewed. Discovery is not presented as the whole engineering lifecycle.

## Mapping to the abstract procedure

This is our interpretation using the [source-evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Partial:** define the customer, value proposition, and desired outcome. Full authority and constraints need local provisions. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Supported:** distinguish customer opportunities from solutions, and connect candidate solutions to assumptions worth investigating. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** focus on a small opportunity and test risky assumptions across alternatives. Exact evidence thresholds depend on the research protocol. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Supported:** interviews and assumption tests produce findings that inform what to build. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Partial:** use research evidence to assess alternatives and whether further discovery is warranted. Delivery verification is outside this component's scope. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Supported:** refine or replace ideas, revisit opportunities, and update the tree as understanding changes. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Partial:** research informs decisions to pursue delivery or change direction. Complete handoff and acceptance records are not established. |

## Loops and concern placement

- **Supported:** repeated investigation, evaluation, and adaptation operate towards an outcome, informed by regular customer contact.
- **Partial:** the tree's conceptual hierarchy does not establish four development-loop levels. Cadence alone also does not establish an independently accepted scope.
- **Partial:** discovery examines assumptions about desirability, viability, feasibility, usability, and ethics. Detailed authority, evidence thresholds, and transfer of remaining obligations to delivery need a concrete procedure.

## Additional criteria to establish conformance

Findings use the [evaluation classifications](../references/evaluating-procedures.md#3-classify-findings). No actual contradiction is established.

| Original contract criterion | Finding | What the concrete implementation must establish |
| --- | --- | --- |
| [Preparation](../SKILL.md#3-select-and-prepare-the-next-increment) and [evaluation](../SKILL.md#5-evaluate-the-result) | **Unknown** | The question and evidence criterion for each bounded investigation, plus its result and remaining uncertainty. |
| [3. Exception handling and 4. Decision authority](../SKILL.md#conformance-requirements) | **Unknown** | Who may redirect discovery, accept uncertainty, or escalate blocked work, and under what conditions. |
| [5. Traceability](../SKILL.md#conformance-requirements) and [7. Concern coverage](../SKILL.md#concern-placement) | **Unknown** | How findings and residual obligations reach a receiving delivery owner, including reconsideration triggers and relevant concern ownership. |
| [Software evaluation](../SKILL.md#5-evaluate-the-result) and [delivery closure](../SKILL.md#7-close-the-agreed-scope) | **Scope mismatch** | The engineering process that implements and verifies selected solutions. Assumption evidence alone cannot establish production readiness. |

## What remains implementation-specific

A learning commitment can conclude while discovery continues indefinitely. Do not require termination of customer learning to accept a bounded finding. Equally, finishing an assumption test does not automatically complete a feature or a release.

**Lesson for the abstraction:** findings can be valid increments without being software deliverables, and a persistent learning process can contain bounded commitments and handoffs.
