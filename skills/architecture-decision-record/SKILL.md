---
name: architecture-decision-record
description: Create, revise, or review Architecture Decision Records (ADRs). Use when documenting architectural decisions, eliciting decision rationale, comparing options, recording trade-offs, superseding previous decisions, or setting up ADR practices and templates.
license: MIT
version: 1.0.0
metadata:
  author: itzcull
---

## Purpose

Help an agent elicit decision-influencing information from an author and turn it into a concise, reviewable Architecture Decision Record. The skill focuses on capturing why a decision was made: the context, forces, options, trade-offs, consequences, confidence, and lifecycle status.

An ADR is not a design guide. It is an append-only decision log entry that records one architecturally significant choice at a specific point in time.

## When to use

- The user asks to create, write, draft, revise, or review an ADR
- The user says "architecture decision record", "architectural decision", "decision log", "record this decision", or "document why we chose"
- A technical choice affects system structure, quality attributes, operational model, team workflow, security posture, deployment model, data ownership, integration style, or long-term maintainability
- The user wants to compare architectural options and preserve the reasoning
- The user needs to supersede, reject, deprecate, or retroactively document a previous decision
- A team is setting up ADR templates, naming conventions, review practices, or governance

Do not use this skill for ordinary code comments, runbooks, implementation plans, or exhaustive solution design documents. Use `system-design` first when the decision itself still needs broad architecture exploration.

## Inputs expected

Ask for missing information only when it materially affects the ADR. Prefer targeted questions over a long intake form.

- **Decision scope**: the single decision being recorded
- **Status**: Proposed, Accepted, Rejected, Superseded, or Deprecated
- **Context**: current system state, business situation, problem, and timing
- **Decision drivers**: functional requirements, quality attributes, constraints, risks, team skills, compliance needs, cost, deadlines, and operational forces
- **Options**: alternatives considered, including doing nothing
- **Trade-offs**: positive, negative, and neutral consequences for each viable option
- **Outcome**: what was decided and how it will govern implementation
- **Confidence**: High, Medium, or Low, with uncertainty called out explicitly
- **Confirmation**: how the team will verify the decision is followed
- **Reevaluation triggers**: events that should cause the decision to be reconsidered
- **Stakeholders**: deciders, consulted people, and informed people when relevant
- **Links**: superseded ADRs, related ADRs, proposals, diagrams, tickets, PRs, or evidence

## Core principles

- **One decision per ADR**: split broad initiatives into separate records.
- **Why over what**: capture rationale, not a complete implementation guide.
- **Append-only accepted records**: do not rewrite accepted history; create a new ADR to supersede it.
- **Alternatives matter**: document rejected options to prevent repeated debates.
- **Negative consequences matter more**: hidden drawbacks turn ADRs into marketing documents.
- **Context is temporal**: explain why the decision made sense when it was made.
- **Assertive and factual tone**: write as a concise ruling, not a speculative essay.
- **Reviewable artifact**: structure the ADR so it can be debated in a pull request.

## Workflow

### Step 1: Determine the ADR mode

Identify whether the user needs:

- **New proposed ADR**: decision is under review and does not yet govern implementation
- **Accepted ADR**: decision has been ratified and governs implementation
- **Rejected ADR**: proposal was considered and dismissed
- **Superseding ADR**: a previous accepted decision is being replaced or materially changed
- **Deprecated ADR**: a technology, component, or practice is being phased out
- **Retrospective ADR**: a brownfield decision is being reconstructed from historical knowledge
- **Template or process setup**: the user wants an ADR system, not a specific record

If the mode is unclear, ask one direct question before drafting.

### Step 2: Check decision scope

Verify that the ADR captures one focused architectural decision.

Split the request when it contains multiple independent choices. For example, "migrate to cloud" should become separate ADRs for identity provider, compute platform, database migration strategy, network topology, observability, and deployment model.

Proceed with a single ADR only when the decision can be stated in one sentence.

### Step 3: Elicit decision-influencing information

If essential information is missing, ask targeted questions grouped by the smallest useful set. Do not ask for every template field when the answer is already clear from context.

High-signal questions:

- What exact decision should this ADR record?
- What problem or force made the decision necessary now?
- What constraints are non-negotiable?
- Which options were seriously considered?
- Why is the chosen option better in this context?
- What drawbacks, risks, or debts does the team accept?
- How will the team know the decision is being followed?
- What future change should trigger reevaluation?
- Who decides, who was consulted, and who needs to be informed?

If the user asks for a draft despite incomplete information, write the ADR with explicit `TBD` markers for unknown facts and list assumptions after the draft.

### Step 4: Draft the ADR

Use `references/adr-template.md` as the default structure.

Write the ADR with these style constraints:

- Use short sections and direct prose
- State the decision outcome assertively
- Include doing nothing as an option when it was viable
- Categorize option analysis as Good, Bad, and Neutral when useful
- Keep implementation details out unless they are necessary to define the decision boundary
- Link deeper design documents instead of expanding the ADR into a design guide
- Prefer concrete verification checks over vague statements like "team alignment"

Filename convention when creating a file:

- Prefer the existing repository convention if one exists
- Otherwise use `docs/decisions/ADR-0001-short-title.md` or `docs/adr/ADR-0001-short-title.md`
- Use monotonically increasing numbers; never reuse a number
- Use a short kebab-case title after the number

### Step 5: Handle lifecycle changes

For accepted ADRs, preserve the historical record.

- To replace an ADR, create a new ADR with status `Accepted` or `Proposed`, then update the old ADR status to `Superseded` and link both records
- To reject a proposal, keep the ADR with status `Rejected` and explain why it was rejected
- To phase something out without a direct replacement, mark it `Deprecated` and describe the migration impact
- To reconstruct brownfield history, mark uncertainty explicitly and distinguish known facts from inferred rationale

### Step 6: Review before finalizing

Use `references/adr-quality-checklist.md` before presenting the final ADR or saving it to a file.

Check that:

- The ADR is about one decision
- The context explains why the decision was necessary
- Decision drivers are explicit enough to evaluate options
- Alternatives are honest and not strawmen
- Negative consequences are specific
- Confirmation can be observed or tested
- Reevaluation triggers are concrete
- Status and supersession links are correct

## Output format

When drafting an ADR, output either the file path created or the complete Markdown document.

When gathering information, output a concise question set with only the missing decision-influencing information.

When reviewing an ADR, lead with findings ordered by severity, then provide a corrected draft only if requested.

## Escalation conditions

Stop and ask the user before drafting when:

- The requested decision is too broad to fit one ADR
- The chosen option is known but the rationale is absent
- The status is unclear and would change the wording or lifecycle handling
- Superseding an accepted ADR would require editing historical records without a new ADR
- The document requires confidential, compliance, or security-sensitive details that should be redacted
- Stakeholder approval is needed but the deciders are unknown

## Anti-patterns

- Writing an ADR after the fact as a justification for a favored technology
- Omitting rejected alternatives
- Hiding operational complexity, cost, security risk, or migration burden
- Bundling a program strategy into one ADR
- Turning the ADR into a tutorial, runbook, or implementation plan
- Rewriting accepted history instead of superseding it
- Using vague drivers such as "modern", "scalable", or "best practice" without context-specific meaning

## Reference files

- `references/adr-template.md` -- default ADR template
- `references/adr-quality-checklist.md` -- review checklist, lifecycle rules, and anti-patterns
