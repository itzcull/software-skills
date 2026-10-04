---
name: structured-development
description: Define, adapt, or assess structured procedures for implementing a series of software behaviours or features. Use when designing development workflows, comparing methodologies, or checking whether a concrete workflow fulfils a shared development contract. Separates abstract responsibilities from implementation-specific protocols such as autonomous engineering, TDD, and spec-driven development.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Structured development defines a methodology-independent contract for incremental software development within a broader software lifecycle. Concrete procedures specify how its responsibilities are fulfilled.

Advance development through bounded, evidence-producing increments. This skill governs development through completion or handoff of agreed scope; it does not define the entire software development lifecycle (SDLC), including deployment, operations, and retirement.

## Authority and terminology

This file is authoritative for the abstract procedure and conformance requirements. Concrete implementation skills own their execution rules. The researched examples illustrate possible mappings; they do not add requirements to the contract.

- **Behaviour**: an observable response of a system under specified conditions.
- **Feature**: a capability realised through one or more behaviours.
- **Increment**: a bounded piece of work with an intended outcome and an explicit basis for evaluating it. An increment can deliver software or resolve a development uncertainty; those outcomes are not interchangeable.
- **Implementation**: a concrete development procedure that fulfils the abstract responsibilities below.
- **Protocol**: the steps, progression conditions, evidence, and exception handling prescribed for an activity.
- **Modality**: how participation and decision-making are arranged, such as guided collaboration or autonomous execution within agreed boundaries.

An implementation may combine protocols and modalities. Neither autonomous execution nor the use of this skill grants permission to delegate, commit, deploy, or make decisions outside the user's agreed authority.

## Using the abstraction

1. Establish whether the task is to define an implementation, assess an existing one, or execute one already selected.
2. Read the concrete implementation when one exists. Read only the researched examples relevant to a comparison or unresolved design choice.
3. Map the implementation to the responsibilities and conformance requirements below. Identify missing provisions rather than inventing them silently.
4. For execution, resolve missing provisions that materially affect the next increment before proceeding. Reuse existing decisions and evidence where they remain applicable.

Do not force a new document or tool for each responsibility. Existing plans, tests, discussions, and review records can provide the required information if it remains accessible and unambiguous.

## Abstract procedure

These are recurring responsibilities, not seven once-only stages. An implementation may combine, revisit, or overlap activities, including work on independent increments, provided it preserves their obligations and manages dependencies.

### 1. Establish intent and boundaries

Identify the intended outcomes and beneficiaries, relevant existing behaviour, system context, constraints, exclusions, and decision authority. Establish what successful completion would mean and expose unresolved assumptions.

**Required result:** a sufficiently clear basis for choosing work, with uncertainty and limits of authority visible.

### 2. Structure the work

Identify behaviours or features and their relationships. Distinguish desired outcomes from implementation tasks. Decompose enough to select a bounded increment; refine the remaining work as understanding improves.

**Required result:** a navigable account of scope, dependencies, and outstanding questions. Exhaustive upfront decomposition is not required.

### 3. Select and prepare the next increment

Choose work using value, dependencies, risk, and uncertainty. Establish its intended outcome, boundaries, relevant constraints, evaluation criteria, and any decisions or unknowns that must be addressed first.

If the increment is exploratory, state the question being investigated and how its findings will inform a decision. Do not present exploratory code as delivered functionality without the necessary delivery checks.

**Required result:** a bounded commitment with an explicit basis for evaluating its outcome.

### 4. Execute the increment

Apply the concrete implementation's protocol. Make necessary design decisions and changes within the agreed boundaries. Surface discoveries that invalidate the commitment rather than silently widening it.

**Required result:** a candidate software change, or explicit findings that inform subsequent work.

### 5. Evaluate the result

Assess conformance to the specified behaviour and constraints, and fitness for the intended need to the extent currently demonstrable. For software changes, evaluate integration and effects on existing behaviour, not only the isolated change. For exploratory work, evaluate the evidence against the question posed.

Keep observed results separate from assumptions and checks that were not performed.

**Required result:** evidence supporting acceptance, rework, or a clearly stated limitation.

### 6. Reconcile and adapt

Compare the result with the commitment. Update scope, assumptions, dependencies, and remaining work. Decide whether to continue, revise, investigate, pause, or stop. Apply the declared decision authority to changes in scope or acceptance criteria.

**Required result:** an explicit disposition of the increment and an updated basis for the next decision.

### 7. Close the agreed scope

Evaluate the combined result against the overall goal. Account for incomplete, deferred, and unverified work. Preserve the information needed for review or continuation.

**Required result:** an evidence-backed completion or handoff statement. Distinguish implemented, verified, accepted, and released; do not imply one from another.

## Conformance requirements

When defining or assessing an implementation, explain:

1. **Responsibility coverage:** how it fulfils each abstract responsibility, with links to the relevant protocol or instructions.
2. **Progression conditions:** what permits work to start, advance, and finish, and what evidence supports those decisions.
3. **Exception handling:** how it handles failed checks, ambiguity, blockers, and changed assumptions, including how work resumes.
4. **Decision authority:** who can accept results, change scope, or select alternatives, and when escalation is required.
5. **Traceability:** how intended outcomes remain connected to increments, results, and evidence across handoffs.

A responsibility may be discharged using applicable existing evidence; it may not be silently omitted. A document that names all seven activities without explaining how they are fulfilled is not sufficient. Distinguish a procedure's stated coverage from evidence that a particular execution followed it.

Implementations may add stricter rules but must not weaken this contract. Test-first sequencing, increment size, execution modality, parallelism, artifact formats, review gates, and commit cadence are implementation choices, subject to applicable project and user constraints.

When reporting an assessment, identify covered responsibilities, gaps, and the concrete provisions needed to close them. Do not certify an entire methodology from a partial source description.

## Relationship to other skills

Treat `autonomous-engineering` as a concrete implementation candidate: its strict TDD, ambiguity escalation, ADR practices, and review artifacts provide particular ways to fulfil these responsibilities. Assess its full instructions before claiming complete conformance.

Use `test-driven-development` for its implementation cycle and phase rules, not as a replacement for this broader contract. Other implementations can use different protocols without inheriting TDD-specific requirements.

## Researched examples

Each example separates the source's described practices from our mapping and any additions needed for a concrete implementation. The mappings use these evidence labels:

- **Supported:** the cited material describes a relevant practice. This does not certify full conformance.
- **Partial:** the material supports part of the responsibility; the remaining provision is identified.
- **Not established:** the material reviewed does not establish the provision. This is a limit of the evidence, not proof that the wider methodology lacks it.

The examples paraphrase selected sources rather than reproduce their complete methodologies. Follow the external sources for fuller definitions. Keep implementation-specific rules in examples or implementation skills, not in the abstract procedure.

- [Test-driven development](examples/test-driven-development.md): a fine-grained implementation and verification protocol.
- [Behaviour-driven development](examples/behaviour-driven-development.md): shared understanding and examples carried into automation.
- [Feature-driven development](examples/feature-driven-development.md): feature-level organisation and repeated design/build cycles.
- [Shape Up](examples/shape-up.md): emergent scopes and explicit treatment of uncertainty.
- [Spiral development](examples/spiral-development.md): a process family defined through invariants and risk reduction.
- [Spec-driven development with GitHub Spec Kit](examples/spec-driven-development.md): explicit artifacts connecting intent to execution.
