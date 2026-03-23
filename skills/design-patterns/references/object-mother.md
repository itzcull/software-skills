# Object Mother Pattern

## Overview

The Object Mother pattern is a factory method for creating standard test fixtures across multiple tests. It was "described by Martin Fowler as a catchy name for a factory that returns standard fixtures" used in testing.

## Key Characteristics

- Builds upon the [Factory Method pattern](factory-method.md)
- Adds methods to:
  - Customize object creation
  - Update objects during testing
  - Enable object deletion from data storage

## Example Structure

```
TestUsers
+CreateRegularUser()
+CreateMemberUser()
+CreateAlumniUser()
+CreateAdminUser()
```

## Potential Drawbacks

The pattern can become problematic over time due to:
- Potential code bloat
- Repetitive code creation
- Violation of the [DRY (Don't Repeat Yourself)](../principles/dont-repeat-yourself.md) principle

## Alternative Pattern

An alternative to the Object Mother pattern is the [Builder pattern](builder.md).

## References

- [Object Mother - Martin Fowler](https://martinfowler.com/bliki/ObjectMother.html)
- [Object Mother - C2.com](https://wiki.c2.com/?ObjectMother)

## See Also

- [Builder Pattern](builder.md)
- [Factory Method Pattern](factory-method.md)
- [Testing - Overview](../testing/overview.md)