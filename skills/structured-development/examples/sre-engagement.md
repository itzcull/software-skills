# Google SRE engagement models

## Source and scope

- [Google SRE: The Evolving SRE Engagement Model](https://sre.google/sre-book/evolving-sre-engagement-model/).

**Type:** operational engagement and ownership-transfer process. **Contract assessed:** `7c10199`.

The reviewed chapter contrasts Simple Production Readiness Review (PRR), commonly applied to an already launched service, with Early Engagement during development. It also describes shared frameworks. This example focuses on onboarding, remediation, transfer, and feedback; the workbook and linked operational checklists were not reviewed.

## Mapping to the abstract procedure

This is our interpretation using the [source-evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Supported:** engagement establishes goals, staffing, reliability needs, and an agreement between development and SRE. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Partial:** service-specific analysis identifies shortcomings, dependencies, and required improvements. Full outcome-to-task traceability is not established. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** teams prioritise improvements and negotiate an execution plan. Per-increment evidence criteria need concrete provisions. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Supported:** development and SRE participate in reliability improvements, refactoring, and operational preparation. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Partial:** readiness review, training, and exercises support operational assessment. Complete per-change verification protocols are not established. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Partial:** incidents and operational experience generate development proposals and shared guidance. Failed-check and exception dispositions need further detail. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Partial:** sufficient improvements and readiness precede progressive SRE takeover, with development backup. Complete signoff and residual-work records are not established. |

## Loops and concern placement

- **Supported:** operational experience informs improvements and updates to shared practices. PRR can proceed alongside the development lifecycle rather than being a child of a release phase.
- **Partial:** named onboarding phases do not by themselves establish nested loops; the exact commitment and acceptance protocol for each improvement needs definition.
- **Supported:** Early Engagement places reliability trade-offs in design, instrumentation and controls in implementation, validation in launch activity, and further learning after launch. Simple PRR addresses many of those needs later, before operational ownership transfer.

## Additional criteria to establish conformance

Findings use the [evaluation classifications](../references/evaluating-procedures.md#3-classify-findings). No actual contradiction is established.

| Original contract criterion | Finding | What the concrete implementation must establish |
| --- | --- | --- |
| [1. Responsibility coverage](../SKILL.md#conformance-requirements) and [scope closure](../SKILL.md#7-close-the-agreed-scope) | **Scope mismatch** | The separate software-delivery procedure and its release evidence. SRE takeover does not retroactively certify the earlier release. |
| [2. Progression conditions](../SKILL.md#conformance-requirements) and [evaluation](../SKILL.md#5-evaluate-the-result) | **Unknown** | The configured PRR checklist, readiness thresholds, and verification evidence for remediation work. |
| [3. Exception handling and 4. Decision authority](../SKILL.md#conformance-requirements) | **Unknown** | Who accepts residual risks or changed criteria, and how failed checks block, reshape, or defer transfer. |
| [5. Traceability](../SKILL.md#conformance-requirements) and [concern handoffs](../SKILL.md#concern-placement) | **Unknown** | Records connecting findings to fixes, retained development obligations, receiving owners, and evidence accepted at transfer. |

## What remains implementation-specific

Readiness for release and readiness for SRE ownership are different claims. Later instrumentation is not inherently nonconforming; its acceptability depends on the obligations due at each boundary. Being in production does not itself prove readiness for transfer.

**Lesson for the abstraction:** the same concern can legitimately have different timing and ownership boundaries. Evaluate the claim actually being made, without collapsing operational handoff into release approval.
