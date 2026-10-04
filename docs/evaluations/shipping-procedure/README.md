# Executed shipping-procedure exercise

## What was tested

A single executor used the skills at [`f309ede`](https://github.com/itzcull/software-skills/tree/f309ede22a1afbcfd05d7a0639a09bea8af741f4) to implement and evaluate a small checkout change in temporary Git repositories. The [procedure](procedure.md) declares its loops, decision authority, inherited concerns, checks, and completion boundaries.

The exercised composition was [structured-development](../../../skills/structured-development/SKILL.md), [test-design](../../../skills/test-design/SKILL.md), [TDD phase execution](../../../skills/test-driven-development/SKILL.md), [Git conventions](../../../skills/git-conventions/SKILL.md), [code review](../../../skills/code-review/SKILL.md), and [sync-branch](../../../skills/sync-branch/SKILL.md). Other skills were not exercised by this run.

Unlike the earlier prescription walkthrough, this exercise ran actual tests, commits, a conflict-free rebase, and local-remote operations. It persisted and consumed phase handoffs. However, the executor also authored the scenarios and played the fixture controller. Product decisions were explicitly scripted, not live stakeholder approvals; review was not independent.

## Observed outcomes

| Case | Observation | Disposition and evidence |
| --- | --- | --- |
| Normal completion | A new free-shipping test failed with `500 !== 0`. Minimal implementation then passed all 3 checks, followed by explicit no-refactor assessment. | Fixture increment accepted and committed with test and implementation together. [RED](evidence/05-normal-red.json), [GREEN](evidence/06-normal-green.json), [cycle report](handoffs/normal-cycle-report.md). |
| Ambiguity | The discount request omitted gross-versus-net eligibility. The worktree and source fingerprint remained unchanged at the recorded pause. After a scripted net-subtotal decision, the new CLI test failed, then all 4 checks passed. | Escalated before RED, then resumed under the recorded decision. [Pause](evidence/11-ambiguity-stop.json), [question](handoffs/ambiguity-stop.md), [decision](handoffs/decision-a1.md), [cycle report](handoffs/discount-cycle-report.md). |
| Failed verification | A controller-owned parser change passed its 2 old baseline tests. Rebase of the feature completed without a textual conflict. Both quote tests still passed, but both CLI tests failed because the parser now multiplied cent inputs by 100. | Integration remained blocked. No push was attempted in the recorded sync case; the remote feature SHA before and after was identical. [Clean rebase](evidence/24-sync-rebase.json), [failed gate](evidence/25-sync-required-check.json), [before](evidence/22-sync-remote-before.json), [after](evidence/26-sync-remote-after.json), [escalation](handoffs/sync-blocked.md). |
| Changed requirement | The controller explicitly superseded the 5000-cent threshold with 7500 cents. The revised expectation failed against old production code, then passed after the policy change. The completed cycle did not itself satisfy feature acceptance. | Two additional checkout boundary checks were required by the enclosing loop; acceptance waited until all 6 checks passed. [Decision](handoffs/decision-c1.md), [RED](evidence/29-change-red.json), [cycle disposition](handoffs/change-cycle-report.md), [feature checks](evidence/32-change-feature-checks.json), [scoped acceptance](handoffs/change-feature-acceptance.md). |

The changed-requirement case deliberately started from the accepted pre-sync checkpoint, not the blocked integration tree. Its acceptance does **not** establish compatibility with the latest fixture trunk. That integration remains unresolved. Nothing was deployed or released.

## Evidence and replay

- [Command evidence](evidence/): 35 records containing commands, actual exit codes, stdout/stderr, Git heads, worktree status, and source fingerprints before and after each recorded boundary.
- [Source snapshots](snapshots.json): the 10 distinct source states referenced by those fingerprints, including the tests used in each state.
- [Handoffs](handoffs/): phase evidence, escalation requests, scripted decisions, and separate cycle/feature dispositions. Record filenames in these handoffs are relative to this exercise's `evidence/` directory.
- [Recorder](record-command.py): the helper used during the original run, archived with subsequent formatting, type-checking, and input-error handling cleanup. The archived records factor source contents into `snapshots.json` without changing their fingerprints; the recorder originally stored those contents inline.

From the repository root, run:

```bash
python3 docs/evaluations/shipping-procedure/replay-evidence.py
```

When elsewhere, use the script's absolute path; it locates evidence relative to itself. It requires Python 3.10+ and Node.js with `node:test`. The original run used Python 3.14.8, Node.js 26.3.0, and Git 2.50.1.

[Replay](replay-evidence.py) checks snapshot integrity and the recorded progression boundaries, reconstructs each test source state in a fresh temporary directory, and executes all 13 recorded test states. It verifies the observed test totals and passes/failures, including the expected RED and blocked-integration failures. It does not mutate this repository, contact a remote, rerun Git operations, or invoke an LLM.

The replay completed successfully for all 13 states. Negative controls also confirmed rejection of a tampered source snapshot and a missing command record. A successful replay means the captured application outcomes are reproducible; it does not prove that an agent would make the same decisions on a new task. The archived fixture is executable code and should be reviewed before replaying it.

## What this establishes

For this bounded execution, the existing model represented:

- A behavior loop that supplied evidence to, but did not automatically complete, its feature loop.
- Inherited currency-unit and verification obligations spanning implementation and branch integration.
- An ambiguity pause followed by an explicitly sourced change to cycle inputs.
- A clean Git operation that failed the enclosing verification gate and was not pushed.
- A requirement change that superseded one criterion while preserving other commitments.
- Distinct implemented, verified, fixture-accepted, blocked, and unreleased states.

These are observed outcomes of this selected procedure, not new universal phases. No representational failure was demonstrated, so this run supplies no basis for changing the abstract model. It also provides no evidence that all combinations of repository skills will behave correctly.

## Limitations and setup faults

- One task, one executor, and scripted decisions: no blind comparison, independent review, repeated-run reliability estimate, or unprompted ambiguity-detection measurement.
- Direct sequential phase execution was tested, not separate-context orchestration, live guided-pairing approval, or skill-trigger selection.
- The application is deliberately small and dependency-free. Valid integer inputs are assumed. Production deployment, security, persistence, performance, and the other supporting skills remain outside scope.
- The blocked sync case was not repaired. Recovery after that blocker and latest-trunk acceptance remain untested.
- Command records capture selected boundaries, not an authenticated complete interaction transcript. Git history and authority decisions are not independently replayed.
- No linter, type checker, or separate build was configured for the JavaScript fixture; none is claimed as a passing check. Executed Node tests parse and run the fixture modules.
- The first recorder attempt encountered macOS `/tmp` versus `/private/tmp` path normalization before saving a record. It was corrected and the baseline check rerun. The local bare remote also needed its HEAD explicitly set to `master` before the upstream fixture checkout. These were harness setup faults, not passing skill evaluations.
- One empty scratch placeholder was inadvertently created outside the temporary fixture and immediately removed, without modifying existing files. This was an executor scope mistake; no blanket claim of error-free execution is made.

The next stronger evaluation would use an independently executing agent against withheld scenario interventions and real or independently supplied authority decisions. That would test whether the skills reliably cause these behaviors, rather than only showing that this executor could follow them.
