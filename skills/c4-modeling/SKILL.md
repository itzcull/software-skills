---
name: c4-modeling
description: Create, review, or maintain C4 model architecture diagrams and architecture-as-code artifacts. Use for system context, container, component, dynamic, deployment, or landscape diagrams; Structurizr DSL; Mermaid architecture diagrams; architecture visualization; diagram audits; and codebase-derived software architecture maps.
license: MIT
version: 1.0.0
metadata:
  author: itzcull
---

## Purpose

Help an agent create, audit, and maintain software architecture models using the C4 model. The skill emphasizes progressive disclosure, stakeholder-appropriate views, architecture-as-code, and reviewable diagram artifacts that avoid ambiguous "boxes and lines" communication.

Use C4 to communicate structure, responsibilities, and relationships. Do not use it as a complete enterprise modeling framework, detailed UML replacement, deployment runbook, or exhaustive source-code map.

## When to use

- The user asks for a C4 model, C4 diagram, system context diagram, container diagram, component diagram, dynamic diagram, deployment diagram, or system landscape
- The user wants to visualize software architecture, system boundaries, service dependencies, runtime collaboration, or deployment topology
- The user asks for Structurizr DSL, Mermaid, PlantUML, diagram-as-code, or architecture-as-code for software architecture
- The user wants to audit an existing architecture diagram for clarity, abstraction-level mixing, missing relationship labels, missing protocols, or diagram drift
- The user wants to derive architecture documentation from a codebase, repository structure, dependency manifests, IaC, deployment configuration, or service catalog metadata
- The user needs an architecture diagram for an ADR, design review, onboarding document, platform catalog, or engineering proposal

Do not use this skill for broad distributed-systems design tradeoffs before the architecture exists; use `system-design` first. Use `architecture-decision-record` when the main artifact is a decision record rather than a model.

## Inputs expected

Ask for missing information only when it materially changes the diagram or output artifact.

- **System scope**: the software system or portfolio being modeled
- **Audience**: executives, product stakeholders, architects, DevOps, developers, maintainers, or reviewers
- **View type**: landscape, context, container, component, dynamic, or deployment; default to context plus container when unclear
- **Evidence source**: codebase, README, architecture docs, dependency manifests, IaC, service catalog, cloud config, or user-provided description
- **Output format**: Structurizr DSL by default for durable architecture-as-code; Mermaid when lightweight Markdown embedding is more important
- **Known constraints**: organizational standards, cloud provider, protocols, compliance boundaries, deployment environments, or naming conventions

## Core principles

- **Progressive disclosure**: model architecture as zoom levels. Do not mix abstraction tiers on one diagram.
- **Audience fit**: omit implementation detail that the target audience does not need.
- **Model before view**: define stable elements and relationships before rendering individual diagrams.
- **Prefer Level 1 and Level 2**: System Context and Container views satisfy most documentation needs.
- **Use Component views selectively**: create them only when a container's internal structure is too important or complex to infer from code.
- **Avoid Level 4 by default**: Code diagrams drift quickly and should be reserved for unusually complex implementation logic.
- **Every relationship earns its line**: each arrow must be directional, labeled with a verb phrase, and include a technology or protocol when known.
- **Diagrams must be self-contained**: include enough naming, descriptions, boundaries, and legends for review without a verbal walkthrough.
- **Architecture-as-code prevents drift**: prefer text artifacts that are version-controlled, diffable, and generated from one structural model.

## Workflow

### Step 1: Establish the modeling goal

Identify the audience, decision or communication need, and artifact format.

Default choices:

- Use **System Context** for scope, users, external systems, and stakeholder alignment.
- Use **Container** for deployable or runnable units, data stores, message brokers, clients, and protocols.
- Use **Component** only for one container whose internal modules matter to maintainers.
- Use **Dynamic** for a specific runtime workflow, user story, transaction, or asynchronous message flow.
- Use **Deployment** for infrastructure mapping, network boundaries, availability zones, runtime nodes, or operational reliability.
- Use **System Landscape** for an enterprise or portfolio-level map across many systems.

If the user asks for "a C4 diagram" without a level, generate a System Context and Container view unless the available evidence only supports one of them.

### Step 2: Ground the model in evidence

Before generating architecture-as-code from an existing project, inspect the most relevant sources:

- Repository README and docs for stated system purpose and user-facing boundaries
- Dependency manifests for runtime stacks and major framework choices
- Application entry points, routing, API definitions, and client apps for containers and exposed behavior
- Infrastructure-as-code, Docker Compose, Kubernetes manifests, CI/CD config, or cloud config for deployable units and deployment nodes
- Message schemas, queue config, database migrations, and environment variables for relationships and backing services

Distinguish observed facts from inferred architecture. Mark uncertain relationships as assumptions rather than presenting them as verified structure.

### Step 3: Choose the output notation

Prefer `Structurizr DSL` when the artifact is intended to be maintained, reviewed, or rendered into multiple synchronized views. Use Mermaid only when the user needs a small diagram embedded directly in Markdown and does not need a reusable architectural model.

When generating Structurizr DSL:

- Define people, software systems, containers, components, deployment nodes, and relationships in the `model` block.
- Define diagrams separately in the `views` block.
- Use `include *` only when it does not pull in unrelated detail.
- Apply `autoLayout` instead of hand-positioning unless the user requests manual layout.

### Step 4: Generate or revise the model

Create the smallest useful model that satisfies the communication need.

For every element, include:

- A concrete name
- Its C4 type
- A short responsibility description
- Technology metadata when relevant at that abstraction level

For every relationship, include:

- Source and destination
- Direction
- Descriptive verb phrase
- Protocol, format, or mechanism when known

### Step 5: Audit before presenting

Review the output against the C4 quality checklist:

- No mixed abstraction levels on a single view
- No unlabeled arrows
- No relationship labels that are vague nouns such as "data" or "business logic"
- No containers in a context view unless represented as the software system boundary
- No database tables, classes, or functions in context or container views
- No unexplained colors, icons, shapes, borders, or line styles
- No bidirectional arrows unless the bidirectionality is intentional and explicitly labeled
- No inferred protocols presented as facts
- No component or code views unless they add clarity beyond existing code structure

### Step 6: Present the artifact

Return the generated DSL or Markdown diagram plus a short explanation of:

- Which views were created and why
- What evidence or assumptions shaped the model
- Any known gaps, uncertainties, or follow-up questions
- How to render or maintain the artifact when relevant

## Output format

When creating architecture-as-code, output one of:

- A file path created in the repository
- A complete Structurizr DSL block
- A complete Mermaid diagram block
- A concise review report for existing diagrams

When reviewing, lead with findings ordered by severity, then include a corrected version only if requested.

## Escalation conditions

Stop and ask before generating the final artifact when:

- The system boundary is ambiguous enough that a context diagram would mislead readers
- The user requests mixed C4 levels in one diagram and does not accept separating them
- Required deployment, protocol, or data-flow facts are unavailable and guessing would create false confidence
- The diagram would expose secrets, internal network details, regulated data paths, or security-sensitive topology
- The requested output is really an ADR, threat model, runbook, or detailed UML design rather than a C4 model

## Anti-patterns

- Treating C4 as decorative boxes and lines
- Modeling everything in one diagram
- Placing database tables, classes, or functions in high-level views
- Generating Level 4 code diagrams for ordinary code
- Using vague element names such as "Backend", "Manager", "Logic", or "Database" without responsibility and technology context
- Drawing arrows without verbs or protocols
- Maintaining hand-drawn diagrams as the source of truth when DSL artifacts would fit the workflow
- Treating inferred LLM output as authoritative without codebase or infrastructure evidence

## Reference files

- `references/core-model.md` -- C4 levels, supplementary views, audiences, and default usage
- `references/modeling-rules.md` -- notation quality checklist, relationship rules, and anti-patterns
- `references/architecture-as-code.md` -- Structurizr DSL, Mermaid, and architecture-as-code guidance
- `references/agentic-workflow.md` -- codebase-grounded agent workflow for generating and auditing C4 models
