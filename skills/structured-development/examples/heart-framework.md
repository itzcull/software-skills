# HEART and Goals–Signals–Metrics

## Sources and scope

- [Google Research: Measuring the User Experience on a Large Scale](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/).
- [Rodden, Hutchinson, and Fu: original CHI 2010 paper](https://research.google.com/pubs/archive/36299.pdf).

**Type:** user-experience measurement framework and measurement-design process. **Contract assessed:** `7c10199`.

The reviewed paper defines HEART categories—Happiness, Engagement, Adoption, Retention, and Task success—and a Goals–Signals–Metrics process. It distinguishes product goals from feature goals and discusses instrumentation and metric accuracy. This example uses the paper's extracted text, not a current tool implementation or an observed team procedure.

## Mapping to the abstract procedure

This is our interpretation using the [source-evidence labels](../SKILL.md#researched-examples).

| Responsibility | Mapping and limits |
| --- | --- |
| [1. Intent and boundaries](../SKILL.md#1-establish-intent-and-boundaries) | **Supported:** articulate product or feature goals and seek team agreement before choosing measurements. |
| [2. Structure the work](../SKILL.md#2-structure-the-work) | **Partial:** connect goals to observable signals and metrics. This structures measurement reasoning, not the full software implementation backlog. |
| [3. Prepare the next increment](../SKILL.md#3-select-and-prepare-the-next-increment) | **Partial:** select relevant categories and signals, considering sensitivity and data sources. Bounded delivery commitments and acceptance thresholds are not specified. |
| [4. Execute](../SKILL.md#4-execute-the-increment) | **Partial:** the paper discusses collecting signals through logs, surveys, and other sources. Instrumentation implementation protocols are not defined. |
| [5. Evaluate](../SKILL.md#5-evaluate-the-result) | **Supported:** use metrics to assess goals, address accuracy problems, and triangulate with other research rather than treating metrics as sufficient alone. |
| [6. Reconcile and adapt](../SKILL.md#6-reconcile-and-adapt) | **Partial:** examples show measurement informing product decisions. A general decision-authority or escalation protocol is not specified. |
| [7. Close the scope](../SKILL.md#7-close-the-agreed-scope) | **Not established:** the paper does not define acceptance of a measurement implementation or overall software delivery. |

## Loops and concern placement

- **Supported:** measurement can concern a product or an individual feature, and metrics tracked over time inform decisions.
- **Partial:** Goals, Signals, and Metrics are reasoning steps, not three nested loops. The framework alone does not declare commitment, authority, and completion conditions at each product scope.
- **Supported:** learning goals, signal availability, and metric interpretation are distinct concerns. The paper explicitly discusses whether relevant actions are logged and the accuracy of log-based measurements; it does not simply ignore instrumentation quality.

## Additional criteria to establish conformance

Findings use the [evaluation classifications](../references/evaluating-procedures.md#3-classify-findings). No actual contradiction is established.

| Original contract criterion | Finding | What the concrete implementation must establish |
| --- | --- | --- |
| [1. Responsibility coverage](../SKILL.md#conformance-requirements) and [execution](../SKILL.md#4-execute-the-increment) | **Scope mismatch** | The delivery process that builds instrumentation and the software being measured. A measurement framework is not a full engineering procedure. |
| [2. Progression conditions](../SKILL.md#conformance-requirements) and [evaluation](../SKILL.md#5-evaluate-the-result) | **Unknown** | Evidence that data collection is implemented accurately and the boundary at which it must be ready. Defining a metric is not proof that it can be measured reliably. |
| [4. Decision authority and 5. Traceability](../SKILL.md#conformance-requirements) | **Unknown** | Who approves goals and metric changes, owns collection and analysis, and preserves their connection to decisions and implementation evidence. |
| [6. Loop structure](../SKILL.md#development-loops) and [7. Concern coverage](../SKILL.md#concern-placement) | **Unknown** | Placement and review triggers across product, feature, delivery, and operational processes, including event-taxonomy governance and privacy where relevant. |
| [3. Exception handling](../SKILL.md#conformance-requirements) | **Unknown** | What happens when signals are unavailable, data is unreliable, or findings do not answer the learning question. |

## What remains implementation-specific

The paper allows selection among HEART categories; the contract does not require all five. Measurement of launched products complements rather than replaces formative research. Event naming, instrumentation tooling, implementation tests, and acceptance responsibilities belong to the adopting procedure.

**Lesson for the abstraction:** deciding what success means, collecting trustworthy observations, and acting on evidence are separate commitments that must be connected.
