---
name: structured-development
description: Define, adapt, or assess structured procedures for implementing a series of software behaviours or features. Use when designing development workflows, defining nested development loops and cross-cutting concern placement, comparing methodologies, or checking whether a concrete workflow fulfils a shared development contract. Separates abstract responsibilities from implementation-specific protocols such as autonomous engineering, TDD, and spec-driven development.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Structured development defines a methodology-independent contract for incremental software development within a broader software lifecycle. Concrete procedures specify how its responsibilities are fulfilled.

Advance development through bounded, evidence-producing increments. This skill defines a development contract, not a complete operational lifecycle. Implementations declare their lifecycle boundaries and how development connects to relevant operational concerns and feedback.

## Authority and terminology

This file is authoritative for the abstract procedure and conformance requirements. Concrete implementation skills own their execution rules. The researched examples illustrate possible mappings; they do not add requirements to the contract.

- **Behaviour**: an observable response of a system under specified conditions.
- **Feature**: a capability realised through one or more behaviours.
- **Increment**: a bounded piece of work with an intended outcome and an explicit basis for evaluating it. An increment can deliver software or resolve a development uncertainty; those outcomes are not interchangeable.
- **Development loop**: a recurring cycle of commitment, execution, evaluation, and adaptation at a particular scope. An iteration advances that scope through one or more increments, which may involve nested loops.
- **Level**: the scope at which a loop governs outcomes and decisions, not its elapsed duration. Timing describes when work or decisions occur relative to other activities or boundaries.
- **Concern**: an aspect of development that needs deliberate decisions, work, or evidence, potentially across multiple loops; for example, observability, behavioural analytics, security, or accessibility.
- **Completion boundary**: a point at which an implementation claims a defined scope or readiness condition has been satisfied, subject to specified evidence.
- **Implementation**: a concrete development procedure that fulfils the abstract responsibilities below.
- **Protocol**: the steps, progression conditions, evidence, and exception handling prescribed for an activity.
- **Modality**: how participation and decision-making are arranged, such as guided collaboration or autonomous execution within agreed boundaries.

An implementation may combine protocols and modalities. Neither autonomous execution nor the use of this skill grants permission to delegate, commit, deploy, or make decisions outside the user's agreed authority.

## Using the abstraction

1. Establish whether the task is to define an implementation, assess an existing one, or execute one already selected.
2. Read the concrete implementation when one exists. Read only the researched examples relevant to a comparison or unresolved design choice.
3. Identify the implementation's development loops and concern placements, then map them to the responsibilities and conformance requirements below. Identify missing provisions rather than inventing them silently.
4. For execution, resolve missing provisions that materially affect the next increment before proceeding. Reuse existing decisions and evidence where they remain applicable.

Do not force a new document or tool for each responsibility. Existing plans, tests, discussions, and review records can provide the required information if it remains accessible and unambiguous.

## Development loops

Declare the loops used by the implementation. Use levels that fit the work; a product → feature → behaviour hierarchy is illustrative, not mandatory. A simple implementation can use a single loop. Distinct phases or task lists do not by themselves establish nested loops.

For each loop, specify:

| Element | Required explanation |
| --- | --- |
| Scope | The outcome governed by the loop |
| Progression | What starts an iteration, permits progress, and establishes completion |
| Authority | Decisions it can make locally and those requiring another authority |
| Relationships | Enclosing, nested, or related loops and their dependencies |
| Feedback | What causes repetition or reconsideration, where findings go, and who acts on them |

Explain how constraints flow into dependent work, evidence contributes to broader evaluation, and discoveries reopen decisions in affected loops. Completion of nested loops supplies evidence for enclosing loops; it does not automatically establish their completion.

Do not force every relationship into a tree. Shared concerns can span several feature loops, and operational feedback can cross releases. Where a related process is outside the implementation's scope, declare the handoff rather than inventing an internal loop for it.

Allocate the abstract responsibilities explicitly across the declared loops. A loop may rely on inherited constraints, local work, and enclosing evaluation; do not require seven separately documented steps at every level. Identify the source of inherited decisions and how their continued applicability is checked. Allocation must not leave a responsibility unfulfilled or permit a completion claim before its required evaluation.

## Concern placement

Identify the concerns considered relevant to the agreed scope, using its goals, risks, and constraints. Consider operational and product-learning needs alongside functional behaviour; examples include observability, behavioural analytics, security, privacy, and accessibility. This is not a mandatory or exhaustive concern list.

For each relevant concern, declare:

- **Placement:** the loops or external processes where decisions are made, supporting work occurs, and evidence is evaluated.
- **Timing:** what triggers consideration or reconsideration, and the boundary by which each decision or result is required.
- **Evidence:** how the required outcome is demonstrated at that boundary.
- **Authority:** who makes the decisions, evaluates results, and accepts any handoff.

Separate deciding what evidence is needed from implementing its collection and assessing its usefulness. A concern can have several placements. For observability, defining diagnostic needs, implementing traces and spans, and evaluating their usefulness in operation need not occur at the same level or time.

For example, an implementation could place behavioural analytics as follows. These are illustrative policies, not universal sequencing requirements:

| Loop or scope | Decision or work | Evidence and required boundary | Authority |
| --- | --- | --- | --- |
| Product evolution | Govern shared event taxonomy and privacy constraints | Applicable conventions identified before feature-specific event design is approved | Product and privacy decision-makers |
| Feature delivery | Define the learning question and required observations | Agreed question before measurement design is finalised | Feature decision-maker |
| Behaviour implementation | Implement and verify event emission | Verified event properties before the instrumented behaviour is accepted | Implementer and reviewer |
| Operational review | Evaluate data quality and measurement usefulness | Findings at a declared post-release review trigger | Named operational owner |

Record deferrals and exclusions with their rationale, authorising decision-maker, and effect on completion claims. For deferred work, identify its destination and reconsideration trigger or required boundary. For out-of-scope work, name the receiving process or owner and the evidence or obligations being handed off. An unresolved handoff is a visible gap, not proof that the concern has been handled.

## Abstract procedure

These are recurring responsibilities, not seven once-only stages. Apply them through the declared [development loops](#development-loops) and [concern placements](#concern-placement). An implementation may combine, revisit, or overlap activities, including work on independent increments, provided it preserves their obligations and manages dependencies.

### 1. Establish intent and boundaries

Identify the intended outcomes and beneficiaries, relevant existing behaviour, system context, constraints, exclusions, and decision authority. Establish what successful completion would mean and expose unresolved assumptions. Identify applicable loops, relevant concerns, and lifecycle handoffs.

**Required result:** a sufficiently clear basis for choosing work, with uncertainty and limits of authority visible.

### 2. Structure the work

Identify behaviours or features and their relationships. Distinguish desired outcomes from implementation tasks. Locate the work within the declared loops and their dependencies. Decompose enough to select a bounded increment; refine the remaining work as understanding improves.

**Required result:** a navigable account of scope, dependencies, and outstanding questions. Exhaustive upfront decomposition is not required.

### 3. Select and prepare the next increment

Choose work using value, dependencies, risk, and uncertainty. Establish its intended outcome, boundaries, relevant constraints, evaluation criteria, and any decisions or unknowns that must be addressed first.

Identify the concern obligations due for this increment and the applicable progression or completion boundary.

If the increment is exploratory, state the question being investigated and how its findings will inform a decision. Do not present exploratory code as delivered functionality without the necessary delivery checks.

**Required result:** a bounded commitment with an explicit basis for evaluating its outcome.

### 4. Execute the increment

Apply the concrete implementation's protocol. Make necessary design decisions and changes within the agreed boundaries. Surface discoveries that invalidate the commitment rather than silently widening it.

**Required result:** a candidate software change, or explicit findings that inform subsequent work.

### 5. Evaluate the result

Assess conformance to the specified behaviour and constraints, and fitness for the intended need to the extent currently demonstrable. For software changes, evaluate integration and effects on existing behaviour, not only the isolated change. For exploratory work, evaluate the evidence against the question posed.

Check the concern evidence required at the current boundary using the declared placements. Keep observed results separate from assumptions and checks that were not performed.

**Required result:** evidence supporting acceptance, rework, or a clearly stated limitation.

### 6. Reconcile and adapt

Compare the result with the commitment. Update scope, assumptions, dependencies, and remaining work. Decide whether to continue, revise, investigate, pause, or stop. Apply the declared decision authority to changes in scope or acceptance criteria. Route discoveries to affected loops or external owners using the declared feedback relationships.

**Required result:** an explicit disposition of the increment and an updated basis for the next decision.

### 7. Close the agreed scope

Evaluate the combined result against the overall goal. Account for incomplete, deferred, and unverified work. Check obligations due at this completion boundary, including those inherited from enclosing loops, and account for outstanding handoffs. Preserve the information needed for review or continuation.

**Required result:** an evidence-backed completion or handoff statement. Distinguish implemented, verified, accepted, and released; do not imply one from another.

## Conformance requirements

When defining or assessing an implementation, explain:

1. **Responsibility coverage:** how it fulfils each abstract responsibility, with links to the relevant protocol or instructions.
2. **Progression conditions:** what permits work to start, advance, and finish, and what evidence supports those decisions.
3. **Exception handling:** how it handles failed checks, ambiguity, blockers, and changed assumptions, including how work resumes.
4. **Decision authority:** who can accept results, change scope, or select alternatives, and when escalation is required.
5. **Traceability:** how intended outcomes remain connected to increments, results, and evidence across handoffs.
6. **Loop structure:** how it satisfies the declarations and boundary relationships in [Development loops](#development-loops).
7. **Concern coverage:** how it satisfies [Concern placement](#concern-placement), including explicit treatment of relevant lifecycle handoffs, deferrals, and exclusions.

A responsibility may be discharged using applicable existing evidence; it may not be silently omitted. A document that names all seven activities without explaining how they are fulfilled is not sufficient. Distinguish a procedure's stated coverage from evidence that a particular execution followed it.

Implementations may add stricter rules but must not weaken this contract. Test-first sequencing, increment size, execution modality, parallelism, artifact formats, review gates, and commit cadence are implementation choices, subject to applicable project and user constraints.

When reporting an assessment, identify covered responsibilities, gaps, and the concrete provisions needed to close them. Do not certify an entire methodology from a partial source description.

For evidence-based procedure assessments or proposals to improve this model, follow [Evaluating procedures and improving the model](references/evaluating-procedures.md). It distinguishes procedure conformance from limitations of the contract itself; this file remains authoritative for the contract.

## Relationship to other skills

Treat `autonomous-engineering` as a concrete implementation candidate: its strict TDD, ambiguity escalation, ADR practices, and review artifacts provide particular ways to fulfil these responsibilities. Assess its full instructions before claiming complete conformance.

Use `test-driven-development` for its implementation cycle and phase rules, not as a replacement for this broader contract. Other implementations can use different protocols without inheriting TDD-specific requirements.

## Researched examples

Each example maps the seven responsibilities and discusses loop structure and concern placement. It separates the source's described practices from our interpretation and any additions needed for a concrete implementation. The mappings use these evidence labels:

- **Supported:** the cited material describes a relevant practice. This does not certify full conformance.
- **Partial:** the material supports part of the responsibility; the remaining provision is identified.
- **Not established:** the material reviewed does not establish the provision. This is a limit of the evidence, not proof that the wider methodology lacks it.

The examples include development processes, frameworks, and concern-specific practices; inclusion does not certify full conformance. They paraphrase selected sources rather than reproduce complete methodologies. Follow the external sources for fuller definitions. Keep implementation-specific rules in examples or implementation skills, not in the abstract procedure.

Additional-criteria tables link unresolved obligations back to this contract and use the [evaluation classifications](references/evaluating-procedures.md#3-classify-findings). They distinguish insufficient evidence from obligations belonging to a surrounding procedure, rather than treating either as a proven failure. The adopting team must establish these provisions in its concrete, composed procedure before claiming conformance.

- [Test-driven development](examples/test-driven-development.md): a fine-grained implementation and verification protocol.
- [Behaviour-driven development](examples/behaviour-driven-development.md): shared understanding and examples carried into automation.
- [Feature-driven development](examples/feature-driven-development.md): feature-level organisation and repeated design/build cycles.
- [Shape Up](examples/shape-up.md): emergent scopes and explicit treatment of uncertainty.
- [Spiral development](examples/spiral-development.md): a process family defined through invariants and risk reduction.
- [Spec-driven development with GitHub Spec Kit](examples/spec-driven-development.md): explicit artifacts connecting intent to execution.
- [OpenUP](examples/openup.md): micro-increments, iteration delivery, and project-level decisions.
- [Scrum](examples/scrum.md): product and Sprint feedback with distinct Increment quality and release boundaries.
- [Google SRE engagement models](examples/sre-engagement.md): operational concern timing and readiness for ownership transfer.
- [Continuous Discovery](examples/continuous-discovery.md): bounded learning commitments within ongoing product discovery.
- [Microsoft Security Development Lifecycle](examples/security-development-lifecycle.md): security practices spanning governance, development, and operation.
- [HEART and Goals–Signals–Metrics](examples/heart-framework.md): measurement design connecting product goals to trustworthy observations.
