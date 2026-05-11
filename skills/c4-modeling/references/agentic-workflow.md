# Agentic Workflow For C4 Modeling

## Purpose

LLM agents are useful for C4 modeling when they operate inside deterministic constraints: inspect evidence, infer cautiously, generate text-based models, and audit the output against C4 rules.

Do not ask an agent to draw a visual architecture diagram from imagination. Ask it to produce architecture-as-code from verified sources.

## Phase 1: Prompt Grounding

Before modeling, establish:

- Target audience
- System boundary
- Desired C4 view
- Output notation
- Evidence available
- Whether the task is creation, revision, audit, or reverse engineering

Default behavior:

- Generate System Context and Container views first.
- Skip Component views unless they add clear value.
- Skip Code views unless explicitly requested.
- Use Structurizr DSL for durable artifacts.
- Separate uncertain assumptions from observed facts.

## Phase 2: Codebase And Infrastructure Parsing

For reverse engineering, inspect evidence in this order when available:

1. README and existing architecture docs
2. Dependency manifests and package metadata
3. Application entry points and routing definitions
4. API specifications, schema files, and client SDKs
5. Docker Compose, Dockerfiles, Kubernetes manifests, Terraform, CDK, Pulumi, or cloud config
6. CI/CD pipelines and deployment scripts
7. Database migrations, message topics, queue definitions, and environment variable names
8. Observability, service catalog, or Backstage metadata

Map evidence to C4 carefully:

- Repository or product boundary can indicate a software system, but verify from docs or deployment context.
- Deployable services, clients, workers, databases, and brokers usually map to containers.
- Internal modules, controllers, adapters, repositories, and domain services can map to components only inside one selected container.
- Cloud resources and runtime hosts map to deployment nodes or infrastructure elements.

## Phase 3: DSL Generation

Generate text artifacts, not screenshots.

For each element, include:

- C4 type
- Name
- Responsibility
- Technology when known
- Evidence or confidence when the source is uncertain

For each relationship, include:

- Direction
- Verb phrase
- Protocol or mechanism when known
- Evidence source when derived from code or infrastructure

If the evidence supports a relationship but not a protocol, state the relationship and mark the protocol as unknown rather than inventing one.

## Phase 4: Audit Loop

Review the generated model before presenting it.

Audit questions:

- Does each view answer one clear question?
- Are abstraction levels separated?
- Are all arrows directional and labeled?
- Are protocols real or clearly marked as assumptions?
- Are element names domain-specific rather than generic?
- Are boundaries explicit?
- Would the target audience understand the diagram without a walkthrough?
- Is any sensitive infrastructure or security detail exposed unnecessarily?

If the model fails the audit, revise it before presenting the final artifact.

## Phase 5: Artifact Delivery

Deliver the smallest useful artifact:

- Structurizr DSL workspace for durable architecture-as-code
- Mermaid diagram for lightweight Markdown embedding
- Review findings for an existing diagram
- A list of missing facts when reliable modeling is not possible

Include a short note covering:

- Views generated
- Evidence inspected
- Assumptions made
- Known gaps
- Rendering or maintenance instructions

## Multi-Agent Review Pattern

For high-stakes architecture artifacts, use separate roles conceptually even if one agent performs the work:

- **Generator:** creates the first model from requirements and evidence
- **C4 Auditor:** checks abstraction levels, labels, notation, and C4 compliance
- **Operational Reviewer:** checks deployment, protocols, resilience, and infrastructure implications
- **Security Reviewer:** checks sensitive topology exposure, trust boundaries, and data-flow clarity

The final model should reflect verified corrections from these perspectives, not raw first-pass generation.
