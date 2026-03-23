# Naming & Readability

Category 9 -- Can a human understand it quickly?

## Subcategories

- **Unclear variable/function/class names** -- names that do not convey purpose or meaning
- **Misleading names** -- names that suggest different behaviour from what the code does
- **Inconsistent naming conventions** -- mixing camelCase and snake_case, or PascalCase for non-classes
- **Single-letter variables in non-trivial scope** -- `x`, `d`, `t` used beyond a tiny lambda or loop index
- **Abbreviations without context** -- `mgr`, `ctx`, `cfg`, `impl` where the full word adds clarity
- **Overly long names** -- names that try to encode too much information (more than ~40 characters)
- **Boolean naming** -- booleans that do not read as yes/no questions (`isReady`, `hasPermission`)
- **Negated booleans** -- `isNotValid`, `disableFeature` that require mental inversion
- **Verb/noun confusion** -- functions named as nouns, variables named as verbs
- **Generic names** -- `data`, `result`, `value`, `item`, `info`, `temp`, `stuff` without qualification

## What to Look For

- Functions whose name does not describe their primary action (a function called `process` that actually validates and transforms)
- Variables named `data`, `result`, `response`, `item` without a qualifying prefix or suffix
- Boolean variables that do not start with `is`, `has`, `can`, `should`, `was`, or `will`
- Negated conditions in boolean names (`isNotEmpty` instead of `isEmpty`, `disableLogging` instead of `enableLogging`)
- Inconsistent naming of similar concepts (e.g. `user` in one module, `account` in another for the same entity)
- Abbreviations that require domain knowledge to decode (`txn`, `amt`, `qty` in non-financial contexts)
- Function parameters that shadow outer scope variables
- Pluralisation errors (`users` for a single user, `user` for a collection)
- Names that encode types (`userArray`, `nameString`) instead of semantic meaning
- Callback parameters named `cb`, `fn`, `handler` instead of describing what they do

## Positive Example

```typescript
function calculateMonthlyPayment(
  principal: number,
  annualInterestRate: number,
  termInMonths: number,
): number {
  const monthlyRate = annualInterestRate / 12;
  const compoundFactor = Math.pow(1 + monthlyRate, termInMonths);
  return principal * (monthlyRate * compoundFactor) / (compoundFactor - 1);
}
```

Every name describes its domain meaning. Intermediate variables document the calculation steps.

## Negative Example

```typescript
// READABILITY: names obscure what the code does
function calc(p: number, r: number, n: number): number {
  const mr = r / 12;
  const cf = Math.pow(1 + mr, n);
  return p * (mr * cf) / (cf - 1);
}
```

Single-letter parameters and abbreviated variables make the algorithm opaque.

## Common False Positives

- Single-letter variables in tiny scopes: `items.map(x => x.id)` or `for (let i = 0; i < len; i++)`
- Domain-standard abbreviations where the team has established conventions (e.g. `tx` for database transaction in a data layer)
- Short names in mathematical code where the variable maps to a known formula symbol
- Generic names in genuinely generic utility functions (`value` in a `clamp` function)

## Severity Guide

| Severity | When |
|---|---|
| Critical | Misleading name that causes a reader to assume wrong behaviour (e.g. `isValid` returning true for invalid data) |
| Major | Unclear names in complex business logic where misunderstanding has real consequences |
| Minor | Generic names in straightforward code; abbreviations that are locally understandable |
| Nitpick | Stylistic preference between two equally clear naming approaches |

## Related Categories

- [Code Structure & Organisation](code-structure-and-organisation.md) -- poorly named abstractions are also structural issues
- [Documentation](documentation.md) -- good names reduce the need for comments
- [Logic & Correctness](logic-and-correctness.md) -- misleading names lead to incorrect usage
