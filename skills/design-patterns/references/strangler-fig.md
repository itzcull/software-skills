# Strangler Fig Design Pattern

## Overview

The Strangler Fig pattern is a software migration strategy that enables gradual transformation of a legacy system to a new system, module by module, with minimal disruption.

## When to Use

Use the Strangler Fig pattern when:
- Migrating legacy backend architecture to a newer architecture
- Transforming systems over an extended period
- Needing to minimize disruption during system migration

## When Not to Use

Avoid this pattern when:
- The system replacement is small
- Backend calls cannot be intercepted
- Migration can be completed quickly

## How It Works

The pattern is named after the strangler fig tree, which grows around and eventually replaces a host tree. In software, it uses the [Facade pattern](facade.md) to gradually shift system roots from the old system to the new system.

### Migration Phases

```
Phase 1 - Client sends a request
Phase 2 - Client sends request to facade. Old system responds.
Phase 3 - Client sends request to facade. New system responds.
Phase 4 - Client sends request to new system. Old system is "strangled".
```

## Advantages

- Incremental migration with minimal system disruption
- Ability to pause and resume migration
- Reduced risk through gradual transformation
- Flexibility to add new services while maintaining old services

## Disadvantages

- Requires ability to quickly roll back
- Potential for development stagnation
- Extensive routing maintenance
- Managing multiple systems simultaneously

## References

- Martin Fowler's Strangler Fig Application
- Microsoft's Incremental ASP.NET to ASP.NET Core update
- Azure and AWS cloud design pattern documentation