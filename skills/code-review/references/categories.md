# Code Review Category Index

Master reference for the 16 error categories, review profiles, and classification scales.

## Categories

| # | Category | Key Concern | Reference File |
|---|---|---|---|
| 1 | Logic & Correctness | Does it behave as intended? | `logic-and-correctness.md` |
| 2 | Data Handling | Is data used safely and correctly? | `data-handling.md` |
| 3 | Error Handling | Does it fail gracefully? | `error-handling.md` |
| 4 | Security | Is it safe from attack? | `security.md` |
| 5 | Concurrency & Timing | Is it safe under concurrent access? | `concurrency-and-timing.md` |
| 6 | Performance | Is it efficient enough? | `performance.md` |
| 7 | Resource Management | Are resources properly acquired and released? | `resource-management.md` |
| 8 | API & Interface | Are contracts correct and stable? | `api-and-interface.md` |
| 9 | Naming & Readability | Can a human understand it quickly? | `naming-and-readability.md` |
| 10 | Code Structure & Organisation | Is it well-organised and appropriately decomposed? | `code-structure-and-organisation.md` |
| 11 | Style & Formatting | Does it follow project conventions? | `style-and-formatting.md` |
| 12 | Documentation | Is intent captured where needed? | `documentation.md` |
| 13 | Testing | Are changes adequately tested? | `testing.md` |
| 14 | Design & Architecture | Are structural decisions sound? | `design-and-architecture.md` |
| 15 | Configuration & Build | Is config correct and environment-safe? | `configuration-and-build.md` |
| 16 | Compatibility | Does it work across targets? | `compatibility.md` |

## Review Profiles

| Profile | Active Categories |
|---|---|
| `quick` | 1, 3, 4, 6 |
| `correctness` | 1, 2, 3, 5 |
| `security` | 4, 5, 7, 8 |
| `maintainability` | 9, 10, 11, 12, 14 |
| `testing` | 13, 1, 3 |
| `full` | All 16 |

## Severity Scale

| Level | Definition | Merge Impact |
|---|---|---|
| **Critical** | Causes data loss, security breach, crash, or fundamentally wrong behaviour | Must fix before merge |
| **Major** | Significant correctness, performance, or maintainability issue | Should fix before merge |
| **Minor** | Improvement that enhances quality but does not affect correctness | Fix recommended, not blocking |
| **Nitpick** | Stylistic preference or trivial improvement | Non-blocking, optional |

Most findings in a typical review are Minor or Nitpick. A review dominated by Critical findings should trigger self-verification -- either the code is genuinely dangerous or the reviewer is miscalibrated.

## Confidence Scale

| Level | Definition | Presentation |
|---|---|---|
| **High** | Clear violation of a well-defined rule, or obvious defect with unambiguous evidence | Present as a finding |
| **Medium** | Likely issue but context-dependent; reasonable people could disagree | Present as a suggestion with reasoning |
| **Low** | Possible concern that needs human judgement or additional context | Present as a question or thought |

## ODC Qualifier

Every finding is additionally tagged with one qualifier describing the nature of the defect:

| Qualifier | Definition | Example |
|---|---|---|
| **Missing** | Something that should exist but does not | Missing null check, missing error handling, missing test |
| **Incorrect** | Something that exists but is wrong | Wrong operator, incorrect return value, flawed logic |
| **Extraneous** | Something that exists but should not | Dead code, unused import, redundant check |

## Finding Template

```
#### [Concise title describing the issue]
- **Location:** `file-path:line-number`
- **Category:** [Category Name] > [Subcategory]
- **Confidence:** [High | Medium | Low]
- **Qualifier:** [Missing | Incorrect | Extraneous]
- **Description:** [What the issue is. Why it matters. What could go wrong.]
- **Suggestion:** [Concrete fix, direction, or alternative approach.]
```

## Empirical Distribution

Research across industrial and open-source code reviews consistently finds:

- ~75% of findings are maintainability/evolvability concerns (categories 9-14)
- ~20% are functional/correctness concerns (categories 1-8)
- ~5% are process/configuration concerns (categories 15-16)

A review that deviates significantly from this distribution is not necessarily wrong, but warrants a brief sanity check -- the code may genuinely be unusual, or the reviewer may be miscalibrated toward one concern area.
