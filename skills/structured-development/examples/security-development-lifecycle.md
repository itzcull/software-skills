# Microsoft Security Development Lifecycle

## Sources and scope

- [Microsoft: Security Development Lifecycle practices](https://www.microsoft.com/en-us/securityengineering/sdl/practices).
- [Microsoft Learn: Microsoft Security Development Lifecycle](https://learn.microsoft.com/en-us/compliance/assurance/assurance-microsoft-security-development-lifecycle), updated September 29, 2025.

**Type:** security practices integrated into development and operation. **Contract assessed:** `7c10199`.

The practices overview organises security across design, code, build/deploy, run, and governance. The assurance article describes Microsoft's requirements, design, implementation, verification, release, training, and response activities. These are complementary presentations, not evidence that every adopter must use one fixed phase sequence. Neither source specifies a complete general-purpose feature-delivery procedure.

## Mapping to the abstract procedure

This is our interpretation using the [source-evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Supported:** define and track security/privacy requirements using data sensitivity, threats, regulations, and incident lessons. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Partial:** threat models identify and prioritise mitigations that become requirements. General feature decomposition belongs to the enclosing delivery procedure. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** risk-rated threats inform mitigation work. Bounded increments and their local acceptance criteria are not fully specified. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Supported:** secure development practices and tooling support implementation of the requirements. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Supported:** independent review and automated security checks precede release; threat models are reviewed for accuracy and unacceptable risks. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Supported:** findings return to the submitter for correction and re-review; requirements and threat models change with the software and threat landscape. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Partial:** required security checks precede staged release, followed by monitoring and response. Overall product acceptance and full handoff accounting are not established. |

## Loops and concern placement

- **Supported:** correction and re-review form a local feedback cycle; evolving threats and incidents feed requirements and design.
- **Partial:** lifecycle stages and deployment rings are not automatically nested development loops. Their complete authority and progression relationships require a configured implementation.
- **Supported:** security is distributed across governance, design, implementation, verification, and operation rather than reserved for one final check. The reviewed material establishes more concern placement than a generic methodology overview.

## Additional criteria to establish conformance

Findings use the [evaluation classifications](../references/evaluating-procedures.md#3-classify-findings). No actual contradiction is established.

| Original contract criterion | Finding | What the concrete implementation must establish |
| --- | --- | --- |
| [1. Responsibility coverage](../SKILL.md#conformance-requirements) and [work structuring](../SKILL.md#2-structure-the-work) | **Scope mismatch** | The enclosing product/feature-delivery procedure into which security work is integrated. Security practices do not independently define all functional development. |
| [6. Loop structure](../SKILL.md#development-loops) | **Unknown** | How governance, feature decisions, checks, and operational feedback relate to the implementation's declared loops and completion claims. |
| [3. Exception handling and 4. Decision authority](../SKILL.md#conformance-requirements) | **Unknown** | Authority for changed requirements, unresolved risks, and escalations beyond the documented correction/re-review path. Do not invent permission to waive mandatory checks. |
| [5. Traceability](../SKILL.md#conformance-requirements) and [scope closure](../SKILL.md#7-close-the-agreed-scope) | **Unknown** | Evidence linking requirements and mitigations to accepted results, plus outstanding obligations and receiving operational owners. |
| [7. Concern coverage](../SKILL.md#concern-placement) | **Scope mismatch** | Placement of other relevant concerns in the composed procedure. SDL's security focus is not proof that analytics or accessibility are handled elsewhere. |

## What remains implementation-specific

The reviewed practice already specifies requirements, verification, remediation, and operational monitoring; do not misclassify those as absent. The additional questions concern how an adopter composes those practices with its complete development procedure.

**Lesson for the abstraction:** one concern can have explicit lifecycle-wide practices while the surrounding delivery loops and other concerns still require specification.
