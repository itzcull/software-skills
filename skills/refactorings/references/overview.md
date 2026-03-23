# Refactoring Catalog

Refactoring is the process of changing a software system in such a way that it does not alter the external behavior of the code yet improves its internal structure. It's a disciplined way to clean up code that minimizes the chances of introducing bugs.

This catalog documents common refactoring operations that can be applied across different programming languages. Each refactoring describes a specific code transformation that improves code quality without changing functionality.

## Categories of Refactorings

### Composing Methods
Refactorings that help organize methods and make them more readable.

- [Extract Function](extract-function.md) - Turn a code fragment into its own function
- [Inline Function](inline-function.md) - Replace a function call with the function's content
- [Extract Variable](extract-variable.md) - Turn an expression into a variable with a meaningful name
- [Inline Variable](inline-variable.md) - Replace references to a variable with the expression itself
- [Change Function Declaration](change-function-declaration.md) - Change a function's name, parameters, or both
- [Encapsulate Variable](encapsulate-variable.md) - Provide access functions for a variable
- [Rename Variable](rename-variable.md) - Give a variable a more meaningful name
- [Introduce Parameter Object](introduce-parameter-object.md) - Replace groups of parameters with an object
- [Combine Functions into Class](combine-functions-into-class.md) - Group related functions into a class
- [Combine Functions into Transform](combine-functions-into-transform.md) - Group related functions into a transform function
- [Split Phase](split-phase.md) - Split code that does two things into separate modules

### Moving Features Between Objects
Refactorings that move functionality between classes or objects.

- [Move Function](move-function.md) - Move a function from one class to another
- [Move Field](move-field.md) - Move a field from one class to another
- [Move Statements into Function](move-statements-into-function.md) - Move statements into a called function
- [Move Statements to Callers](move-statements-to-callers.md) - Move statements from a function to its callers
- [Replace Inline Code with Function Call](replace-inline-code-with-function-call.md) - Replace inline code with a call to an existing function
- [Slide Statements](slide-statements.md) - Move related code together
- [Split Loop](split-loop.md) - Split a loop doing two things into separate loops
- [Replace Loop with Pipeline](replace-loop-with-pipeline.md) - Replace loops with collection pipelines

### Organizing Data
Refactorings that help organize data structures.

- [Split Variable](split-variable.md) - Split a variable that's used for multiple purposes
- [Rename Field](rename-field.md) - Give a field a more meaningful name
- [Replace Derived Variable with Query](replace-derived-variable-with-query.md) - Replace a stored value with a calculation
- [Change Reference to Value](change-reference-to-value.md) - Change a reference object to a value object
- [Change Value to Reference](change-value-to-reference.md) - Change a value object to a reference object
- [Replace Magic Literal](replace-magic-literal.md) - Replace magic numbers/strings with named constants

### Simplifying Conditional Expressions
Refactorings that make conditional logic easier to understand.

- [Decompose Conditional](decompose-conditional.md) - Extract complex conditional logic into well-named functions
- [Consolidate Conditional Expression](consolidate-conditional-expression.md) - Combine multiple conditionals with the same result
- [Replace Nested Conditional with Guard Clauses](replace-nested-conditional-with-guard-clauses.md) - Use guard clauses for special cases
- [Replace Conditional with Polymorphism](replace-conditional-with-polymorphism.md) - Replace conditional logic with polymorphic behavior
- [Introduce Special Case](introduce-special-case.md) - Create a special-case element to remove special-case logic
- [Introduce Assertion](introduce-assertion.md) - Make assumptions explicit with assertions
- [Replace Control Flag with Break](replace-control-flag-with-break.md) - Use break/return instead of control flags

### Simplifying Method Calls
Refactorings that make method calls easier to understand and use.

- [Rename Function](change-function-declaration.md) - Give a function a more meaningful name
- [Add Parameter](change-function-declaration.md) - Add a new parameter to a function
- [Remove Parameter](change-function-declaration.md) - Remove an unused parameter
- [Separate Query from Modifier](separate-query-from-modifier.md) - Separate methods that return values from methods that change state
- [Parameterize Function](parameterize-function.md) - Replace similar functions with one parameterized function
- [Remove Flag Argument](remove-flag-argument.md) - Replace boolean parameters with explicit methods
- [Preserve Whole Object](preserve-whole-object.md) - Pass whole objects instead of multiple values
- [Replace Parameter with Query](replace-parameter-with-query.md) - Remove a parameter by computing it inside the function
- [Replace Query with Parameter](replace-query-with-parameter.md) - Replace internal queries with parameters
- [Remove Setting Method](remove-setting-method.md) - Remove setters for fields that shouldn't change
- [Replace Constructor with Factory Function](replace-constructor-with-factory-function.md) - Replace constructor calls with factory functions
- [Replace Function with Command](replace-function-with-command.md) - Turn a function into a command object
- [Replace Command with Function](replace-command-with-function.md) - Turn a command object into a function
- [Return Modified Value](return-modified-value.md) - Have functions return modified values instead of modifying parameters

### Dealing with Generalization
Refactorings that deal with abstraction and inheritance hierarchies.

- [Pull Up Method](pull-up-method.md) - Move identical methods to the superclass
- [Pull Up Field](pull-up-field.md) - Move identical fields to the superclass
- [Pull Up Constructor Body](pull-up-constructor-body.md) - Move common constructor code to the superclass
- [Push Down Method](push-down-method.md) - Move methods from superclass to specific subclasses
- [Push Down Field](push-down-field.md) - Move fields from superclass to specific subclasses
- [Extract Subclass](extract-class.md) - Create a subclass for a subset of features
- [Extract Superclass](extract-superclass.md) - Create a superclass for common features
- [Extract Class](extract-class.md) - Create a new class for a subset of features
- [Inline Class](inline-class.md) - Merge a class into another class
- [Collapse Hierarchy](collapse-hierarchy.md) - Merge a subclass and superclass
- [Replace Subclass with Delegate](replace-subclass-with-delegate.md) - Replace inheritance with delegation
- [Replace Superclass with Delegate](replace-superclass-with-delegate.md) - Replace superclass inheritance with delegation
- [Replace Type Code with Subclasses](replace-type-code-with-subclasses.md) - Replace type codes with subclasses

### Large Scale Refactorings
More complex refactorings that often combine multiple smaller refactorings.

- [Replace Error Code with Exception](replace-error-code-with-exception.md) - Use exceptions instead of error codes
- [Replace Exception with Precheck](replace-exception-with-precheck.md) - Test for errors before causing exceptions
- [Extract Class](extract-class.md) - Create a new class from an existing class
- [Inline Class](inline-class.md) - Move all features from a class into another
- [Hide Delegate](hide-delegate.md) - Hide delegation from clients
- [Remove Middle Man](remove-middle-man.md) - Remove unnecessary delegation
- [Substitute Algorithm](substitute-algorithm.md) - Replace an algorithm with a clearer one
- [Replace Temp with Query](replace-temp-with-query.md) - Replace temporary variables with method calls
- [Encapsulate Record](encapsulate-record.md) - Replace records with data classes
- [Encapsulate Collection](encapsulate-collection.md) - Make collections accessible only through methods
- [Replace Primitive with Object](replace-primitive-with-object.md) - Replace primitive values with small objects
- [Remove Dead Code](remove-dead-code.md) - Delete code that isn't used
- [Remove Subclass](remove-subclass.md) - Replace subclasses with fields in the parent

## Core Principles

### When to Refactor
- **During feature development**: Clean up code as you add new features
- **When fixing bugs**: Improve code structure to make bugs easier to fix
- **During code reviews**: Identify opportunities for improvement
- **When code is hard to understand**: Make the code express its purpose clearly

### When NOT to Refactor
- Code that works and doesn't need to be changed
- When you're close to a deadline
- Code that should be rewritten from scratch

### The Refactoring Process
1. Ensure you have comprehensive tests
2. Make small changes
3. Test after each change
4. Commit working code frequently
5. Use your IDE's automated refactoring tools when available

## Related Resources
- [Martin Fowler's Refactoring Website](https://refactoring.com)
- Book: "Refactoring: Improving the Design of Existing Code" by Martin Fowler
- [Code Smells](../antipatterns/overview.md) - Signs that code needs refactoring
- [Design Patterns](../design-patterns/overview.md) - Common solutions to design problems