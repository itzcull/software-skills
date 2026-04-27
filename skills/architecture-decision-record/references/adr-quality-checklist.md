# ADR Quality Checklist

Use this checklist before presenting, saving, or approving an Architecture Decision Record.

## Scope

- The ADR records exactly one decision.
- The decision can be summarized in one sentence.
- Broad programs are split into smaller ADRs.
- Implementation details only appear when they define the decision boundary.

## Context

- The context explains why a decision is needed now.
- The record includes business, technical, operational, social, compliance, or timing forces that materially influenced the decision.
- The context is specific enough for a future team to judge whether the decision still applies.
- Brownfield or retrospective ADRs distinguish known facts from reconstructed assumptions.

## Decision Drivers

- Drivers are concrete and context-specific.
- Quality attributes are named precisely, such as latency, availability, consistency, auditability, deployability, operability, security, cost, or time-to-market.
- Vague drivers like "modern", "scalable", "simple", or "best practice" are explained in local terms.
- Non-negotiable constraints are separated from preferences.

## Options

- Serious alternatives are documented, including doing nothing when viable.
- Rejected options are not strawmen.
- The chosen option is evaluated against the same drivers as the alternatives.
- Trade-offs are phrased as evidence or reasoned judgement, not personal preference.

## Decision

- The decision statement is assertive and factual.
- The decision boundary is clear: what is adopted, rejected, governed, or out of scope.
- The ADR does not read like a tutorial, sales pitch, or implementation plan.
- Confidence is stated when uncertainty affects future risk.

## Consequences

- Positive consequences describe concrete benefits.
- Negative consequences describe accepted costs, risks, debt, migration burden, operational complexity, or future constraints.
- Neutral consequences capture relevant facts that are neither clearly positive nor negative.
- The consequences would help a future maintainer understand the burden the team accepted.

## Confirmation

- The ADR explains how compliance with the decision will be verified.
- Confirmation uses observable checks where possible.
- Automation is named when available, such as tests, lint rules, architecture fitness functions, policy checks, or deployment guardrails.
- Manual confirmation is tied to a concrete review practice.

## Lifecycle

- Status is one of Proposed, Accepted, Rejected, Superseded, or Deprecated.
- Accepted ADRs are treated as append-only historical records.
- Superseded ADRs link to the newer ADR.
- New superseding ADRs link back to the older ADR.
- Rejected ADRs explain why the option was dismissed.
- Deprecated ADRs explain what is being phased out and what migration impact remains.

## Review Culture

- Review comments focus on problems, evidence, trade-offs, and alternatives.
- Reviewers do not psychoanalyze the author or infer motives.
- Critique is direct, technical, fair, and actionable.
- The review keeps the ADR concise instead of expanding it into a design document.

## Common Anti-Patterns

- **Illusion of choice**: the team makes a verbal decision but records no rationale.
- **Post-hoc advocacy**: the ADR justifies a preferred technology instead of weighing forces.
- **Hidden downside**: negative consequences are omitted to make approval easier.
- **Mega-ADR**: one record bundles many independent decisions.
- **Design guide drift**: the ADR becomes a long implementation manual.
- **Mutable history**: accepted ADRs are edited in place instead of superseded.
- **Context-free best practice**: the record relies on generic industry advice without explaining local fit.

## Final Pass Questions

- Would a new engineer understand why this decision made sense at the time?
- Would the team know when to revisit this decision?
- Would rejected alternatives stay rejected for understandable reasons?
- Would an incident responder or auditor know which architectural constraint applies?
- Is the ADR short enough to review in a pull request?
