# Code Structure & Organisation

Category 10 -- Is it well-organised and appropriately decomposed?

## Subcategories

- **God class/function** -- a single unit doing too many unrelated things (multiple reasons to change)
- **Inappropriate coupling** -- modules depending on internal details of other modules
- **Missing abstraction** -- duplicated logic that should be extracted into a shared function or module
- **Incorrect module boundaries** -- responsibilities split across modules in ways that do not match the domain
- **Circular dependencies** -- modules that depend on each other, creating a tightly coupled cycle
- **Deep nesting** -- more than 2-3 levels of indentation from conditionals, loops, or callbacks
- **Long methods** -- functions that exceed ~30-40 lines and do not read as a single coherent operation
- **Duplicate code** -- identical or near-identical logic in multiple places (knowledge duplication, not structural similarity)
- **Dead code** -- unreachable code, unused functions, unused imports, commented-out code
- **Feature envy** -- a function that accesses another object's data more than its own
- **Primitive obsession** -- using raw strings, numbers, or booleans where a domain type would be clearer

## What to Look For

- Functions longer than ~40 lines -- consider whether they have natural seams for extraction
- Files longer than ~300 lines -- consider whether they contain multiple distinct responsibilities
- `if/else` chains or `switch` statements deeper than 2 levels
- Functions that take more than 3-4 parameters (suggests the function does too much, or needs an options object)
- Importing internal details from another module (reaching into private implementation)
- Copy-pasted blocks with minor variations (same knowledge expressed multiple times)
- Commented-out code or functions that are never called
- Functions that read data from one object to make decisions about another (feature envy)
- Raw strings used as identifiers, status codes, or enum-like values without type safety
- Module A imports from Module B and Module B imports from Module A

## Positive Example

```typescript
// Single responsibility: each function does one thing
function validateOrder(order: Order): ValidationResult {
  return combineValidations([
    validateLineItems(order.items),
    validateShippingAddress(order.shipping),
    validatePaymentMethod(order.payment),
  ]);
}
```

Composed from focused sub-functions. Each validation can change independently.

## Negative Example

```typescript
// GOD FUNCTION: validates, calculates, persists, and notifies
async function processOrder(order: Order): Promise<void> {
  // 20 lines of validation...
  // 15 lines of price calculation...
  // 10 lines of tax calculation...
  // 8 lines of database persistence...
  // 12 lines of email notification...
  // 5 lines of analytics tracking...
}
```

70+ lines with 6 distinct responsibilities. Changes to tax rules require modifying the same function as changes to email templates.

## Common False Positives

- Long functions that are inherently sequential (e.g. test setup, migration scripts, configuration builders) where extraction would scatter the narrative
- Structurally similar but semantically distinct code -- DRY applies to knowledge, not to code that looks alike
- Deeply nested code that is only 3-4 lines deep and reads clearly (e.g. nested ternary for a simple mapping)
- Files with many small exported functions that all belong to the same domain concept
- Dead code that is intentionally kept behind a feature flag for imminent rollback

## Severity Guide

| Severity | When |
|---|---|
| Critical | Circular dependency that prevents independent deployment or testing; god class at the centre of the system |
| Major | Significant code duplication of business logic; function with 5+ responsibilities; deep nesting obscuring control flow |
| Minor | Slightly long function that could be split; mild feature envy; one or two unused imports |
| Nitpick | Preferring one structural approach over another for already-clear code |

## Code Smell Mapping

This category covers several classic code smells (Fowler/Beck):

- **Bloaters**: Long Method, Large Class, Long Parameter List, Primitive Obsession
- **Dispensables**: Duplicate Code, Dead Code, Lazy Class, Speculative Generality
- **Couplers**: Feature Envy, Inappropriate Intimacy, Message Chains
- **Change Preventers**: Divergent Change, Shotgun Surgery

## Related Categories

- [Naming & Readability](naming-and-readability.md) -- structural clarity and naming clarity reinforce each other
- [Design & Architecture](design-and-architecture.md) -- structural issues at the module level become architectural issues at the system level
- [Performance](performance.md) -- inappropriate data structure choices overlap both categories
- [Testing](testing.md) -- tightly coupled code is difficult to test
