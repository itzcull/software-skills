# Evaluating procedures and improving the model

## Purpose and authority

Evaluate both whether a procedure satisfies the current structured-development contract and whether studying that procedure exposes a weakness in the contract itself. Do not assume every mismatch is a defect in the procedure.

[SKILL.md](../SKILL.md) is authoritative for the development contract and its terminology. This document governs the evaluation and revision-proposal process; it does not add development obligations. Refer to the contract rather than maintaining a second checklist of its rules here.

## 1. Establish the evaluation scope

Record:

- The procedure's purpose, intended users, and lifecycle boundaries.
- Whether it is a complete workflow, a concern-specific protocol, or a component of an enclosing procedure.
- The sources reviewed, their versions or access dates where relevant, and material evidence limitations.
- Whether the subject is prescribed practice, a configured team procedure, or an observed execution. Do not substitute evidence about one for evidence about another.
- The version or commit of the structured-development contract used for the assessment.

State the question being investigated. For example: does this procedure adequately express nested feedback loops, or does it reveal that the contract over-constrains the timing of instrumentation?

Do not require a component to fulfil the entire contract independently. Identify its enclosing procedure and handoffs; if those are unavailable, limit the assessment accordingly.

## 2. Map evidence to the contract

Map the procedure to the [abstract responsibilities](../SKILL.md#abstract-procedure), [development loops](../SKILL.md#development-loops), [concern placement](../SKILL.md#concern-placement), and [conformance requirements](../SKILL.md#conformance-requirements).

For each material mapping, retain:

- The source passage, instruction, or observed execution evidence.
- The applicable contract obligation, linked to its authoritative definition.
- Our interpretation, clearly separated from the source's claims.
- Any unresolved question that could change the assessment.

Use the existing [source-evidence labels](../SKILL.md#researched-examples) when recording researched examples. Those labels describe support in reviewed material; they do not by themselves establish conformance or successful execution.

## 3. Classify findings

Apply findings to specific obligations and scopes, not indiscriminately to an entire methodology.

| Finding | Meaning |
| --- | --- |
| Conforms | Evidence demonstrates fulfilment of the obligation within the assessed scope. |
| Contradicts | An explicit procedure rule, or an observed action when assessing execution, conflicts with a contract obligation. |
| Missing provision | A sufficiently specified procedure leaves a required obligation unaddressed. |
| Unknown | Available evidence is insufficient to determine fulfilment or conflict. |
| Scope mismatch | The obligation belongs to an enclosing or collaborating procedure rather than the component being assessed. |
| Model limitation | The procedure exposes a useful distinction the model cannot adequately express, an unnecessary restriction, or an insufficient safeguard. |

A model limitation is a finding about the contract, and can coexist with a conformance finding about the procedure. Neither automatically cancels the other: assess against the recorded contract version, then propose a revision separately.

Do not infer a missing provision from silence in an overview. Use **Unknown** until there is sufficient evidence about the actual procedure. A scope mismatch does not prove that another procedure fulfils the obligation; an unidentified handoff remains unresolved.

Distinguish conformance from effectiveness. A conforming procedure is not guaranteed to produce good outcomes, and a successful project does not prove that its procedure fulfilled the contract.

### Classification examples

- A measurement-design framework does not describe deployment: **Scope mismatch**, not automatically a violation by that framework. Inspect the enclosing delivery procedure if deployment is relevant to its scope.
- A methodology overview does not mention observability: **Unknown**, not proof that observability is omitted.
- A procedure schedules instrumentation after functional implementation, with explicit ownership, evidence, and readiness boundaries: the ordering alone is not a contradiction. Evaluate the declared obligations rather than imposing a preferred sequence.
- A procedure permits a readiness claim despite a failed check that its declared boundary requires: **Contradicts**. Identify the exact rule or execution evidence; do not attribute this permission to a methodology merely because teams sometimes behave that way.

## 4. Challenge the model

For each significant mismatch, ask:

- Is the requirement necessary to the contract's purpose, or does it encode a preferred practice?
- Does our interpretation confuse phases, tasks, scopes, or feedback loops?
- Can a useful procedure satisfy the underlying intent without satisfying the current wording?
- Can a procedure technically conform while still hiding an obligation, losing feedback, or making an unjustified completion claim?
- Does the model force artificial documents, invented hierarchy, or duplication of inherited decisions?
- Is the issue already handled by an existing obligation that needs clearer explanation rather than a new rule?

Test both **false rejection** (excluding a useful procedure because the model is unnecessarily restrictive) and **false acceptance** (accepting a procedure despite a failure the contract intends to prevent).

Use a concrete scenario to show the problem. Distinguish observed outcomes from hypothetical counterexamples, and explain why the scenario tests the model rather than merely showing a poor execution of an adequate procedure.

## 5. Choose a disposition and propose the smallest change

A valid evaluation can conclude that we should:

- Leave the contract unchanged.
- Gather more evidence.
- Correct a researched example or its interpretation.
- Improve a concrete implementation or its handoff to another procedure.
- Clarify, add, remove, or relax a model requirement.

Do not expand the model merely to accommodate terminology from another methodology. Prefer an implementation-specific provision when the distinction does not need to constrain all implementations.

For a proposed model change, record:

1. The problem, relevant sources, and current finding.
2. The smallest proposed change to the authoritative contract, with its rationale.
3. Why an example correction or implementation-specific provision is insufficient.
4. The effect on existing implementations and examples, including any changed conformance judgments.
5. The motivating scenario and a contrasting case that tests whether the change generalises.
6. Remaining uncertainty and the decision requested from the user or designated maintainer.

Treat evaluation as grounds for a proposal, not automatic permission to change the contract. After an authorised revision, re-evaluate the affected mappings and scenarios. Update references and example interpretations as needed, without rewriting source descriptions to fit the revised model.

## Evaluation output

Return a concise record containing the subject and scope, contract version, evidence-backed findings, model challenges, and recommended disposition. Include the change proposal only when one is justified.

State what could not be established and what additional evidence would resolve it. Avoid an overall conformance claim when material obligations remain unknown or outside the assessed scope.
