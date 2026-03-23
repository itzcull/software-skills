---
name: code-review
description: Structured, taxonomy-guided code review with selective category focus. Performs two-pass review (detect then verify) across 16 error categories with independent severity, confidence, and qualifier axes. Use when reviewing a PR, reviewing staged changes, performing a pre-merge quality gate, or when asked to review specific files or a diff.
license: MIT
version: 1.0.0
metadata:
  author: itzcull
---

## Purpose

Perform structured code review guided by a formal error taxonomy. Instead of open-ended "review this code" analysis, this skill loads specific error categories with concrete review rules, examples, and severity guidance. The reviewer selectively focuses on chosen categories -- improving detection precision by narrowing the search space per the "mental attitude hypothesis" (focused reviewers detect 8x more issues in their focus area).

## When to use

- Reviewing a pull request or branch diff
- Reviewing staged changes before commit
- Pre-merge quality gate on a feature branch
- Reviewing specific files for targeted concerns (e.g. "review this for security")
- When asked to "review", "check", "audit", or "critique" code changes

## Inputs expected

- **Diff source**: one of branch (vs trunk), staged changes, specific file paths, or a provided diff
- **Category selection**: specific categories by name, a review profile, or "all" (defaults to `quick` if unspecified)
- **Severity threshold**: minimum severity to report (defaults to Minor -- excludes Nitpick unless requested)
- **Project conventions**: any project-specific style guides, lint configs, or architectural constraints when known

## Review Profiles

Profiles are predefined category bundles. Use a profile name as shorthand, or specify individual categories by name.

| Profile | Categories | Use When |
|---|---|---|
| `quick` | Logic & Correctness, Error Handling, Security, Performance | Fast review focusing on highest-signal defect categories |
| `correctness` | Logic & Correctness, Data Handling, Error Handling, Concurrency & Timing | Verifying functional behaviour is correct |
| `security` | Security, Concurrency & Timing, Resource Management, API & Interface | Security-focused audit |
| `maintainability` | Naming & Readability, Code Structure & Organisation, Style & Formatting, Documentation, Design & Architecture | Code quality and long-term health |
| `testing` | Testing, Logic & Correctness, Error Handling | Verifying test adequacy and quality |
| `full` | All 16 categories | Comprehensive review -- use for critical changes |

## Process

### Step 1: Gather the diff

Determine the diff source from user input:

- **Branch review**: detect trunk (`main` or `master`), find merge-base, run `git diff <merge-base>..HEAD`
- **Staged changes**: run `git diff --cached`
- **Specific files**: run `git diff` on the named files, or read them directly
- **Provided diff**: use the diff text as given

Also gather: `git diff --stat` for the overview, and `git log --oneline` for commit context when reviewing a branch.

### Step 2: Determine review scope

Resolve the active categories:

1. If the user named a profile, expand it to its category list
2. If the user named specific categories, use those
3. If no selection was given, default to the `quick` profile
4. Load the corresponding reference files from `references/<category>.md`

Read `references/categories.md` for the severity, confidence, and qualifier definitions that apply to all findings.

### Step 3: First pass -- detect candidates

Read through the diff with the loaded category rules active. For each potential finding:

- Identify the **location** (file and line)
- Assign the **category** and **subcategory**
- Assign initial **severity** (Critical / Major / Minor / Nitpick)
- Assign initial **confidence** (High / Medium / Low)
- Tag the **qualifier** (Missing / Incorrect / Extraneous)
- Draft a brief **description**

Cast a wide net in this pass. Include anything that might be an issue.

### Step 4: Second pass -- verify and filter

Re-examine each candidate finding against the full context:

- **Promote** findings where surrounding code confirms the issue
- **Demote** findings that are likely false positives (check the "Common False Positives" section in each category reference)
- **Drop** Low-confidence findings that lack supporting evidence after re-examination
- **Merge** duplicate findings that describe the same root cause in different locations
- **Adjust severity** based on the specific context (a null dereference in a hot path is Critical; in dead code it may be Minor)

This two-stage pipeline reduces false positives -- raw single-pass LLM output carries too many for production use.

### Step 5: Present the report

Produce the structured output defined below. Group findings by severity (Critical first), then by category within each severity level. Include positive observations where genuine.

## Output Format

```
## Code Review: [branch-name, file-name, or "staged changes"]

**Scope:** [what was reviewed -- file count, line count from diff stat]
**Categories:** [which categories were active]
**Profile:** [profile name if used, or "custom"]
**Severity threshold:** [minimum severity reported]

**Summary:** [count] findings ([count] critical, [count] major, [count] minor, [count] nitpick)

---

### Critical

#### [Finding title]
- **Location:** `file:line`
- **Category:** [category] > [subcategory]
- **Confidence:** [High | Medium | Low]
- **Qualifier:** [Missing | Incorrect | Extraneous]
- **Description:** [what the issue is and why it matters]
- **Suggestion:** [concrete fix or direction]

[...repeat for each critical finding...]

### Major

[...same format...]

### Minor

[...same format...]

### Nitpick

[...same format, only included if severity threshold permits...]

---

### Observations
- [Positive patterns worth noting]
- [Architectural notes that are not findings but merit discussion]
- [Areas that were reviewed and found clean]
```

If no findings are produced, state this explicitly with a brief note on what was checked.

## Escalation Conditions

Stop and ask when:

- The diff is too large to review meaningfully in one pass (500+ changed files) -- suggest splitting by module or area
- The category selection does not match the nature of the changes (e.g. security profile on a CSS-only change)
- A finding has high severity but low confidence and could block a merge incorrectly
- Project conventions are needed to judge a finding but are not available
- The diff context is insufficient to determine correctness (e.g. deleted code whose callers are not visible)

## Constraints

- **Read-only analysis** -- do not modify files, make commits, or apply fixes unless explicitly asked
- **Honest assessment** -- flag genuine risks; do not soften findings to be polite; do not inflate findings to appear thorough
- **Proportional depth** -- spend more analysis on complex or risky changes, less on trivial formatting
- **No false authority** -- use Medium or Low confidence when genuinely uncertain; never present speculation as fact
- **Respect scope** -- review only the diff provided; do not audit the entire codebase unless asked
- **Category discipline** -- only report findings within the active categories; do not silently expand scope
- **Severity honesty** -- most findings in any review are Minor or Nitpick; a review with many Critical findings should prompt self-verification

## Reference Documentation

- `references/categories.md` -- master category index, scales, and finding template
- `references/<category-name>.md` -- individual category review rules with examples
- `~/.claude/docs/testing.md` -- for Testing category context
- `~/.claude/docs/code-style.md` -- for Style and Naming category context
- `~/.claude/docs/typescript.md` -- for TypeScript-specific review rules
- `~/.claude/docs/workflow.md` -- for understanding TDD and commit expectations
