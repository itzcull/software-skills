# Software skill composition assessment

## Scope and authority

This assessment examines whether the repository's skills provide usable contributions to a user's structured-development procedure. The baseline is [`9217b61`](https://github.com/itzcull/software-skills/tree/9217b61bba5307a22c88ac8682281bb4b02e5967), after PRs #9–13. The corrections described below accompany this assessment.

[Structured development](../skills/structured-development/SKILL.md) remains authoritative for the contract. Its [evaluation framework](../skills/structured-development/references/evaluating-procedures.md) governs findings. Each supporting skill's relationship section now links its contributions to specific existing responsibilities or conformance requirements; those sections, not this assessment, own the current mappings.

The subject is prescribed guidance, not an observed execution or a complete user-configured procedure. Coverage includes all 17 skill entry points and selected workflow, handoff, verification, and review references. This is not an exhaustive technical audit of every catalog entry, code sample, or external source. No agent-execution or skill-trigger evaluations were run.

## Contribution coverage

All 16 supporting skills have a representable contribution. They need not each implement a complete loop or independently discharge all seven responsibilities. The table records the operational evidence inspected beyond the new relationship prose; it does not define phases or an execution order.

| Skill | Evidence of a usable contribution | Boundary for composition |
| --- | --- | --- |
| [Architecture decision records](../skills/architecture-decision-record/SKILL.md#workflow) | Decision scope, elicitation, lifecycle handling, and the [quality checklist](../skills/architecture-decision-record/references/adr-quality-checklist.md) connect rationale to confirmation and reconsideration. | Recorded status must reflect the deciders' authority, not approval inferred from a finished document. |
| [C4 modeling](../skills/c4-modeling/SKILL.md#workflow) | Evidence grounding, view selection, and the [artifact workflow](../skills/c4-modeling/references/agentic-workflow.md) yield models with assumptions and gaps. | A proposed view is not an observed runtime fact or an approved design. |
| [Code review](../skills/code-review/SKILL.md#process) | Scope selection, two-pass finding verification, and the report provide evidence for disposition. The [testing category](../skills/code-review/references/testing.md) must respect the selected test policy. | Findings and clean reports apply only to the assessed revision, scope, and categories. |
| [Comment guidance](../skills/comment-guidance/SKILL.md#workflow) | Source inspection, surface selection, and truth/drift checks preserve local contracts and report discrepancies. | Describing a guarantee does not prove it; conflicting sources require a decision. |
| [Design patterns](../skills/design-patterns/SKILL.md#pattern-catalog) | A selectable catalog provides alternatives for concrete design problems. | Reference guidance informs a decision; consulting it is not approval to restructure code. |
| [Diffdive](../skills/diffdive/SKILL.md#process) | Branch/base identification, history inspection, and a situation report establish context and open questions. | Inferred intent remains distinct from agreed requirements; inspection is not verification. |
| [Domain-driven design](../skills/domain-driven-design/SKILL.md#key-concepts) | Domain language, context boundaries, and strategic/tactical guidance support behavioral and design choices. | A proposed model needs domain evidence; no particular external advisor is required. |
| [Git conventions](../skills/git-conventions/references/git-commits.md#stability-invariant) | Stability, atomic commits, and PR conventions preserve reviewable change history. | Commit boundaries and execution evidence must not be confused; see the corrected findings below. |
| [Package upgrader](../skills/package-upgrader/references/upgrade-workflow.md) | Baseline, risk classification, bounded upgrades, verification, failure handling, and rollback provide a maintenance protocol. | A newer version or resolved lockfile alone does not establish compatibility or acceptance. |
| [Refactorings](../skills/refactorings/SKILL.md#categories) | A selectable transformation catalog supports explicitly scoped structural changes. | Behavior preservation requires evidence; incompatible changes need a separate scope decision. |
| [Semantic naming](../skills/semantic-naming/references/naming-decision-process.md) | Local-language inspection, role classification, and boundary checks connect proposed names to responsibilities. | A role mismatch is a design question, not permission to redesign under a rename. |
| [Sync branch](../skills/sync-branch/SKILL.md#workflow) | Preflight, integration, conflict resolution, verification, and reporting supply a bounded repository operation. | Inherited verification conditions still apply to conflict-free integration. |
| [System design](../skills/system-design/SKILL.md#reference-files) | Selectable building blocks, architecture concepts, and trade-offs support context-specific options. | Recommendations are not measured capacity, accepted decisions, or runtime readiness. |
| [Test design](../skills/test-design/SKILL.md#test-level-heuristic) | Public-interface test levels, doubles policy, and authoritative test data support meaningful evaluation. | Test selection and scheduling cannot silently waive agreed acceptance evidence. |
| [Test-driven development](../skills/test-driven-development/SKILL.md#cycle-orchestration) | Phase entry/exit rules, [handoffs](../skills/test-driven-development/references/phase-handoffs.md), escalation, and cycle reports connect behavior to execution evidence. | Cycle completion is local; integration and feature acceptance remain scoped obligations of the enclosing procedure. |
| [Twelve-factor](../skills/twelve-factor/SKILL.md#checklist) | Application-specific practices and a checklist supply deployability guidance and assessment questions. | Applicable practices do not independently prove operational usefulness or production readiness. |

`structured-development` is the contract and assessment capability, not another implementation step. No skill is excluded merely because it supplies reference knowledge, context, or change-management support rather than production code.

## Findings and corrections

The following are findings about the baseline instructions or their composition, not new obligations imposed on the abstract model.

### Conflicting TDD and commit evidence rules

**Finding: Contradicts — local progression and evidence rules conflict.** The Git reference forbade RED commits and required stable commits, yet called separate failing-test commits good practice and treated tests plus implementation in one commit as evidence against TDD. It also claimed every stable commit was deployable.

**Correction:** [Git conventions](../skills/git-conventions/references/git-commits.md#assessing-tdd-compliance) now separate test-first execution evidence from commit history. Stable tests-plus-implementation commits are valid; missing RED evidence leaves test-first ordering unestablished. Required checks and authorized commit boundaries govern checkpoints, without implying release readiness.

### Verification deferral can override an inherited boundary

**Finding: Contradicts in a composed scenario.** The sync workflow explicitly skipped checks after clean integration. That conflicts with a procedure requiring an integration check before any push, even if Git reports no textual conflict. Test-reference speed advice similarly recommended skipping checks by cadence without qualifying inherited boundaries.

**Correction:** [Sync verification](../skills/sync-branch/SKILL.md#step-7-verify) now honors required checks regardless of conflict status and distinguishes permitted CI deferral from verified completion. Test scheduling advice in the [integration](../skills/test-design/references/integration-testing.md#speed-considerations) and [E2E](../skills/test-design/references/e2e-testing.md#tips-for-speed) references cannot waive an agreed evaluation boundary.

This does not require every operation to run every test. A procedure may deliberately place evidence at another boundary, provided that placement and the receiving gate are explicit.

### Review rules conflict with the test-design policy

**Finding: Contradicts when these skills are composed.** The testing review category treated real external dependencies as missing doubles, discouraged production constructors in fixtures, and broadly classified repository interactions as implementation details. The test-design skill deliberately permits isolated real integration dependencies, application-owned constructors, and observable outgoing effects through owned roles.

**Correction:** The [testing review category](../skills/code-review/references/testing.md) references the authoritative test-design policy and distinguishes uncontrolled dependencies and internal interaction assertions from valid boundary tests. It evaluates observable behavior rather than demanding a test per function or branch.

### Unstated external dependencies

**Finding: Missing provision — availability and authority were not qualified.** Domain and system design named specific advisors without explaining their availability or authorization; the Git reference directed readers to a `software-practices` skill absent from this repository.

**Correction:** Design analysis can run directly; advisors are optional and require explicit authorization. Git guidance now links to the bundled TDD skill for cycle evidence rather than requiring an unavailable source.

## Composition walkthroughs

These are manual checks of the revised prescriptions against hypothetical cases, not executed agent tests. The public interfaces under examination are skill inputs, instructions, reports, and decisions returned to the enclosing procedure—not exact wording or internal document structure.

| Given / when | Expected result under the revised guidance | Source of the decision |
| --- | --- | --- |
| A behavior test was observed failing, the implementation passes, and both are committed together after required checks. | The commit can be stable and test-first; the cycle evidence, not separate RED commits, establishes ordering. | [TDD evidence](../skills/git-conventions/references/git-commits.md#assessing-tdd-compliance) |
| The same commit exists but no RED execution evidence is available. | Report test-first ordering as unestablished, without inferring either compliance or violation. | [TDD evidence](../skills/git-conventions/references/git-commits.md#assessing-tdd-compliance) |
| A branch integrates cleanly but an inherited pre-push integration check fails or cannot run. | Stop before push and return the failed or blocked check; textual merge success cannot discharge it. | [Sync verification](../skills/sync-branch/SKILL.md#step-7-verify) |
| Integration is clean, no check is required before push, and the procedure explicitly assigns verification to a named post-push CI gate. | Push may proceed in push mode; report deferred verification, not a CI pass or feature acceptance. | [Sync verification](../skills/sync-branch/SKILL.md#step-7-verify) |
| A required E2E check is expensive, while a speed tip suggests deferral. | Preserve the required boundary; a scheduling preference is not authorization to waive evidence. | [E2E scheduling](../skills/test-design/references/e2e-testing.md#tips-for-speed) |
| An adapter test uses an isolated real database and fixtures built with application-owned constructors. | Assess its boundary behavior and isolation; do not report missing mocks or invalid fixtures solely for those choices. | [Testing review](../skills/code-review/references/testing.md) |
| A nominal unit test unexpectedly contacts a shared production service. | Report the uncontrolled dependency; permission for deliberate integration testing does not justify this case. | [Testing review](../skills/code-review/references/testing.md) |
| An ADR is drafted without acceptance from the identified decider, or a C4 relationship is only inferred. | Preserve proposed or uncertain status; document completion does not supply the missing approval or observation. | [ADR workflow](../skills/architecture-decision-record/SKILL.md#workflow), [C4 grounding](../skills/c4-modeling/SKILL.md#step-2-ground-the-model-in-evidence) |

## Disposition and remaining uncertainty

**Keep the abstract model unchanged.** The examined capabilities are faithfully representable through its existing responsibilities, loops, concern placement, evidence, and authority. The discovered conflicts concern concrete progression rules and interpretation; none demonstrates representational failure.

All supporting skills have an identified contribution and an explicit boundary. That is narrower than a claim that every possible combination conforms. Which skills to select, who accepts their results, how inherited constraints are supplied, and which checks are due at each boundary remain properties of a concrete user procedure.

Full execution conformance remains **Unknown** until such a procedure and its execution evidence are assessed. Resolve that uncertainty with realistic end-to-end skill evaluations covering normal progress, missing inputs, failed checks, revised decisions, and final acceptance. Catalog-wide technical correctness and the quality of generated software remain outside this assessment.
