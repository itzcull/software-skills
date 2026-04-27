# Architecture Decision Record Template

Use this template for one architecturally significant decision. Keep the record concise, factual, and focused on why the decision was made.

```md
# ADR-0000: Short Decision Title

## Status

Proposed | Accepted | Rejected | Superseded | Deprecated

## Metadata

- Date: YYYY-MM-DD
- Deciders: Name, Name
- Consulted: Name, Name
- Informed: Name, Name
- Confidence: High | Medium | Low
- Supersedes: ADR-0000 if applicable
- Superseded by: ADR-0000 if applicable
- Related: ADR-0000, ticket, PR, proposal, diagram, or evidence link

## Context

Describe the current situation, problem, and timing that made a decision necessary.

Include the relevant business priorities, technical constraints, operational forces, team context, compliance needs, and quality attributes. Explain why this decision matters now.

## Decision Drivers

- Driver 1
- Driver 2
- Driver 3

## Considered Options

- Option 1
- Option 2
- Option 3
- Do nothing, if viable

## Option Analysis

### Option 1: Name

Good:
- Benefit or satisfied driver

Bad:
- Cost, risk, or drawback

Neutral:
- Relevant fact that is neither clearly positive nor negative

### Option 2: Name

Good:
- Benefit or satisfied driver

Bad:
- Cost, risk, or drawback

Neutral:
- Relevant fact that is neither clearly positive nor negative

## Decision

We will choose [option] for [scope].

This decision means [clear boundary of what is adopted, changed, rejected, or governed].

## Consequences

Positive:
- Expected benefit

Negative:
- Accepted cost, risk, debt, or operational burden

Neutral:
- Side effect, limitation, or implementation implication

## Confirmation

Describe how the team will verify the decision is followed.

Examples:
- Code review checks
- Architecture fitness functions
- Automated policy checks
- Deployment guardrails
- Observability signals
- Runbook or operational review criteria

## Reevaluation Triggers

- Trigger 1
- Trigger 2
- Trigger 3

## Links

- Related ADRs
- Design proposal
- Architecture diagram
- Benchmark results
- Security or compliance review
- Incident or postmortem
```

## Status Definitions

- **Proposed**: under discussion or review; does not govern implementation yet.
- **Accepted**: ratified and actively governs implementation.
- **Rejected**: evaluated and dismissed; preserved to avoid repeating the same analysis.
- **Superseded**: replaced or materially changed by a newer ADR.
- **Deprecated**: being phased out without necessarily having a direct replacement.

## Optional Y-Statement Summary

Add this compact summary when the team benefits from an at-a-glance rationale.

```md
In the context of [functional requirement, user story, or architecture component],
facing [non-functional requirement, force, or quality attribute],
we decided for [decision outcome],
and neglected [rejected options],
to achieve [benefits],
accepting that [drawbacks].
```
