---
title: "Change Function Declaration"
description: "Modify a function's signature to improve its clarity, usability, or alignment with current requirements"
category: "Change Function Declaration"
tags: ["function", "signature", "parameters", "naming", "interface", "api"]
related: ["rename-function", "add-parameter", "remove-parameter", "parameterize-function"]
---

# Change Function Declaration

Modify a function's signature to improve its clarity, usability, or alignment with current requirements. This involves changing the function's name, parameters, or both to better express its purpose or adapt to new requirements.

## Also Known As
- Rename Function
- Rename Method
- Add Parameter
- Remove Parameter
- Change Signature

## Motivation

Function names and signatures are crucial for code readability. A well-chosen name and parameter list make it immediately clear what a function does and how to use it. As software evolves, the original names and parameters may no longer accurately reflect the function's purpose or may not support new requirements.

## Example

### Simple Rename
```javascript
// Before
function circum(radius) {
  return 2 * Math.PI * radius;
}

// After
function circumference(radius) {
  return 2 * Math.PI * radius;
}
```

### Adding a Parameter
```javascript
// Before
function addReservation(customer) {
  this._reservations.push(customer);
}

// After
function addReservation(customer, isPriority = false) {
  if (isPriority) {
    this._reservations.unshift(customer);
  } else {
    this._reservations.push(customer);
  }
}
```

### Removing a Parameter
```javascript
// Before
function getPayAmount(isAlive, isSeparated, isRetired) {
  if (isAlive && !isSeparated && !isRetired) {
    return normalPayAmount();
  }
  return 0;
}

// After
function getPayAmount() {
  if (employee.isAlive && !employee.isSeparated && !employee.isRetired) {
    return normalPayAmount();
  }
  return 0;
}
```

## Mechanics

### Simple Mechanics (for simple cases)
1. If you're removing a parameter, ensure the function doesn't reference it
2. Change the function declaration
3. Find all references to the old function and update them
4. Test

### Migration Mechanics (for complex cases)
1. If necessary, refactor the function body to make it easy to do the following extraction
2. Use Extract Function on the function body to create the new function
3. If the extracted function needs additional parameters, use the simple mechanics to add them
4. Test
5. Apply Inline Function to the old function
6. If you used a temporary name, use Change Function Declaration again to restore the original name
7. Test

## When to Use

- **Poor naming**: When a function name doesn't clearly express what it does
- **Parameter evolution**: When you need to add or remove parameters to support new features
- **Consistency**: When aligning with naming conventions or patterns in your codebase
- **API improvement**: When designing better interfaces for your functions

## Trade-offs

### Benefits
- Improves code readability and self-documentation
- Makes APIs more intuitive and easier to use
- Reduces cognitive load when reading code
- Supports evolving requirements

### Drawbacks
- Can break existing code if not done carefully
- Requires updating all call sites
- May require coordination in team environments
- Can be disruptive to ongoing work

## Related Refactorings

- [Rename Variable](rename-variable.md) - Similar concept applied to variables
- [Extract Function](extract-function.md) - Often used in migration mechanics
- [Inline Function](inline-function.md) - Used to complete the migration
- [Introduce Parameter Object](introduce-parameter-object.md) - Alternative when dealing with many parameters