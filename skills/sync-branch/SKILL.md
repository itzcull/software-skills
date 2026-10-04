---
name: sync-branch
description: >-
  Sync the current feature/PR branch with trunk — fetch latest master/main,
  rebase by default or merge it in, resolve conflicts, verify, and optionally
  push. Use when asked to "pull down latest master, resolve conflicts, commit
  and push", update a stale branch, rebase onto trunk, or refresh a PR against
  main/master before merge. Arguments are positional: push|keep-local then
  rebase|merge, defaulting to push rebase.
license: MIT
metadata:
  author: itzcull
---

## Purpose

Integrate the latest trunk into the current feature branch safely and repeatably. This
captures the recurring ritual performed on most PRs — "pull down the latest master, resolve any
conflicts, commit and push" — so it runs the same careful way every time, while allowing the
synced branch to be kept local when requested.

The default strategy is **rebase** (keeps a linear history; the branch replays on top of fresh
trunk). **Merge** is available when a merge commit is preferred or history must not be rewritten.

The default destination behavior is **push**. Use **keep-local** when the branch should be synced
locally without updating the remote branch.

## Relationship to structured development

Within [structured development](../structured-development/SKILL.md), this skill supplies a bounded repository-integration operation when a development branch needs current trunk changes. It supports [preparing further work](../structured-development/SKILL.md#3-select-and-prepare-the-next-increment) and [reconciling changes](../structured-development/SKILL.md#6-reconcile-and-adapt) without selecting new feature scope.

Use the current branch, trunk, agreed strategy and destination mode, and existing worktree state as described in [Inputs / Arguments](#inputs--arguments) and preflight. Return the [sync report](#step-10-report), including conflicts, verification, push outcome, and restored-work status. Route irreconcilable intent, failed checks, or unresolved local changes back to the enclosing procedure before it continues on assumptions that the operation succeeded.

Successful synchronization is not feature acceptance or proof of behavioral integration. Apply the [verification rules](#step-7-verify) to both conflict resolution and inherited progression conditions; when local checks may be deferred to CI, report that distinction rather than claiming checks passed. The enclosing procedure remains responsible for obtaining the evidence required at its next acceptance boundary. Preserve the requested push or keep-local mode; synchronization does not authorize merging the feature into trunk or releasing it.

## When to use

- The user says "pull down the latest master/main, resolve conflicts, commit and push"
- Syncing or refreshing a PR branch against trunk before review or merge
- Rebasing the current branch onto the latest trunk
- Updating a stale branch that has fallen behind trunk
- Keeping a locally synced branch without pushing, when requested with `keep-local`

Operates on the **current branch only**. It never modifies trunk and never touches other branches.

## Inputs / Arguments

Arguments are positional:

```text
/sync-branch [push|keep-local] [rebase|merge]
```

- First argument: destination behavior. `push` updates the remote branch after a successful sync.
  `keep-local` skips pushing and leaves the synced branch local. Default: `push`.
- Second argument: sync strategy. `rebase` replays the current branch on top of trunk. `merge`
  merges trunk into the current branch. Default: `rebase`.

Examples:

- `/sync-branch` → `push rebase`
- `/sync-branch push` → `push rebase`
- `/sync-branch keep-local` → `keep-local rebase`
- `/sync-branch push merge` → `push merge`
- `/sync-branch keep-local merge` → `keep-local merge`

If an unknown value is passed in either position, stop and ask the user to choose one of the
supported values rather than guessing.

## Strategy

- **Rebase (default)** — `git rebase origin/<trunk>`, replaying branch commits on top of trunk.
  History is rewritten, so push mode uses `git push --force-with-lease`.
- **Merge** — `git merge origin/<trunk>`, producing a merge commit. History is preserved, so the
  push is a plain `git push`.

## Workflow

### Step 1: Resolve arguments

Resolve the positional arguments before running git commands:

- `pushMode`: first argument, default `push`, allowed values `push` or `keep-local`.
- `syncStrategy`: second argument, default `rebase`, allowed values `rebase` or `merge`.

If the user describes the behavior in prose instead of slash-command arguments, map it to the same
contract. For example, "commit and push" means `push`; "don't push" or "keep it local" means
`keep-local`; "merge master" means `merge`; "rebase onto master" means `rebase`.

### Step 2: Preflight safety

- Identify the current branch: `git branch --show-current`.
  - If empty (detached HEAD), stop and ask which branch to sync.
  - If the current branch **is** trunk (see Step 3), stop — there is nothing to sync onto itself.
- Check for uncommitted work: `git status --porcelain`. If the working tree is dirty, stash it
  (`git stash push -u -m sync-branch`) and remember to restore it in Step 9.
- Record the current commit as a rollback anchor: `git rev-parse HEAD`. If the integration goes
  wrong, `git reset --hard <anchor>` restores the pre-sync state.

### Step 3: Determine trunk

Detect the trunk branch in this order:

1. `git symbolic-ref --quiet refs/remotes/origin/HEAD` → strip to the branch name (most reliable;
   reflects the remote's actual default branch).
2. Fall back to `main`, then `master`, whichever exists.

Verify the chosen trunk exists with `git rev-parse --verify origin/<trunk>`. If none can be found,
ask the user to specify it.

### Step 4: Fetch latest trunk

Determine the remote (default `origin`, or the current branch's upstream remote). Fetch:

```
git fetch <remote>
```

### Step 5: Integrate

- Rebase (default): `git rebase <remote>/<trunk>`
- Merge: `git merge <remote>/<trunk>`

### Step 6: Resolve conflicts autonomously

If the integration reports conflicts, resolve them without waiting for approval, then continue.
Set a `conflictsOccurred` flag (it gates Step 7).

For each conflicted file:

- Read **both** sides and understand the intent behind each. See "Conflict resolution guidance".
- Write a resolution that **preserves both intents** — never silently drop a side.
- `git add` the resolved file.

Then continue the integration:

- Rebase: `git rebase --continue` (repeat resolution for each replayed commit until done).
- Merge: commit the merge (`git commit --no-edit`).

If a conflict is genuinely irreconcilable (the two sides express contradictory intent that cannot
be combined), stop, restore with the rollback anchor or `git rebase --abort` / `git merge --abort`,
and surface the specific conflict to the user rather than guessing.

### Step 7: Verify

Establish which checks the repository or enclosing procedure requires before pushing or handing
back the branch. A conflict-free integration does not waive those progression conditions.

- Detect the repo's checks from `package.json` scripts, `Makefile`, or CI config (build, test, lint,
  typecheck), together with any checks inherited from the agreed task.
- If conflicts were resolved, run the relevant repository checks before pushing or reporting
  success. Also run any checks required at this boundary, even when integration was conflict-free.
- Only defer local checks to CI after a clean integration when the agreed progression conditions
  permit it. State that verification is deferred, identify the receiving CI gate, and do not report
  unobserved CI results as passes.
- If any check fails or a required check cannot run: **stop, do not push or report verified completion.**
  Return the evidence and blocker for resolution rather than silently skipping the check.

### Step 8: Push or keep local

If `pushMode` is `push`:

- Rebase: `git push --force-with-lease`
- Merge: `git push`

If the branch has no upstream yet: `git push -u <remote> <branch>` (force-with-lease is unnecessary
on the first push of a new branch).

If `pushMode` is `keep-local`, skip pushing. Report the exact command the user can run later:

- Rebase: `git push --force-with-lease`
- Merge: `git push`
- No upstream: `git push -u <remote> <branch>`

### Step 9: Restore stash

If Step 2 stashed work, restore it now: `git stash pop`. If the pop conflicts, surface it to the
user — the integrated branch state is already correct; only the local WIP needs attention.

### Step 10: Report

Summarise:

- Strategy used (rebase/merge) and trunk branch
- Destination behavior (push/keep-local)
- Commits replayed (rebase) or the merge commit (merge)
- Conflicts encountered and how each was resolved
- Verification commands and results (passed / failed / blocked / deferred), with the required boundary and receiving CI gate for deferred checks
- Push result, or skipped push with the command to run later
- Stash restoration status

## Conflict resolution guidance

The quality of conflict resolution is the core value of this skill. Resolve like a careful engineer,
not a mechanical merge tool:

- **Combine intents.** When both sides changed the same region for different reasons, integrate both
  changes so neither is lost. Picking one side wholesale is rarely correct.
- **Never drop a side silently.** If you cannot keep a change, say so explicitly in the report.
- **Regenerate generated files.** For lockfiles and other generated artifacts, do not hand-merge
  conflict markers — take one side, then regenerate (e.g. re-run the package manager's install/lock
  command) so the file is internally consistent.
- **Re-apply formatting.** After resolving, run the repo's formatter on touched files so the result
  matches project style.
- **Keep it minimal and faithful.** Resolve only the conflict; do not refactor or "improve"
  surrounding code while resolving.
- **Trust the intent, not the line position.** Read enough surrounding context to understand what
  each side was trying to do before deciding how they combine.

## Constraints

- **Only force-push the current feature branch.** Never force-push trunk or shared branches.
- **Use `--force-with-lease`, never bare `--force`** — it refuses to clobber remote commits you have
  not seen.
- **Never push in `keep-local` mode.** Leave the synced commits local and report how to push later.
- **Never run on detached HEAD or directly on trunk.**
- **Respect verification boundaries** — stop on failed local checks or unverified required pre-push checks; follow Step 7 for permitted CI deferrals.
- **Leave a recoverable state.** On a broken integration, prefer `git rebase --abort` /
  `git merge --abort` (or `git reset --hard <anchor>`) and surface the problem rather than leaving a
  half-finished rebase or merge.
